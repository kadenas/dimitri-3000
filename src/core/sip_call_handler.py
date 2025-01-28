import threading
import time
import socket
import uuid
import struct
from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Tuple
from PyQt6.QtCore import QObject, pyqtSignal
from .models import CallData, CallState

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

class SIPCall:
    def __init__(self, from_uri: str, to_uri: str):
        self.call_id = f"{int(time.time())}-{uuid.uuid4().hex[:12]}"
        self.from_uri = from_uri
        self.to_uri = to_uri
        self.start_time = datetime.now()
        self.state = CallState.INITIAL.value
        self.direction = "outbound"
        self.rtp_port = None
        self.remote_rtp_port = None
        self.branch = f"z9hG4bK-{uuid.uuid4().hex[:12]}"
        self.from_tag = uuid.uuid4().hex[:12]
        self.to_tag = None
        self.cseq = 1
        self.retransmissions = 0
        self.session_expires = 1800
        self.session_refresher = 'uac'
        self.last_refresh = None

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
    call_status_changed = pyqtSignal(str, str)  # call_id, status
    call_stats_updated = pyqtSignal(int, int, int)  # active, failed, total

    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.active_calls = {}
        self.next_origin = 1001
        self.next_dest = 2001
        self.burst_running = False
        self.burst_thread = None
        self.rtp_sessions = {}
        self.timers = {}
        self.transaction_states = {}
        
        self.local_ip = config.get('local_ip', '127.0.0.1')
        self.local_port = config.get('local_port', 5060)
        self.remote_ip = config.get('remote_ip', '127.0.0.1')
        self.remote_port = config.get('remote_port', 5060)
        
        self.session_timer = SessionTimer()
        self.stats = {"active": 0, "failed": 0, "total": 0}
        
        self._start_session_refresh_timer()
        self.trunk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.trunk.bind((self.local_ip, self.local_port))

    def start_single_call(self, from_uri: str, to_uri: str) -> bool:
        try:
            call = SIPCall(from_uri, to_uri)
            invite_msg = self._create_invite_message(call)
            
            is_valid, error = SDPValidator.validate_sdp(self._create_sdp(call))
            if not is_valid:
                raise SIPError(400, f"SDP inválido: {error}")
            
            self.active_calls[call.call_id] = call
            self._start_transaction_timer(call)
            
            self.trunk.send_message(invite_msg.encode())
            self.stats["active"] += 1
            self.stats["total"] += 1
            self._update_stats()
            
            return True
            
        except SIPError as e:
            print(f"Error SIP: {e}")
            return False
        except Exception as e:
            print(f"Error general: {e}")
            return False

    def start_call_burst(self, interval: int, max_calls: int):
        self.burst_running = True
        self.burst_thread = threading.Thread(
            target=self._burst_worker,
            args=(interval, max_calls)
        )
        self.burst_thread.daemon = True
        self.burst_thread.start()

    def _burst_worker(self, interval: int, max_calls: int):
        while self.burst_running and len(self.active_calls) < max_calls:
            from_number = str(self.next_origin)
            to_number = str(self.next_dest)
            
            self.start_single_call(from_number, to_number)
            
            self.next_origin += 1
            self.next_dest += 1
            
            time.sleep(interval)

    def stop_call_burst(self):
        self.burst_running = False
        if self.burst_thread:
            self.burst_thread.join(timeout=1.0)

    def _create_invite_message(self, call: SIPCall, is_refresh: bool = False) -> str:
        try:
            if not is_refresh:
                call.rtp_port = self._get_next_rtp_port()
            
            headers = [
                f"INVITE sip:{call.to_uri}@{self.remote_ip} SIP/2.0",
                f"Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};branch={call.branch}",
                f"From: <sip:{call.from_uri}@{self.local_ip}>;tag={call.from_tag}",
                f"To: <sip:{call.to_uri}@{self.remote_ip}>{';tag='+call.to_tag if call.to_tag else ''}",
                f"Call-ID: {call.call_id}",
                f"CSeq: {call.cseq} INVITE",
                f"Contact: <sip:{call.from_uri}@{self.local_ip}:{self.local_port}>",
                "Max-Forwards: 70",
                f"Session-Expires: {call.session_expires};refresher={call.session_refresher}",
                "Min-SE: 90",
                "Supported: timer",
                "Content-Type: application/sdp"
            ]
            
            sdp = self._create_sdp(call)
            headers.extend(["", sdp])
            
            return "\r\n".join(headers)
            
        except Exception as e:
            print(f"Error creando INVITE: {e}")
            raise

    def _create_sdp(self, call: SIPCall) -> str:
        timestamp = int(time.time())
        lines = [
            "v=0",
            f"o=PySIPP {timestamp} {timestamp} IN IP4 {self.local_ip}",
            "s=PySIPP Call",
            f"c=IN IP4 {self.local_ip}",
            "t=0 0",
            f"m=audio {call.rtp_port} RTP/AVP 0",
            "a=rtpmap:0 PCMU/8000",
            "a=ptime:20",
            "a=sendrecv"
        ]
        return "\r\n".join(lines)

    def handle_response(self, response: str, source_address: tuple):
        try:
            lines = response.split('\r\n')
            status_line = lines[0]
            response_code = int(status_line.split()[1])
            
            call_id = self._extract_header(response, 'Call-ID')
            if not call_id or call_id not in self.active_calls:
                return
                
            call = self.active_calls[call_id]
            
            if response_code >= 400:
                self._handle_error_response(response_code, call)
                return
                
            if response_code == 100:
                call.state = CallState.TRYING.value
            elif response_code == 180:
                call.state = CallState.RINGING.value
            elif response_code == 200:
                if call.state != CallState.ESTABLISHED.value:
                    call.state = CallState.ESTABLISHED.value
                    self._process_200_ok(call, response)
                    self._start_rtp(call)
                else:
                    self._process_refresh_response(call, response)
                    
            self.call_status_changed.emit(call_id, call.state)
            
        except Exception as e:
            print(f"Error procesando respuesta: {e}")

    def _handle_error_response(self, response_code: int, call: SIPCall):
        error_handlers = {
            SIPResponse.BAD_REQUEST.value: self._handle_bad_request,
            SIPResponse.UNAUTHORIZED.value: self._handle_unauthorized,
            SIPResponse.NOT_FOUND.value: self._handle_not_found,
            SIPResponse.SERVER_ERROR.value: self._handle_server_error
        }
        
        handler = error_handlers.get(response_code, self._handle_generic_error)
        handler(call)
        self._handle_call_failure(call)

    def _handle_bad_request(self, call: SIPCall):
        print(f"Error 400: Solicitud mal formada para llamada {call.call_id}")

    def _handle_unauthorized(self, call: SIPCall):
        print(f"Error 401: Llamada no autorizada {call.call_id}")

    def _handle_not_found(self, call: SIPCall):
        print(f"Error 404: Destino no encontrado {call.call_id}")

    def _handle_server_error(self, call: SIPCall):
        print(f"Error 500: Error del servidor para llamada {call.call_id}")

    def _handle_generic_error(self, call: SIPCall):
        print(f"Error genérico en llamada {call.call_id}")

    def _process_200_ok(self, call: SIPCall, response: str):
        self._extract_to_tag(call, response)
        self._process_sdp_response(call, response)
        self._send_ack(call)
        self.session_timer.start_session(call.call_id)

    def _extract_to_tag(self, call: SIPCall, response: str):
        for line in response.split('\r\n'):
            if line.startswith('To:'):
                if ';tag=' in line:
                    call.to_tag = line.split(';tag=')[1]
                break

    def _process_sdp_response(self, call: SIPCall, response: str):
        try:
            sdp_start = response.find('\r\n\r\n') + 4
            if sdp_start > 4:
                sdp = response[sdp_start:]
                for line in sdp.split('\r\n'):
                    if line.startswith('m=audio '):
                        call.remote_rtp_port = int(line.split()[1])
                        break
        except Exception as e:
            print(f"Error procesando SDP: {e}")

    def _start_rtp(self, call: SIPCall):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.local_ip, call.rtp_port))
            
            self.rtp_sessions[call.call_id] = {
                'socket': sock,
                'remote_ip': self.remote_ip,
                'remote_port': call.remote_rtp_port,
                'running': True
            }
            
            threading.Thread(
                target=self._rtp_sender,
                args=(call.call_id,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"Error iniciando RTP: {e}")

    def _rtp_sender(self, call_id: str):
        session = self.rtp_sessions.get(call_id)
        if not session:
            return
            
        sequence = 0
        timestamp = 0
        
        while session['running']:
            payload = b'\x00' * 160
            header = struct.pack('!BBHII',
                0x80, 0x00, sequence,
                timestamp, 0x12345678)
            
            session['socket'].sendto(
                header + payload,
                (session['remote_ip'], session['remote_port'])
            )
            
            sequence = (sequence + 1) & 0xFFFF
            timestamp += 160
            time.sleep(0.02)

    def terminate_all_calls(self, bye_interval: float = 0.5):
        active_calls = list(self.active_calls.values())
        for call in active_calls:
            self._send_bye(call)
            self._cleanup_rtp_session(call.call_id)
            time.sleep(bye_interval)

    def _send_bye(self, call: SIPCall):
            try:
                call.cseq += 1
                bye_message = (
                    f"BYE sip:{call.to_uri}@{self.remote_ip} SIP/2.0\r\n"
                    f"Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};branch={call.branch}\r\n"
                    f"From: <sip:{call.from_uri}@{self.local_ip}>;tag={call.from_tag}\r\n"
                    f"To: <sip:{call.to_uri}@{self.remote_ip}>{';tag='+call.to_tag if call.to_tag else ''}\r\n"
                    f"Call-ID: {call.call_id}\r\n"
                    f"CSeq: {call.cseq} BYE\r\n"
                    "Max-Forwards: 70\r\n"
                    "Content-Length: 0\r\n\r\n"
                )
                self.trunk.send_message(bye_message.encode())
                self._cleanup_call(call.call_id)
            except Exception as e:
                print(f"Error enviando BYE: {e}")

    def _send_ack(self, call: SIPCall):
        try:
            ack_message = (
                f"ACK sip:{call.to_uri}@{self.remote_ip} SIP/2.0\r\n"
                f"Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};branch={call.branch}\r\n"
                f"From: <sip:{call.from_uri}@{self.local_ip}>;tag={call.from_tag}\r\n"
                f"To: <sip:{call.to_uri}@{self.remote_ip}>;tag={call.to_tag}\r\n"
                f"Call-ID: {call.call_id}\r\n"
                f"CSeq: {call.cseq} ACK\r\n"
                "Max-Forwards: 70\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            self.trunk.send_message(ack_message.encode())
        except Exception as e:
            print(f"Error enviando ACK: {e}")

    def handle_incoming_call(self, invite_message: str):
        try:
            call_id = self._extract_header(invite_message, 'Call-ID')
            from_uri = self._extract_uri(invite_message, 'From')
            to_uri = self._extract_uri(invite_message, 'To')
            via = self._extract_header(invite_message, 'Via')
            
            call = SIPCall(from_uri, to_uri)
            call.call_id = call_id
            call.direction = "inbound"
            call.state = CallState.INITIAL.value
            call.via = via
            
            self.active_calls[call_id] = call
            self.stats["active"] += 1
            self.stats["total"] += 1
            
            self._send_100_trying(call, invite_message)
            self._send_180_ringing(call, invite_message)
            time.sleep(1)
            self._send_200_ok(call, invite_message)
            
            self._update_stats()
            
        except Exception as e:
            print(f"Error procesando llamada entrante: {e}")

    def _send_100_trying(self, call: SIPCall, invite_message: str):
        response = (
            "SIP/2.0 100 Trying\r\n"
            f"Via: {self._extract_header(invite_message, 'Via')}\r\n"
            f"From: {self._extract_header(invite_message, 'From')}\r\n"
            f"To: {self._extract_header(invite_message, 'To')}\r\n"
            f"Call-ID: {call.call_id}\r\n"
            f"CSeq: {self._extract_header(invite_message, 'CSeq')}\r\n"
            "Content-Length: 0\r\n\r\n"
        )
        self.trunk.send_message(response.encode())

    def _send_180_ringing(self, call: SIPCall, invite_message: str):
        response = (
            "SIP/2.0 180 Ringing\r\n"
            f"Via: {self._extract_header(invite_message, 'Via')}\r\n"
            f"From: {self._extract_header(invite_message, 'From')}\r\n"
            f"To: {self._extract_header(invite_message, 'To')};tag={call.from_tag}\r\n"
            f"Call-ID: {call.call_id}\r\n"
            f"CSeq: {self._extract_header(invite_message, 'CSeq')}\r\n"
            "Content-Length: 0\r\n\r\n"
        )
        self.trunk.send_message(response.encode())

    def _send_200_ok(self, call: SIPCall, invite_message: str):
        call.rtp_port = self._get_next_rtp_port()
        sdp = self._create_sdp(call)
        
        response = (
            "SIP/2.0 200 OK\r\n"
            f"Via: {self._extract_header(invite_message, 'Via')}\r\n"
            f"From: {self._extract_header(invite_message, 'From')}\r\n"
            f"To: {self._extract_header(invite_message, 'To')};tag={call.from_tag}\r\n"
            f"Call-ID: {call.call_id}\r\n"
            f"CSeq: {self._extract_header(invite_message, 'CSeq')}\r\n"
            f"Contact: <sip:{self.local_ip}:{self.local_port}>\r\n"
            "Content-Type: application/sdp\r\n"
            f"Content-Length: {len(sdp)}\r\n"
            "\r\n"
            f"{sdp}"
        )
        self.trunk.send_message(response.encode())

    def _extract_header(self, message: str, header: str) -> str:
        for line in message.split('\r\n'):
            if line.startswith(f"{header}:"):
                return line.split(':', 1)[1].strip()
        return ""

    def _extract_uri(self, message: str, header: str) -> str:
        header_value = self._extract_header(message, header)
        if '<sip:' in header_value and '>' in header_value:
            uri = header_value.split('<sip:', 1)[1].split('@', 1)[0]
            return uri
        return ""

    def _get_next_rtp_port(self) -> int:
        rtp_port = 10000
        while any(call.rtp_port == rtp_port for call in self.active_calls.values()):
            rtp_port += 2
            if rtp_port > 20000:
                rtp_port = 10000
        return rtp_port

    def _cleanup_call(self, call_id: str):
        if call_id in self.active_calls:
            del self.active_calls[call_id]
            self.stats["active"] -= 1
            self._update_stats()
        self._cleanup_rtp_session(call_id)
        self._cleanup_transaction(call_id)

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

    def _update_stats(self):
        self.call_stats_updated.emit(
            self.stats["active"],
            self.stats["failed"],
            self.stats["total"]
        )

    def _start_session_refresh_timer(self):
        def refresh_worker():
            while True:
                for call_id, call in list(self.active_calls.items()):
                    if self.session_timer.needs_refresh(call_id):
                        self._send_session_refresh(call)
                time.sleep(5)
                
        threading.Thread(target=refresh_worker, daemon=True).start()