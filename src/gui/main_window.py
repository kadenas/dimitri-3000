from ..core.logger import logger
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Inicializar componentes
        self._setup_components()
        # Conectar señales
        self._setup_connections()
        
    def _setup_components(self):
        """Configura los componentes iniciales."""
        # Crear y configurar el call handler
        config = {
            'local_ip': '192.168.0.137',  # Asegúrate de que esta IP es correcta
            'local_port': 5060,
            'remote_ip': '192.168.0.133',  # Asegúrate de que esta IP es correcta
            'remote_port': 5060,
            'transport': 'UDP'
        }
        self.call_handler = SIPCallHandler(config)
        
        # Configurar valores por defecto
        self.ui.txtIntervalo.setText("1")
        self.ui.txtMaxLlamadas.setText("10")
        
        # Deshabilitar botones inicialmente
        self.ui.btnStopMetralleta.setEnabled(False)
        self.ui.btnBye.setEnabled(False)

        # Añadir botón para ver logs
        self.ui.btnVerLogs = QPushButton("Ver Logs", self)
        self.ui.verticalLayout.addWidget(self.ui.btnVerLogs)
        self.ui.btnVerLogs.clicked.connect(self._show_logs)

    def _setup_connections(self):
        """Configura las conexiones de señales y slots."""
        # Conexiones existentes
        self.ui.btnLlamada.clicked.connect(self._handle_single_call)
        self.ui.chkOptions.stateChanged.connect(self._handle_options_toggle)
        self.ui.btnServidor.clicked.connect(self._handle_server_toggle)
        
        # Conexiones para metralleta y BYE
        self.ui.btnMetralleta.clicked.connect(self._handle_burst_start)
        self.ui.btnStopMetralleta.clicked.connect(self._handle_burst_stop)
        self.ui.btnBye.clicked.connect(self._handle_terminate_all)

    def _handle_burst_start(self):
        """Maneja el inicio de la ráfaga de llamadas."""
        try:
            interval = int(self.ui.txtIntervalo.text())
            max_calls = int(self.ui.txtMaxLlamadas.text())
            
            if interval <= 0 or max_calls <= 0:
                QMessageBox.warning(self, "Error", "El intervalo y máximo de llamadas deben ser mayores a 0")
                return
                
            logger.debug(f"Iniciando ráfaga: intervalo={interval}s, max={max_calls}")
            self.call_handler.start_call_burst(interval, max_calls)
            
            # Actualizar estado de botones
            self.ui.btnMetralleta.setEnabled(False)
            self.ui.btnStopMetralleta.setEnabled(True)
            self.ui.btnBye.setEnabled(True)
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error iniciando ráfaga: {str(e)}")

    def _handle_burst_stop(self):
        """Maneja la detención de la ráfaga de llamadas."""
        try:
            logger.debug("Deteniendo ráfaga de llamadas")
            self.call_handler.stop_call_burst()
            
            # Actualizar estado de botones
            self.ui.btnMetralleta.setEnabled(True)
            self.ui.btnStopMetralleta.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error deteniendo ráfaga: {str(e)}")

    def _handle_terminate_all(self):
        """Maneja la terminación de todas las llamadas."""
        try:
            logger.debug("Terminando todas las llamadas")
            self.call_handler.terminate_all_calls()
            
            # Actualizar estado de botones
            self.ui.btnMetralleta.setEnabled(True)
            self.ui.btnStopMetralleta.setEnabled(False)
            self.ui.btnBye.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error terminando llamadas: {str(e)}")

    def _handle_single_call(self):
        """Maneja una llamada individual."""
        try:
            from_uri = self.ui.txtOrigen.text() or "1001"
            to_uri = self.ui.txtDestino.text() or "2001"
            
            logger.info(f"Iniciando llamada: {from_uri} -> {to_uri}")
            logger.debug(f"Estado del call handler: {self.call_handler}")
            
            if self.call_handler.start_single_call(from_uri, to_uri):
                logger.info("Llamada iniciada correctamente")
            else:
                logger.error("Error iniciando llamada")
                QMessageBox.warning(self, "Error", "No se pudo iniciar la llamada")
                
        except Exception as e:
            logger.error(f"Error en llamada individual: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def _show_logs(self):
        """Muestra los logs en una ventana."""
        try:
            log_file = Path.home() / '.pysipp' / 'logs' / 'pysipp.log'
            if log_file.exists():
                with open(log_file) as f:
                    logs = f.read()
                    
                dialog = QDialog(self)
                dialog.setWindowTitle("Logs")
                layout = QVBoxLayout()
                
                text_edit = QTextEdit()
                text_edit.setPlainText(logs)
                text_edit.setReadOnly(True)
                
                layout.addWidget(text_edit)
                dialog.setLayout(layout)
                dialog.resize(800, 600)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "Archivo de logs no encontrado")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error mostrando logs: {str(e)}") 