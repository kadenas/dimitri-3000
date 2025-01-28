from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class CallState(Enum):
    INITIAL = "INITIAL"
    TRYING = "TRYING"
    RINGING = "RINGING"
    ESTABLISHED = "ESTABLISHED"
    FAILED = "FAILED"
    FINISHED = "FINISHED"

@dataclass
class CallData:
    call_id: str
    from_uri: str
    to_uri: str
    state: CallState
    direction: str
    start_time: datetime
    duration: Optional[str] = None