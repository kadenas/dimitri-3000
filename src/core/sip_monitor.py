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

    def __init__(self):
        super().__init__()
        
        # Estado del monitor
        self._monitoring_active = False
        self._stop_monitoring = threading.Event()
        self._options_thread: Optional[threading.Thread] = None
        
        # Conexiones
        self._server_socket: Optional[socket.socket] = None
        self._active_trunk: Optional[SIPTrunk] = None
        self._active_connection: Optional[TCPConnection] = None
        
        # Contadores y tiempos
        self._udp_cseq = 0
        self._cseq_lock = threading.Lock()
        self._last_options_response: Optional[datetime] = None
        self._last_rtt: Optional[float] = None
        self.active_calls = {}  # Diccionario para almacenar llamadas
        
        # Estadísticas
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

    # Propiedades
    @property
    def last_options_response(self) -> Optional[datetime]:
        return self._last_options_response
    
    @last_options_response.setter
    def last_options_response(self, value: datetime):
        self._last_options_response = value
        
    @property
    def last_rtt(self) -> Optional[float]:
        return self._last_rtt
        
    @property
    def is_monitoring(self) -> bool:
        return self._monitoring_active
        
    @property
    def stats(self) -> Dict:
        return self._stats.copy()

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

    def start_server(self, local_ip: str, local_port: int, transport: str) -> bool:
        """Inicia el servidor SIP."""
        try:
            # Guardar la configuración
            self.config = {
                'local_ip': local_ip,
                'local_port': local_port,
                'transport': transport,
            }
            
            # Crear el socket del servidor
            if transport.upper() == "UDP":
                self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Configuración específica para TCP
                self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if hasattr(socket, 'SO_REUSEPORT'):  # No disponible en todos los sistemas
                    self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            
            # Diagnóstico pre-bind
            print(f"Intentando vincular a {local_ip}:{local_port} ({transport})")
            
            # Vincular el socket
            self._server_socket.bind((local_ip, local_port))
            
            # Diagnóstico post-bind
            sock_name = self._server_socket.getsockname()
            print(f"Socket vinculado exitosamente a {sock_name}")
            
            # Para UDP, configurar un timeout para que el bucle pueda verificar la señal de parada
            if transport.upper() == "UDP":
                self._server_socket.settimeout(1.0)
            else:
                # Para TCP, escuchar conexiones
                self._server_socket.listen(5)
                # Sin timeout para TCP, accept() se bloqueará
            
            # Reiniciar variables de estado
            self._server_running = True
            self._active_connection = None
            
            # Iniciar el hilo del servidor
            self._server_thread = threading.Thread(
                target=self._run_server,
                args=(transport,),
                daemon=True
            )
            self._server_thread.start()
            
            print(f"Servidor iniciado en {local_ip}:{local_port} ({transport})")
            return True
            
        except Exception as e:
            print(f"Error iniciando servidor: {str(e)}")
            if self._server_socket:
                self._server_socket.close()
                self._server_socket = None
            return False

    def _run_server(self, transport: str):
        """Ejecuta el bucle del servidor."""
        print("Debug: _run_server iniciado")
        buffer_size = 65535
        
        try:
            print(f"Servidor escuchando en modo {transport}")
            while self._server_running:
                try:
                    if transport.upper() == "UDP":
                        try:
                            data, addr = self._server_socket.recvfrom(buffer_size)
                            if data:
                                self._handle_message(data, addr, transport)
                        except socket.timeout:
                            continue
                    else:  # TCP
                        try:
                            # En TCP primero aceptamos la conexión
                            client_socket, addr = self._server_socket.accept()
                            print(f"Nueva conexión TCP desde {addr}")
                            
                            # Configurar socket TCP
                            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                            if hasattr(socket, 'TCP_KEEPIDLE'):  # Solo en Linux
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                            
                            # Configurar timeout para operaciones de lectura/escritura
                            client_socket.settimeout(5)
                            
                            # Crear hilo para manejar esta conexión
                            client_thread = threading.Thread(
                                target=self._handle_tcp_client,
                                args=(client_socket, addr),
                                daemon=True
                            )
                            client_thread.start()
                            
                        except socket.timeout:
                            continue
                        except socket.error as e:
                            if not self._server_running:  # Error esperado al cerrar
                                break
                            print(f"Error aceptando conexión TCP: {e}")
                            continue
                                
                except Exception as e:
                    if self._server_running:  # Solo mostrar error si el servidor está activo
                        print(f"Error procesando conexión: {e}")
                    
        except Exception as e:
            print(f"Error en el bucle del servidor: {str(e)}")
        finally:
            # Limpieza al salir
            if self._server_socket:
                try:
                    self._server_socket.close()
                except:
                    pass
                self._server_socket = None
                
            # Cerrar conexión activa si existe
            if self._active_connection:
                try:
                    self._active_connection.socket.close()
                except:
                    pass
                self._active_connection = None
                
            print("Servidor detenido y sockets cerrados")

    def _handle_tcp_client(self, client_socket, addr):
        """Maneja una conexión TCP individual."""
        print(f"Debug: Iniciando manejo de cliente TCP {addr}")
        connection = None
        
        try:
            # Crear objeto de conexión
            connection = TCPConnection(client_socket, addr)
            
            # Si es el peer con el que queremos mantener el trunk, guardamos la conexión
            if addr[0] == self.config.get('remote_ip'):
                print(f"Debug: Usando conexión {addr} como conexión principal del trunk")
                self._active_connection = connection
                
            while self._server_running:
                try:
                    data = client_socket.recv(65535)
                    if not data:
                        print(f"Debug: Conexión cerrada por el cliente {addr}")
                        break
                    
                    # Procesar mensajes completos
                    messages = connection.add_data(data)
                    for msg in messages:
                        self._handle_message(msg, addr, "TCP")
                        
                except socket.timeout:
                    # Timeout normal, verificar actividad
                    if time.time() - connection.last_activity > self.config.get('timeout', 30):
                        print(f"Debug: Timeout en conexión TCP con {addr}")
                        break
                    continue
                    
        except Exception as e:
            print(f"Error en conexión TCP con {addr}: {e}")
            
        finally:
            # Limpiar recursos
            try:
                if connection and connection == self._active_connection:
                    print(f"Debug: Cerrando conexión principal con {addr}")
                    self._active_connection = None
                
                client_socket.close()
                print(f"Debug: Conexión TCP cerrada y eliminada para {addr}")
                
            except Exception as e:
                print(f"Error al limpiar conexión TCP: {e}")

    def _handle_udp_message(self, data: bytes, addr: tuple):
        """Procesa mensajes UDP entrantes."""
        try:
            message = data.decode('utf-8')
            if "OPTIONS" in message:
                self._stats['options_received'] += 1  # Contador explícito
                response = self._create_response_to_options(message)
                if response:
                    self._server_socket.sendto(response.encode(), addr)
                    self._stats['ok_sent'] += 1
                    logger.debug(f"Respuesta 200 OK enviada a {addr}")
                    
        except Exception as e:
            logger.error(f"Error procesando mensaje UDP: {str(e)}", exc_info=True)
        
    def _create_response_to_options(self, options_message: str) -> str:
        try:
            headers = {}
            for line in options_message.split('\r\n'):
                if ':' in line:
                    name, value = line.split(':', 1)
                    headers[name.strip()] = value.strip()

            if not all(h in headers for h in ['Via', 'From', 'To', 'Call-ID', 'CSeq']):
                return None

            return (
                "SIP/2.0 200 OK\r\n"
                f"Via: {headers['Via']}\r\n"
                f"From: {headers['From']}\r\n"
                f"To: {headers['To']};tag={uuid.uuid4().hex[:12]}\r\n"
                f"Call-ID: {headers['Call-ID']}\r\n"
                f"CSeq: {headers['CSeq']}\r\n"
                f"Contact: <sip:sip@{self.config['local_ip']}:{self.config['local_port']}>\r\n"
                "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE\r\n"
                "Supported: 100rel, timer\r\n"
                "User-Agent: PySIPP/1.0\r\n"
                "Content-Length: 0\r\n\r\n"
            )
        except Exception as e:
            print(f"Error creando respuesta OPTIONS: {e}")
            return None

    def _generate_tag(self):
        """Genera tag aleatorio para respuestas SIP"""
        return f"{int(time.time())}-{uuid.uuid4().hex[:6]}"

    def _handle_message(self, data: str, addr: tuple, transport: str):
        print(f"Debug: Recibiendo mensaje de {addr} por {transport}")
        if transport.upper() == "TCP" and self._active_trunk:
            print("Debug: Delegando mensaje a trunk TCP activo")
            return self._active_trunk.handle_incoming_message(data)
        else:
            print("Debug: Procesando mensaje UDP")
            return self._handle_udp_message(data, addr)

    def start_options_monitoring(self, config: Dict) -> bool:
        print("Debug: start_options_monitoring llamado")
        
        if self._monitoring_active:
            print("Debug: Monitoreo ya activo") 
            return False
            
        try:
            print(f"Debug: Configurando monitoreo con config: {config}")
            self.config.update(config)
            self._stop_monitoring.clear()
            self._monitoring_active = True
            
            if config['transport'].upper() == "TCP":
                print("Debug: Configurando trunk TCP")
                if not self._active_trunk:
                    print("Debug: Creando nuevo SIPTrunk")
                    self._active_trunk = SIPTrunk(config)
                    if not self._active_trunk.connect():
                        print("Debug: Error conectando trunk")
                        self._monitoring_active = False
                        return False
                    print("Debug: Trunk conectado exitosamente")
            
            print("Debug: Iniciando thread de monitoreo")
            self._options_thread = threading.Thread(
                target=self._options_monitoring_loop,
                args=(config,),
                daemon=True
            )
            self._options_thread.start()
            print("Debug: Thread de monitoreo iniciado")
            return True
        except Exception as e:
            print(f"Error al iniciar monitoreo: {e}")
            self._monitoring_active = False
            return False

    def stop_options_monitoring(self):
        """Detiene el monitoreo OPTIONS."""
        print("Debug: Deteniendo monitoreo OPTIONS")
        if self._monitoring_active:
            self._stop_monitoring.set()
            if self._options_thread:
                self._options_thread.join(timeout=1)
            self._monitoring_active = False
        print("Debug: Monitoreo OPTIONS detenido")

    def _options_monitoring_loop(self, config: Dict) -> None:
        logger.debug("Iniciando loop de monitoreo OPTIONS")
        while not self._stop_monitoring.is_set():
            try:
                success = False
                transport = config['transport'].upper()
                
                if transport == "TCP":
                    if self._active_trunk:
                        logger.debug("Enviando keepalive TCP usando trunk persistente")
                        success = self._active_trunk.send_keepalive()
                else:  # UDP
                    logger.debug("Enviando OPTIONS UDP independiente")
                    success = self._send_options_udp(config)
                
                # Actualizar estado y estadísticas
                if success:
                    self._stats['active'] += 1
                    self.trunk_state_changed.emit("UP")
                    logger.info(f"Monitoreo {transport} exitoso")
                else:
                    self._stats['failed'] += 1
                    self.trunk_state_changed.emit("DEGRADED")
                    logger.warning(f"Monitoreo {transport} fallido")
                
                self.stats_updated.emit()  # Notificar GUI
                
                interval = config.get('interval', 30)
                logger.debug(f"Esperando {interval}s para próximo ciclo")
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error en loop de monitoreo: {str(e)}", exc_info=True)
                time.sleep(5)

    def _send_options(self, config: Dict) -> bool:
        """Envía un mensaje OPTIONS y maneja la respuesta."""
        start_time = time.time()
        sock = None
        
        try:
            options_message = (
                f"OPTIONS sip:{config['remote_ip']} SIP/2.0\r\n"
                f"Via: SIP/2.0/{config['transport']} {config['local_ip']}:{config['local_port']}"
                f";branch=z9hG4bK-{int(time.time())}\r\n"
                f"From: <sip:{config['local_ip']}:{config['local_port']}>;tag={int(time.time())}\r\n"
                f"To: <sip:{config['remote_ip']}:{config['remote_port']}>\r\n"
                f"Call-ID: {int(time.time())}\r\n"
                "CSeq: 1 OPTIONS\r\n"
                f"Contact: <sip:{config['local_ip']}:{config['local_port']}>\r\n"
                "Max-Forwards: 70\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            print(f"\nDebug: Mensaje OPTIONS a enviar:")
            print("-" * 50)
            print(options_message)
            print("-" * 50)
            
            # Crear e inicializar socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(config.get('timeout', 5))
            
            # Registrar el envío y enviar el mensaje
            self._stats['options_sent'] += 1
            send_time = time.time()  # Tiempo exacto de envío
            sock.sendto(options_message.encode(), (config['remote_ip'], config['remote_port']))
            
            # Esperar y procesar respuesta
            try:
                data, addr = sock.recvfrom(65535)
                receive_time = time.time()  # Tiempo exacto de recepción
                response = data.decode('utf-8', errors='ignore')
                
                print(f"Respuesta recibida de {addr}:")
                print("-" * 50)
                print(response)
                print("-" * 50)
                
                if "200 OK" in response:
                    # Calcular y actualizar métricas
                    latency = (receive_time - send_time) * 1000  # Convertir a milisegundos
                    self._stats['ok_received'] += 1
                    self._stats['last_latency'] = latency
                    self._last_rtt = latency
                    self._last_options_response = datetime.now()
                    
                    print(f"Debug: Latencia medida: {latency:.2f} ms")
                    return True
                    
                response_line = response.split('\r\n')
                print(f"Debug: Respuesta recibida pero no es 200 OK: {response_line[0]}")
                return False
                    
            except socket.timeout:
                print(f"Debug: No se recibió respuesta OPTIONS de {config['remote_ip']}:{config['remote_port']} "
                        f"(timeout: {config.get('timeout', 5)}s)")
                self._stats['timeouts'] += 1
                return False
                    
        except Exception as e:
            print(f"Error enviando OPTIONS: {e}")
            return False
            
        finally:
            if sock:
                try:
                    sock.close()
                except Exception as e:
                    print(f"Error cerrando socket: {e}")

    def _send_options_udp(self, config: Dict) -> bool:
        """Envía OPTIONS UDP con validación de CSeq"""
        sock = None
        try:
            with self._cseq_lock:
                self._udp_cseq += 1
                current_cseq = self._udp_cseq

            # Construcción del mensaje
            call_id = f"{uuid.uuid4()}@{config['local_ip']}"
            branch_id = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
            from_tag = uuid.uuid4().hex[:8]

            options_message = (
                f"OPTIONS sip:{config['remote_ip']} SIP/2.0\r\n"
                f"Via: SIP/2.0/UDP {config['local_ip']}:{config['local_port']};branch={branch_id};rport\r\n"
                f"From: <sip:{config['local_ip']}>;tag={from_tag}\r\n"
                f"To: <sip:{config['remote_ip']}>\r\n"
                f"Call-ID: {call_id}\r\n"
                f"CSeq: {current_cseq} OPTIONS\r\n"
                f"Contact: <sip:{config['local_ip']}:{config['local_port']}>\r\n"
                "Max-Forwards: 70\r\n"
                "User-Agent: PySIPP-Monitor/1.0\r\n"
                "Supported: timer\r\n"
                "Content-Length: 0\r\n\r\n"
            )

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(config.get('timeout', 5))
            
            debug_log(f"Enviando OPTIONS UDP (CSeq: {current_cseq})")
            send_time = time.time()
            sock.sendto(options_message.encode('utf-8'), (config['remote_ip'], config['remote_port']))
            self._stats['options_sent'] += 1
            
            try:
                data, addr = sock.recvfrom(65535)
                receive_time = time.time()
                response = data.decode('utf-8', errors='ignore')
                
                if "SIP/2.0 200 OK" in response:
                    self.last_options_response = datetime.now()
                    # Validación de CSeq
                    received_cseq = self._parse_cseq(response)
                    
                    if received_cseq != current_cseq:
                        debug_log(f"Error: CSeq no coincide. Enviado: {current_cseq}, Recibido: {received_cseq}")
                        self._stats['errors'] += 1
                        return False
                    
                    # Cálculo de latencia
                    latency = (receive_time - send_time) * 1000
                    self._stats['ok_received'] += 1
                    self._stats['last_latency'] = latency
                    debug_log(f"Respuesta válida recibida | Latencia: {latency:.2f}ms")
                    return True
                    
            except socket.timeout:
                debug_log(f"Timeout para CSeq: {current_cseq}")
                self._stats['timeouts'] += 1
            except Exception as e:
                debug_log(f"Error procesando respuesta: {str(e)}")
                self._stats['errors'] += 1
            
            return False
            
        except Exception as e:
            debug_log(f"Error en OPTIONS UDP: {str(e)}")
            return False
        finally:
            if sock:
                try:
                    sock.close()
                except Exception as e:
                    debug_log(f"Error cerrando socket: {str(e)}")

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
        print("Debug: Iniciando parada del servidor SIP")
        self._server_running = False
        
        if self._active_trunk:
            print("Debug: Desconectando trunk TCP activo")
            self._active_trunk.disconnect()
            
        if self._server_socket:
            print("Debug: Cerrando socket del servidor")
            self._server_socket.close()
            self._server_socket = None
        print("Debug: Servidor detenido completamente")

    @property
    def stats(self) -> Dict:
        """Retorna las estadísticas actuales."""
        # Para TCP, combinar estadísticas del trunk si existe
        if self._active_trunk:
            trunk_stats = self._active_trunk.stats
            self._stats.update(trunk_stats)
        return self._stats
    
    @property
    def last_rtt(self) -> Optional[float]:
        return self._last_rtt
