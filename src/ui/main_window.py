from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QTabWidget, QApplication, QStatusBar)
from PyQt6.QtCore import Qt, pyqtSlot
from src.ui.components.network_panel import NetworkPanel
from src.ui.components.terminal_widget import TerminalWidget
from src.ui.components.call_control_panel import CallControlPanel
from src.ui.themes.cyber_theme import RetroCyberTheme
from src.ui.retro_style import RetroStyle
from datetime import datetime
from typing import Dict
from src.core.sip_monitor import SIPMonitor
from src.core.sip_call_handler import SIPCallHandler


class MainWindow(QMainWindow):
    def __init__(self, config_manager=None):
        super().__init__()
        self.config_manager = config_manager
        self.call_handler = None
        self.sip_monitor = None
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Configura la interfaz principal."""
        self.setWindowTitle("DIMITRI-3000")
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Panel de red
        self.network_panel = NetworkPanel()
        self.tabs.addTab(self.network_panel, "Red")
        
        # Panel de control de llamadas
        self.call_panel = CallControlPanel()
        self.call_panel.setEnabled(False)
        self.tabs.addTab(self.call_panel, "Control de Llamadas")
        
        # Terminal
        self.terminal = TerminalWidget()
        self.tabs.addTab(self.terminal, "Terminal")
        
        layout.addWidget(self.tabs)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Aplicar tema retro
        self.apply_theme()  # <-- Método que faltaba
        self.log_message("Aplicación iniciada")

    def apply_theme(self):
        """Aplica el tema cyberpunk a toda la aplicación"""
        try:
            # Obtener la instancia de la aplicación
            app = QApplication.instance()
            
            # 1. Configurar paleta de colores GLOBAL (para todos los widgets)
            cyber_palette = RetroCyberTheme.get_palette()
            app.setPalette(cyber_palette)  # Aplicar a toda la app, no solo a la ventana
            
            # 2. Configurar fuente global
            cyber_font = RetroCyberTheme.get_font()
            app.setFont(cyber_font)
            
            # 3. Aplicar hoja de estilos completa del tema
            app.setStyleSheet(RetroCyberTheme.get_stylesheet())
            
            # 4. Configuraciones adicionales específicas
            self.status_bar.setStyleSheet("""
                QStatusBar::item {
                    border: none;  /* Eliminar bordes entre elementos */
                }
                QStatusBar QLabel {
                    margin-right: 15px;  /* Espaciado entre elementos */
                }
            """)
            
        except Exception as e:
            print(f"Error aplicando tema: {str(e)}")
            # Opcional: Revertir a estilo por defecto
            app.setStyle("Fusion")

    def log_message(self, message: str):
        """Registra un mensaje en el terminal con timestamp."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            
            if hasattr(self, 'terminal') and self.terminal is not None:
                self.terminal.append_text(formatted_message)
            else:
                print(f"Terminal no disponible: {formatted_message}")
                
        except Exception as e:
            print(f"Error registrando mensaje: {str(e)}")

    def setup_connections(self):
        """Configura las conexiones de señales y slots."""
        try:
            # Conexiones del panel de red
            self.network_panel.log_message.connect(self.log_message)
            self.network_panel.connectivity_status_changed.connect(self.handle_connectivity_status)
            self.network_panel.options_status_changed.connect(self.handle_options_status)
            
            if hasattr(self.network_panel, 'server_button'):
                self.network_panel.server_button.toggled.connect(self.handle_server_status)
            
            # Conexiones del panel de llamadas
            if hasattr(self, 'call_panel'):
                self.call_panel.call_initiated.connect(self.handle_call_initiation)
                self.call_panel.burst_started.connect(self.handle_burst_start)
                self.call_panel.burst_stopped.connect(self.handle_burst_stop)
                self.call_panel.bye_all.connect(self.handle_bye_all)
                
        except Exception as e:
            self.log_message(f"Error configurando conexiones: {str(e)}")

    def setup_call_handler(self):
        """Configura el manejador de llamadas SIP."""
        try:
            if not self.call_handler:
                self.call_handler = SIPCallHandler()
                self.log_message("Manejador de llamadas inicializado")
                
            if hasattr(self, 'call_panel'):
                self.call_panel.set_call_handler(self.call_handler)
                
        except Exception as e:
            self.log_message(f"Error inicializando call handler: {str(e)}")

    @pyqtSlot(str)
    def update_trunk_status(self, status: str):
        """Actualiza el estado del trunk en la barra de estado."""
        status_colors = {
            "UP": "#4CAF50",    # Verde
            "DOWN": "#F44336",  # Rojo
            "DEGRADED": "#FFC107" # Amarillo
        }
        self.status_bar.showMessage(f"Estado del trunk: {status}")
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {status_colors.get(status, "#FFFFFF")};
                color: #000000;
                font-family: "Courier New";
            }}
        """)

    def start_monitoring(self, config: dict):
        """Inicia el servicio de monitoreo SIP."""
        try:
            if not self.sip_monitor:
                self.sip_monitor = SIPMonitor()
                self.sip_monitor.trunk_state_changed.connect(self.update_trunk_status)
                self.sip_monitor.stats_updated.connect(self.update_stats)
                self.log_message("Monitor SIP inicializado")
                
            if self.sip_monitor.start_options_monitoring(config):
                self.log_message("Monitoreo SIP iniciado correctamente")
                
        except Exception as e:
            self.log_message(f"Error iniciando monitoreo: {str(e)}")

    @pyqtSlot()
    def update_stats(self):
        """Actualiza las estadísticas en la UI."""
        if self.sip_monitor:
            stats = self.sip_monitor.stats
            self.network_panel.update_stats(
                latency=stats.get('last_latency', 0),
                options_sent=stats.get('options_sent', 0),
                ok_received=stats.get('ok_received', 0)
            )

    def handle_server_status(self, is_active: bool):
        """Maneja cambios en el estado del servidor."""
        try:
            if is_active:
                self.setup_call_handler()
                if self.call_handler:
                    self.call_panel.set_call_handler(self.call_handler)
                    self.call_panel.setEnabled(True)
                    self.log_message("Servidor SIP activado")
            else:
                self.call_panel.setEnabled(False)
                self.log_message("Servidor SIP desactivado")
                
        except Exception as e:
            self.log_message(f"Error cambiando estado del servidor: {str(e)}")

    # Resto de métodos se mantienen igual...
    # (handle_connectivity_status, handle_options_status, apply_theme, etc.)

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana."""
        try:
            if self.sip_monitor:
                self.sip_monitor.stop_options_monitoring()
                self.sip_monitor.stop_server()
                self.log_message("Monitor SIP detenido")
                
            self.network_panel.cleanup()
            
            if hasattr(self, 'call_panel'):
                self.call_panel.cleanup()
                
            event.accept()
        except Exception as e:
            self.log_message(f"Error durante el cierre: {str(e)}")
            event.ignore()

    def cleanup(self):
        """Limpia recursos al cerrar la aplicación"""
        try:
            # Detener monitoreo SIP
            if self.sip_monitor:
                self.sip_monitor.stop_options_monitoring()
                self.sip_monitor.stop_server()
            
            # Limpiar otros componentes
            self.network_panel.cleanup()
            
            if hasattr(self, 'call_panel'):
                self.call_panel.cleanup()
                
            self.log_message("Aplicación cerrada correctamente")
            
        except Exception as e:
            print(f"Error durante cleanup: {str(e)}")