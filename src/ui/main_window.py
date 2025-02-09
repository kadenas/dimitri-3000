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
        
        # Panel de control de llamadas - Usar el del NetworkPanel
        self.call_panel = self.network_panel.call_control_panel
        self.tabs.addTab(self.call_panel, "Control de Llamadas")
        
        # Terminal
        self.terminal = TerminalWidget()
        self.tabs.addTab(self.terminal, "Terminal")
        
        layout.addWidget(self.tabs)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Aplicar tema retro
        self.apply_theme()
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
        try:
            # Primero conectar el monitor SIP
            if hasattr(self.network_panel, 'sip_monitor'):
                self.network_panel.sip_monitor.trunk_state_changed.connect(self.handle_trunk_state)
                self.log_message("Monitor SIP conectado")

            # Resto de conexiones
            self.network_panel.log_message.connect(self.log_message)
            self.network_panel.server_button.toggled.connect(self.handle_server_status)
            self.network_panel.connectivity_status_changed.connect(self.handle_connectivity_status)
            self.network_panel.options_status_changed.connect(self.handle_options_status)
                
            # Panel de llamadas
            if hasattr(self, 'call_panel'):
                self.call_panel.setEnabled(False)  # Deshabilitado inicialmente
                self.call_panel.call_initiated.connect(self.handle_call_initiation)
                self.call_panel.burst_started.connect(self.handle_burst_start)
                self.call_panel.burst_stopped.connect(self.handle_burst_stop)
                self.call_panel.bye_all.connect(self.handle_bye_all)
        except Exception as e:
            self.log_message(f"Error en setup_connections: {str(e)}")
    def handle_call_initiation(self, from_uri: str, to_uri: str):
        try:
            if self.call_handler:
                success = self.call_handler.start_single_call(from_uri, to_uri)
                self.log_message(f"Llamada iniciada: {from_uri} -> {to_uri}")
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def handle_burst_start(self, interval: int, max_calls: int):
        try:
            if self.call_handler:
                self.call_handler.start_call_burst(interval, max_calls)
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def handle_burst_stop(self):
        try:
            if self.call_handler:
                self.call_handler.stop_call_burst()
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def handle_bye_all(self):
        try:
            if self.call_handler:
                self.call_handler.terminate_all_calls()
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def handle_trunk_state(self, state: str):
        try:
            self.log_message(f"Recibido estado trunk: {state}")
            if state == "UP":
                if hasattr(self, 'call_panel'):
                    self.call_panel.setEnabled(True)
                    self.log_message("Panel de llamadas activado")
        except Exception as e:
            self.log_message(f"Error en handle_trunk_state: {str(e)}")

    def handle_connectivity_status(self, is_connected: bool):
        """Maneja eventos de conectividad."""
        try:
            message = "Conectividad establecida" if is_connected else "Sin conectividad"
            self.log_message(message)
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def handle_options_status(self, is_active: bool):
        """Maneja eventos de estado OPTIONS."""
        try:
            if is_active:
                self.call_panel.setEnabled(True)
                self.log_message("Monitoreo OPTIONS activo - Panel de llamadas habilitado")
            else:
                self.call_panel.setEnabled(False)
                self.log_message("Monitoreo OPTIONS inactivo")
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

    def setup_call_handler(self):
        try:
            # Usar el call handler del NetworkPanel
            self.call_handler = self.network_panel.call_handler
            if self.call_handler:
                self.log_message("Usando call handler del NetworkPanel")
                if hasattr(self, 'call_panel'):
                    self.call_panel.setEnabled(True)
            else:
                self.log_message("Error: Call handler no disponible en NetworkPanel")
        except Exception as e:
            self.log_message(f"Error crítico inicializando call handler: {str(e)}")

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
                # Forzar habilitación del panel
                if hasattr(self, 'call_panel'):
                    self.call_panel.setEnabled(True)
                    self.log_message("Panel de control de llamadas habilitado")
            else:
                if hasattr(self, 'call_panel'):
                    self.call_panel.setEnabled(False)
                    
        except Exception as e:
            self.log_message(f"Error: {str(e)}")

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