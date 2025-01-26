from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QPushButton, QSpinBox, QLabel, QTableWidget,
                           QTableWidgetItem, QHeaderView, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
import traceback  # Añadir esta línea
from src.core.sip_call_handler import SIPCallHandler  # Esta es la única que necesitamos
from src.ui.components.call_monitor_table import CallMonitorTable
from src.core.sip_monitor import SIPMonitor

class CallControlPanel(QWidget):
    # Señales para comunicación con el controlador principal
    call_initiated = pyqtSignal(str, str)  # from_uri, to_uri
    burst_started = pyqtSignal(int, int)   # interval, max_calls
    burst_stopped = pyqtSignal()
    bye_all = pyqtSignal(float)            # bye_interval

    def __init__(self, parent=None):
        super().__init__(parent)
        self.call_monitor = SIPMonitor()  # Crear instancia del monitor
        self.init_ui()


    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel Superior - Control Servidor
        server_group = QGroupBox("Control Servidor")
        server_layout = QVBoxLayout()

        # Configuración de llamadas
        call_config_layout = QHBoxLayout()
        
        # Número origen
        from_layout = QHBoxLayout()
        from_layout.addWidget(QLabel("Número Origen:"))
        self.from_number = QLineEdit()
        self.from_number.setPlaceholderText("ej: 1001")
        from_layout.addWidget(self.from_number)
        
        # Número destino
        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("Número Destino:"))
        self.to_number = QLineEdit()
        self.to_number.setPlaceholderText("ej: 2001")
        to_layout.addWidget(self.to_number)
        
        call_config_layout.addLayout(from_layout)
        call_config_layout.addLayout(to_layout)
        
        # Botones de control
        buttons_layout = QHBoxLayout()
        self.llamada_btn = QPushButton("LLAMADA")
        self.metralleta_btn = QPushButton("METRALLETA")
        self.stop_metralleta_btn = QPushButton("Stop Metralleta")
        self.bye_btn = QPushButton("BYE")
        
        for btn in [self.llamada_btn, self.metralleta_btn, 
                self.stop_metralleta_btn, self.bye_btn]:
            buttons_layout.addWidget(btn)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #002200;
                    color: #00FF00;
                    border: 1px solid #00FF00;
                    padding: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #003300;
                }
                QPushButton:pressed {
                    background-color: #004400;
                }
            """)

        # Configuración de metralleta
        metralleta_config = QHBoxLayout()
        metralleta_config.addWidget(QLabel("Intervalo (seg):"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)
        self.interval_spin.setValue(1)
        metralleta_config.addWidget(self.interval_spin)
        
        metralleta_config.addWidget(QLabel("Max. Llamadas:"))
        self.max_calls_spin = QSpinBox()
        self.max_calls_spin.setRange(1, 100)
        self.max_calls_spin.setValue(1)
        metralleta_config.addWidget(self.max_calls_spin)
        
        # Añadir layouts al panel servidor
        server_layout.addLayout(call_config_layout)
        server_layout.addLayout(buttons_layout)
        server_layout.addLayout(metralleta_config)
        server_group.setLayout(server_layout)

        # Monitor de Llamadas
        monitor_group = QGroupBox("Monitor de Llamadas")
        monitor_layout = QVBoxLayout()

        # Contadores
        counters_layout = QHBoxLayout()
        self.active_calls = QLabel("Activas: 0")
        self.failed_calls = QLabel("Fallidas: 0")
        self.total_calls = QLabel("Total: 0")
        for label in [self.active_calls, self.failed_calls, self.total_calls]:
            counters_layout.addWidget(label)

        # Nueva tabla de llamadas
        self.calls_table = CallMonitorTable()
        monitor_layout.addWidget(self.calls_table)

        # Conectar señales del monitor
        self.call_monitor.stats_updated.connect(self.update_counters)
        
        monitor_layout.addLayout(counters_layout)
        monitor_layout.addWidget(self.calls_table)
        monitor_group.setLayout(monitor_layout)

        # Añadir grupos al layout principal
        main_layout.addWidget(server_group)
        main_layout.addWidget(monitor_group)

        # Conectar señales
        self.llamada_btn.clicked.connect(self._handle_call_button)
        self.metralleta_btn.clicked.connect(self._handle_burst_button)
        self.stop_metralleta_btn.clicked.connect(self.burst_stopped.emit)
        self.bye_btn.clicked.connect(lambda: self.bye_all.emit(0.5))

    def set_sipp_controller(self, controller):
        """Establece el controlador SIPP"""
        self.sipp_controller = controller

    def _handle_call_button(self):
        try:
            from_uri = self.from_number.text().strip()
            to_uri = self.to_number.text().strip()
            
            if not from_uri or not to_uri:
                return
                
            call_data = CallData(
                call_id=f"{int(time.time())}-{uuid.uuid4().hex[:8]}",
                from_uri=from_uri,
                to_uri=to_uri,
                state=CallState.INITIAL,
                direction="outbound",
                start_time=datetime.now()
            )
            
            self.call_monitor.add_call(call_data)
            self.call_initiated.emit(from_uri, to_uri)
                
        except Exception as e:
            print(f"Error: {e}")

    def _handle_burst_button(self):
        """Maneja el click en el botón de metralleta."""
        try:
            interval = self.interval_spin.value()
            max_calls = self.max_calls_spin.value()
            print(f"Debug: Iniciando modo metralleta (intervalo: {interval}s, max: {max_calls})")
            self.burst_started.emit(interval, max_calls)
        except Exception as e:
            print(f"Error en handle_burst_button: {str(e)}")

    def update_call_status(self, call_data):
        """Actualiza el estado de una llamada en la tabla"""
        self.calls_table.add_call({
            'state': call_data['status'],
            'from_uri': call_data['from_uri'],
            'to_uri': call_data['to_uri'],
            'duration': call_data.get('duration', '0:00')
        })

    def _create_server_panel(self):
        group = QGroupBox("Control Servidor")
        layout = QVBoxLayout()

        # Botones de control
        buttons_layout = QHBoxLayout()
        self.single_call_btn = QPushButton("LLAMADA")
        self.burst_call_btn = QPushButton("METRALLETA")
        self.stop_burst_btn = QPushButton("Stop Metralleta")
        self.bye_all_btn = QPushButton("BYE")
        
        buttons_layout.addWidget(self.single_call_btn)
        buttons_layout.addWidget(self.burst_call_btn)
        buttons_layout.addWidget(self.stop_burst_btn)
        buttons_layout.addWidget(self.bye_all_btn)
        
        layout.addLayout(buttons_layout)

        # Configuración de metralleta
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Intervalo (seg):"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)
        config_layout.addWidget(self.interval_spin)
        
        config_layout.addWidget(QLabel("Max. Llamadas:"))
        self.max_calls_spin = QSpinBox()
        self.max_calls_spin.setRange(1, 100)
        config_layout.addWidget(self.max_calls_spin)
        
        layout.addLayout(config_layout)
        group.setLayout(layout)
        return group

    def _create_client_panel(self):
        group = QGroupBox("Control Cliente")
        layout = QVBoxLayout()

        # Configuración de cliente
        client_layout = QHBoxLayout()
        client_layout.addWidget(QLabel("Max. Llamadas Entrantes:"))
        self.max_incoming_spin = QSpinBox()
        self.max_incoming_spin.setRange(1, 100)
        client_layout.addWidget(self.max_incoming_spin)
        
        layout.addLayout(client_layout)
        
        # Contadores
        counters_layout = QHBoxLayout()
        self.active_calls_label = QLabel("Activas: 0")
        self.failed_calls_label = QLabel("Fallidas: 0")
        self.total_calls_label = QLabel("Total: 0")
        
        counters_layout.addWidget(self.active_calls_label)
        counters_layout.addWidget(self.failed_calls_label)
        counters_layout.addWidget(self.total_calls_label)
        
        layout.addLayout(counters_layout)
        group.setLayout(layout)
        return group

    def _create_monitor_panel(self):
        group = QGroupBox("Monitor de Llamadas")
        layout = QVBoxLayout()

        # Tabla de llamadas
        self.calls_table = QTableWidget()
        self.calls_table.setColumnCount(6)
        headers = ["Hora", "Call-ID", "Estado", "Dirección", "Origen", "Destino"]
        self.calls_table.setHorizontalHeaderLabels(headers)
        
        # Ajustar columnas
        header = self.calls_table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.calls_table)
        group.setLayout(layout)
        return group
    
    def set_call_handler(self, handler):
        """
        Establece el manejador de llamadas SIP y configura las conexiones necesarias.
        
        Args:
            handler: Instancia de SIPCallHandler para manejar las operaciones de llamadas
        """
        try:
            self.call_handler = handler
            if self.call_handler is not None:
                # Conectar señales del handler con los slots del panel
                self.call_handler.call_status_changed.connect(self.update_call_status)
                self.call_handler.call_stats_updated.connect(self.update_counters)
                
                # Conectar botones con métodos del handler
                self.llamada_btn.clicked.connect(
                    lambda: self.call_handler.start_single_call(
                        self.from_number.text(),
                        self.to_number.text()
                    )
                )
                
                self.metralleta_btn.clicked.connect(
                    lambda: self.call_handler.start_call_burst(
                        self.interval_spin.value(),
                        self.max_calls_spin.value()
                    )
                )
                
                self.stop_metralleta_btn.clicked.connect(self.call_handler.stop_call_burst)
                
                self.bye_btn.clicked.connect(
                    lambda: self.call_handler.terminate_all_calls(0.5)
                )
                
                print("Debug: Call handler configurado correctamente")
                
        except Exception as e:
            print(f"Error al configurar call handler: {str(e)}\n", 
                "Trace:", traceback.format_exc())

    def update_call_status(self, call_id: str, status: str):
        """Actualiza el estado de una llamada en la interfaz."""
        try:
            row = self.calls_table.rowCount()
            self.calls_table.insertRow(row)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            items = [
                QTableWidgetItem(timestamp),
                QTableWidgetItem(call_id),
                QTableWidgetItem(status),
                QTableWidgetItem("Saliente"),
                QTableWidgetItem("-"),
                QTableWidgetItem("-")
            ]
            
            for col, item in enumerate(items):
                self.calls_table.setItem(row, col, item)
                
        except Exception as e:
            print(f"Error actualizando estado de llamada: {e}")

    def update_counters(self, active: int, failed: int, total: int):
        """
        Actualiza los contadores en la interfaz.
        
        Args:
            active: Número de llamadas activas
            failed: Número de llamadas fallidas
            total: Número total de llamadas
        """
        try:
            self.active_calls.setText(f"Activas: {active}")
            self.failed_calls.setText(f"Fallidas: {failed}")
            self.total_calls.setText(f"Total: {total}")
        except Exception as e:
            print(f"Error actualizando contadores: {e}")

    def add_call_to_table(self, call_id: str, timestamp: str, status: str, 
                        direction: str, from_uri: str, to_uri: str):
        """
        Añade una nueva llamada a la tabla de monitoreo.
        
        Args:
            call_id: Identificador único de la llamada
            timestamp: Marca de tiempo
            status: Estado de la llamada
            direction: Dirección (entrante/saliente)
            from_uri: URI de origen
            to_uri: URI de destino
        """
        try:
            row = self.calls_table.rowCount()
            self.calls_table.insertRow(row)
            
            items = [
                QTableWidgetItem(timestamp),
                QTableWidgetItem(call_id),
                QTableWidgetItem(status),
                QTableWidgetItem(direction),
                QTableWidgetItem(from_uri),
                QTableWidgetItem(to_uri)
            ]
            
            for col, item in enumerate(items):
                self.calls_table.setItem(row, col, item)
                
        except Exception as e:
            print(f"Error añadiendo llamada a la tabla: {e}")

    def update_call_in_table(self, call_id: str, status: str):
        """
        Actualiza el estado de una llamada existente en la tabla.
        
        Args:
            call_id: Identificador de la llamada
            status: Nuevo estado
        """
        try:
            for row in range(self.calls_table.rowCount()):
                if self.calls_table.item(row, 1).text() == call_id:
                    self.calls_table.item(row, 2).setText(status)
                    break
        except Exception as e:
            print(f"Error actualizando estado en tabla: {e}")


    def handle_single_call(self):
        """Maneja una llamada individual saliente."""
        try:
            from_number = self.from_number.text().strip()
            to_number = self.to_number.text().strip()
            
            if not self._validate_numbers(from_number, to_number):
                self.log_message.emit("Error: Números no válidos")
                return
                
            if self.sipp_controller.start_call(from_number, to_number):
                self._add_call_to_monitor(
                    direction="saliente",
                    from_uri=from_number,
                    to_uri=to_number,
                    state="iniciando"
                )
                self.log_message.emit(f"Llamada iniciada: {from_number} -> {to_number}")
            else:
                self.log_message.emit("Error al iniciar llamada")
                
        except Exception as e:
            self.log_message.emit(f"Error en llamada: {str(e)}")

    def handle_incoming_call(self, invite_message):
        """Maneja una llamada entrante."""
        try:
            # Extraer información del INVITE
            from_uri = self._extract_header(invite_message, "From")
            to_uri = self._extract_header(invite_message, "To")
            call_id = self._extract_header(invite_message, "Call-ID")
            
            # Verificar límite de llamadas
            if self.active_calls >= int(self.max_incoming_spin.value()):
                self.log_message.emit(f"Llamada rechazada (límite alcanzado): {from_uri}")
                return
                
            # Registrar la llamada
            self._add_call_to_monitor(
                direction="entrante",
                from_uri=from_uri,
                to_uri=to_uri,
                state="recibida",
                call_id=call_id
            )
            
            self.log_message.emit(f"Llamada entrante de {from_uri}")
            
        except Exception as e:
            self.log_message.emit(f"Error procesando llamada entrante: {str(e)}")

    def cleanup(self):
        """Limpia recursos antes de cerrar el panel."""
        try:
            # Limpiar tabla
            self.calls_table.setRowCount(0)
            # Resetear contadores
            self.update_counters(0, 0, 0)
            print("Debug: CallControlPanel cleanup completado")
        except Exception as e:
            print(f"Error durante cleanup de CallControlPanel: {e}")