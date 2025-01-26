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
    
    def __init__(self, socket: Optional[socket.socket] = None, 
                addr: Optional[Tuple[str, int]] = None):
        """
        Inicializa una conexión TCP.
        
        Args:
            socket: Socket TCP existente
            addr: Tupla (host, port) de la conexión
        """
        self.socket = socket
        self.addr = addr
        self.buffer = b""  # Cambiado a bytes para mejor manejo de datos binarios
        self.last_activity = time.time()
        
        # Control de buffer
        self._max_buffer_size = 65535
        self._cleanup_threshold = 32768
        
        # Estadísticas detalladas
        self.stats = {
            'bytes_sent': 0,
            'bytes_received': 0,
            'messages_processed': 0,
            'incomplete_messages': 0,
            'buffer_overflows': 0,
            'connection_time': time.time(),
            'last_cleanup': time.time()
        }
        print(f"Debug: TCPConnection inicializada para {addr}")

    def _extract_sip_messages(self) -> List[bytes]:
        messages = []
        while True:
            # Buscar el final de los headers
            header_end = self.buffer.find(b"\r\n\r\n")
            if header_end == -1:
                break
                
            headers_part = self.buffer[:header_end + 4]
            headers = self._parse_headers(headers_part)
            
            # Obtener Content-Length
            content_length = int(headers.get(b'Content-Length', b'0')[0]) if headers.get(b'Content-Length') else 0
            
            total_length = header_end + 4 + content_length
            if len(self.buffer) < total_length:
                break  # Mensaje incompleto
                
            full_message = self.buffer[:total_length]
            messages.append(full_message)
            self.buffer = self.buffer[total_length:]
            
        return messages

    def _parse_headers(self, headers_part: bytes) -> Dict[bytes, List[bytes]]:
        headers = {}
        for line in headers_part.split(b'\r\n'):
            if b':' in line:
                name, value = line.split(b':', 1)
                headers.setdefault(name.strip().lower(), []).append(value.strip())
        return headers

    def _decode_message(self, message: bytes) -> Optional[str]:
        try:
            # Decodificar headers como UTF-8
            header_part = message.split(b'\r\n\r\n')[0]
            body_part = message[len(header_part)+4:]
            
            headers = header_part.decode('utf-8')
            body = body_part.decode(self._detect_encoding(headers))
            
            return headers + '\r\n\r\n' + body
        except UnicodeDecodeError as e:
            logger.error(f"Error decodificando mensaje: {e}")
            return None

    def _detect_encoding(self, headers: str) -> str:
        # Buscar Content-Type con charset
        for line in headers.split('\r\n'):
            if line.lower().startswith('content-type'):
                if 'charset=' in line:
                    return line.split('charset=')[1].split(';')[0].strip()
        return 'utf-8'  # Default según RFC

    def add_data(self, data: bytes) -> List[bytes]:
        try:
            self.buffer += data
            self.stats['bytes_received'] += len(data)
            
            messages = self._extract_sip_messages()
            logger.debug(f"Procesados {len(messages)} mensajes desde el buffer")
            
            # Limpieza periódica
            if len(self.buffer) > self._max_buffer_size:
                self._cleanup_buffer()
                
            return messages
        except Exception as e:
            logger.error(f"Error crítico en add_data: {e}")
            return []

    def send_keepalive(self) -> bool:
        """Envía CRLF keep-alive según RFC 5626"""
        try:
            self.socket.sendall(b"\r\n")
            logger.debug("Keep-alive CRLF enviado")
            return True
        except socket.error as e:
            logger.error(f"Error enviando keep-alive: {e}")
            return False

    def _process_messages(self) -> List[str]:
        """
        Procesa el buffer y extrae mensajes SIP completos.
        Implementa detección de mensajes incompletos.
        
        Returns:
            Lista de mensajes SIP completos
        """
        messages = []
        start_time = time.time()
        
        while "\r\n\r\n" in self.buffer:
            try:
                message, remaining = self.buffer.split("\r\n\r\n", 1)
                
                # Verificar si el mensaje es válido
                if self._is_valid_sip_message(message + "\r\n\r\n"):
                    messages.append(message + "\r\n\r\n")
                    self.buffer = remaining
                    self.stats['messages_processed'] += 1
                else:
                    # Mensaje inválido, incrementar contador
                    self.stats['incomplete_messages'] += 1
                    # Avanzar buffer hasta el siguiente delimitador
                    self.buffer = remaining
                    
            except Exception as e:
                logger.error(f"Error procesando mensaje individual: {e}")
                break
                
        return messages

    def _is_valid_sip_message(self, message: bytes) -> bool:
        try:
            # Verificar línea de inicio (request o response)
            first_line = message.split(b'\r\n')[0]
            if not (first_line.startswith(b'SIP/2.0 ') or b' SIP/2.0' in first_line):
                return False
                
            # Verificar headers obligatorios
            headers = self._parse_headers(message)
            required = [b'via', b'from', b'to', b'call-id', b'cseq']
            return all(h in headers for h in required)
        except Exception as e:
            logger.error(f"Error validando mensaje: {e}")
            return False

    def _cleanup_buffer(self):
        if len(self.buffer) > self._max_buffer_size:
            # Preservar los últimos 512 bytes que podrían contener headers
            self.buffer = self.buffer[-512:]
            self.stats['buffer_overflows'] += 1
            logger.warning("Buffer truncado por exceso de tamaño")

    def send_data(self, data: str) -> bool:
        try:
            encoded = data.encode('utf-8')
            self.socket.sendall(encoded)
            self.stats['bytes_sent'] += len(encoded)
            logger.debug(f"Datos enviados a {self.addr}")
            return True
        except (BrokenPipeError, ConnectionResetError) as e:
            logger.warning(f"Conexión cerrada por el peer: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado en send_data: {e}")
            return False

    def get_connection_info(self) -> Dict:
        """
        Obtiene información detallada sobre la conexión.
        
        Returns:
            Diccionario con información completa de la conexión
        """
        current_time = time.time()
        return {
            'peer_address': self.addr,
            'last_activity': datetime.fromtimestamp(self.last_activity),
            'connection_duration': current_time - self.stats['connection_time'],
            'bytes_sent': self.stats['bytes_sent'],
            'bytes_received': self.stats['bytes_received'],
            'messages_processed': self.stats['messages_processed'],
            'incomplete_messages': self.stats['incomplete_messages'],
            'buffer_overflows': self.stats['buffer_overflows'],
            'current_buffer_size': len(self.buffer),
            'last_cleanup_age': current_time - self.stats['last_cleanup']
        }

    def close(self):
        print(f"Debug: Cerrando conexión para {self.addr}")
        if self.socket:
            try:
                self.socket.close()
                print("Debug: Socket cerrado correctamente")
            except Exception as e:
                print(f"Error cerrando socket: {e}")
            self.socket = None

    def __del__(self):
        """Limpieza al destruir el objeto."""
        self.close()