from typing import Dict, Optional
import uuid
import logging
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

class SIPCall:
    """Representa una llamada SIP individual."""
    def __init__(self, from_uri: str, to_uri: str):
        self.call_id = str(uuid.uuid4())
        self.from_uri = from_uri
        self.to_uri = to_uri
        self.local_tag = str(uuid.uuid4())[:8]
        self.remote_tag = None
        self.cseq = 1
        self.state = "INITIAL"
        self.start_time = datetime.now()
        self.direction = "outbound"
        self.branch = f"z9hG4bK-{uuid.uuid4().hex[:16]}"

class SIPCallManager(QObject):
    """Gestiona las llamadas SIP."""
    
    # Señales
    call_state_changed = pyqtSignal(str, str)  # call_id, state
    call_failed = pyqtSignal(str, str)  # call_id, reason
    
    def __init__(self, sip_monitor):
        super().__init__()
        self.sip_monitor = sip_monitor
        self.active_calls: Dict[str, SIPCall] = {}
        
    def create_invite(self, call: SIPCall) -> str:
        """Crea un mensaje INVITE."""
        local_ip = self.sip_monitor.config['local_ip']
        local_port = self.sip_monitor.config['local_port']
        
        message = (
            f"INVITE sip:{call.to_uri} SIP/2.0\r\n"
            f"Via: SIP/2.0/{self.sip_monitor.config['transport']} {local_ip}:{local_port}"
            f";branch={call.branch}\r\n"
            f"From: <sip:{call.from_uri}>;tag={call.local_tag}\r\n"
            f"To: <sip:{call.to_uri}>\r\n"
            f"Call-ID: {call.call_id}\r\n"
            f"CSeq: {call.cseq} INVITE\r\n"
            f"Contact: <sip:{local_ip}:{local_port}>\r\n"
            "Max-Forwards: 70\r\n"
            "User-Agent: DIMITRI-3000\r\n"
            "Content-Type: application/sdp\r\n"
            "Content-Length: 0\r\n\r\n"
        )
        return message
        
    def start_call(self, from_uri: str, to_uri: str) -> Optional[str]:
        """Inicia una nueva llamada."""
        try:
            # Crear nueva llamada
            call = SIPCall(from_uri, to_uri)
            self.active_calls[call.call_id] = call
            
            # Crear y enviar INVITE
            invite = self.create_invite(call)
            logger.debug(f"Enviando INVITE para llamada {call.call_id}")
            
            if self.sip_monitor.config['transport'].upper() == 'TCP':
                success = self.sip_monitor.send_tcp_message(invite.encode())
            else:
                success = self.sip_monitor.send_udp_message(invite.encode())
                
            if success:
                call.state = "CALLING"
                self.call_state_changed.emit(call.call_id, call.state)
                return call.call_id
            else:
                self.active_calls.pop(call.call_id)
                self.call_failed.emit(call.call_id, "Error enviando INVITE")
                return None
                
        except Exception as e:
            logger.error(f"Error iniciando llamada: {e}")
            return None
            
    def handle_response(self, response: str, call_id: str):
        """Maneja respuestas a mensajes de llamada."""
        try:
            call = self.active_calls.get(call_id)
            if not call:
                logger.warning(f"Respuesta recibida para llamada desconocida: {call_id}")
                return
                
            if "100 Trying" in response:
                call.state = "TRYING"
            elif "180 Ringing" in response:
                call.state = "RINGING"
            elif "200 OK" in response and "CSeq: " in response and "INVITE" in response:
                call.state = "ESTABLISHED"
                # Enviar ACK
                self._send_ack(call)
                
            self.call_state_changed.emit(call_id, call.state)
            
        except Exception as e:
            logger.error(f"Error procesando respuesta: {e}")
            
    def _send_ack(self, call: SIPCall):
        """Envía ACK para confirmar establecimiento de llamada."""
        try:
            local_ip = self.sip_monitor.config['local_ip']
            local_port = self.sip_monitor.config['local_port']
            
            ack = (
                f"ACK sip:{call.to_uri} SIP/2.0\r\n"
                f"Via: SIP/2.0/{self.sip_monitor.config['transport']} {local_ip}:{local_port}"
                f";branch={call.branch}\r\n"
                f"From: <sip:{call.from_uri}>;tag={call.local_tag}\r\n"
                f"To: <sip:{call.to_uri}>{';tag=' + call.remote_tag if call.remote_tag else ''}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} ACK\r\n"
                f"Contact: <sip:{local_ip}:{local_port}>\r\n"
                "Max-Forwards: 70\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            
            if self.sip_monitor.config['transport'].upper() == 'TCP':
                self.sip_monitor.send_tcp_message(ack.encode())
            else:
                self.sip_monitor.send_udp_message(ack.encode())
                
        except Exception as e:
            logger.error(f"Error enviando ACK: {e}") 