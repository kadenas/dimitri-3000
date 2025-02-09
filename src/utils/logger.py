import logging
from typing import Any
logger = logging.getLogger('pysipp')
logger.propagate = False  # Evita que los logs se muestren en el root

def debug_log(message: Any, *args: Any, **kwargs: Any) -> None:
    """Función híbrida para debug que usa print y logging"""
    print(f"DEBUG: {message}", *args, **kwargs)
    
    # Deshabilitar logging estándar para DEBUG
    logging.disable(logging.INFO)  # Solo muestra logs de INFO o superior
    logging.debug(str(message), *args, **kwargs)
    logging.disable(logging.NOTSET)  # Restaurar configuración