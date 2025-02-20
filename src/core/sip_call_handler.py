import threading
import time
import socket
import uuid
import struct
from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Tuple
from PyQt6.QtCore import QObject, pyqtSignal
from .models import CallData, CallState, SIPCall
import logging

logger = logging.getLogger(__name__)

class CallState(Enum):
    INITIAL = "INITIAL"
    TRYING = "TRYING"
    RINGING = "RINGING"
    ESTABLISHED = "ESTABLISHED"
    FAILED = "FAILED"
    TERMINATED = "TERMINATED"

class SIPResponse(Enum):
    TRYING = 100
    RINGING = 180
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    REQUEST_TIMEOUT = 408
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

class TimeoutConfig:
    INVITE_TIMEOUT = 32  # RFC 3261 Timer B
    RESPONSE_TIMEOUT = 4  # Timer F
    TRANSACTION_TIMEOUT = 64  # Timer H
    ACK_TIMEOUT = 32  # Timer I

class SIPError(Exception):
    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason
        super().__init__(f"SIP Error {code}: {reason}")

class SDPValidator:
    @staticmethod
    def validate_sdp(sdp: str) -> Tuple[bool, Optional[str]]:
        required_fields = ['v=', 'o=', 's=', 'c=', 't=', 'm=']
        try:
            lines = sdp.split('\r\n')
            found_fields = set()
            
            for line in lines:
                for field in required_fields:
                    if line.startswith(field):
                        found_fields.add(field)
                        
                if line.startswith('m='):
                    parts = line.split()
                    if len(parts) < 4:
                        return False, "Invalid media description"
                    if not parts[1].isdigit():
                        return False, "Invalid port number"
                        
            missing = set(required_fields) - found_fields
            if missing:
                return False, f"Missing required fields: {', '.join(missing)}"
                
            return True, None
            
        except Exception as e:
            return False, f"SDP parsing error: {str(e)}"

class SessionTimer:
    def __init__(self, expires: int = 1800, min_se: int = 90):
        self.session_expires = expires
        self.min_se = min_se
        self.active_sessions = {}
        
    def start_session(self, call_id: str, refresher: str = 'uac'):
        self.active_sessions[call_id] = {
            'expires': self.session_expires,
            'refresher': refresher,
            'last_refresh': datetime.now()
        }
        
    def needs_refresh(self, call_id: str) -> bool:
        if call_id not in self.active_sessions:
            return False
        session = self.active_sessions[call_id]
        elapsed = (datetime.now() - session['last_refresh']).total_seconds()
        return elapsed > (session['expires'] * 0.9)

