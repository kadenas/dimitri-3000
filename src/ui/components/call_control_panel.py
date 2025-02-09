from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QPushButton, QSpinBox, QLabel, QTableWidget,
                           QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from datetime import datetime
import traceback  # Añadir esta línea
from src.core.sip_call_handler import SIPCallHandler  # Esta es la única que necesitamos
from src.ui.components.call_monitor_table import CallMonitorTable
from src.core.sip_monitor import SIPMonitor
import uuid
import time
from src.core.models import CallData, CallState
import logging

logger = logging.getLogger(__name__)

class CallControlPanel(QWidget):
    # Señales para comunicación con el controlador principal
    call_initiated = pyqtSignal(str, str)  # from_uri, to_uri
    burst_started = pyqtSignal(int, int)   # interval, max_calls
    burst_stopped = pyqtSignal()
    bye_all = pyqtSignal(float)            # bye_interval
    call_terminated = pyqtSignal(str)      # call_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._call_interval = 1
        self._max_calls = 1
        self._barrage_active = False
        self._barrage_timer = QTimer()
        self._barrage_timer.timeout.connect(self._on_barrage_timer)
        self._bye_timer = QTimer()
        self._bye_timer.timeout.connect(self._on_bye_timer)
        self.active_calls = {}
        
        # Inicializar UI
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Panel de Control
        control_panel = QGroupBox("Control de Llamadas")
        control_layout = QVBoxLayout()
        
        # Números y Botones
        numbers_layout = QHBoxLayout()
        self.from_number = QLineEdit("ej: 1001")
        self.to_number = QLineEdit("ej: 2001")
        numbers_layout.addWidget(QLabel("Número Origen:"))
        numbers_layout.addWidget(self.from_number)
        numbers_layout.addWidget(QLabel("Número Destino:"))
        numbers_layout.addWidget(self.to_number)
        
        # Botones
        buttons_layout = QHBoxLayout()
        self.llamada_btn = QPushButton("LLAMADA")
        self.llamada_btn.setObjectName("llamada_btn")
        
        # Conectar el botón de llamada de forma segura
        try:
            if self.llamada_btn.receivers(self.llamada_btn.clicked) > 0:
                self.llamada_btn.clicked.disconnect()
            self.llamada_btn.clicked.connect(self.on_call_button_clicked)
            logger.debug("Botón LLAMADA conectado a on_call_button_clicked")
        except Exception as e:
            logger.debug(f"No había conexiones previas para desconectar: {e}")
        
        self.metralleta_btn = QPushButton("METRALLETA")
        self.stop_metralleta_btn = QPushButton("Stop Metralleta")
        self.bye_btn = QPushButton("BYE")
        
        # Asegurarnos de que el botón de metralleta no interfiere
        self._barrage_active = False
        self._barrage_timer = QTimer()
        self._barrage_timer.timeout.connect(self._on_barrage_timer)
        
        for btn in [self.llamada_btn, self.metralleta_btn, 
                   self.stop_metralleta_btn, self.bye_btn]:
            buttons_layout.addWidget(btn)
        
        # Conectar el botón BYE de forma segura
        try:
            if self.bye_btn.receivers(self.bye_btn.clicked) > 0:
                self.bye_btn.clicked.disconnect()
            self.bye_btn.clicked.connect(self.on_bye_button_clicked)
            logger.debug("Botón BYE conectado")
        except Exception as e:
            logger.debug(f"No había conexiones previas para BYE: {e}")
        
        # Configuración
        config_layout = QHBoxLayout()
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)
        self.interval_spin.setValue(1)
        self.max_calls_spin = QSpinBox()
        self.max_calls_spin.setRange(1, 1000)
        self.max_calls_spin.setValue(1)
        
        config_layout.addWidget(QLabel("Intervalo (seg):"))
        config_layout.addWidget(self.interval_spin)
        config_layout.addWidget(QLabel("Max. Llamadas:"))
        config_layout.addWidget(self.max_calls_spin)
        
        # Monitor de Llamadas
        monitor_panel = QGroupBox("Monitor de Llamadas")
        monitor_layout = QVBoxLayout()
        
        # Tabla de llamadas
        self.calls_table = QTableWidget()
        self.calls_table.setColumnCount(6)
        headers = ["Hora", "Call-ID", "Estado", "Dirección", "Origen", "Destino"]
        self.calls_table.setHorizontalHeaderLabels(headers)
        
        # Contadores
        counters_layout = QHBoxLayout()
        self.active_calls_label = QLabel("Activas: 0")
        self.failed_calls_label = QLabel("Fallidas: 0")
        self.total_calls_label = QLabel("Total: 0")
        
        counters_layout.addWidget(self.active_calls_label)
        counters_layout.addWidget(self.failed_calls_label)
        counters_layout.addWidget(self.total_calls_label)
        
        # Añadir todo al layout
        control_layout.addLayout(numbers_layout)
        control_layout.addLayout(buttons_layout)
        control_layout.addLayout(config_layout)
        control_panel.setLayout(control_layout)
        
        monitor_layout.addWidget(self.calls_table)
        monitor_layout.addLayout(counters_layout)
        monitor_panel.setLayout(monitor_layout)
        
        layout.addWidget(control_panel)
        layout.addWidget(monitor_panel)

        # Conectar señales de los botones
        self.llamada_btn.clicked.connect(self.on_call_button_clicked)
        self.metralleta_btn.clicked.connect(self.start_barrage)
        self.stop_metralleta_btn.clicked.connect(self.stop_barrage)
        self.bye_btn.clicked.connect(self.on_bye_button_clicked)
        
        # Configurar estado inicial de botones
        self.stop_metralleta_btn.setEnabled(False)
        self.bye_btn.setEnabled(False)

    def set_sipp_controller(self, controller):
        """Establece el controlador SIPP"""
        self.sipp_controller = controller

    def on_call_button_clicked(self):
        """Maneja el click en el botón de llamada."""
        try:
            from_uri = self.from_number.text().strip()
            to_uri = self.to_number.text().strip()
            
            if not from_uri or not to_uri:
                QMessageBox.warning(self, "Error", "Debe especificar origen y destino")
                return
            
            if self.call_handler:
                # Verificar si ya existe una llamada activa con estos URIs
                for call in self.call_handler.active_calls.values():
                    if (call.from_uri == from_uri and call.to_uri == to_uri and 
                        call.state not in [CallState.TERMINATED.value, CallState.FAILED.value]):
                        QMessageBox.warning(self, "Error", "Ya existe una llamada activa con estos números")
                        return
                
                logger.debug(f"Iniciando llamada única: {from_uri} -> {to_uri}")
                self.llamada_btn.setEnabled(False)  # Deshabilitar después de validaciones
                
                success = self.call_handler.start_single_call(from_uri, to_uri)
                if not success:
                    QMessageBox.warning(self, "Error", "No se pudo iniciar la llamada")
            
            else:
                logger.error("Call handler no inicializado")
                QMessageBox.warning(self, "Error", "Sistema no inicializado")
            
        except Exception as e:
            logger.error(f"Error al iniciar llamada: {e}")
            QMessageBox.critical(self, "Error", f"Error al iniciar llamada: {str(e)}")
        finally:
            QTimer.singleShot(2000, lambda: self.llamada_btn.setEnabled(True))

    def start_barrage(self):
        """Inicia el modo metralleta."""
        try:
            if not self._barrage_active:
                self._barrage_active = True
                interval = float(self.interval_spin.value())
                self._barrage_timer.start(int(interval * 1000))
                
                # Actualizar UI
                self.metralleta_btn.setEnabled(False)
                self.stop_metralleta_btn.setEnabled(True)
                self.llamada_btn.setEnabled(False)
                logger.debug(f"Modo metralleta iniciado (intervalo: {interval}s)")
                
        except Exception as e:
            logger.error(f"Error iniciando metralleta: {e}")
            self.stop_barrage()

    def stop_barrage(self):
        """Detiene el modo metralleta."""
        try:
            self._barrage_active = False
            self._barrage_timer.stop()
            
            # Restaurar UI
            self.metralleta_btn.setEnabled(True)
            self.stop_metralleta_btn.setEnabled(False)
            self.llamada_btn.setEnabled(True)
            logger.debug("Modo metralleta detenido")
            
        except Exception as e:
            logger.error(f"Error deteniendo metralleta: {e}")
        
    def start_bye_sequence(self):
        """Inicia la secuencia de BYE."""
        if self.active_calls:
            self._bye_timer.start(self._call_interval * 1000)
            logger.debug("Secuencia BYE iniciada")
            
    def _on_barrage_timer(self):
        """Manejador del timer de metralleta."""
        if len(self.active_calls) < self._max_calls:
            self.on_call_button_clicked()
        else:
            self.stop_barrage()
            
    def _on_bye_timer(self):
        """Manejador del timer de BYE."""
        if self.active_calls:
            # Obtener la llamada más antigua
            oldest_call_id = min(self.active_calls.keys(), 
                               key=lambda k: self.active_calls[k]['start_time'])
            self.call_terminated.emit(oldest_call_id)
            del self.active_calls[oldest_call_id]
        else:
            self._bye_timer.stop()
            
    def _update_interval(self, value):
        """Actualiza el intervalo entre llamadas."""
        self._call_interval = value
        
    def _update_max_calls(self, value):
        """Actualiza el máximo de llamadas simultáneas."""
        self._max_calls = value
        
    def _validate_uris(self, from_uri: str, to_uri: str) -> bool:
        """Valida las URIs de origen y destino."""
        return bool(from_uri and to_uri and from_uri != to_uri)

    def update_call_status(self, call_data: dict):
        """Actualiza el estado de una llamada en la tabla."""
        try:
            # Buscar si la llamada ya existe en la tabla
            call_id = call_data['call_id']
            row = -1
            for i in range(self.calls_table.rowCount()):
                if self.calls_table.item(i, 1).text() == call_id:
                    row = i
                    break
            
            # Si no existe, añadir nueva fila
            if row == -1:
                row = self.calls_table.rowCount()
                self.calls_table.insertRow(row)
            
            # Actualizar datos
            items = [
                QTableWidgetItem(call_data.get('start_time', datetime.now().strftime('%H:%M:%S'))),
                QTableWidgetItem(call_id),
                QTableWidgetItem(call_data['state']),
                QTableWidgetItem(call_data.get('direction', 'outbound')),
                QTableWidgetItem(call_data['from_uri']),
                QTableWidgetItem(call_data['to_uri'])
            ]
            
            for col, item in enumerate(items):
                self.calls_table.setItem(row, col, item)
                
        except Exception as e:
            logger.error(f"Error actualizando estado de llamada: {e}")

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
        """Establece el manejador de llamadas SIP."""
        try:
            logger.debug(f"Estableciendo call handler: {handler}")
            self.call_handler = handler
            
            if self.call_handler is not None:
                logger.debug("Call handler no es None")
                
                # Verificar el monitor en el call handler
                if not hasattr(self.call_handler, 'sip_monitor') or self.call_handler.sip_monitor is None:
                    logger.error("Call handler no tiene monitor configurado")
                    return
                
                # Establecer referencia local al monitor
                self._monitor_ref = self.call_handler.sip_monitor
                logger.debug(f"Referencia local al monitor establecida: {self._monitor_ref}")
                
                # Verificar que el monitor tiene configuración
                if not hasattr(self._monitor_ref, 'config'):
                    logger.error("Monitor no tiene configuración")
                    return
                
                logger.debug(f"Monitor config: {self._monitor_ref.config}")
                
                # Conectar señales del handler con los slots del panel
                self.call_handler.call_status_changed.connect(self.update_call_status)
                self.call_handler.call_stats_updated.connect(self.update_counters)
                
                logger.debug("Call handler y señales configurados correctamente")
                
        except Exception as e:
            logger.error(f"Error configurando call handler: {e}", exc_info=True)

    def update_counters(self, active: int, failed: int, total: int):
        """Actualiza los contadores en la interfaz."""
        try:
            self.active_calls_label.setText(f"Activas: {active}")
            self.failed_calls_label.setText(f"Fallidas: {failed}")
            self.total_calls_label.setText(f"Total: {total}")
        except Exception as e:
            logger.error(f"Error actualizando contadores: {e}")

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
        """Limpia recursos antes de cerrar."""
        try:
            # Detener timers
            if hasattr(self, '_barrage_timer'):
                self._barrage_timer.stop()
            if hasattr(self, '_bye_timer'):
                self._bye_timer.stop()
                
            # Limpiar tabla
            if hasattr(self, 'calls_table'):
                self.calls_table.setRowCount(0)
                
            # Resetear contadores
            if all(hasattr(self, attr) for attr in ['active_calls_label', 'failed_calls_label', 'total_calls_label']):
                self.update_counters(0, 0, 0)
                
            logger.debug("CallControlPanel cleanup completado")
        except Exception as e:
            logger.error(f"Error durante cleanup de CallControlPanel: {e}")

    def on_bye_button_clicked(self):
        """Maneja el click en el botón BYE."""
        try:
            if self.call_handler:
                self.bye_btn.setEnabled(False)
                self.call_handler.terminate_all_calls()
                logger.debug("BYE enviado para todas las llamadas activas")
        except Exception as e:
            logger.error(f"Error enviando BYE: {e}")
        finally:
            self.bye_btn.setEnabled(True)