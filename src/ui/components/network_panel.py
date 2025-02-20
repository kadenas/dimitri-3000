from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QComboBox, QSpinBox, QLineEdit, QGroupBox,
                           QPushButton, QCheckBox, QMessageBox, QGridLayout, QTableWidgetItem, QTableWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from datetime import datetime
import socket
import logging
import time

# Importaciones de componentes propios
from src.core.sip_monitor import SIPMonitor
from src.core.sip_trunk import SIPTrunk  # Asegúrate de que esta línea está presente
from src.utils.network_utils import get_local_ip
from src.ui.components.led_indicator import LedIndicator
from src.ui.components.call_control_panel import CallControlPanel  # Solo una vez
from src.core.sip_call_handler import SIPCallHandler

logger = logging.getLogger(__name__)  # Añadir esta línea

class NetworkPanel(QWidget):
    """Panel de configuración de redd con monitoreo SIP integrado."""
    
    # Señales para notificar eventos
    options_status_changed = pyqtSignal(bool)
    connectivity_status_changed = pyqtSignal(bool)
    log_message = pyqtSignal(str)  # Para enviar mensajes al terminal
    enable_call_control = pyqtSignal(bool)  # Nueva señal para control de llamadas
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)
        self._last_monitoring_state = False
        self.trunk_manager = None
        
        # Configuración inicial
        self.main_layout = QVBoxLayout(self)
        self.local_ip = self._get_local_ip()
        self.local_port = 5060
        self.remote_ip = ""
        self.remote_port = 5060
        self.transport = "UDP"  # Valor por defecto
        
        # Crear el monitor y mantener una referencia fuerte
        initial_config = {
            'local_ip': self.local_ip,
            'local_port': self.local_port,
            'remote_ip': self.remote_ip,
            'remote_port': self.remote_port,
            'transport': self.transport
        }
        
        # Crear y configurar el monitor
        self.sip_monitor = SIPMonitor()
        self.sip_monitor.config = initial_config
        self._monitor_ref = self.sip_monitor
        logger.debug(f"Monitor creado con config inicial: {initial_config}")
        
        # Crear y configurar el call handler
        self.call_handler = SIPCallHandler(initial_config)
        self.call_handler.sip_monitor = self.sip_monitor
        logger.debug("Call handler creado y configurado con monitor")
        
        # Crear y configurar el panel de control
        self.call_control_panel = CallControlPanel(self)
        self.call_control_panel.set_call_handler(self.call_handler)
        logger.debug("Panel de control configurado")
        
        self.setup_ui()
        self.setup_connections()
        self.init_local_ip()
        self.setup_call_handler()  # Conectar señales al iniciar
        logger.debug("NetworkPanel inicializado completamente")
    
    def setup_ui(self):
        """Configura la interfaz del panel de red."""
        main_layout = self.main_layout
        
        # Protocolo común
        protocol_layout = QHBoxLayout()
        protocol_label = QLabel("Protocolo:")
        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["UDP", "TCP", "TLS"])
        self.transport_combo.currentTextChanged.connect(self.on_transport_changed)
        protocol_layout.addWidget(protocol_label)
        protocol_layout.addWidget(self.transport_combo)
        protocol_layout.addStretch()
        
        # Grupo Origen (Local)
        local_group = QGroupBox("Configuración Local")
        local_layout = QVBoxLayout()
        
        # IP Local
        local_ip_layout = QHBoxLayout()
        local_ip_label = QLabel("IP Local:")
        self.local_ip_edit = QLineEdit()
        self.local_ip_edit.setPlaceholderText("192.168.1.100")
        self.local_ip_edit.setToolTip("Dirección IP de esta máquina")
        local_ip_layout.addWidget(local_ip_label)
        local_ip_layout.addWidget(self.local_ip_edit)
        
        # Puerto Local
        local_port_layout = QHBoxLayout()
        local_port_label = QLabel("Puerto Local:")
        self.local_port_spin = QSpinBox()
        self.local_port_spin.setRange(1, 65535)
        self.local_port_spin.setValue(self.local_port)
        self.local_port_spin.setToolTip("Puerto local para escuchar conexiones SIP")
        self.local_port_spin.valueChanged.connect(self.on_port_changed)
        local_port_layout.addWidget(local_port_label)
        local_port_layout.addWidget(self.local_port_spin)
        local_port_layout.addStretch()
        
        local_layout.addLayout(local_ip_layout)
        local_layout.addLayout(local_port_layout)
        local_group.setLayout(local_layout)
        
        # Grupo Destino (Remoto)
        remote_group = QGroupBox("Configuración Remota")
        remote_layout = QVBoxLayout()
        
        # IP Remota
        remote_ip_layout = QHBoxLayout()
        remote_ip_label = QLabel("IP Remota:")
        self.remote_ip_edit = QLineEdit()
        self.remote_ip_edit.setPlaceholderText("192.168.1.200")
        self.remote_ip_edit.setToolTip("Dirección IP del servidor SIP remoto")
        self.remote_ip_edit.textChanged.connect(self.on_remote_ip_changed)
        remote_ip_layout.addWidget(remote_ip_label)
        remote_ip_layout.addWidget(self.remote_ip_edit)
        
        # Puerto Remoto
        remote_port_layout = QHBoxLayout()
        remote_port_label = QLabel("Puerto Remoto:")
        self.remote_port_spin = QSpinBox()
        self.remote_port_spin.setRange(1, 65535)
        self.remote_port_spin.setValue(self.remote_port)
        self.remote_port_spin.setToolTip("Puerto del servidor SIP remoto")
        self.remote_port_spin.valueChanged.connect(self.on_remote_port_changed)
        remote_port_layout.addWidget(remote_port_label)
        remote_port_layout.addWidget(self.remote_port_spin)
        remote_port_layout.addStretch()
        
        remote_layout.addLayout(remote_ip_layout)
        remote_layout.addLayout(remote_port_layout)
        remote_group.setLayout(remote_layout)
        
        # Grupo de Pruebas de Conectividad
        connectivity_group = QGroupBox("Pruebas de Conectividad")
        connectivity_layout = QVBoxLayout()
        
        # Botón de prueba de red básica
        self.test_network_btn = QPushButton("Probar Conectividad de Red")
        self.test_network_btn.setStyleSheet("background-color: #002200;")
        
        # Indicador de estado de red
        self.network_status_label = QLabel("Estado: No probado")
        
        connectivity_layout.addWidget(self.test_network_btn)
        connectivity_layout.addWidget(self.network_status_label)
        connectivity_group.setLayout(connectivity_layout)
        
        # Grupo de Configuración OPTIONS
        options_group = QGroupBox("Configuración OPTIONS")
        options_layout = QVBoxLayout()
        
        # Activar monitoreo OPTIONS
        self.enable_options_cb = QCheckBox("Activar Monitoreo OPTIONS")
        self.enable_options_cb.setObjectName("enable_options_cb")
        
        # Intervalo de OPTIONS
        options_interval_layout = QHBoxLayout()
        options_interval_label = QLabel("Intervalo (seg):")
        self.options_interval_spin = QSpinBox()
        self.options_interval_spin.setRange(1, 3600)
        self.options_interval_spin.setValue(15)
        options_interval_layout.addWidget(options_interval_label)
        options_interval_layout.addWidget(self.options_interval_spin)
        options_interval_layout.addStretch()
        
        # Timeout OPTIONS
        options_timeout_layout = QHBoxLayout()
        options_timeout_label = QLabel("Timeout (seg):")
        self.options_timeout_spin = QSpinBox()
        self.options_timeout_spin.setRange(1, 60)
        self.options_timeout_spin.setValue(10)
        options_timeout_layout.addWidget(options_timeout_label)
        options_timeout_layout.addWidget(self.options_timeout_spin)
        options_timeout_layout.addStretch()
        
        # Estado OPTIONS
        self.options_status_label = QLabel("Estado OPTIONS: Inactivo")
        
        options_layout.addWidget(self.enable_options_cb)
        options_layout.addLayout(options_interval_layout)
        options_layout.addLayout(options_timeout_layout)
        options_layout.addWidget(self.options_status_label)
        options_group.setLayout(options_layout)
        
        # Grupo de Estadísticas
        stats_group = QGroupBox("Estadísticas de Monitoreo")
        stats_layout = QVBoxLayout()
        
        # Layout superior para LED y latencia
        status_layout = QHBoxLayout()
        self.led_indicator = LedIndicator()
        self.led_indicator.setFixedSize(20, 20)
        self.led_indicator.setActive(False)
        latency_label = QLabel("Latencia:")
        self.latency_value = QLabel("-- ms")
        status_layout.addWidget(QLabel("Estado:"))
        status_layout.addWidget(self.led_indicator)
        status_layout.addWidget(latency_label)
        status_layout.addWidget(self.latency_value)
        status_layout.addStretch()
        
        # Grid para contadores
        counters_layout = QGridLayout()
        
        # Contadores
        self.sent_options = QLabel("OPTIONS Enviados: 0")
        self.received_options = QLabel("OPTIONS Recibidos: 0")
        self.sent_ok = QLabel("200 OK Enviados: 0")
        self.received_ok = QLabel("200 OK Recibidos: 0")
        self.timeouts = QLabel("Timeouts: 0")
        
        # Añadir contadores al grid
        counters_layout.addWidget(self.sent_options, 0, 0)
        counters_layout.addWidget(self.received_options, 0, 1)
        counters_layout.addWidget(self.sent_ok, 1, 0)
        counters_layout.addWidget(self.received_ok, 1, 1)
        counters_layout.addWidget(self.timeouts, 2, 0)
        
        # Añadir layouts al grupo de estadísticas
        stats_layout.addLayout(status_layout)
        stats_layout.addLayout(counters_layout)
        stats_group.setLayout(stats_layout)
        
        # Control de Servidor SIP
        server_group = QGroupBox("Control de Servidor SIP")
        server_layout = QVBoxLayout()
        
        # Botón de inicio/parada
        self.server_button = QPushButton("Iniciar Servidor")
        self.server_button.setCheckable(True)
        self.server_status_label = QLabel("Estado: Detenido")
        
        server_layout.addWidget(self.server_button)
        server_layout.addWidget(self.server_status_label)
        server_group.setLayout(server_layout)
        
        # Reservar espacio para el panel de control de llamadas
        self.call_control_container = QWidget()
        call_control_layout = QVBoxLayout(self.call_control_container)
        main_layout.addWidget(self.call_control_container)
        
        # Añadir todo al layout principal
        main_layout.addLayout(protocol_layout)
        main_layout.addWidget(local_group)
        main_layout.addWidget(remote_group)
        main_layout.addWidget(connectivity_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(stats_group)
        main_layout.addWidget(server_group)
        main_layout.addWidget(self.call_control_panel)
        main_layout.addStretch()
        
        # Configurar estilos
        style = """
            QGroupBox {
                border: 1px solid #00AA00;
                margin-top: 1ex;
                color: #00FF00;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
            QLabel, QCheckBox {
                color: #00FF00;
            }
            QLineEdit, QSpinBox, QComboBox, QPushButton {
                background-color: #000000;
                color: #00FF00;
                border: 1px solid #00AA00;
                padding: 2px;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPushButton:hover {
                border: 1px solid #00FF00;
            }
            QPushButton {
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #003300;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                color: #00FF00;
            }
        """
        self.setStyleSheet(style)
        
        # Ocultar el panel de control de llamadas inicialmente
        self.call_control_panel.setVisible(False)

    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"Error obteniendo IP local: {e}")
            return "127.0.0.1"  # Fallback

    def get_trunk_manager(self):
        """Obtiene el trunk SIP asociado al panel de red."""
        try:
            if hasattr(self, 'sipp_controller'):
                print("Debug: Devolviendo controlador SIPP existente")
                return self.sipp_controller
            else:
                print("Debug: No hay controlador SIPP disponible")
                return None
                
        except Exception as e:
            print(f"Error al obtener controlador SIPP: {e}")
            return None

    def initialize_trunk_manager(self):
        """
        Inicializa el trunk manager con la configuración actual.
        Solo debe llamarse cuando los widgets estén inicializados.
        """
        try:
            config = {
                'local_ip': self.local_ip_edit.text(),
                'local_port': self.local_port_spin.value(),
                'remote_ip': self.remote_ip_edit.text(),
                'remote_port': self.remote_port_spin.value(),
                'transport': self.transport_combo.currentText().lower(),
                'timeout': self.options_timeout_spin.value(),
                'interval': self.options_interval_spin.value()
            }
            
            print(f"Debug: Configuración preparada: {config}")
            
            self.trunk_manager = SIPTrunk(config)
            print("Debug: SIPTrunk creado exitosamente")
            return self.trunk_manager
                
        except Exception as e:
            print(f"Error detallado al inicializar trunk_manager: {str(e)}")
            return None

    def setup_connections(self):
        """Configura las conexiones de señales y slots."""
        print("Debug: Configurando conexiones")
        
        # Conexión del botón de prueba de red
        self.test_network_btn.clicked.connect(self.test_network_connectivity)
        print("Debug: Conectado botón de test")
        
        # Conexión del checkbox de OPTIONS
        if hasattr(self, 'enable_options_cb'):
            print("Debug: Conectando checkbox de OPTIONS")
            self.enable_options_cb.stateChanged.connect(self.toggle_options_monitoring)
        else:
            print("Error: No se encontró el checkbox de OPTIONS")
        
        # Conexión del botón de servidor
        if hasattr(self, 'server_button'):
            print("Debug: Conectando botón de servidor")
            self.server_button.toggled.connect(self.toggle_server)
        else:
            print("Error: No se encontró el botón de servidor")
        
        print("Debug: Conexiones configuradas")

    def init_local_ip(self):
        """Inicializa la IP local con la IP real del sistema."""
        local_ip = get_local_ip()
        if local_ip:
            self.local_ip = local_ip  # Actualizar el atributo
            self.local_ip_edit.setText(local_ip)
            self.log_message.emit(f"IP local detectada: {local_ip}")
        else:
            self.local_ip = "0.0.0.0"  # Actualizar el atributo
            self.local_ip_edit.setText("0.0.0.0")
            self.log_message.emit("No se pudo detectar la IP local")

    def get_config(self):
        """Obtiene la configuración actual."""
        return {
            'local_ip': self.local_ip_edit.text(),
            'local_port': self.local_port_spin.value(),
            'remote_ip': self.remote_ip_edit.text(),
            'remote_port': self.remote_port_spin.value(),
            'transport': self.transport_combo.currentText().upper(),
            'interval': self.options_interval_spin.value(),
            'timeout': self.options_timeout_spin.value()
        }

    def validate_ip(self, ip_address: str) -> bool:
        """Valida el formato de una dirección IP."""
        try:
            parts = ip_address.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except (AttributeError, TypeError, ValueError):
            return False

    def on_local_ip_changed(self, value):
        if self.validate_ip(value):
            self.local_ip = value
            self.local_ip_edit.setStyleSheet("")
        else:
            self.local_ip_edit.setStyleSheet("border: 1px solid red")

    def on_remote_ip_changed(self):
        """Maneja cambios en la IP remota."""
        try:
            new_ip = self.remote_ip_edit.text().strip()
            if new_ip != self.remote_ip:
                self.remote_ip = new_ip
                # Actualizar configuración en monitor y call handler
                if self.sip_monitor:
                    self.sip_monitor.config['remote_ip'] = new_ip
                if self.call_handler:
                    self.call_handler.update_config('remote_ip', new_ip)
                logger.debug(f"IP remota actualizada a: {new_ip}")
        except Exception as e:
            logger.error(f"Error actualizando IP remota: {e}")

    def toggle_options_monitoring(self, state):
        """Activa o desactiva el monitoreo OPTIONS."""
        print(f"Debug: toggle_options_monitoring llamado con estado: {state}")
        print(f"Debug: Tipo de estado: {type(state)}")
        
        if not self.validate_config():
            print("Debug: Configuración no válida")
            self.enable_options_cb.setChecked(False)
            return
            
        config = self.get_config()
        print(f"Debug: Configuración obtenida: {config}")
        
        # Estado 2 es Qt.CheckState.Checked
        if state == 2:
            print("Debug: INICIANDO monitoreo")
            self.log_message.emit("Intentando iniciar monitoreo OPTIONS...")
            
            # Forzar el inicio del monitoreo
            if not hasattr(self.sip_monitor, '_options_thread') or self.sip_monitor._options_thread is None:
                print("Debug: Creando nuevo hilo de monitoreo")
                success = self.sip_monitor.start_options_monitoring(config)
                print(f"Debug: Resultado del inicio de monitoreo: {success}")
                
                if success:
                    print("Debug: Monitoreo iniciado con éxito")
                    self.options_status_label.setText("Estado OPTIONS: Monitoreando")
                    self.log_message.emit("Monitoreo OPTIONS iniciado")
                    self.options_interval_spin.setEnabled(False)
                    self.options_timeout_spin.setEnabled(False)
                else:
                    print("Debug: Error al iniciar monitoreo")
                    self.enable_options_cb.setChecked(False)
                    self.log_message.emit("Error al iniciar monitoreo OPTIONS")
                    self.led_indicator.setActive(False)
            else:
                print("Debug: El hilo de monitoreo ya existe")
        else:
            print("Debug: DETENIENDO monitoreo")
            self.sip_monitor.stop_options_monitoring()
            self.options_status_label.setText("Estado OPTIONS: Inactivo")
            self.log_message.emit("Monitoreo OPTIONS detenido")
            self.options_interval_spin.setEnabled(True)
            self.options_timeout_spin.setEnabled(True)
            self.led_indicator.setActive(False)

    def update_status(self):
        """Actualiza los contadores de estado."""
        try:
            if not self.sip_monitor:
                return
            
            stats = self.sip_monitor._stats
            logger.debug(f"Actualizando estadísticas: {stats}")
            
            # Actualizar contadores
            self.sent_options.setText(f"OPTIONS Enviados: {stats['options_sent']}")
            self.received_options.setText(f"OPTIONS Recibidos: {stats['options_received']}")
            self.sent_ok.setText(f"200 OK Enviados: {stats['ok_sent']}")
            self.received_ok.setText(f"200 OK Recibidos: {stats['ok_received']}")
            self.timeouts.setText(f"Timeouts: {stats['timeouts']}")
            
            # Actualizar latencia si existe
            if 'last_latency' in stats and stats['last_latency'] is not None:
                self._update_latency(stats['last_latency'])
            
        except Exception as e:
            logger.error(f"Error actualizando estado: {e}")

    def toggle_server(self, checked):
        """Maneja el cambio de estado del servidor."""
        logger.debug(f"toggle_server llamado con checked={checked}")
        
        if checked:
            # Intentar iniciar el servidor
            self.reset_counters()
            if self.validate_config():
                try:
                    config = self.get_config()
                    logger.debug(f"Iniciando servidor con config: {config}")
                    
                    # Añadir call_handler a la configuración
                    config['call_handler'] = self.call_handler
                    logger.debug(f"Call handler añadido a config: {self.call_handler}")
                    
                    # Actualizar configuración del monitor
                    self.sip_monitor.config = config.copy()
                    
                    # Iniciar el servidor
                    if self.sip_monitor.start_server(config):
                        # Actualizar UI
                        self.server_button.setText("Detener Servidor")
                        self.server_status_label.setText("Estado: Activo")
                        self.log_message.emit(f"Servidor SIP iniciado en {config['local_ip']}:{config['local_port']}")
                        self.enable_call_control.emit(True)
                        self.call_control_panel.setVisible(True)
                        return
                    else:
                        raise Exception("No se pudo iniciar el servidor")
                    
                except Exception as e:
                    logger.error(f"Error iniciando servidor: {str(e)}", exc_info=True)
                    self.handle_error(f"Error iniciando servidor: {str(e)}", True)
            
            # Si llegamos aquí, hubo un error - restaurar estado del botón
            self.server_button.blockSignals(True)  # Evitar recursión
            self.server_button.setChecked(False)
            self.server_button.setText("Iniciar Servidor")
            self.server_button.blockSignals(False)
        
        else:
            # Intentar detener el servidor
            try:
                logger.debug("Deteniendo servidor...")
                
                # Detener monitoreo OPTIONS si está activo
                if self.enable_options_cb.isChecked():
                    self.enable_options_cb.setChecked(False)
                
                # Detener el servidor
                if hasattr(self, 'sip_monitor') and self.sip_monitor is not None:
                    self.sip_monitor.stop_server()
                    
                # Actualizar UI
                self.server_button.setText("Iniciar Servidor")
                self.server_status_label.setText("Estado: Detenido")
                self.log_message.emit("Servidor SIP detenido")
                self.enable_call_control.emit(False)
                self.call_control_panel.setVisible(False)
                
                # Esperar un momento para asegurar que el socket se libera
                time.sleep(0.5)
                
                logger.debug("Servidor detenido correctamente")
                
            except Exception as e:
                logger.error(f"Error al detener servidor: {e}")
                self.handle_error(f"Error al detener servidor: {str(e)}", True)
            finally:
                # Asegurar que el botón refleja el estado correcto
                self.server_button.blockSignals(True)
                self.server_button.setChecked(False)
                self.server_button.setText("Iniciar Servidor")
                self.server_button.blockSignals(False)

    def handle_single_call(self):
        """Maneja una llamada individual."""
        try:
            if not hasattr(self, 'sipp_controller') or not self.sipp_controller:
                self.log_message.emit("Error: El servidor SIP no está iniciado")
                return

            print("Debug: Iniciando llamada individual")
            if self.sipp_controller.start_call():
                self.log_message.emit("Llamada iniciada correctamente")
            else:
                self.log_message.emit("Error al iniciar la llamada")
                
        except Exception as e:
            print(f"Error en handle_single_call: {e}")
            self.log_message.emit(f"Error al iniciar llamada: {str(e)}")

    def handle_call_initiation(self, from_uri: str, to_uri: str):
        if self.call_handler:
            self.call_handler.start_single_call(from_uri, to_uri)
        else:
            print("Debug: Error - No hay call_handler disponible")

    def cleanup(self):
        """Limpia recursos antes de cerrar."""
        try:
            logger.debug("Iniciando limpieza de NetworkPanel")
            
            # Detener timer de actualización
            if hasattr(self, 'update_timer'):
                self.update_timer.stop()
            
            # Limpiar call handler primero
            if hasattr(self, 'call_handler'):
                self.call_handler.cleanup()
            
            # Luego detener el monitor
            if hasattr(self, 'sip_monitor'):
                self.sip_monitor.stop_options_monitoring()
                self.sip_monitor.stop_server()
            
            logger.debug("Limpieza de NetworkPanel completada")
            
        except Exception as e:
            logger.error(f"Error durante cleanup de NetworkPanel: {e}")

    def on_port_changed(self, value):
        self.local_port = value

    def on_remote_port_changed(self, value):
        self.remote_port = value

    def on_transport_changed(self, value):
        self.transport = value.upper()  # Guardamos en mayúsculas para consistencia

    def save_config(self):
        """Guarda la configuración actual."""
        config = {
            'local_ip': self.local_ip,
            'local_port': self.local_port,
            'remote_ip': self.remote_ip,
            'remote_port': self.remote_port,
            'transport': self.transport
        }
        return config

    def load_config(self, config: dict):
        """Carga una configuración guardada."""
        if config:
            self.local_ip = config.get('local_ip', self.local_ip)
            self.local_port = config.get('local_port', self.local_port)
            self.remote_ip = config.get('remote_ip', self.remote_ip)
            self.remote_port = config.get('remote_port', self.remote_port)
            self.transport = config.get('transport', self.transport)
            
            # Actualizar UI
            self.local_ip_edit.setText(self.local_ip)
            self.local_port_spin.setValue(self.local_port)
            self.remote_ip_edit.setText(self.remote_ip)
            self.remote_port_spin.setValue(self.remote_port)
            self.transport_combo.setCurrentText(self.transport)

    def handle_error(self, error_msg: str, show_dialog: bool = False):
        """Maneja errores de manera centralizada."""
        print(f"Debug: Error - {error_msg}")
        self.log_message.emit(f"Error: {error_msg}")
        
        if show_dialog:
            QMessageBox.critical(self, "Error", error_msg)

    def is_port_available(self, port: int) -> bool:
        """Verifica si un puerto está disponible."""
        # Si el servidor ya está usando este puerto, considerarlo como disponible
        if hasattr(self, 'sip_monitor') and hasattr(self.sip_monitor, '_server'):
            return True
            
        try:
            # Solo verificar si el puerto está en uso por otra aplicación
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                return result != 0
        except OSError:
            return False

    def validate_config(self):
        """Valida la configuración antes de iniciar el servidor."""
        if not self.validate_ip(self.local_ip_edit.text()):
            self.handle_error("IP local inválida", True)
            return False
            
        if not self.validate_ip(self.remote_ip_edit.text()):
            self.handle_error("IP remota inválida", True)
            return False
            
        # Solo verificar el puerto si el servidor no está activo
        if not hasattr(self, 'sip_monitor') or not hasattr(self.sip_monitor, '_server'):
            if not self.is_port_available(self.local_port_spin.value()):
                self.handle_error(f"El puerto {self.local_port_spin.value()} no está disponible", True)
                return False
            
        return True

    def test_network_connectivity(self):
        """Prueba la conectividad básica de red con el servidor remoto."""
        if not self.validate_config():
            return
            
        config = self.get_config()
        self.network_status_label.setText("Estado: Probando...")
        self.test_network_btn.setEnabled(False)
        
        try:
            if config['transport'].upper() == "UDP":
                # Para UDP, solo verificamos que podamos crear y vincular un socket
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(2)
                    # Intentar vincular a una dirección local
                    s.bind((config['local_ip'], 0))  # Puerto efímero
                    # Intentar enviar un paquete vacío
                    s.sendto(b"", (config['remote_ip'], config['remote_port']))
                    success = True
            else:
                # Para TCP, intentar establecer conexión
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    result = s.connect_ex((config['remote_ip'], config['remote_port']))
                    success = (result == 0)
                
            if success:
                self.network_status_label.setText("Estado: Conectividad OK")
                self.connectivity_status_changed.emit(True)
                self.log_message.emit(
                    f"Conectividad establecida con {config['remote_ip']}:{config['remote_port']}"
                )
            else:
                self.network_status_label.setText("Estado: Error de Conectividad")
                self.connectivity_status_changed.emit(False)
                self.log_message.emit(
                    f"Error de conectividad con {config['remote_ip']}:{config['remote_port']}"
                )
                    
        except Exception as e:
            self.network_status_label.setText("Estado: Error")
            self.log_message.emit(f"Error al probar conectividad: {str(e)}")
            self.connectivity_status_changed.emit(False)
            
        finally:
            self.test_network_btn.setEnabled(True)

    def is_ready_for_operation(self) -> bool:
        """Verifica si el panel está listo para operaciones."""
        if not self.local_ip or not self.remote_ip:
            self.handle_error("Configuración de IPs incompleta", True)
            return False
            
        if not self.validate_ip(self.local_ip) or not self.validate_ip(self.remote_ip):
            self.handle_error("IPs configuradas no son válidas", True)
            return False
            
        if not self.is_port_available(self.local_port_spin.value()):
            self.handle_error(f"Puerto local {self.local_port_spin.value()} no disponible", True)
            return False
            
        return True

    def restore_defaults(self):
        """Restaura la configuración a valores por defecto."""
        self.local_ip = self._get_local_ip()
        self.local_port = 5060
        self.remote_ip = ""
        self.remote_port = 5060
        self.transport = "UDP"
        
        # Actualizar UI
        self.local_ip_edit.setText(self.local_ip)
        self.local_port_spin.setValue(self.local_port)
        self.remote_ip_edit.setText(self.remote_ip)
        self.remote_port_spin.setValue(self.remote_port)
        self.transport_combo.setCurrentText(self.transport)

    def reset_counters(self):
        """Resetea todos los contadores de mensajes."""
        try:
            if hasattr(self, 'sip_monitor'):
                # Solo intentar reset_stats si existe el método
                if hasattr(self.sip_monitor, 'reset_stats'):
                    self.sip_monitor.reset_stats()
        except Exception as e:
            print(f"Debug: Error reseteando estadísticas: {e}")
        
        # Actualizar UI independientemente del estado del monitor
        self.sent_options.setText("OPTIONS Enviados: 0")
        self.received_options.setText("OPTIONS Recibidos: 0")
        self.sent_ok.setText("200 OK Enviados: 0")
        self.received_ok.setText("200 OK Recibidos: 0")
        self.timeouts.setText("Timeouts: 0")
        self.latency_value.setText("-- ms")
        self.led_indicator.setActive(False)

    def setup_call_handler(self):
        """Configura el manejador de llamadas."""
        if self.call_handler:
            # No conectar señales relacionadas con llamadas aquí
            # Solo mantener las señales de monitorización
            pass

    def update_call_status(self, call_data: dict):
        """Actualiza el estado de una llamada en la UI."""
        try:
            logger.debug(f"Actualizando estado de llamada: {call_data}")
            # Actualizar la tabla de llamadas
            self.add_call_to_table(
                call_data['call_id'],
                call_data['state'],
                call_data['direction'],
                call_data['from_uri'],
                call_data['to_uri'],
                call_data['start_time']
            )
        except Exception as e:
            logger.error(f"Error actualizando estado de llamada: {e}")

    def add_call_to_table(self, call_id: str, state: str, direction: str, from_uri: str, to_uri: str, start_time: str):
        """Añade o actualiza una llamada en la tabla."""
        try:
            # Buscar si la llamada ya existe en la tabla
            found = False
            for row in range(self.calls_table.rowCount()):
                if self.calls_table.item(row, 1).text() == call_id:  # Columna Call-ID
                    # Actualizar fila existente
                    self.calls_table.item(row, 2).setText(state)  # Estado
                    found = True
                    break
                
            if not found:
                # Añadir nueva fila
                row = self.calls_table.rowCount()
                self.calls_table.insertRow(row)
                
                # Añadir datos
                self.calls_table.setItem(row, 0, QTableWidgetItem(start_time))  # Hora
                self.calls_table.setItem(row, 1, QTableWidgetItem(call_id))    # Call-ID
                self.calls_table.setItem(row, 2, QTableWidgetItem(state))      # Estado
                self.calls_table.setItem(row, 3, QTableWidgetItem(direction))  # Dirección
                self.calls_table.setItem(row, 4, QTableWidgetItem(from_uri))   # Origen
                self.calls_table.setItem(row, 5, QTableWidgetItem(to_uri))     # Destino
                
            logger.debug(f"Tabla actualizada para llamada {call_id} en estado {state}")
            
        except Exception as e:
            logger.error(f"Error actualizando tabla de llamadas: {e}")

    def _connect_monitor_signals(self):
        """Conecta las señales del monitor SIP."""
        try:
            if self.sip_monitor:
                logger.debug("Conectando señales del monitor SIP")
                # Desconectar señales existentes primero
                try:
                    self.sip_monitor.rtt_updated.disconnect()
                    self.sip_monitor.stats_updated.disconnect()
                except:
                    pass
                
                # Conectar señales
                self.sip_monitor.rtt_updated.connect(self._update_latency)
                self.sip_monitor.stats_updated.connect(self.update_status)
                logger.debug("Señales del monitor conectadas")
        except Exception as e:
            logger.error(f"Error conectando señales del monitor: {e}")

    def _update_latency(self, rtt: float):
        """Actualiza el indicador de latencia."""
        try:
            if rtt > 0:
                self.latency_value.setText(f"{rtt:.2f} ms")
                self.led_indicator.setActive(True)
                logger.debug(f"Latencia actualizada: {rtt:.2f} ms")
            else:
                self.latency_value.setText("-- ms")
                self.led_indicator.setActive(False)
                logger.debug("LED desactivado - sin latencia")
        except Exception as e:
            logger.error(f"Error actualizando latencia: {e}")

    def init_monitor(self):
        """Inicializa el monitor SIP."""
        try:
            # Crear configuración inicial
            config = {
                'local_ip': self.local_ip,
                'local_port': self.local_port,
                'remote_ip': self.remote_ip,
                'remote_port': self.remote_port,
                'transport': self.transport
            }
            
            # Crear y configurar el monitor
            self.sip_monitor = SIPMonitor()
            self.sip_monitor.config = config
            
            # Crear y configurar el call handler
            self.call_handler = SIPCallHandler(config)
            self.call_handler.sip_monitor = self.sip_monitor
            
            # Configurar el monitor para usar el call handler
            self.sip_monitor.call_handler = self.call_handler
            
            # Crear y configurar el panel de control de llamadas
            self.call_control_panel = CallControlPanel(self)
            self.call_control_panel.set_call_handler(self.call_handler)
            
            # Añadir el panel de control al layout
            self.call_control_container.layout().addWidget(self.call_control_panel)
            
            logger.debug(f"Monitor SIP inicializado con config: {config}")
            logger.debug("Panel de control de llamadas configurado")
            
        except Exception as e:
            logger.error(f"Error inicializando monitor: {e}")

              
