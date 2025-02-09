PySIPP GUI
Una interfaz gráfica para gestión de tráfico SIP utilizando PySIPP.
Características

Interfaz gráfica con estilo retro-terminal
Soporte para modo cliente y servidor
Múltiples protocolos de transporte (UDP, TCP, TLS)
Simulación de condiciones de red
Monitorización de SIPtrunk
Gestión de llamadas múltiples
Personalización de mensajes SIP
Pruebas de carga con SIP + RTP

Requisitos

Python 3.8 o superior
Ubuntu 24.04
SIPp instalado en el sistema

Instalación

Clonar el repositorio:

bashCopygit clone https://github.com/yourusername/pysipp-gui.git
cd pysipp-gui

Crear un entorno virtual (recomendado):

bashCopypython -m venv venv
source venv/bin/activate  # En Linux/Mac

Instalar dependencias:

bashCopypip install -e ".[dev]"  # Incluye dependencias de desarrollo
Uso

Iniciar la aplicación:

bashCopypython -m pysipp_gui

Para desarrollo:

bashCopy# Ejecutar tests
pytest

# Formatear código
black src/

# Verificar estilo
flake8 src/
Estructura del Proyecto
pysipp-gui/
│
├── README.md
├── requirements.txt
├── setup.py
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── sipp_controller.py     # Control principal de SIPP
│   │   ├── sip_message_builder.py # Construcción de mensajes SIP
│   │   ├── network_simulator.py   # Simulación de condiciones de red
│   │   └── call_manager.py        # Gestión de llamadas y RTP
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py        # Ventana principal
│   │   ├── retro_style.py        # Estilos retro
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── network_panel.py  # Panel de configuración de red
│   │   │   ├── sip_panel.py      # Panel de configuración SIP
│   │   │   └── monitor_panel.py  # Panel de monitorización
│   │   └── themes/
│   │       ├── __init__.py
│   │       └── retro_theme.py    # Definición del tema retro
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_manager.py     # Gestión de configuración
│   │   ├── logger.py             # Sistema de logging
│   │   └── network_utils.py      # Utilidades de red
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_sipp_controller.py
│       ├── test_network_simulator.py
│       └── test_call_manager.py
│
└── config/
    ├── default_config.yaml       # Configuración por defecto
    └── sip_templates/            # Plantillas de mensajes SIP
        ├── invite.xml
        ├── options.xml
        └── register.xml
Desarrollo
Configuración del Entorno de Desarrollo

Instalar dependencias de desarrollo:

bashCopypip install -e ".[dev]"

Configurar pre-commit hooks (opcional):

bashCopypre-commit install
Guías de Contribución

Crear una rama para tu característica
Escribir tests para nuevas funcionalidades
Asegurar que todos los tests pasan
Crear un pull request

Licencia
[Tu licencia aquí]