class SIPCallHandler(QObject):
    call_status_changed = pyqtSignal(dict)  # Emite actualizaciones de estado
    call_stats_updated = pyqtSignal(int, int, int)  # active, failed, total
    monitoring_stats_updated = pyqtSignal(dict)  # Emite estadísticas de monitorización
    call_failed = pyqtSignal(str, str)  # Emite señal cuando una llamada falla

    def __init__(self, config):
        super().__init__()
        # Volver a la configuración directa
        self.config = config
        self.local_ip = config.get('local_ip', '127.0.0.1')
        self.local_port = config.get('local_port', 5060)
        self.remote_ip = config.get('remote_ip', '127.0.0.1')
        self.remote_port = config.get('remote_port', 5060)
        self.transport = config.get('transport', 'UDP')
        
        # Mantener una referencia fuerte al monitor
        self._monitor = None
        self._monitor_ref = None
        
        self.active_calls = {}
        self.rtp_sessions = {}
        self.transaction_states = {}
        self.timers = {}
        self.next_rtp_port = 10000
        self.next_origin = 1001
        self.next_dest = 2001
        self.burst_running = False
        self.burst_thread = None
        
        self.stats = {
            "active": 0,
            "failed": 0,
            "total": 0,
            "options": {
                "sent": 0,
                "received": 0,
                "ok_sent": 0,
                "ok_received": 0
            }
        }
        
        self.session_timer = SessionTimer()
        self._start_session_refresh_timer()

        # Añadir mapeo de estados
        self.call_states = {
            'INITIAL': 'Inicial',
            'TRYING': 'Intentando',
            'RINGING': 'Timbrando',
            'ESTABLISHED': 'Establecida',
            'FAILED': 'Fallida',
            'TERMINATED': 'Terminada'
        }

        self._shutting_down = False  # Nueva bandera para control de cierre
        self._transaction_ids = set()  # Para rastrear transacciones únicas

        logger.debug("=== INICIALIZACIÓN DE CALL HANDLER ===")
        logger.debug(f"Configuración inicial: {config}")
        logger.debug("Diccionario de llamadas inicializado")

    @property
    def sip_monitor(self):
        return self._monitor

    @sip_monitor.setter
    def sip_monitor(self, monitor):
        """Configura el monitor SIP y obtiene su configuración."""
        self._monitor = monitor
        if monitor and monitor.config:
            # Actualizar la configuración y las IPs
            self.config = monitor.config
            self.local_ip = monitor.config.get('local_ip', self.local_ip)
            self.remote_ip = monitor.config.get('remote_ip', self.remote_ip)
            self.local_port = monitor.config.get('local_port', self.local_port)
            self.remote_port = monitor.config.get('remote_port', self.remote_port)
            self.transport = monitor.config.get('transport', self.transport)
            logger.debug(f"Configuración actualizada - Local: {self.local_ip}, Remote: {self.remote_ip}")

    def send_message(self, message: bytes) -> bool:
        """Envía un mensaje SIP usando el monitor."""
        if self._monitor is None:
            logger.error("SIPMonitor no inicializado")
            return False
            
        try:
            decoded_msg = message.decode()
            logger.debug(f"Enviando mensaje SIP via {self.transport}:\n{'-'*20}\n{decoded_msg}\n{'-'*20}")
            
            if self.transport == "TCP":
                result = self._monitor.send_tcp_message(message)
            else:
                result = self._monitor.send_udp_message(message)
                
            logger.debug(f"Resultado del envío: {'Éxito' if result else 'Fallo'}")
            return result
            
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}", exc_info=True)
            return False

    def _get_next_rtp_port(self) -> int:
        """Obtiene el siguiente puerto RTP disponible."""
        port = self.next_rtp_port
        self.next_rtp_port = (self.next_rtp_port + 2) % 65535
        if self.next_rtp_port < 10000:
            self.next_rtp_port = 10000
        return port

    def _start_transaction_timer(self, call: SIPCall):
        """Inicia el timer de transacción INVITE."""
        timer_id = f"{call.call_id}_transaction"
        
        def on_timeout():
            if call.call_id in self.active_calls:
                if call.state in [CallState.INITIAL.value, CallState.TRYING.value]:
                    logger.warning(f"Timeout de transacción para llamada {call.call_id}")
                    self._handle_call_failure(call, "Timeout de transacción")
                
        # Timer B (RFC 3261) - 32 segundos
        self.timers[timer_id] = threading.Timer(32.0, on_timeout)
        self.timers[timer_id].start()

    def _handle_call_failure(self, call: SIPCall, reason: str = "Llamada fallida"):
        """Maneja el fallo de una llamada."""
        call.state = CallState.FAILED.value
        self._update_call_state(call.call_id, call.state)
        self.stats["failed"] += 1
        self.stats["active"] -= 1
        self._cleanup_call(call.call_id)
        self.call_failed.emit(call.call_id, reason)

    def _update_stats(self):
        """Actualiza las estadísticas de llamadas."""
        try:
            active = len([c for c in self.active_calls.values() 
                         if c.state not in ['TERMINATED', 'FAILED']])
            failed = len([c for c in self.active_calls.values() 
                         if c.state == 'FAILED'])
            total = len(self.active_calls)
            
            logger.debug(f"Actualizando estadísticas - Activas: {active}, Fallidas: {failed}, Total: {total}")
            
            self.stats["active"] = active
            self.stats["failed"] = failed
            self.stats["total"] = total
            
            self.call_stats_updated.emit(active, failed, total)
        except Exception as e:
            logger.error(f"Error actualizando estadísticas: {e}")

    @staticmethod
    def _extract_uri(header_value: str) -> str:
        """Extrae la URI de un valor de header SIP."""
        try:
            start = header_value.find('<sip:') + 5
            end = header_value.find('@', start)
            if start > 4 and end > start:
                return header_value[start:end]
            return ""
        except Exception:
            return ""

    def _create_invite_message(self, call: SIPCall) -> str:
        """Crea un mensaje INVITE con SDP."""
        try:
            # Validar que tenemos las IPs necesarias
            if not self.remote_ip or not self.local_ip:
                logger.error(f"IPs no configuradas correctamente - Local: {self.local_ip}, Remote: {self.remote_ip}")
                return ""
            
            # Generar SDP
            sdp = self._create_sdp_body(call)
            
            # Construir Request-URI y headers con formato correcto
            request_uri = f"sip:{call.to_uri}@{self.remote_ip}"
            from_uri = f"<sip:{call.from_uri}@{self.local_ip}>"
            to_uri = f"<sip:{call.to_uri}@{self.remote_ip}>"
            contact = f"<sip:{call.from_uri}@{self.local_ip}:{self.local_port}>"
            
            message = (
                f"INVITE {request_uri} SIP/2.0\r\n"
                f"Via: SIP/2.0/{self.transport} {self.local_ip}:{self.local_port}"
                f";branch={call.branch}\r\n"
                f"From: {from_uri};tag={call.from_tag}\r\n"
                f"To: {to_uri}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} INVITE\r\n"
                f"Contact: {contact}\r\n"
                "Max-Forwards: 70\r\n"
                "Allow: INVITE, ACK, CANCEL, BYE, OPTIONS\r\n"
                "Supported: timer, 100rel\r\n"
                "Content-Type: application/sdp\r\n"
                f"Content-Length: {len(sdp)}\r\n"
                f"\r\n{sdp}"
            )
            
            logger.debug(f"INVITE creado:\n{message}")
            return message
            
        except Exception as e:
            logger.error(f"Error creando INVITE: {e}")
            return ""

    def _create_sdp_body(self, call: SIPCall) -> str:
        """Crea el cuerpo SDP para el INVITE."""
        try:
            timestamp = int(time.time())
            sdp = (
                "v=0\r\n"
                f"o=PySIPP {call.call_id} {timestamp} IN IP4 {self.local_ip}\r\n"
                "s=PySIPP Call\r\n"
                f"c=IN IP4 {self.local_ip}\r\n"
                "t=0 0\r\n"
                f"m=audio {call.local_rtp_port} RTP/AVP 0 8 101\r\n"
                "a=rtpmap:0 PCMU/8000\r\n"
                "a=rtpmap:8 PCMA/8000\r\n"
                "a=rtpmap:101 telephone-event/8000\r\n"
                "a=fmtp:101 0-15\r\n"
                "a=ptime:20\r\n"
                "a=sendrecv\r\n"
            )
            return sdp
            
        except Exception as e:
            logger.error(f"Error creando SDP: {e}")
            return ""

    def handle_incoming_invite(self, invite_message: str):
        """Maneja INVITE entrante."""
        try:
            logger.debug(f"INVITE entrante recibido:\n{invite_message}")
            
            # Extraer headers necesarios
            call_id = self._extract_header(invite_message, "Call-ID")
            from_header = self._extract_header(invite_message, "From")
            to_header = self._extract_header(invite_message, "To")
            contact = self._extract_header(invite_message, "Contact")
            
            if not all([call_id, from_header, to_header]):
                logger.error("Headers requeridos no encontrados en INVITE")
                return
            
            # Extraer URIs
            from_uri = self._extract_uri(from_header)
            to_uri = self._extract_uri(to_header)
            
            # Verificar si ya existe la llamada
            if call_id in self.active_calls:
                logger.warning(f"INVITE recibido para llamada existente: {call_id}")
                return
            
            # Crear nueva llamada
            call = SIPCall(
                from_uri=from_uri,
                to_uri=to_uri,
                call_id=call_id,
                direction='inbound'
            )
            
            # Extraer from_tag
            if ';tag=' in from_header:
                call.from_tag = from_header.split(';tag=')[1]
            
            # Generar to_tag
            call.to_tag = uuid.uuid4().hex[:8]
            
            # Registrar llamada
            self.active_calls[call_id] = call
            call.state = CallState.TRYING.value
            self._update_call_state(call_id, call.state)
            
            # Enviar respuestas en secuencia
            self._send_trying(call)
            time.sleep(0.5)  # Pequeña pausa
            self._send_ringing(call)
            time.sleep(1)  # Simular tiempo de ring
            self._send_ok(call)
            
            logger.debug(f"Procesamiento de INVITE completado para llamada {call_id}")
            
        except Exception as e:
            logger.error(f"Error procesando INVITE entrante: {e}")

    def _send_trying(self, call: SIPCall):
        """Envía respuesta 100 Trying."""
        try:
            response = (
                "SIP/2.0 100 Trying\r\n"
                f"Via: {call.via}\r\n"
                f"From: {call.from_header}\r\n"
                f"To: {call.to_header}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} INVITE\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            self.send_message(response.encode())
            logger.debug(f"100 Trying enviado para llamada {call.call_id}")
        except Exception as e:
            logger.error(f"Error enviando 100 Trying: {e}")

    def _send_ringing(self, call: SIPCall):
        """Envía respuesta 180 Ringing."""
        try:
            response = (
                "SIP/2.0 180 Ringing\r\n"
                f"Via: {call.via}\r\n"
                f"From: {call.from_header}\r\n"
                f"To: {call.to_header};tag={call.to_tag}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} INVITE\r\n"
                f"Contact: <sip:{call.to_uri}@{self.local_ip}:{self.local_port}>\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            self.send_message(response.encode())
            call.state = CallState.RINGING.value
            self._update_call_state(call.call_id, call.state)
            logger.debug(f"180 Ringing enviado para llamada {call.call_id}")
        except Exception as e:
            logger.error(f"Error enviando 180 Ringing: {e}")

    def _send_ok(self, call: SIPCall):
        """Envía respuesta 200 OK según RFC 3261."""
        try:
            headers = self._extract_all_headers(call)
            call_id = headers.get('call-id')
            if call_id not in self.active_calls:
                logger.error("No se encontró la llamada para enviar 200 OK")
                return
                
            call = self.active_calls[call_id]
            call.rtp_port = self._get_next_rtp_port()
            to_tag = uuid.uuid4().hex[:8]
            call.to_tag = to_tag
            
            sdp = self._create_sdp(call)
            
            # RFC 3261 - Sección 8.2.6: Formato de respuestas
            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers.get('via')}\r\n"
                f"From: {headers.get('from')}\r\n"
                f"To: {headers.get('to')};tag={to_tag}\r\n"
                f"Call-ID: {call_id}\r\n"
                f"CSeq: {headers.get('cseq')}\r\n"
                f"Contact: <sip:{self.local_ip}:{self.local_port};transport={self.transport.lower()}>\r\n"
                # RFC 3261 - Sección 20.32: Supported features
                "Supported: timer, 100rel\r\n"
                # RFC 4028 - Session Timer
                f"Session-Expires: {call.session_expires};refresher=uas\r\n"
                "Allow: INVITE, ACK, CANCEL, BYE, UPDATE, OPTIONS\r\n"
                "Content-Type: application/sdp\r\n"
                f"Content-Length: {len(sdp)}\r\n\r\n"
                f"{sdp}"
            )
            
            self.send_message(response.encode())
            logger.debug("200 OK con SDP enviado")
            
        except Exception as e:
            logger.error(f"Error enviando 200 OK: {e}")

    def terminate_call(self, call_id: str):
        """Termina una llamada específica."""
        if call_id in self.active_calls:
            try:
                bye = self._create_bye(call_id)
                if self.send_message(bye.encode()):
                    self._update_call_state(call_id, 'TERMINATED')
                    logger.debug(f"BYE enviado para llamada {call_id}")
                else:
                    logger.error(f"Error enviando BYE para llamada {call_id}")
            except Exception as e:
                logger.error(f"Error terminando llamada {call_id}: {e}")

    def _update_call_state(self, call_id: str, new_state: str):
        """Actualiza el estado de una llamada."""
        try:
            if call_id in self.active_calls:
                call = self.active_calls[call_id]
                old_state = call.state
                call.state = new_state
                
                logger.debug(f"Llamada {call_id} cambió de estado: {old_state} -> {new_state}")
                
                # Si el estado es final, programar limpieza
                if new_state in ['TERMINATED', 'FAILED']:
                    logger.debug(f"Estado final alcanzado para llamada {call_id}, programando limpieza")
                    self.active_calls.pop(call_id, None)
                    self._update_stats()
                
                # Emitir señal de actualización
                self.call_status_changed.emit({
                    'call_id': call_id,
                    'state': new_state,
                    'from_uri': call.from_uri,
                    'to_uri': call.to_uri
                })
                
        except Exception as e:
            logger.error(f"Error actualizando estado de llamada: {e}")

    def _create_bye(self, call_id: str) -> str:
        """Crea un mensaje BYE para una llamada."""
        # Implementar creación de mensaje BYE
        pass

    def _send_ok(self, invite_message: str):
        """Envía respuesta 200 OK según RFC 3261."""
        try:
            headers = self._extract_all_headers(invite_message)
            call_id = headers.get('call-id')
            if call_id not in self.active_calls:
                logger.error("No se encontró la llamada para enviar 200 OK")
                return
                
            call = self.active_calls[call_id]
            call.rtp_port = self._get_next_rtp_port()
            to_tag = uuid.uuid4().hex[:8]
            call.to_tag = to_tag
            
            sdp = self._create_sdp(call)
            
            # RFC 3261 - Sección 8.2.6: Formato de respuestas
            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers.get('via')}\r\n"
                f"From: {headers.get('from')}\r\n"
                f"To: {headers.get('to')};tag={to_tag}\r\n"
                f"Call-ID: {call_id}\r\n"
                f"CSeq: {headers.get('cseq')}\r\n"
                f"Contact: <sip:{self.local_ip}:{self.local_port};transport={self.transport.lower()}>\r\n"
                # RFC 3261 - Sección 20.32: Supported features
                "Supported: timer, 100rel\r\n"
                # RFC 4028 - Session Timer
                f"Session-Expires: {call.session_expires};refresher=uas\r\n"
                "Allow: INVITE, ACK, CANCEL, BYE, UPDATE, OPTIONS\r\n"
                "Content-Type: application/sdp\r\n"
                f"Content-Length: {len(sdp)}\r\n\r\n"
                f"{sdp}"
            )
            
            self.send_message(response.encode())
            logger.debug("200 OK con SDP enviado")
            
        except Exception as e:
            logger.error(f"Error enviando 200 OK: {e}")

    def _extract_all_headers(self, message: str) -> dict:
        """Extrae todos los headers relevantes de un mensaje SIP."""
        headers = {}
        for line in message.split('\r\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.lower()] = value
            elif line.startswith('Via:'):
                headers['via'] = line[4:].strip()
        return headers

    def _extract_branch(self, message: str) -> str:
        """Extrae el parámetro branch del Via header."""
        try:
            via_header = self._extract_header(message, "Via")
            if via_header and "branch=" in via_header:
                return via_header.split("branch=")[1].split(";")[0]
        except Exception:
            pass
        return ""

    def start_single_call(self, from_uri: str, to_uri: str) -> bool:
        """Inicia una llamada única."""
        try:
            logger.debug(f"=== INICIANDO NUEVA LLAMADA ===")
            logger.debug(f"From: {from_uri}, To: {to_uri}")
            logger.debug(f"Estado actual del diccionario de llamadas: {len(self.active_calls)} llamadas")
            for call_id, call in self.active_calls.items():
                logger.debug(f"Llamada {call_id}: {call.from_uri}->{call.to_uri} [Estado: {call.state}]")
            
            # Limpiar el diccionario de llamadas al inicio
            self.active_calls.clear()
            self._update_stats()
            logger.debug("Diccionario de llamadas limpiado")
            
            # Crear nueva llamada
            call = SIPCall(from_uri=from_uri, to_uri=to_uri)
            logger.debug(f"Nueva llamada creada con ID: {call.call_id}")
            
            # Enviar INVITE y registrar llamada si es exitoso
            if self._send_invite(call):
                self.active_calls[call.call_id] = call
                self._update_call_state(call.call_id, CallState.INITIAL.value)
                logger.debug(f"INVITE enviado y llamada registrada: {call.call_id}")
                return True
            else:
                logger.error("Error enviando INVITE - llamada no registrada")
                return False
                
        except Exception as e:
            logger.error(f"Error iniciando llamada: {e}")
            return False

    def _force_cleanup_calls(self):
        """Fuerza la limpieza de todas las llamadas en estados finales."""
        try:
            # Limpiar todas las llamadas en estados finales
            for call_id in list(self.active_calls.keys()):
                call = self.active_calls[call_id]
                if call.state in ['TERMINATED', 'FAILED']:
                    logger.debug(f"Forzando limpieza de llamada {call_id} en estado {call.state}")
                    del self.active_calls[call_id]
                    self._update_stats()
            
            # Verificar si quedaron llamadas
            if self.active_calls:
                logger.debug(f"Llamadas restantes después de limpieza: {len(self.active_calls)}")
                for call_id, call in self.active_calls.items():
                    logger.debug(f"Llamada {call_id}: {call.from_uri}->{call.to_uri} en estado {call.state}")
        except Exception as e:
            logger.error(f"Error en limpieza forzada: {e}")

    def _send_invite(self, call: SIPCall) -> bool:
        """Envía INVITE para una nueva llamada."""
        try:
            # Verificar que tenemos IP remota antes de intentar enviar
            if not self.remote_ip:
                logger.error("No se puede enviar INVITE - IP remota no configurada")
                return False

            invite_msg = self._create_invite_message(call)
            if not invite_msg:
                logger.error("Error creando mensaje INVITE")
                return False
            
            # Enviar INVITE
            if not self.send_message(invite_msg.encode()):
                logger.error("Error enviando INVITE")
                return False
            
            # Iniciar timer de transacción
            self._start_transaction_timer(call)
            
            logger.debug(f"INVITE enviado correctamente para llamada {call.call_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando INVITE: {e}")
            return False

    def start_call_burst(self, interval: int, max_calls: int):
        """Inicia una ráfaga de llamadas."""
        try:
            logger.debug(f"Iniciando ráfaga de llamadas: intervalo={interval}s, max={max_calls}")
            self.burst_running = True
            self.burst_thread = threading.Thread(
                target=self._burst_worker,
                args=(interval, max_calls)
            )
            self.burst_thread.daemon = True
            self.burst_thread.start()
            logger.debug("Hilo de ráfaga iniciado")
        except Exception as e:
            logger.error(f"Error iniciando ráfaga: {e}")
            self.burst_running = False

    def _burst_worker(self, interval: int, max_calls: int):
        while self.burst_running and len(self.active_calls) < max_calls:
            from_number = str(self.next_origin)
            to_number = str(self.next_dest)
            
            self.start_single_call(from_number, to_number)
            
            self.next_origin += 1
            self.next_dest += 1
            
            time.sleep(interval)

    def stop_call_burst(self):
        """Detiene la ráfaga de llamadas."""
        try:
            logger.debug("Deteniendo ráfaga de llamadas")
            self.burst_running = False
            if self.burst_thread and self.burst_thread.is_alive():
                self.burst_thread.join(timeout=1.0)
            logger.debug("Ráfaga detenida")
        except Exception as e:
            logger.error(f"Error deteniendo ráfaga: {e}")

    def _create_sdp(self, call: SIPCall) -> str:
        """Crea SDP según RFC 4566."""
        try:
            timestamp = int(time.time())
            session_id = uuid.uuid4().hex[:8]
            
            sdp_lines = [
                "v=0",
                # o=<username> <sess-id> <sess-version> <nettype> <addrtype> <unicast-address>
                f"o=pysipp {session_id} {timestamp} IN IP4 {self.local_ip}",
                "s=pysipp call",
                # c=<nettype> <addrtype> <connection-address>
                f"c=IN IP4 {self.local_ip}",
                "t=0 0",
                # m=<media> <port> <proto> <fmt> ...
                f"m=audio {call.rtp_port} RTP/AVP 0 8 101",
                # RFC 3551 - RTP/AVP Payload Types
                "a=rtpmap:0 PCMU/8000",
                "a=rtpmap:8 PCMA/8000",
                "a=rtpmap:101 telephone-event/8000",
                "a=fmtp:101 0-16",
                "a=ptime:20",
                "a=sendrecv",
                # RFC 3605 - RTCP attributes
                f"a=rtcp:{call.rtp_port + 1}",
                "a=ice-ufrag:pysipp",
                "a=ice-pwd:pysippcall"
            ]
            
            return "\r\n".join(sdp_lines) + "\r\n"
            
        except Exception as e:
            logger.error(f"Error creando SDP: {e}")
            raise

    def handle_response(self, response: str):
        """Maneja respuestas a mensajes SIP."""
        try:
            call_id = self._extract_header(response, "Call-ID")
            status_line = response.split('\r\n')[0]
            status_code = int(status_line.split()[1])
            
            if call_id not in self.active_calls:
                logger.error(f"Respuesta para llamada desconocida: {call_id}")
                return
                
            call = self.active_calls[call_id]
            
            # Manejar según el código de respuesta
            if 100 <= status_code < 200:
                # Respuestas provisionales
                if status_code == 100:
                    call.state = CallState.TRYING.value
                elif status_code == 180:
                    call.state = CallState.RINGING.value
                self._update_call_state(call.call_id, call.state)
                
            elif status_code == 200:
                # Extraer to_tag del 200 OK
                to_header = self._extract_header(response, "To")
                if ';tag=' in to_header:
                    call.to_tag = to_header.split(';tag=')[1]
                
                # Actualizar estado y enviar ACK
                call.state = CallState.ESTABLISHED.value
                self._update_call_state(call.call_id, call.state)
                self._send_ack(call)
                
            else:
                # Manejar errores según RFC 3261
                error_messages = {
                    400: "Solicitud incorrecta",
                    401: "No autorizado",
                    403: "Prohibido",
                    404: "No encontrado",
                    408: "Timeout",
                    480: "Temporalmente no disponible",
                    486: "Ocupado",
                    487: "Solicitud terminada",
                    488: "No aceptable",
                    500: "Error interno del servidor",
                    503: "Servicio no disponible",
                    603: "Declinado"
                }
                
                error_msg = error_messages.get(status_code, f"Error {status_code}")
                logger.warning(f"Llamada {call.call_id} fallida: {error_msg}")
                
                # Actualizar estado y limpiar
                call.state = CallState.FAILED.value
                self._update_call_state(call.call_id, call.state)
                self._cleanup_call(call.call_id)
                
                # Notificar UI
                self.call_failed.emit(call.call_id, error_msg)
                
        except Exception as e:
            logger.error(f"Error procesando respuesta: {e}")

    def _handle_trying_response(self, call: SIPCall):
        """Maneja respuesta 100 Trying"""
        if call.state != CallState.TRYING.value:
            call.state = CallState.TRYING.value
            self._update_call_state(call.call_id, call.state)
            logger.debug(f"Llamada {call.call_id} en estado TRYING")

    def _handle_ringing_response(self, call: SIPCall):
        """Maneja respuesta 180 Ringing"""
        if call.state != CallState.RINGING.value:
            call.state = CallState.RINGING.value
            self._update_call_state(call.call_id, call.state)
            logger.debug(f"Llamada {call.call_id} en estado RINGING")

    def _handle_ok_response(self, call: SIPCall, headers: dict, response: str):
        """Maneja respuesta 200 OK"""
        try:
            if "INVITE" not in headers.get('cseq', ''):
                logger.debug("200 OK no es para INVITE, ignorando")
                return
            
            # Extraer to_tag
            to_header = headers.get('to', '')
            if ';tag=' in to_header:
                call.to_tag = to_header.split(';tag=')[1]
                logger.debug(f"To-tag extraído: {call.to_tag}")
            else:
                logger.error("No se encontró to-tag en 200 OK")
                return
            
            # Procesar SDP
            if not self._process_sdp_response(call, response):
                logger.error("Error procesando SDP de 200 OK")
                return
            
            # Actualizar estado
            call.state = CallState.ESTABLISHED.value
            self._update_call_state(call.call_id, call.state)
            logger.debug(f"Llamada {call.call_id} establecida")
            
            # Enviar ACK
            self._send_ack(call)
            
        except Exception as e:
            logger.error(f"Error procesando 200 OK: {e}", exc_info=True)

    def _process_sdp_response(self, call: SIPCall, response: str) -> bool:
        """Procesa el SDP de la respuesta."""
        try:
            # Encontrar el SDP en la respuesta
            sdp_start = response.find('\r\n\r\n') + 4
            if sdp_start <= 4:
                logger.error("No se encontró SDP en la respuesta")
                return False
            
            sdp = response[sdp_start:]
            sdp_lines = sdp.split('\r\n')
            
            # Extraer información necesaria del SDP
            for line in sdp_lines:
                if line.startswith('m=audio '):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            call.remote_rtp_port = int(parts[1])
                            logger.debug(f"Puerto RTP remoto encontrado: {call.remote_rtp_port}")
                            return True
                        except ValueError:
                            logger.error(f"Puerto RTP inválido en SDP: {parts[1]}")
                            return False
        
            logger.error("No se encontró puerto de audio en SDP")
            return False
        
        except Exception as e:
            logger.error(f"Error procesando SDP: {e}")
            return False

    def _send_ack(self, call: SIPCall):
        """Envía ACK para confirmar establecimiento de llamada."""
        try:
            # Generar nuevo branch para el ACK
            ack_branch = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
            
            # Construir ACK según RFC 3261
            ack_message = (
                f"ACK sip:{call.to_uri}@{self.remote_ip} SIP/2.0\r\n"
                f"Via: SIP/2.0/{self.transport} {self.local_ip}:{self.local_port}"
                f";branch={ack_branch}\r\n"
                f"From: <sip:{call.from_uri}@{self.local_ip}>;tag={call.from_tag}\r\n"
                f"To: <sip:{call.to_uri}@{self.remote_ip}>;tag={call.to_tag}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} ACK\r\n"
                "Max-Forwards: 70\r\n"
                f"Contact: <sip:{call.from_uri}@{self.local_ip}:{self.local_port}>\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            logger.debug(f"Enviando ACK para llamada {call.call_id}")
            if self.send_message(ack_message.encode()):
                logger.debug("ACK enviado correctamente")
                return True
            else:
                logger.error("Error enviando ACK")
                return False
            
        except Exception as e:
            logger.error(f"Error enviando ACK: {e}")
            return False

    def terminate_all_calls(self):
        """Termina todas las llamadas activas."""
        try:
            logger.debug("Terminando todas las llamadas activas")
            for call_id, call in list(self.active_calls.items()):
                if call.state not in [CallState.TERMINATED.value, CallState.FAILED.value]:
                    logger.debug(f"Enviando BYE para llamada {call_id}")
                    if self._send_bye(call):
                        time.sleep(0.1)  # Pequeña pausa entre BYEs
                    else:
                        # Si falla el BYE, forzar limpieza
                        self._cleanup_call(call_id)
                    
            # Actualizar estadísticas
            self._update_stats()
            
        except Exception as e:
            logger.error(f"Error terminando llamadas: {e}")

    def _send_bye(self, call: SIPCall) -> bool:
        """Envía mensaje BYE para terminar una llamada."""
        try:
            # Generar nuevo branch para el BYE
            bye_branch = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
            
            # Construir mensaje BYE según RFC 3261
            bye_message = (
                f"BYE sip:{call.to_uri}@{self.remote_ip} SIP/2.0\r\n"
                f"Via: SIP/2.0/{self.transport} {self.local_ip}:{self.local_port}"
                f";branch={bye_branch}\r\n"
                f"From: <sip:{call.from_uri}@{self.local_ip}>;tag={call.from_tag}\r\n"
                f"To: <sip:{call.to_uri}@{self.remote_ip}>;tag={call.to_tag}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq + 1} BYE\r\n"
                "Max-Forwards: 70\r\n"
                f"Contact: <sip:{call.from_uri}@{self.local_ip}:{self.local_port}>\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            logger.debug(f"Enviando BYE para llamada {call.call_id}")
            if self.send_message(bye_message.encode()):
                call.state = CallState.TERMINATED.value
                self._update_call_state(call.call_id, call.state)
                logger.debug("BYE enviado correctamente")
                return True
            else:
                logger.error("Error enviando BYE")
                return False
            
        except Exception as e:
            logger.error(f"Error enviando BYE: {e}")
            return False

    def _cleanup_call(self, call_id: str, emit_signals: bool = True):
        """Limpia los recursos de una llamada."""
        if call_id in self.active_calls:
            try:
                # Limpiar RTP primero
                self._cleanup_rtp_session(call_id)
                
                # Limpiar transacción
                self._cleanup_transaction(call_id)
                
                # Actualizar estadísticas
                self.stats["active"] -= 1
                
                # Emitir señales solo si no estamos en proceso de cierre
                if emit_signals and not self._shutting_down:
                    self._update_stats()
                
                # Finalmente eliminar la llamada
                del self.active_calls[call_id]
                
            except Exception as e:
                logger.error(f"Error en _cleanup_call para {call_id}: {e}")

    def _cleanup_rtp_session(self, call_id: str):
        session = self.rtp_sessions.get(call_id)
        if session:
            session['running'] = False
            session['socket'].close()
            del self.rtp_sessions[call_id]

    def _cleanup_transaction(self, call_id: str):
        timer_id = f"{call_id}_transaction"
        if timer_id in self.timers:
            self.timers[timer_id].cancel()
            del self.timers[timer_id]
            
        if call_id in self.transaction_states:
            del self.transaction_states[call_id]

    def _start_session_refresh_timer(self):
        def refresh_worker():
            while True:
                for call_id, call in list(self.active_calls.items()):
                    if self.session_timer.needs_refresh(call_id):
                        self._send_session_refresh(call)
                time.sleep(5)
                
        threading.Thread(target=refresh_worker, daemon=True).start()

    def cleanup(self):
        """Limpia recursos antes de cerrar."""
        try:
            logger.debug("Iniciando limpieza de SIPCallHandler")
            self._shutting_down = True
            
            # Cancelar todos los timers activos
            for timer_id, timer in list(self.timers.items()):
                try:
                    timer.cancel()
                    del self.timers[timer_id]
                except Exception as e:
                    logger.error(f"Error cancelando timer {timer_id}: {e}")

            # Terminar todas las llamadas activas
            for call_id in list(self.active_calls.keys()):
                try:
                    self._cleanup_call(call_id, emit_signals=False)
                except Exception as e:
                    logger.error(f"Error limpiando llamada {call_id}: {e}")
                    
            # Limpiar otras estructuras
            self.active_calls.clear()
            self.rtp_sessions.clear()
            self.transaction_states.clear()
            
            # Limpiar transacciones
            self._transaction_ids.clear()
            
            logger.debug("Limpieza de SIPCallHandler completada")
            
        except Exception as e:
            logger.error(f"Error durante cleanup de SIPCallHandler: {e}")

    def _extract_header(self, message: str, header_name: str) -> str:
        """Extrae el valor de un header específico del mensaje SIP."""
        try:
            lines = message.split('\r\n')
            for line in lines:
                if line.startswith(f"{header_name}: "):
                    return line[len(header_name) + 2:]
                elif line.startswith(f"{header_name}:"):
                    return line[len(header_name) + 1:]
            return ""
        except Exception as e:
            logger.error(f"Error extrayendo header {header_name}: {e}")
            return ""

    def handle_incoming_options(self, options_message: str):
        """Maneja OPTIONS entrantes."""
        try:
            logger.debug("="*50)
            logger.debug("PROCESANDO OPTIONS ENTRANTE")
            
            # Incrementar contador de OPTIONS recibidos
            self.stats["options"]["received"] += 1
            
            # Crear y enviar respuesta 200 OK
            response = self._create_options_response(options_message)
            if self.send_message(response.encode()):
                self.stats["options"]["ok_sent"] += 1
                logger.debug("200 OK enviado para OPTIONS")
            
            # Emitir actualización de estadísticas
            self._update_monitoring_stats()
            
        except Exception as e:
            logger.error(f"Error procesando OPTIONS entrante: {e}")

    def handle_options_response(self, response: str):
        """Maneja respuestas a OPTIONS enviados."""
        try:
            status_line = response.split('\r\n')[0]
            response_code = int(status_line.split()[1])
            
            if response_code == 200:
                self.stats["options"]["ok_received"] += 1
                logger.debug("200 OK recibido para OPTIONS")
            
            self._update_monitoring_stats()
            
        except Exception as e:
            logger.error(f"Error procesando respuesta OPTIONS: {e}")

    def _update_monitoring_stats(self):
        """Actualiza y emite las estadísticas de monitorización."""
        try:
            # Emitir señal con todas las estadísticas
            self.monitoring_stats_updated.emit({
                "options_sent": self.stats["options"]["sent"],
                "options_received": self.stats["options"]["received"],
                "ok_sent": self.stats["options"]["ok_sent"],
                "ok_received": self.stats["options"]["ok_received"]
            })
            
            logger.debug(f"Estadísticas actualizadas: {self.stats['options']}")
            
        except Exception as e:
            logger.error(f"Error actualizando estadísticas: {e}")

    def _create_options_response(self, options_message: str) -> str:
        """Crea respuesta 200 OK para OPTIONS."""
        try:
            headers = self._extract_all_headers(options_message)
            
            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers.get('via', '')}\r\n"
                f"From: {headers.get('from', '')}\r\n"
                f"To: {headers.get('to', '')}\r\n"
                f"Call-ID: {headers.get('call-id', '')}\r\n"
                f"CSeq: {headers.get('cseq', '')}\r\n"
                "Allow: INVITE, ACK, CANCEL, BYE, OPTIONS\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error creando respuesta OPTIONS: {e}")
            return ""

    def _update_call_status(self, call_info: dict):
        # Implementa la lógica para actualizar la tabla de llamadas en NetworkPanel
        pass

    def update_config(self, key: str, value: any):
        """Actualiza un valor específico de la configuración."""
        try:
            self.config[key] = value
            # Actualizar también los atributos específicos
            if key == 'remote_ip':
                self.remote_ip = value
                logger.debug(f"IP remota actualizada en call handler: {value}")
            elif key == 'local_ip':
                self.local_ip = value
            elif key == 'local_port':
                self.local_port = value
            elif key == 'remote_port':
                self.remote_port = value
            elif key == 'transport':
                self.transport = value
        except Exception as e:
            logger.error(f"Error actualizando configuración: {e}")