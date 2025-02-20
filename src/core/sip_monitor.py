from typing import Optional, Dict, Tuple
import uuid
import socket
import time
import logging
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal
from .sip_trunk import SIPTrunk
from .trunk_states import SIPTrunkState
from .tcp_connection import TCPConnection
from ..utils.logger import debug_log
from .models import CallData

logger = logging.getLogger(__name__)

class SIPMonitor(QObject):
    # Señales
    trunk_state_changed = pyqtSignal(str)       # Estado del trunk
    stats_updated = pyqtSignal()                # Actualización de estadísticas 
    call_status_changed = pyqtSignal(str, str)  # Estado de llamadas
    rtt_updated = pyqtSignal(float)               # Actualización de RTT

    MAX_UDP_SIZE = 65507  # Tamaño máximo de datagrama UDP

    def __init__(self):
        super().__init__()
        
        # Socket y threads
        self._server_socket = None
        self._receive_thread = None
        self._stop_flag = True
        
        # Monitorización
        self._monitoring_active = False
        self._stop_monitoring = threading.Event()
        self._options_thread = None
        
        # Contadores y estado
        self._udp_cseq = 0
        self._cseq_lock = threading.Lock()
        self._last_options_response_time = None
        self._last_options_sent_time = None
        self._last_rtt = None
        
        # Estadísticas
        self._stats = {
            'options_sent': 0,
            'options_received': 0,
            'ok_sent': 0,
            'ok_received': 0,
            'timeouts': 0,
            'errors': 0,
            'last_latency': None
        }
        
        # Configuración
        self.config = None
        self.call_handler = None
        
        # Conexiones
        self._active_trunk: Optional[SIPTrunk] = None
        self._active_connection: Optional[TCPConnection] = None
        
        # Contadores y tiempos
        self.active_calls = {}  # Diccionario para almacenar llamadas
        
        self._observers = []

    # Propiedades
    @property
    def last_options_response(self) -> Optional[datetime]:
        return self._last_options_response_time
    
    @property
    def last_rtt(self) -> Optional[float]:
        return self._last_rtt
        
    @property
    def is_monitoring(self) -> bool:
        return self._monitoring_active
        
    @property
    def stats(self) -> Dict:
        """Retorna las estadísticas actuales combinadas."""
        combined_stats = self._stats.copy()
        
        # Si hay un trunk TCP activo, combinar estadísticas
        if self._active_trunk and self.config.get('transport', '').upper() == 'TCP':
            trunk_stats = self._active_trunk.stats
            logger.debug(f"Obteniendo estadísticas del trunk: {trunk_stats}")
            
            # Actualizar estadísticas desde el trunk
            combined_stats.update({
                'options_sent': trunk_stats.get('options_sent', 0),
                'ok_received': trunk_stats.get('ok_received', 0),
                'last_latency': trunk_stats.get('last_rtt', combined_stats.get('last_latency')),
                'timeouts': trunk_stats.get('timeouts', 0)
            })
            
            # Asegurar que el RTT se propaga
            if trunk_stats.get('last_rtt') is not None:
                self._last_rtt = trunk_stats['last_rtt']
                combined_stats['last_latency'] = self._last_rtt
        
        return combined_stats

    def test_connectivity(self, remote_ip: str, remote_port: int, transport: str = "UDP") -> bool:
        """Prueba la conectividad básica con el destino."""
        print(f"Debug: Probando conectividad con {remote_ip}:{remote_port} via {transport}")
        try:
            if transport.upper() == "TCP" and self._active_trunk:
                # Usar el trunk existente para TCP
                return self._active_trunk.connect()
            
            # Para UDP o si no hay trunk activo
            sock = None
            try:
                if transport.upper() == "UDP":
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(2)
                
                if transport.upper() != "UDP":
                    sock.connect((remote_ip, remote_port))
                else:
                    sock.sendto(b"", (remote_ip, remote_port))
                
                print(f"Debug: Conectividad exitosa con {remote_ip}:{remote_port}")
                return True
                
            finally:
                if sock:
                    sock.close()
                    
        except Exception as e:
            print(f"Debug: Error de conectividad con {remote_ip}:{remote_port} - {str(e)}")
            return False

    def start_server(self, config: Dict) -> bool:
        """Inicia el servidor SIP."""
        try:
            self.config = config
            transport = config.get('transport', 'UDP').upper()
            
            if transport == 'UDP':
                self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
            self._server_socket.bind((config['local_ip'], config['local_port']))
            logger.info(f"Servidor iniciado en {config['local_ip']}:{config['local_port']} ({transport})")
            
            # Iniciar thread de recepción
            self._stop_flag = False
            self._receive_thread = threading.Thread(target=self._receive_loop)
            self._receive_thread.daemon = True
            self._receive_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error iniciando servidor: {e}")
            return False

    def _run_server(self, transport: str):
        """Loop principal del servidor."""
        logger.debug("_run_server iniciado")
        
        try:
            while self._server_running:
                if transport == 'TCP':
                    try:
                        if not self._server_socket:
                            logger.error("Socket del servidor no disponible")
                            break
                            
                        # Configurar timeout para el accept
                        self._server_socket.settimeout(1)
                        
                        try:
                            client_socket, addr = self._server_socket.accept()
                            logger.debug(f"Nueva conexión TCP desde {addr}")
                            client_thread = threading.Thread(
                                target=self._handle_tcp_client,
                                args=(client_socket, addr)
                            )
                            client_thread.daemon = True
                            client_thread.start()
                        except socket.timeout:
                            # Timeout normal, continuar el loop
                            continue
                        except OSError as e:
                            if not self._server_running:
                                # Si el servidor se está deteniendo, salir limpiamente
                                logger.debug("Servidor detenido, cerrando _run_server")
                                break
                            else:
                                # Si es otro error, loggearlo
                                logger.error(f"Error en accept TCP: {e}")
                                
                    except Exception as e:
                        if self._server_running:
                            logger.error(f"Error en loop TCP: {e}")
                        break
                else:  # UDP
                    try:
                        if not self._server_socket:
                            logger.error("Socket del servidor no disponible")
                            break
                            
                        self._server_socket.settimeout(1)
                        try:
                            data, addr = self._server_socket.recvfrom(65535)
                            self._handle_udp_message(data, addr)
                        except socket.timeout:
                            continue
                        except OSError as e:
                            if not self._server_running:
                                break
                            else:
                                logger.error(f"Error en recvfrom UDP: {e}")
                                
                    except Exception as e:
                        if self._server_running:
                            logger.error(f"Error en loop UDP: {e}")
                        break
                    
        except Exception as e:
            logger.error(f"Error en _run_server: {e}")
        finally:
            logger.debug("_run_server finalizado")

    def _handle_tcp_client(self, client_socket, address):
        """Maneja una nueva conexión TCP cliente."""
        try:
            logger.debug(f"Iniciando manejo de cliente TCP {address}")
            connection = TCPConnection.from_existing_connection(client_socket, address)
            
            while True:
                data = connection.handle_incoming_data()
                if not data:
                    break
                
                logger.debug(f"Mensaje TCP recibido de {address}:\n{data}")
                
                # Si es una respuesta SIP
                if data.startswith("SIP/2.0"):
                    if "200 OK" in data:
                        if "OPTIONS" in data:
                            self._handle_options_response(data)
                        else:
                            logger.debug("Pasando respuesta al call handler")
                            if self.call_handler:
                                self.call_handler.handle_response(data)
                    continue
                
                # Si es un INVITE
                if "INVITE" in data:
                    logger.debug("INVITE recibido - pasando al call handler")
                    if self.call_handler:
                        self.call_handler.handle_incoming_invite(data)
                    continue
                
                # Si es un OPTIONS
                if "OPTIONS" in data:
                    logger.debug("OPTIONS TCP recibido")
                    self._stats['options_received'] += 1
                    
                    response = self._create_response_to_options(data)
                    if response and connection.is_connected:
                        if connection.send_data(response):
                            self._stats['ok_sent'] += 1
                            logger.debug(f"200 OK TCP enviado a {address}")
                    
                    self.stats_updated.emit()
                
        except Exception as e:
            logger.error(f"Error en conexión TCP con {address}: {e}")
        finally:
            try:
                connection.disconnect()
                logger.debug(f"Conexión TCP cerrada y eliminada para {address}")
            except Exception as e:
                logger.error(f"Error cerrando conexión TCP: {e}")

    def _handle_udp_message(self, data: bytes, addr: tuple):
        """Maneja mensajes UDP recibidos."""
        try:
            message = data.decode('utf-8', errors='ignore')
            
            # Ignorar mensajes propios (desde nuestra IP)
            if addr[0] == self.config['local_ip']:
                logger.debug(f"Ignorando mensaje desde IP local: {addr[0]}")
                return
            
            logger.debug(f"Mensaje UDP recibido de {addr}:\n{message}")
            
            # Procesar mensajes entrantes
            if message.startswith("OPTIONS"):
                # OPTIONS entrante
                logger.debug("OPTIONS entrante detectado")
                self._stats['options_received'] += 1
                self._handle_options_message(message, addr)
                return
            
            elif message.startswith("SIP/2.0 200 OK"):
                # Verificar si es respuesta a nuestro OPTIONS
                cseq_line = next((line for line in message.split('\r\n') if line.startswith('CSeq:')), None)
                if cseq_line and "OPTIONS" in cseq_line:
                    logger.debug("200 OK entrante para OPTIONS")
                    # Ya no incrementamos aquí ok_received, lo hacemos en _handle_options_response
                    self._handle_options_response(message)
                    return
                elif cseq_line and "INVITE" in cseq_line and self.call_handler:
                    # Respuesta a INVITE - pasar al call handler
                    logger.debug("200 OK entrante para INVITE")
                    self.call_handler.handle_response(message)
                    return
                
            # Si llegamos aquí, es otro tipo de mensaje SIP
            if self.call_handler:
                self.call_handler.handle_message(message, addr)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje UDP: {e}")

    def _handle_options_response(self, response: str):
        """Maneja SOLO respuestas a OPTIONS."""
        try:
            self._last_options_response_time = datetime.now()
            self._stats['ok_received'] += 1  # Solo incrementamos aquí
            
            if self._last_options_sent_time:
                rtt = (datetime.now() - self._last_options_sent_time).total_seconds() * 1000
                self._last_rtt = rtt
                self._stats['last_latency'] = rtt
                logger.debug(f"Emitiendo RTT: {rtt:.2f} ms")
                self.rtt_updated.emit(rtt)
            
            logger.debug("Emitiendo actualización de estadísticas")
            self.stats_updated.emit()
            
        except Exception as e:
            logger.error(f"Error procesando respuesta OPTIONS: {e}")

    def _create_options_response(self, request: str) -> str:
        """Crea una respuesta 200 OK para OPTIONS."""
        try:
            # Extraer headers necesarios de la solicitud
            via = self._extract_header(request, "Via")
            from_header = self._extract_header(request, "From")
            to_header = self._extract_header(request, "To")
            call_id = self._extract_header(request, "Call-ID")
            cseq = self._extract_header(request, "CSeq")

            if not all([via, from_header, to_header, call_id, cseq]):
                logger.error("Faltan headers requeridos en la solicitud OPTIONS")
                return ""

            # Generar tag para To si no existe
            if ";tag=" not in to_header:
                to_header = f"{to_header};tag={uuid.uuid4().hex[:8]}"

            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {via}\r\n"
                f"From: {from_header}\r\n"
                f"To: {to_header}\r\n"
                f"Call-ID: {call_id}\r\n"
                f"CSeq: {cseq}\r\n"
                "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error creando respuesta OPTIONS: {e}")
            return ""

    def _create_response_to_options(self, options_message: str) -> Optional[str]:
        """Crea una respuesta 200 OK para un mensaje OPTIONS."""
        try:
            headers = {}
            for line in options_message.split('\r\n'):
                if ':' in line:
                    name, value = line.split(':', 1)
                    headers[name.strip()] = value.strip()

            if not all(h in headers for h in ['Via', 'From', 'To', 'Call-ID', 'CSeq']):
                logger.error("Faltan headers requeridos en el mensaje OPTIONS")
                return None

            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers['Via']}\r\n"
                f"From: {headers['From']}\r\n"
                f"To: {headers['To']};tag={uuid.uuid4().hex[:12]}\r\n"
                f"Call-ID: {headers['Call-ID']}\r\n"
                f"CSeq: {headers['CSeq']}\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE\r\n"
                "Supported: 100rel, timer\r\n"
                "User-Agent: PySIPP/1.0\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            logger.debug(f"Respuesta OPTIONS creada:\n{response}")
            return response
            
        except Exception as e:
            logger.error(f"Error creando respuesta OPTIONS: {e}")
            return None

    def _generate_tag(self):
        """Genera tag aleatorio para respuestas SIP"""
        return f"{int(time.time())}-{uuid.uuid4().hex[:6]}"

    def _handle_message(self, data: str, addr: tuple, transport: str):
        """Maneja mensajes entrantes."""
        logger.debug(f"Recibiendo mensaje de {addr} por {transport}")
        try:
            if transport.upper() == "TCP" and self._active_trunk and self._active_trunk.tcp_connection:
                logger.debug("Delegando mensaje a trunk TCP activo")
                return self._active_trunk.handle_incoming_message(data)
            else:
                logger.debug("Procesando mensaje UDP")
                return self._handle_udp_message(data.encode(), addr)
        except Exception as e:
            logger.error(f"Error manejando mensaje: {e}")

    def start_options_monitoring(self, config: Dict) -> bool:
        """Inicia el monitoreo OPTIONS."""
        try:
            logger.debug(f"Configurando monitoreo con config: {config}")
            
            # Detener monitoreo existente si lo hay
            self.stop_options_monitoring()
            
            # Configurar nuevo monitoreo
            self._monitoring_active = True
            self._stop_monitoring.clear()
            
            # Para TCP, configurar el trunk primero
            if config['transport'].upper() == 'TCP':
                logger.debug("Configurando trunk TCP")
                self._active_trunk = SIPTrunk(config)
                if not self._active_trunk.connect():
                    logger.error("No se pudo establecer la conexión TCP inicial")
                    return False
                logger.debug("Trunk TCP configurado correctamente")
            
            # Iniciar thread de monitoreo
            logger.debug("Iniciando thread de monitoreo")
            self._options_thread = threading.Thread(
                target=self._options_monitoring_loop,
                args=(config,),
                daemon=True
            )
            self._options_thread.start()
            logger.debug("Thread de monitoreo iniciado")
            
            return True
            
        except Exception as e:
            logger.error(f"Error iniciando monitoreo OPTIONS: {e}")
            self._monitoring_active = False
            return False

    def stop_options_monitoring(self):
        """Detiene el monitoreo OPTIONS."""
        logger.debug("Deteniendo monitoreo OPTIONS")
        if self._monitoring_active:
            self._stop_monitoring.set()
            if self._options_thread:
                self._options_thread.join(timeout=2)
            self._monitoring_active = False
            self._options_thread = None
        logger.debug("Monitoreo OPTIONS detenido")

    def _options_monitoring_loop(self, config: Dict) -> None:
        """Loop principal de monitoreo OPTIONS."""
        logger.debug("Iniciando loop de monitoreo OPTIONS")
        transport = config['transport'].upper()
        last_options_time = 0
        interval = config.get('interval', 30)
        
        while not self._stop_monitoring.is_set():
            try:
                current_time = time.time()
                
                # Verificar si es tiempo de enviar OPTIONS
                if current_time - last_options_time < interval:
                    time.sleep(min(interval, 5))
                    continue
                    
                success = False
                
                if transport == "TCP":
                    if not self._active_trunk:
                        logger.error("No hay trunk TCP configurado")
                        time.sleep(5)
                        continue
                    
                    if not self._active_trunk.tcp_connection.is_connected:
                        logger.debug("Reconectando trunk TCP...")
                        if not self._active_trunk.connect():
                            logger.error("Reconexión TCP fallida")
                            self.trunk_state_changed.emit("DOWN")
                            time.sleep(5)
                            continue
                    
                    logger.debug(f"Enviando OPTIONS por TCP (último envío hace {current_time - last_options_time:.1f}s)")
                    success = self._active_trunk.send_options()
                    
                    if success:
                        last_options_time = current_time
                        # Obtener estadísticas del trunk
                        trunk_stats = self._active_trunk.stats
                        logger.debug(f"Estadísticas recibidas del trunk: {trunk_stats}")
                        
                        # Actualizar estadísticas locales
                        self._stats.update({
                            'options_sent': trunk_stats.get('options_sent', 0),
                            'ok_received': trunk_stats.get('ok_received', 0),
                            'timeouts': trunk_stats.get('timeouts', 0),
                            'last_latency': trunk_stats.get('last_rtt')
                        })
                        
                        # Actualizar RTT si está disponible
                        if trunk_stats.get('last_rtt') is not None:
                            self._last_rtt = trunk_stats['last_rtt']
                            self.rtt_updated.emit(trunk_stats['last_rtt'])
                        
                        # Notificar cambios
                        self.stats_updated.emit()
                        self.trunk_state_changed.emit("UP")
                    else:
                        # En caso de fallo, actualizar timeouts
                        self._stats['timeouts'] = trunk_stats.get('timeouts', 0)
                        self._last_rtt = None
                        self.stats_updated.emit()
                        self.trunk_state_changed.emit("DEGRADED")
                
                else:  # UDP
                    logger.debug("Enviando OPTIONS UDP")
                    start_time = time.time()  # Tiempo de inicio para RTT
                    success = self._send_options_udp(config)
                    if success:
                        last_options_time = current_time
                        # Calcular RTT correctamente
                        rtt = (time.time() - start_time) * 1000
                        self._stats['last_rtt'] = rtt
                        self.rtt_updated.emit(rtt)
                        self.trunk_state_changed.emit("UP")
                    else:
                        self.trunk_state_changed.emit("DEGRADED")
                
                # Notificar actualización de estadísticas
                self.stats_updated.emit()
                
                # Esperar un tiempo razonable antes de la siguiente iteración
                time.sleep(min(interval/2, 5))
                
            except Exception as e:
                logger.error(f"Error en loop de monitoreo: {e}", exc_info=True)
                self.trunk_state_changed.emit("DOWN")
                time.sleep(5)

    def _send_options_udp(self, config: Dict) -> bool:
        """Envía OPTIONS UDP."""
        try:
            with self._cseq_lock:
                self._udp_cseq += 1
            
            message = self._create_options_message()
            logger.debug(f"Enviando OPTIONS:\n{message}")
            
            self._last_options_sent_time = datetime.now()
            
            # Enviar mensaje y actualizar contador de enviados
            try:
                self._server_socket.sendto(
                    message.encode(),
                    (self.config['remote_ip'], self.config['remote_port'])
                )
                self._stats['options_sent'] += 1  # Solo incrementar al enviar
                logger.debug("OPTIONS enviado correctamente")
                
                # Esperar respuesta con timeout
                timeout = config.get('timeout', 5)
                start_time = time.time()
                last_response_time = self._last_options_response_time
                
                while (time.time() - start_time) < timeout:
                    if (self._last_options_response_time and 
                        self._last_options_response_time != last_response_time and
                        self._last_options_response_time > self._last_options_sent_time):
                        return True
                    time.sleep(0.1)
                
                # Timeout
                logger.warning(f"Timeout esperando respuesta OPTIONS ({timeout}s)")
                self._stats['timeouts'] += 1
                self._last_rtt = None
                self._stats['last_latency'] = None
                
                self.rtt_updated.emit(0)
                self.trunk_state_changed.emit("INACTIVE")
                self.stats_updated.emit()
                
                return False
                
            except Exception as e:
                logger.error(f"Error enviando OPTIONS: {e}")
                self.trunk_state_changed.emit("ERROR")
                return False
            
        except Exception as e:
            logger.error(f"Error en _send_options_udp: {e}")
            self.trunk_state_changed.emit("ERROR")
            return False

    def _parse_cseq(self, response: str) -> int:
        """
        Extrae el valor numérico del CSeq de una respuesta SIP
        Returns:
            int: Valor del CSeq o -1 si hay error
        """
        for line in response.split('\r\n'):
            if line.startswith('CSeq:'):
                try:
                    # Formato esperado: "CSeq: 1234 OPTIONS"
                    parts = line.split(': ')[1].strip().split()
                    return int(parts[0])
                except (IndexError, ValueError) as e:
                    debug_log(f"CSeq inválido: {line} - {str(e)}")
                    return -1
        debug_log("No se encontró CSeq en la respuesta")
        return -1

    def send_message(self, message: bytes):
        """
        Envía un mensaje SIP usando el socket del servidor.
        
        Args:
            message: Mensaje en bytes para enviar
        """
        try:
            if not hasattr(self, 'config') or 'remote_ip' not in self.config:
                print("Debug: No hay configuración de IP remota")
                return False
                
            if self._server_socket:
                self._server_socket.sendto(message, (self.config['remote_ip'], self.config['remote_port']))
                print(f"Debug: Mensaje enviado a {self.config['remote_ip']}:{self.config['remote_port']}")
                return True
            else:
                print("Debug: No hay socket de servidor disponible")
                return False
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            return False

    def stop_server(self):
        """Detiene el servidor SIP."""
        try:
            logger.debug("Deteniendo servidor SIP")
            self._stop_flag = True
            
            if hasattr(self, '_server_socket') and self._server_socket:
                try:
                    self._server_socket.close()
                except Exception as e:
                    logger.error(f"Error cerrando socket: {e}")
                    
            if hasattr(self, '_receive_thread') and self._receive_thread:
                try:
                    self._receive_thread.join(timeout=2)
                except Exception as e:
                    logger.error(f"Error esperando thread de recepción: {e}")
                    
            self._server_socket = None
            self._receive_thread = None
            logger.debug("Servidor SIP detenido")
            
        except Exception as e:
            logger.error(f"Error deteniendo servidor: {e}")

    @property
    def last_rtt(self) -> Optional[float]:
        return self._last_rtt

    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)

    def reset_stats(self):
        """Resetea las estadísticas del monitor."""
        self._stats = {
            'options_sent': 0,
            'options_received': 0,
            'ok_sent': 0,
            'ok_received': 0,
            'timeouts': 0,
            'errors': 0,
            'last_latency': None,
            'active': 0,
            'failed': 0
        }
        logger.debug("Estadísticas reseteadas")
        self.stats_updated.emit()

    def send_udp_message(self, message: bytes) -> bool:
        """Envía un mensaje UDP."""
        try:
            if not self._server_socket:
                logger.error("Socket del servidor no inicializado")
                return False
                
            if isinstance(message, str):
                message = message.encode()
                
            # Verificar tamaño del mensaje
            if len(message) > self.MAX_UDP_SIZE:
                logger.error(f"Mensaje excede el tamaño máximo UDP ({len(message)} > {self.MAX_UDP_SIZE})")
                return False
                
            logger.debug(f"Enviando UDP a {self.config['remote_ip']}:{self.config['remote_port']}")
            logger.debug(f"Usando socket local: {self._server_socket.getsockname()}")
            
            bytes_sent = self._server_socket.sendto(message, (self.config['remote_ip'], self.config['remote_port']))
            logger.debug(f"Bytes enviados: {bytes_sent}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error enviando mensaje UDP: {e}", exc_info=True)
            return False

    def send_tcp_message(self, message: bytes) -> bool:
        """Envía un mensaje TCP."""
        try:
            if not self._active_trunk or not self._active_trunk.tcp_connection:
                logger.error("Conexión TCP no disponible")
                return False
                
            if isinstance(message, str):
                message = message.encode()
                
            success = self._active_trunk.tcp_connection.send_data(message.decode())
            if success:
                logger.debug(f"Mensaje TCP enviado a {self.config['remote_ip']}:{self.config['remote_port']}")
            else:
                logger.error("Error enviando mensaje TCP")
            return success
            
        except Exception as e:
            logger.error(f"Error enviando mensaje TCP: {e}")
            return False

    def handle_options_response(self, response):
        """Maneja la respuesta OPTIONS recibida."""
        try:
            if "200 OK" in response:
                self._last_options_response_time = datetime.now()
                # Calcular RTT
                if hasattr(self, '_last_options_sent_time'):
                    self._last_rtt = (self._last_options_response_time - self._last_options_sent_time).total_seconds() * 1000
                self._stats['ok_received'] += 1
                self.stats_updated.emit()
                
            return self._format_options_status()
            
        except Exception as e:
            logger.error(f"Error procesando respuesta OPTIONS: {e}")
            return "Error"

    def _format_options_status(self) -> str:
        """Formatea el estado OPTIONS para mostrar."""
        if not self._monitoring_active:
            return "Inactivo"
        
        if self._last_rtt is not None:
            return f"OK (RTT: {self._last_rtt:.2f}ms)"
        
        return "OK"  # Simplemente mostrar OK sin la hora

    def get_options_status(self) -> str:
        """Retorna el estado actual de OPTIONS."""
        if not self._monitoring_active:
            return "Monitoreo inactivo"
            
        if self._last_rtt is not None:
            return f"OK (RTT: {self._last_rtt:.2f}ms)"
        
        return "Sin respuesta"

    def update_status(self) -> str:
        """Actualiza y retorna el estado del monitor."""
        if not self._monitoring_active:
            return "Monitoreo inactivo"
            
        return self.get_options_status()

    def _create_options_message(self) -> str:
        """Crea un mensaje OPTIONS SIP."""
        try:
            with self._cseq_lock:
                current_cseq = self._udp_cseq
            
            # Generar IDs únicos
            call_id = f"{uuid.uuid4()}@{self.config['local_ip']}"
            branch_id = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
            from_tag = uuid.uuid4().hex[:8]

            # Construir mensaje OPTIONS
            message = (
                f"OPTIONS sip:{self.config['remote_ip']} SIP/2.0\r\n"
                f"Via: SIP/2.0/UDP {self.config['local_ip']}:{self.config['local_port']}"
                f";branch={branch_id};rport\r\n"
                f"From: <sip:{self.config['local_ip']}>;tag={from_tag}\r\n"
                f"To: <sip:{self.config['remote_ip']}>\r\n"
                f"Call-ID: {call_id}\r\n"
                f"CSeq: {current_cseq} OPTIONS\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Max-Forwards: 70\r\n"
                "User-Agent: PySIPP-Monitor/1.0\r\n"
                "Supported: timer\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            logger.debug(f"Mensaje OPTIONS creado:\n{message}")
            return message
            
        except Exception as e:
            logger.error(f"Error creando mensaje OPTIONS: {e}")
            return ""

    def _extract_header(self, message: str, header: str) -> Optional[str]:
        """Extrae un header de una cadena de texto."""
        for line in message.split('\r\n'):
            if line.startswith(f"{header}: "):
                return line[len(header) + 2:]
        return None

    def _handle_options_message(self, message: str, addr: tuple):
        """Maneja SOLO mensajes OPTIONS entrantes."""
        try:
            # Ya incrementamos options_received en _handle_udp_message
            
            response = self._create_options_response(message)
            if response:
                encoded_response = response.encode()
                if len(encoded_response) > self.MAX_UDP_SIZE:
                    logger.error("Respuesta OPTIONS excede el tamaño máximo UDP")
                    return
                    
                self._server_socket.sendto(encoded_response, addr)
                self._stats['ok_sent'] += 1  # Incrementar contador de OK enviados
                logger.debug("200 OK enviado para OPTIONS")
                
            self.stats_updated.emit()
            
        except Exception as e:
            logger.error(f"Error en _handle_options_message: {e}")

    def _handle_sip_response(self, message: str, addr: tuple):
        """Maneja respuestas SIP."""
        try:
            if "200 OK" in message and addr[0] == self.config['remote_ip']:
                cseq_line = next((line for line in message.split('\r\n') if line.startswith('CSeq:')), None)
                if cseq_line:
                    if "OPTIONS" in cseq_line:
                        logger.debug("Respuesta 200 OK a OPTIONS detectada")
                        self._handle_options_response(message)
                        # Asegurar que se emite la señal de actualización
                        self.stats_updated.emit()
                    elif "INVITE" in cseq_line and self.call_handler:
                        logger.debug("Respuesta a INVITE recibida - pasando al call handler")
                        self.call_handler.handle_response(message)
        except Exception as e:
            logger.error(f"Error procesando respuesta SIP: {e}")

    def _receive_loop(self):
        """Loop principal para recibir mensajes UDP."""
        logger.debug("Iniciando loop de recepción UDP")
        
        try:
            while not getattr(self, '_stop_flag', True):
                try:
                    # Configurar timeout para poder chequear _stop_flag
                    self._server_socket.settimeout(0.5)
                    
                    try:
                        data, addr = self._server_socket.recvfrom(self.MAX_UDP_SIZE)
                        if data:
                            # Procesar mensaje en un thread separado para no bloquear
                            threading.Thread(
                                target=self._handle_udp_message,
                                args=(data, addr),
                                daemon=True
                            ).start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if not getattr(self, '_stop_flag', True):
                            logger.error(f"Error recibiendo datos UDP: {e}")
                        continue
                        
                except Exception as e:
                    if not getattr(self, '_stop_flag', True):
                        logger.error(f"Error en loop de recepción: {e}")
                    time.sleep(1)  # Evitar CPU alto en caso de error
                    
        except Exception as e:
            logger.error(f"Error fatal en _receive_loop: {e}")
        finally:
            logger.debug("Loop de recepción UDP finalizado")
