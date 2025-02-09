from typing import Dict, Optional
import socket
import time
import uuid
import threading 
from datetime import datetime
from .trunk_states import SIPTrunkState
import logging
from .tcp_connection import TCPConnection
from PyQt6.QtCore import QObject, pyqtSignal

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SIPTrunk(QObject):
    """
    Representa un trunk SIP con conexión TCP persistente y monitoreo mediante OPTIONS.
    Implementa las recomendaciones de RFC 5626 y RFC 5923.
    """
    
    # Señales
    stats_updated = pyqtSignal()  # Para notificar actualizaciones de estadísticas
    rtt_updated = pyqtSignal(float)  # Para notificar nuevo RTT

    def __init__(self, config: Dict):
        """
        Inicializa un trunk SIP con conexión TCP persistente.
        
        Args:
            config: Diccionario con la configuración del trunk
            {
                'local_ip': str,
                'local_port': int,
                'remote_ip': str,
                'remote_port': int,
                'transport': str,
                'timeout': int,
                'interval': int
            }
        """
        super().__init__()
        self.config = config
        self._state = SIPTrunkState.DOWN
        self._cseq_lock = threading.Lock()
        self._cseq = 0
        self._instance_id = f"<urn:uuid:{uuid.uuid4()}>"
        self._last_options_sent = None
        self._last_keepalive = None
        self.stats = {
            'options_sent': 0,
            'options_received': 0,
            'ok_sent': 0,
            'ok_received': 0,
            'timeouts': 0,
            'reconnects': 0,
            'last_rtt': None,
            'connection_uptime': 0,
            'errors': 0
        }
        
        # Conexión y gestión TCP
        self._connection: Optional[socket.socket] = None
        self._persistent_connection = None
        self._connection_timestamp = None
        self._receive_buffer = b""
        self._keepalive_interval = config.get('interval', 30)  # segundos
        
        # Control de reconexión
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 3
        
        # Flow token y gestión de instancia
        self._flow_token = None
        self._instance_id = str(uuid.uuid4())
        
        # Timestamps y monitoreo
        self._last_keepalive: Optional[datetime] = None
        self._last_activity: Optional[datetime] = None
        
        # Nueva conexión TCP
        self.tcp_connection = TCPConnection()

        logger.debug("Creando nuevo SIPTrunk")

    def send_message(self, message: bytes):
        """Envía un mensaje a través de la conexión TCP."""
        try:
            if not self.tcp_connection or not self.tcp_connection.is_connected:
                logger.error("No hay conexión TCP activa")
                return False
                
            return self.tcp_connection.send_data(message.decode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error enviando mensaje TCP: {e}")
            return False

    def establish_persistent_connection(self) -> bool:
        """Establece una conexión TCP persistente."""
        try:
            if self._connection and self.is_connected:
                print("Debug: Ya existe una conexión persistente activa")
                return True

            print(f"Debug: Estableciendo conexión TCP persistente con {self.config['remote_ip']}:{self.config['remote_port']}")
            
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Configuración de socket para conexión persistente
            self._connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if hasattr(socket, 'TCP_KEEPIDLE'):
                self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
                self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
            
            self._connection.connect((self.config['remote_ip'], self.config['remote_port']))
            self._connection_timestamp = datetime.now()
            self._state = SIPTrunkState.UP
            
            print("Debug: Conexión TCP persistente establecida exitosamente")
            return True
            
        except Exception as e:
            print(f"Error estableciendo conexión persistente: {e}")
            self._handle_connection_failure()
            return False

    def _handle_connection_failure(self):
        """Maneja fallos en la conexión."""
        if self._connection:
            try:
                self._connection.close()
            except:
                pass
            self._connection = None
        self._state = SIPTrunkState.DOWN
    
    # Properties
    @property
    def state(self) -> SIPTrunkState:
        """Estado actual del trunk."""
        return self._state
        
    @property
    def is_connected(self) -> bool:
        """Indica si el trunk tiene una conexión activa y válida."""
        try:
            if self._connection is None:
                return False
            
            # Intentar verificar si la conexión está realmente viva
            # Enviamos un byte de keepalive TCP y vemos si causa error
            self._connection.send(b"\x00", socket.MSG_DONTWAIT)
            return True
        except socket.error:
            # Si hay error, la conexión está muerta
            self._connection = None
            self._state = SIPTrunkState.DOWN
            return False

    @property
    def last_keepalive(self) -> Optional[datetime]:
        """Retorna el timestamp del último keepalive exitoso."""
        return self._last_keepalive
    
    # Métodos de conexión

    def connect(self) -> bool:
        """Establece la conexión TCP."""
        try:
            if self.is_connected:
                logger.debug("Ya existe una conexión activa")
                return True
                
            logger.debug(f"Conectando a {self.config['remote_ip']}:{self.config['remote_port']}")
            
            if not self.tcp_connection:
                self.tcp_connection = TCPConnection()
                
            success = self.tcp_connection.connect(
                self.config['remote_ip'],
                self.config['remote_port'],
                timeout=self.config.get('timeout', 5)
            )
            
            if success:
                self._state = SIPTrunkState.UP
                logger.debug("Conexión TCP establecida")
            else:
                self._state = SIPTrunkState.DOWN
                logger.error("No se pudo establecer la conexión TCP")
                
            return success
            
        except Exception as e:
            logger.error(f"Error en conexión TCP: {e}")
            self._state = SIPTrunkState.DOWN
            return False

    def _send_initial_register(self):
        """Envía REGISTER inicial según RFC 5626 Sección 5.2"""
        try:
            # Verificar parámetros requeridos
            if 'domain' not in self.config or 'user' not in self.config:
                logger.error("Configuración incompleta para REGISTER: faltan 'domain' o 'user'")
                raise ValueError("Parámetros 'domain' y 'user' son requeridos para REGISTER")

            register_msg = (
                f"REGISTER sip:{self.config['domain']} SIP/2.0\r\n"
                f"Via: SIP/2.0/TCP {self.config['local_ip']}:{self.config['local_port']};"
                f"branch={self._generate_branch()}\r\n"
                f"From: <sip:{self.config['user']}@{self.config['domain']}>;"
                f"tag={uuid.uuid4().hex[:8]}\r\n"
                f"To: <sip:{self.config['user']}@{self.config['domain']}>\r\n"
                f"Call-ID: {uuid.uuid4()}@{self.config['local_ip']}\r\n"
                f"CSeq: 1 REGISTER\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']};transport=tcp>;"
                f"reg-id={self.config.get('reg_id', 1)};"
                f"+sip.instance=\"{self._instance_id}\";expires=3600\r\n"
                f"Supported: outbound, path\r\n"
                f"Flow-Token: {self._flow_token}\r\n"
                f"Max-Forwards: 70\r\n"
                f"Content-Length: 0\r\n\r\n"
            )
            
            self._connection.sendall(register_msg.encode())
            logger.debug("REGISTER inicial enviado")
            
        except KeyError as e:
            logger.error(f"Error en configuración: Parámetro faltante {str(e)}")
            raise
        except socket.error as e:
            logger.error(f"Error de conexión al enviar REGISTER: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en registro inicial: {str(e)}")
            raise

    def _generate_branch(self) -> str:
        """Genera parámetro branch según RFC 3261 Sección 8.1.1.7"""
        return f"z9hG4bK-{uuid.uuid4().hex[:16]}"
        
    def _generate_flow_token(self) -> str:
        """RFC 5626 Section 5.1 - Flow Token Format"""
        return f"{self.config.get('reg_id', 1)};" \
            f"+sip.instance=\"{self._instance_id}\";" \
            "ob"

    def maintain_connection(self):
        try:
            if not self.is_connected:
                print("Debug: Reconectando...")
                return self.connect()
                
            # Comparar timestamps en el mismo formato
            if self._last_keepalive:
                elapsed = (datetime.now() - self._last_keepalive).total_seconds()
                if elapsed > self._keepalive_interval:
                    self._connection.send(b"\r\n")
                    self._last_keepalive = datetime.now()
                
            return True
        except socket.error:
            return self._handle_reconnection()
        
    def _handle_reconnection(self):
        """Maneja reconexión con backoff exponencial"""
        delay = min(30, 2 ** self._reconnect_attempts) 
        logger.debug(f"Esperando {delay}s antes de reconectar (intento {self._reconnect_attempts})")
        time.sleep(delay)
        self._reconnect_attempts += 1
        return self.connect()

    def _handle_connection_failure(self):
        """Maneja fallos en la conexión con backoff exponencial."""
        self._reconnect_attempts += 1
        delay = min(30, 2 ** self._reconnect_attempts)  # Máximo 30 segundos
        logger.debug(f"Esperando {delay} segundos antes de reconectar (intento {self._reconnect_attempts})")
        time.sleep(delay)

    def disconnect(self):
        """Cierra la conexión TCP persistente de manera limpia."""
        if self._connection:
            try:
                # Enviar FIN TCP
                self._connection.shutdown(socket.SHUT_RDWR)
                self._connection.close()
            except:
                pass
            finally:
                self._connection = None
        self._state = SIPTrunkState.DOWN
        print("Debug: Conexión TCP persistente cerrada")
    
    def _handle_connection_error(self):
        """Maneja errores de conexión."""
        self._state = SIPTrunkState.RECOVERING
        self._reconnect_attempts += 1
        
        if self._reconnect_attempts <= self._max_reconnect_attempts:
            if self.connect():
                self._reconnect_attempts = 0
                self.stats['reconnects'] += 1
        else:
            self._state = SIPTrunkState.DOWN
    
    # Métodos de keepalive y OPTIONS
    def send_keepalive(self) -> bool:
        """
        Envía un mensaje OPTIONS como keepalive y maneja la respuesta.
        
        Returns:
            bool: True si el keepalive fue exitoso, False en caso contrario
        """
        try:
            # 1. Verificar/restablecer conexión
            if not self.maintain_connection():
                logger.warning("No se pudo establecer la conexión para keepalive")
                return False

            # 2. Seleccionar tipo de mensaje según transporte
            transport = self.config.get('transport', 'TCP').upper()
            if transport == 'TCP':
                options_message = self._create_tcp_options_message()
            else:
                options_message = self._create_udp_options_message()

            logger.debug(f"Enviando keepalive {transport}:\n{options_message}")
            
            # 3. Envío del mensaje
            self._connection.sendall(options_message.encode('utf-8'))
            self.stats['options_sent'] += 1

            # 4. Esperar y procesar respuesta
            start_time = time.time()
            response = self._receive_response()
            
            # 5. Validar respuesta
            if response and "SIP/2.0 200 OK" in response:
                self._update_keepalive_timestamp()
                self.stats['ok_received'] += 1
                self._reconnect_attempts = 0  # Resetear intentos fallidos
                logger.info(f"Keepalive exitoso. RTT: {(time.time() - start_time)*1000:.2f}ms")
                return True

            # 6. Manejar fallo
            logger.warning("Keepalive fallido. No se recibió 200 OK")
            self.stats['timeouts'] += 1

            # 7. Reintentar si es posible
            if self._reconnect_attempts < self._max_reconnect_attempts:
                logger.debug(f"Reintentando keepalive ({self._reconnect_attempts + 1}/{self._max_reconnect_attempts})")
                self._reconnect_attempts += 1
                return self.send_keepalive()

            return False

        except (socket.error, ConnectionResetError, TimeoutError) as e:
            logger.error(f"Error de conexión en keepalive: {str(e)}", exc_info=True)
            self._handle_connection_error()
            return False
        except Exception as e:
            logger.critical(f"Error inesperado en keepalive: {str(e)}", exc_info=True)
            return False
    
    def _create_base_headers(self) -> dict:
        """Genera los headers comunes para TCP y UDP"""
        with self._cseq_lock:
            self._cseq += 1
        
        return {
            'From': f'<sip:{self.config["local_ip"]}>;tag={uuid.uuid4().hex[:8]}',
            'To': f'<sip:{self.config["remote_ip"]}>',
            'Call-ID': f'{uuid.uuid4()}@{self.config["local_ip"]}',
            'CSeq': f'{self._cseq} OPTIONS',
            'Max-Forwards': '70',
            'User-Agent': 'PySIPP-Monitor/1.0',
            'Content-Length': '0'
        }

    def _create_tcp_options_message(self) -> str:
        self._cseq += 1
        return (
            "OPTIONS sip:{remote_ip} SIP/2.0\r\n"
            "Via: SIP/2.0/TCP {local_ip}:{local_port};branch={branch};rport\r\n"
            "From: <sip:{local_ip}>;tag={tag}\r\n"
            "To: <sip:{remote_ip}>\r\n"
            "Call-ID: {call_id}\r\n"
            "CSeq: {cseq} OPTIONS\r\n"
            "Contact: <sip:{local_ip}:{local_port}>;reg-id={reg_id};+sip.instance=\"{instance_id}\"\r\n"
            "Supported: outbound, path, gruu\r\n"  # RFC 5626 Section 5.1
            "Flow-Token: {flow_token}\r\n"
            "User-Agent: PySIPP-Monitor/1.0\r\n"
            "Max-Forwards: 70\r\n"
            "Content-Length: 0\r\n\r\n"
        ).format(
            remote_ip=self.config['remote_ip'],
            local_ip=self.config['local_ip'],
            local_port=self.config['local_port'],
            branch=f"z9hG4bK-{uuid.uuid4().hex}",
            tag=uuid.uuid4().hex[:8],
            call_id=f"{uuid.uuid4()}@{self.config['local_ip']}",
            cseq=self._cseq,
            reg_id=self.config.get('reg_id', 1),
            instance_id=self._instance_id,
            flow_token=self._flow_token
        )

    def _create_udp_options_message(self) -> str:
        """Crea mensaje OPTIONS específico para UDP"""
        headers = self._create_base_headers()
        headers.update({
            'Via': f'SIP/2.0/UDP {self.config["local_ip"]}:{self.config["local_port"]};'
                f'branch=z9hG4bK-{uuid.uuid4().hex[:16]};rport',
            'Contact': f'<sip:{self.config["local_ip"]}:{self.config["local_port"]}>',
            'Supported': 'timer'
        })
        return self._build_sip_message(headers)

    def _build_sip_message(self, headers: dict) -> str:
        """Construye el mensaje SIP completo desde los headers"""
        request_line = f'OPTIONS sip:{self.config["remote_ip"]} SIP/2.0\r\n'
        headers_str = '\r\n'.join(f'{k}: {v}' for k, v in headers.items())
        return f'{request_line}{headers_str}\r\n\r\n'

    
    def handle_incoming_message(self, message: str) -> bool:
        """Maneja mensajes entrantes en el trunk."""
        try:
            logger.debug(f"Mensaje recibido en trunk:\n{message}")
            
            # Si es OPTIONS, procesar y responder
            if "OPTIONS" in message:
                logger.debug("OPTIONS recibido en trunk")
                self.stats['options_received'] += 1
                
                response = self._create_options_response(message)
                if response:
                    success = self.tcp_connection.send_data(response)
                    if success:
                        self.stats['ok_sent'] += 1
                        logger.debug("200 OK enviado desde trunk")
                    return success
                
            # Si es respuesta 200 OK
            elif "SIP/2.0 200 OK" in message:
                logger.debug("200 OK recibido en trunk")
                self.stats['ok_received'] += 1
                
            # Notificar actualización de estadísticas
            if hasattr(self, 'stats_updated'):
                self.stats_updated.emit()
                
            return True
            
        except Exception as e:
            logger.error(f"Error manejando mensaje en trunk: {e}")
            return False
    
    def _create_options_response(self, options_message: str) -> Optional[str]:
        """
        Crea una respuesta 200 OK basada en el mensaje OPTIONS recibido.
        Mantiene los campos necesarios del mensaje original.
        """
        try:
            # Extraer campos necesarios del OPTIONS recibido
            via_header = None
            from_header = None
            to_header = None
            call_id = None
            cseq = None

            # Procesar el mensaje línea por línea
            for line in options_message.split('\r\n'):
                if line.startswith('Via:'):
                    via_header = line
                elif line.startswith('From:'):
                    from_header = line
                elif line.startswith('To:'):
                    to_header = line
                elif line.startswith('Call-ID:'):
                    call_id = line
                elif line.startswith('CSeq:'):
                    cseq = line

            # Verificar que tenemos todos los campos necesarios
            if not all([via_header, from_header, to_header, call_id, cseq]):
                print("Error: Mensaje OPTIONS incompleto")
                return None

            # Construir la respuesta manteniendo los campos originales
            response = (
                "SIP/2.0 200 OK\r\n"
                f"{via_header}\r\n"
                f"{from_header}\r\n"
                f"{to_header}\r\n"
                f"{call_id}\r\n"
                f"{cseq}\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Content-Length: 0\r\n"
                "\r\n"
            )

            return response

        except Exception as e:
            print(f"Error creando respuesta OPTIONS: {e}")
            return None
    
    # Métodos de manejo de mensajes TCP

    def _receive_response(self, timeout: int = 5) -> Optional[str]:
        """Recibe una respuesta SIP a través de la conexión TCP."""
        try:
            if not self.tcp_connection or not self.tcp_connection.is_connected:
                logger.error("No hay conexión TCP activa para recibir respuesta")
                return None

            start_time = time.time()
            response = ""
            
            while time.time() - start_time < timeout:
                data = self.tcp_connection.receive_data()
                if data:
                    response += data
                    if "\r\n\r\n" in response:  # Mensaje SIP completo
                        logger.debug(f"Respuesta recibida: {response}")
                        return response
                time.sleep(0.1)  # Pequeña pausa para no saturar CPU
                
            logger.warning("Timeout esperando respuesta SIP")
            self.stats['timeouts'] += 1
            return None
            
        except Exception as e:
            logger.error(f"Error recibiendo respuesta: {e}")
            return None

    @property
    def is_connected(self) -> bool:
        """Verifica si la conexión TCP persistente está activa."""
        if not self._connection:
            return False
            
        try:
            # Intento de envío de datos nulos para verificar conexión
            self._connection.send(b"", socket.MSG_DONTWAIT)
            
            # Verificar tiempo desde último keepalive exitoso
            if self._last_keepalive:
                elapsed = (datetime.now() - self._last_keepalive).total_seconds()
                if elapsed > self._keepalive_interval * 2:
                    print("Debug: Conexión expirada por timeout de keepalive")
                    return False
                    
            return True
            
        except socket.error:
            print("Debug: Conexión TCP no disponible")
            return False

    @property
    def flow_token(self) -> Optional[str]:
        """
        Getter para obtener el flow token actual.
        Returns:
            Optional[str]: El flow token actual o None si no está establecido
        """
        return self._flow_token

    @property
    def last_keepalive(self) -> Optional[datetime]:
        """
        Getter para obtener el timestamp del último keepalive exitoso.
        Returns:
            Optional[datetime]: Timestamp del último keepalive o None si no hay
        """
        return self._last_keepalive

    def _update_keepalive_timestamp(self):
        """
        Actualiza el timestamp del último keepalive exitoso al momento actual.
        """
        self._last_keepalive = datetime.now()

    def is_keepalive_expired(self, timeout_seconds: int = 35) -> bool:
        """
        Verifica si el keepalive ha expirado según el timeout especificado.
        
        Args:
            timeout_seconds: Segundos después de los cuales se considera expirado
                            (35 segundos por defecto según RFC 5626)
        
        Returns:
            bool: True si el keepalive ha expirado, False si está vigente
        """
        if not self._last_keepalive:
            return True
            
        elapsed = (datetime.now() - self._last_keepalive).total_seconds()
        return elapsed > timeout_seconds

    
    def __del__(self):
        """Limpieza al destruir el objeto."""
        self.disconnect()

    def handle_options_response(self, response):
        """Maneja las respuestas OPTIONS."""
        try:
            if response and 'headers' in response:
                timestamp = datetime.now()
                if self._last_options_sent:
                    rtt = (timestamp - self._last_options_sent).total_seconds() * 1000
                    self.last_rtt = rtt
                    
                self.stats['ok_received'] += 1
                self._update_led_status(True)
                return True
        except Exception as e:
            logger.error(f"Error handling OPTIONS response: {e}")
        return False

    def _update_led_status(self, active: bool):
        """Actualiza el estado del LED basado en la actividad."""
        if hasattr(self, 'led_indicator'):
            self.led_indicator.setActive(active)

    def _ensure_tcp_connection(self):
        """Asegura que la conexión TCP está activa."""
        try:
            if not self.tcp_connection or not self.tcp_connection.is_connected:
                logger.debug("Reconectando TCP...")
                return self.connect()
            return True
        except Exception as e:
            logger.error(f"Error en _ensure_tcp_connection: {e}")
            return False

    def send_options(self) -> bool:
        """Envía mensaje OPTIONS manteniendo la conexión TCP."""
        try:
            if not self._ensure_tcp_connection():
                logger.error("No hay conexión TCP disponible")
                return False
            
            message = self._create_options_message()
            logger.debug(f"Enviando OPTIONS: {message}")
            
            # Incrementar contador y guardar tiempo de envío
            self.stats['options_sent'] += 1
            send_time = time.time()
            
            if self.config.get('transport', 'TCP').upper() == "TCP":
                if not self.send_message(message.encode('utf-8')):
                    logger.error("Error enviando mensaje TCP")
                    return False
                    
                # Esperar respuesta con timeout
                response = self._receive_response(timeout=self.config.get('timeout', 5))
                if response:
                    if "200 OK" in response:
                        # Calcular RTT aquí donde realmente ocurre el intercambio
                        rtt = (time.time() - send_time) * 1000
                        self.stats['last_rtt'] = rtt
                        logger.debug(f"RTT TCP calculado en trunk: {rtt:.2f}ms")
                        
                        self._update_keepalive_timestamp()
                        self.stats['ok_received'] += 1
                        self._state = SIPTrunkState.UP
                        
                        # Emitir señales para actualizar UI
                        self.rtt_updated.emit(rtt)
                        self.stats_updated.emit()
                        
                        logger.debug("Respuesta 200 OK recibida")
                        return True
                    else:
                        logger.warning(f"Respuesta no esperada: {response.splitlines()[0]}")
                        self._state = SIPTrunkState.DEGRADED
                else:
                    logger.warning("No se recibió respuesta al OPTIONS")
                    self.stats['timeouts'] += 1
                    self._state = SIPTrunkState.DOWN
                    self.stats_updated.emit()
            
            return False
            
        except Exception as e:
            logger.error(f"Error en send_options: {e}")
            self._state = SIPTrunkState.DOWN
            return False

    def _create_options_message(self) -> str:
        """Crea un mensaje OPTIONS SIP."""
        branch = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
        call_id = f"{uuid.uuid4()}@{self.config['local_ip']}"
        from_tag = uuid.uuid4().hex[:8]
        
        with self._cseq_lock:
            self._cseq += 1
            cseq = self._cseq

        message = (
            f"OPTIONS sip:{self.config['remote_ip']} SIP/2.0\r\n"
            f"Via: SIP/2.0/TCP {self.config['local_ip']}:{self.config['local_port']}"
            f";branch={branch};rport\r\n"
            f"Max-Forwards: 70\r\n"
            f"From: <sip:{self.config['local_ip']}>;tag={from_tag}\r\n"
            f"To: <sip:{self.config['remote_ip']}>\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: {cseq} OPTIONS\r\n"
            f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
            "User-Agent: PySIPP-Monitor/1.0\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        
        logger.debug(f"Mensaje OPTIONS creado:\n{message}")
        self._last_options_sent = datetime.now()
        return message

    def _create_response_to_options(self, options_message: str) -> Optional[str]:
        """Crea una respuesta 200 OK para un mensaje OPTIONS."""
        try:
            # Extraer campos necesarios del OPTIONS recibido
            headers = {}
            for line in options_message.split('\r\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers[key.lower()] = value
                elif line.startswith('Via:'):
                    headers['via'] = line[4:].strip()
                elif line.startswith('From:'):
                    headers['from'] = line[5:].strip()
                elif line.startswith('To:'):
                    headers['to'] = line[3:].strip()
                elif line.startswith('Call-ID:'):
                    headers['call-id'] = line[8:].strip()
                elif line.startswith('CSeq:'):
                    headers['cseq'] = line[5:].strip()

            # Construir respuesta
            response = (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers.get('via', '')}\r\n"
                f"From: {headers.get('from', '')}\r\n"
                f"To: {headers.get('to', '')};tag={uuid.uuid4().hex[:8]}\r\n"
                f"Call-ID: {headers.get('call-id', '')}\r\n"
                f"CSeq: {headers.get('cseq', '')}\r\n"
                f"Contact: <sip:{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Content-Length: 0\r\n"
                "\r\n"
            )
            
            logger.debug(f"Respuesta OPTIONS creada:\n{response}")
            return response
            
        except Exception as e:
            logger.error(f"Error creando respuesta OPTIONS: {e}")
            return None

