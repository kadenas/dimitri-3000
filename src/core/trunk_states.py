from enum import Enum, auto

class SIPTrunkState(Enum):
    """Estados posibles de un trunk SIP."""
    DOWN = auto()        # No hay conexión
    UP = auto()          # Conexión establecida y OPTIONS OK
    RECOVERING = auto()  # Intentando restablecer conexión
    CONNECTING = auto()  # Estableciendo conexión inicial

    def __str__(self):
        return self.name