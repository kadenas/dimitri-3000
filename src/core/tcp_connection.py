import socket
import time
import logging
from typing import Optional, List, Tuple, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TCPConnection:
    """
    Maneja una conexión TCP individual para SIP.
    Se integra con SIPTrunk para el manejo de conexiones persistentes.
    """
    
    def __init__(self):
        self._socket = None
        self._connected = False
        self._last_error = None
        self.buffer = ""
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'last_activity': None,
            'connection_time': None,
            'reconnection_attempts': 0
        }
        self.max_buffer_size = 8192  # Aumentado para mensajes SIP más grandes
        self._keep_alive_interval = 30  # segundos
        self._last_keep_alive = None

    @property
    def is_connected(self):
        return self._connected and self._socket is not None
        
    def connect(self, host: str, port: int, timeout: int = 5) -> bool:
        """Establece la conexión TCP."""
        try:
            if self.is_connected:
                logger.debug("Ya existe una conexión activa")
                return True

            logger.debug(f"Conectando a {host}:{port}")
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(timeout)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Intentar conexión
            logger.debug(f"Intentando conexión TCP a {host}:{port}")
            self._socket.connect((host, port))
            
            self._connected = True
            self._last_host = host
            self._last_port = port
            self.stats['connection_time'] = datetime.now()
            logger.debug("Conexión TCP establecida exitosamente")
            return True
            
        except ConnectionRefusedError:
            logger.error(f"Conexión rechazada por {host}:{port}")
            self._connected = False
            return False
        except Exception as e:
            logger.error(f"Error estableciendo conexión TCP: {e}")
            self._connected = False
            return False

    def disconnect(self):
        if self._socket:
            try:
                self._socket.close()
            finally:
                self._socket = None
                self._connected = False

    def receive_data(self, size: int = 4096) -> Optional[str]:
        """Recibe datos del socket y los añade al buffer."""
        try:
            if not self._socket:
                return None
                
            data = self._socket.recv(size)
            if not data:
                self._connected = False
                return None
                
            decoded_data = data.decode('utf-8')
            self.buffer += decoded_data
            self.stats['messages_received'] += 1
            self.stats['last_activity'] = datetime.now()
            
            # Verificar tamaño máximo del buffer
            if len(self.buffer) > self.max_buffer_size:
                self.buffer = self.buffer[-self.max_buffer_size:]
                logger.warning("Buffer truncado por exceder tamaño máximo")
                
            return decoded_data
            
        except socket.timeout:
            return None
        except Exception as e:
            self._last_error = str(e)
            self._connected = False
            return None

    def parse_sip_message(self) -> Optional[Dict]:
        """Parsea un mensaje SIP del buffer."""
        try:
            if '\r\n\r\n' not in self.buffer:
                return None
                
            # Encontrar el final del mensaje
            message, remaining = self.buffer.split('\r\n\r\n', 1)
            
            # Parsear la primera línea
            lines = message.split('\r\n')
            first_line = lines[0].split(' ')
            
            # Determinar tipo de mensaje
            message_type = 'request' if first_line[0] in ['OPTIONS', 'REGISTER', 'INVITE'] else 'response'
            
            # Parsear headers
            headers = {}
            for line in lines[1:]:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers[key.lower()] = value
                    
            # Actualizar el buffer
            self.buffer = remaining
            
            return {
                'type': message_type,
                'first_line': first_line,
                'headers': headers,
                'raw': message + '\r\n\r\n'
            }
            
        except Exception as e:
            logger.error(f"Error parsing SIP message: {e}")
            return None

    def update_stats(self, event_type: str):
        """Actualiza las estadísticas de la conexión."""
        timestamp = datetime.now()
        if event_type not in self.stats:
            self.stats[event_type] = {
                'count': 0,
                'last_time': None,
                'first_time': timestamp
            }
        
        self.stats[event_type]['count'] += 1
        self.stats[event_type]['last_time'] = timestamp

    def send_data(self, data: str) -> bool:
        """Envía datos a través de la conexión TCP."""
        try:
            if not self._socket or not self._connected:
                logger.error("Intento de envío sin conexión activa")
                return False
                
            logger.debug(f"Enviando datos TCP: {data}")
            self._socket.sendall(data.encode('utf-8'))
            self.stats['messages_sent'] += 1
            self.stats['last_activity'] = datetime.now()
            return True
            
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Error enviando datos TCP: {e}")
            self._connected = False
            return False
    
    def keep_alive(self) -> bool:
        """Verifica si la conexión sigue activa."""
        try:
            if not self._socket:
                return False
                
            # Enviar un byte de keepalive
            self._socket.send(b'\r\n')
            self.update_stats('keepalive')
            return True
            
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Error en keepalive: {e}")
            self._connected = False
            return False
    
    @property
    def last_error(self) -> Optional[str]:
        """Retorna el último error registrado."""
        return self._last_error
    
    def get_stats(self) -> Dict:
        """Retorna las estadísticas de la conexión."""
        return {
            'connected': self._connected,
            'buffer_size': len(self.buffer),
            'events': self.stats
        }

    def is_alive(self) -> bool:
        """Verifica si la conexión está viva sin enviar datos."""
        if not self._socket or not self._connected:
            return False
            
        try:
            # Verificar el estado del socket sin enviar datos
            self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            return True
        except:
            self._connected = False
            return False

    def get_connection_info(self) -> Dict:
        """Retorna información detallada sobre la conexión."""
        if not self._socket:
            return {'status': 'disconnected'}
            
        try:
            local_addr = self._socket.getsockname()
            remote_addr = self._socket.getpeername()
            
            return {
                'status': 'connected' if self._connected else 'disconnected',
                'local_address': f"{local_addr[0]}:{local_addr[1]}",
                'remote_address': f"{remote_addr[0]}:{remote_addr[1]}",
                'stats': self.stats,
                'last_error': self._last_error
            }
        except:
            return {'status': 'error', 'last_error': self._last_error}

    def maintain_connection(self):
        """Mantiene la conexión TCP activa."""
        if not self._last_keep_alive or \
           (datetime.now() - self._last_keep_alive).seconds > self._keep_alive_interval:
            if self.keep_alive():
                self._last_keep_alive = datetime.now()
            else:
                self.reconnect()

    def reconnect(self):
        """Intenta reconectar si la conexión se pierde."""
        if self._socket and self._connected:
            return True

        try:
            self.stats['reconnection_attempts'] += 1
            return self.connect(self._last_host, self._last_port)
        except Exception as e:
            self._last_error = f"Reconnection failed: {str(e)}"
            return False

    @classmethod
    def from_existing_connection(cls, sock, address):
        """Crea una instancia de TCPConnection desde una conexión existente."""
        instance = cls()
        instance._socket = sock
        instance._connected = True
        instance._last_host = address[0]
        instance._last_port = address[1]
        instance.stats['connection_time'] = datetime.now()
        return instance

    def handle_incoming_data(self) -> Optional[str]:
        """Maneja datos entrantes en la conexión TCP."""
        try:
            data = self.receive_data()
            if data:
                logger.debug(f"Datos recibidos: {data}")
                # Solo retornamos los datos, el manejo de OPTIONS se hace en el SIPTrunk
                return data
            return None
        except Exception as e:
            logger.error(f"Error manejando datos entrantes: {e}")
            return None