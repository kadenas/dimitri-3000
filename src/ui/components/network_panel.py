from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QComboBox, QSpinBox, QLineEdit, QGroupBox,
                           QPushButton, QCheckBox, QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from datetime import datetime

# Importaciones de componentes propios
from src.core.sip_monitor import SIPMonitor
from src.core.sip_trunk import SIPTrunk  # Asegúrate de que esta línea está presente
from src.utils.network_utils import get_local_ip
from src.ui.components.led_indicator import LedIndicator
from src.ui.components.call_control_panel import CallControlPanel  # Solo una vez


class NetworkPanel(QWidget):
    """Panel de configuración de red con monitoreo SIP integrado."""
    
    # Señales para notificar eventos
    options_status_changed = pyqtSignal(bool)
    connectivity_status_changed = pyqtSignal(bool)
    log_message = pyqtSignal(str)  # Para enviar mensajes al terminal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)
        self._last_monitoring_state = False
        self.trunk_manager = None
        self.sip_monitor = SIPMonitor()  # Añadir esta línea
        self.main_layout = QVBoxLayout(self)
        self.setup_ui()
        self.setup_connections()
        self.init_local_ip()
        print("Debug: NetworkPanel inicializado")
    
    def setup_ui(self):
        """Configura la interfaz del panel de red."""
        main_layout = self.main_layout
        
        # Protocolo común
        protocol_layout = QHBoxLayout()
        protocol_label = QLabel("Protocolo:")
        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["UDP", "TCP", "TLS"])
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
        local_ip_layout.addWidget(local_ip_label)
        local_ip_layout.addWidget(self.local_ip_edit)
        
        # Puerto Local
        local_port_layout = QHBoxLayout()
        local_port_label = QLabel("Puerto Local:")
        self.local_port_spin = QSpinBox()
        self.local_port_spin.setRange(1, 65535)
        self.local_port_spin.setValue(5060)
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
        remote_ip_layout.addWidget(remote_ip_label)
        remote_ip_layout.addWidget(self.remote_ip_edit)
        
        # Puerto Remoto
        remote_port_layout = QHBoxLayout()
        remote_port_label = QLabel("Puerto Remoto:")
        self.remote_port_spin = QSpinBox()
        self.remote_port_spin.setRange(1, 65535)
        self.remote_port_spin.setValue(5060)
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
        latency_label = QLabel("Latencia:")
        self.latency_value = QLabel("-- ms")
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
        
        # Añadir todo al layout principal
        main_layout.addLayout(protocol_layout)
        main_layout.addWidget(local_group)
        main_layout.addWidget(remote_group)
        main_layout.addWidget(connectivity_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(stats_group)
        main_layout.addWidget(server_group)
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
            self.local_ip_edit.setText(local_ip)
            self.log_message.emit(f"IP local detectada: {local_ip}")
        else:
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

    def validate_config(self):
        """Valida la configuración actual."""
        config = self.get_config()
        
        if not config['local_ip'] or not config['remote_ip']:
            QMessageBox.warning(self, "Error de Configuración",
                              "Las direcciones IP no pueden estar vacías.")
            return False
            
        try:
            # Validar formato de IPs
            from ipaddress import ip_address
            ip_address(config['local_ip'])
            ip_address(config['remote_ip'])
        except ValueError:
            QMessageBox.warning(self, "Error de Configuración",
                              "Formato de IP inválido.")
            return False
            
        return True

    def test_network_connectivity(self):
        """Prueba la conectividad de red básica."""
        if not self.validate_config():
            return
            
        config = self.get_config()
        self.network_status_label.setText("Estado: Probando...")
        self.test_network_btn.setEnabled(False)
        
        try:
            result = self.sip_monitor.test_connectivity(
                config['remote_ip'],
                config['remote_port'],
                config['transport']
            )
            
            if result:
                self.network_status_label.setText("Estado: Conectividad OK")
                self.connectivity_status_changed.emit(True)
                self.log_message.emit(f"Conectividad establecida con {config['remote_ip']}:{config['remote_port']}")
            else:
                self.network_status_label.setText("Estado: Error de Conectividad")
                self.connectivity_status_changed.emit(False)
                self.log_message.emit(f"Error de conectividad con {config['remote_ip']}:{config['remote_port']}")
                
        except Exception as e:
            self.network_status_label.setText("Estado: Error")
            self.log_message.emit(f"Error al probar conectividad: {str(e)}")
            
        finally:
            self.test_network_btn.setEnabled(True)


    def toggle_server(self):
        """Maneja el inicio/parada del servidor SIP."""
        try:
            if self.server_button.isChecked():
                # Validar configuración
                if not self.validate_config():
                    self.server_button.setChecked(False)
                    return
                    
                print("Debug: Iniciando servidor SIP...")
                # Inicializar SIPP
                from src.core.sipp_controller import SIPPController
                
                config = {
                    'local_ip': self.local_ip_edit.text(),
                    'local_port': self.local_port_spin.value(),
                    'remote_ip': self.remote_ip_edit.text(),
                    'remote_port': self.remote_port_spin.value(),
                    'transport': self.transport_combo.currentText().lower()
                }
                
                self.sipp_controller = SIPPController(config)
                if self.sipp_controller.initialize():
                    self.server_status_label.setText("Estado: Activo")
                    self.log_message.emit("Servidor SIP iniciado correctamente")
                else:
                    self.server_button.setChecked(False)
                    self.server_status_label.setText("Estado: Error")
                    self.log_message.emit("Error al iniciar el servidor SIP")
            else:
                print("Debug: Deteniendo servidor SIP...")
                if hasattr(self, 'sipp_controller'):
                    # Limpiar recursos si es necesario
                    self.sipp_controller = None
                self.server_status_label.setText("Estado: Detenido")
                self.log_message.emit("Servidor SIP detenido")
                
        except Exception as e:
            print(f"Error en toggle_server: {e}")
            self.server_button.setChecked(False)
            self.server_status_label.setText("Estado: Error")
            self.log_message.emit(f"Error en el servidor: {str(e)}")

    def validate_config(self):
        """Valida la configuración antes de iniciar el servidor."""
        if not self.local_ip_edit.text().strip():
            self.log_message.emit("Error: IP local es requerida")
            return False
        if not self.local_port_spin.value():
            self.log_message.emit("Error: Puerto local es requerido")
            return False
        return True

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
        """Actualiza el estado mostrado en la interfaz."""
        try:
            # Verificar si el monitor está inicializado
            if not hasattr(self, 'sip_monitor') or self.sip_monitor is None:
                return

            # Obtener valores con protección contra None
            stats = getattr(self.sip_monitor, 'stats', {})
            last_response = getattr(self.sip_monitor, 'last_options_response', None)
            last_rtt = getattr(self.sip_monitor, 'last_rtt', None)
            
            if self.sip_monitor.is_monitoring:
                # Actualizar contadores con valores por defecto
                self.sent_options.setText(f"OPTIONS Enviados: {stats.get('options_sent', 0)}")
                self.received_options.setText(f"OPTIONS Recibidos: {stats.get('options_received', 0)}")
                self.sent_ok.setText(f"200 OK Enviados: {stats.get('ok_sent', 0)}")
                self.received_ok.setText(f"200 OK Recibidos: {stats.get('ok_received', 0)}")
                self.timeouts.setText(f"Timeouts: {stats.get('timeouts', 0)}")
                
                # Manejar latencia
                latency = stats.get('last_latency')
                self.latency_value.setText(f"{latency:.2f} ms" if latency else "-- ms")

                # Lógica del LED y estado
                if last_response:
                    current_time = datetime.now()
                    interval = self.options_interval_spin.value() * 1.5
                    time_since_last = (current_time - last_response).total_seconds()
                    
                    self.led_indicator.setActive(time_since_last < interval)
                    
                    status_text = f"Estado OPTIONS: OK (Última respuesta: {last_response.strftime('%H:%M:%S')}"
                    if last_rtt:
                        status_text += f", RTT: {last_rtt:.2f}ms)"
                    else:
                        status_text += ")"
                else:
                    self.led_indicator.setActive(False)
                    status_text = "Estado OPTIONS: Esperando respuesta inicial..."
                
                self.options_status_label.setText(status_text)
                
            else:
                # Estado cuando el monitoreo está inactivo
                self.led_indicator.setActive(False)
                self.options_status_label.setText("Estado OPTIONS: Monitoreo inactivo")
                self._last_monitoring_state = False

        except Exception as e:
            print(f"Error en update_status: {str(e)}")
            # Opcional: registrar el error en el terminal
            self.log_message(f"Error actualizando estado: {str(e)}")

    def toggle_server(self, checked):
        """Inicia o detiene el servidor SIP."""
        print(f"Debug: toggle_server llamado con estado: {checked}")
        if checked:
            if self.validate_config():
                try:
                    config = self.get_config()
                    self.sip_monitor = SIPMonitor()
                    print(f"Debug: Iniciando servidor con config: {config}")
                    
                    success = self.sip_monitor.start_server(
                        config['local_ip'],
                        config['local_port'],
                        config['transport']
                    )
                    
                    if success:
                        print("Debug: Servidor iniciado con éxito")
                        self.server_button.setText("Detener Servidor")
                        self.server_status_label.setText(
                            f"Estado: Escuchando en {config['local_ip']}:{config['local_port']}"
                        )
                        self.log_message.emit(
                            f"Servidor SIP iniciado en {config['local_ip']}:{config['local_port']}"
                        )
                        
                        # Inicializar trunk
                        self.trunk = self.initialize_trunk_manager()
                        if self.trunk:
                            print("Debug: Trunk inicializado correctamente")
                            # Inicializar el manejador de llamadas
                            try:
                                from src.core.sip_call_handler import SIPCallHandler
                                self.call_handler = SIPCallHandler({
                                    'trunk': self.trunk,  # Usar el trunk inicializado
                                    'local_ip': config['local_ip'],
                                    'local_port': config['local_port'],
                                    'remote_ip': config['remote_ip'],
                                    'remote_port': config['remote_port'],
                                    'transport': config['transport']
                                })
                                print("Debug: Manejador de llamadas inicializado correctamente")
                            except Exception as call_error:
                                print(f"Debug: Error inicializando manejador de llamadas: {call_error}")
                        else:
                            print("Debug: Error inicializando trunk")
                            
                        # Deshabilitar campos de configuración
                        self.local_ip_edit.setEnabled(False)
                        self.local_port_spin.setEnabled(False)
                        self.transport_combo.setEnabled(False)
                        
                    else:
                        print("Debug: Error al iniciar servidor")
                        self.server_button.setChecked(False)
                        self.log_message.emit("Error al iniciar el servidor SIP")
                        
                except Exception as e:
                    print(f"Debug: Excepción al iniciar servidor: {e}")
                    self.server_button.setChecked(False)
                    self.log_message.emit(f"Error al iniciar el servidor: {str(e)}")
                    self.server_status_label.setText("Estado: Error al iniciar")
            else:
                print("Debug: Configuración no válida")
                self.server_button.setChecked(False)
        else:
            print("Debug: Deteniendo servidor")
            self.sip_monitor.stop_server()
            
            if hasattr(self, 'call_handler'):
                print("Debug: Limpiando manejador de llamadas")
                delattr(self, 'call_handler')
            
            if hasattr(self, 'trunk'):
                delattr(self, 'trunk')
                
            self.server_button.setText("Iniciar Servidor")
            self.server_status_label.setText("Estado: Detenido")
            self.log_message.emit("Servidor SIP detenido")
            
            self.local_ip_edit.setEnabled(True)
            self.local_port_spin.setEnabled(True)
            self.transport_combo.setEnabled(True)
    
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
        print("Debug: Iniciando limpieza de recursos")
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        if hasattr(self, 'sip_monitor'):
            self.sip_monitor.stop_options_monitoring()
            self.sip_monitor.stop_server()
        print("Debug: Limpieza completada")
              
