from typing import Dict, Optional
import socket
import time
import uuid
import threading 
from datetime import datetime
from .trunk_states import SIPTrunkState
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SIPTrunk:
    """
    Representa un trunk SIP con conexión TCP persistente y monitoreo mediante OPTIONS.
    Implementa las recomendaciones de RFC 5626 y RFC 5923.
    """
    
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
        # Configuración básica
        self.config = config
        self._state = SIPTrunkState.DOWN
        self._cseq_lock = threading.Lock()
        self._cseq = 0
        self._instance_id = f"<urn:uuid:{uuid.uuid4()}>"

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
        
        # Estadísticas
        self.stats = {
            'options_sent': 0,
            'options_received': 0,
            'ok_sent': 0,
            'ok_received': 0,
            'timeouts': 0,
            'reconnects': 0,
            'last_rtt': None,
            'connection_uptime': 0
        }
        
        # Buffer para mensajes TCP
        self._receive_buffer = b""

    def send_message(self, message: bytes):
        try:
            if self._connection:
                self._connection.sendall(message)
                return True
            return False
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
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
        """Establece conexión TCP persistente según RFC 5626 Sección 5.5 y RFC 5923."""
        max_retries = 3
        backoff_base = 2  # segundos para backoff exponencial
        timeout = self.config.get('timeout', 30)  # RFC 5923 Sección 4.1
        
        for attempt in range(max_retries):
            try:
                # 1. Limpieza inicial (RFC 5923 Sección 4.2.1)
                if self._connection:
                    self.disconnect()
                
                # 2. Configuración inicial del socket
                self._state = SIPTrunkState.CONNECTING
                self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # 3. Configurar Keep-Alive según RFC 5626 Sección 5.5
                self._connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                if hasattr(socket, 'TCP_KEEPIDLE'):
                    self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)  # 30s inactividad
                    self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)  # 10s entre checks
                    self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)    # 3 intentos
                
                # 4. Timeouts según RFC 5923 Sección 4.1
                connect_timeout = min(30, timeout * (attempt + 1))
                self._connection.settimeout(connect_timeout)
                
                # 5. Establecer conexión
                logger.debug(f"Intento {attempt+1} de conexión a {self.config['remote_ip']}:{self.config['remote_port']}")
                self._connection.connect((self.config['remote_ip'], self.config['remote_port']))
                
                # 6. Configuración post-conexión
                self._connection.settimeout(timeout)
                self._flow_token = self._generate_flow_token()
                self._state = SIPTrunkState.UP
                self._last_keepalive = datetime.now()
                
                # 7. Registro inicial (RFC 5626 Sección 5.2)
                if self.config.get('auto_register', False):
                    self._send_initial_register()
                
                logger.info(f"Conexión establecida (Intento {attempt+1})")
                return True
                
            except (socket.timeout, ConnectionRefusedError) as e:
                logger.warning(f"Error de conexión (Intento {attempt+1}): {str(e)}")
                time.sleep(backoff_base ** attempt)
                continue
                
            except Exception as e:
                logger.error(f"Error inesperado: {str(e)}", exc_info=True)
                self._handle_connection_error()
                break
                
        # Si fallan todos los intentos
        self._state = SIPTrunkState.DOWN
        logger.error("Falló la conexión después de %d intentos", max_retries)
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
                if self._reconnect_attempts < self._max_reconnect_attempts:
                    if self.connect():
                        self._reconnect_attempts = 0
                        return True
                return False

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
        try:
            if isinstance(message, bytes):
                message = message.decode('utf-8', errors='ignore')
                
            if "OPTIONS" in message.split('\r\n')[0]:
                self.stats['options_received'] += 1
                response = self._create_response_to_options(message)
                
                if response and self._connection:
                    try:
                        response_bytes = response.encode('utf-8')
                        self._connection.sendall(response_bytes)
                        self.stats['ok_sent'] += 1
                        print(f"Debug: Mensaje SIP recibido y procesado: {message[:50]}...")
                        return True
                    except socket.error as e:
                        print(f"Error enviando respuesta: {e}")
                        self._handle_connection_error()
                        return False
                        
            return False
            
        except Exception as e:
            print(f"Error manejando mensaje entrante: {e}")
            return False
    
    def _create_response_to_options(self, options_message: str) -> Optional[str]:
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

    def _receive_response(self, buffer_size: int = 4096) -> Optional[str]:
        buffer = b""
        start_time = time.time()
        timeout = self.config.get('timeout', 10)
        
        try:
            self._connection.settimeout(timeout/2)
            
            while time.time() - start_time < timeout:
                try:
                    chunk = self._connection.recv(buffer_size)
                    if not chunk:
                        continue
                    
                    buffer += chunk
                    if b"\r\n\r\n" in buffer:
                        return buffer.decode('utf-8')
                    
                except socket.timeout:
                    continue
                
            return None
            
        except socket.error as e:
            print(f"Debug: Error en socket durante recepción: {e}")
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

