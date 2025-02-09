from dataclasses import dataclass
from datetime import datetime
import uuid
from enum import Enum
from typing import Optional

class CallState(Enum):
    INITIAL = "INITIAL"
    TRYING = "TRYING"
    RINGING = "RINGING"
    ESTABLISHED = "ESTABLISHED"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"

@dataclass
class CallData:
    call_id: str
    from_uri: str
    to_uri: str
    state: CallState
    direction: str
    start_time: datetime
    duration: Optional[str] = None

@dataclass
class SIPCall:
    from_uri: str
    to_uri: str
    call_id: str = None
    branch: str = None
    from_tag: str = None
    to_tag: str = None
    cseq: int = 1
    state: str = CallState.INITIAL.value
    start_time: datetime = None
    local_rtp_port: int = None
    remote_rtp_port: int = None
    session_expires: int = 1800
    session_refresher: str = "uac"
    
    def __post_init__(self):
        if not self.call_id:
            self.call_id = str(uuid.uuid4())
        if not self.branch:
            self.branch = f"z9hG4bK-{uuid.uuid4().hex[:16]}"
        if not self.from_tag:
            self.from_tag = uuid.uuid4().hex[:8]
        if not self.start_time:
            self.start_time = datetime.now()
        if not self.local_rtp_port:
            self.local_rtp_port = 10000