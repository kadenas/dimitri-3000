import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configura el sistema de logging."""
    # Crear el logger
    logger = logging.getLogger('pysipp')
    logger.setLevel(logging.DEBUG)

    # Crear el directorio de logs si no existe
    log_dir = Path.home() / '.pysipp' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'pysipp.log'

    # Configurar el formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler para archivo
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Añadir handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Crear el logger global
logger = setup_logger() 