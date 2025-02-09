from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QObject, pyqtSignal
from src.core.models import CallData, CallState

class CallState(Enum):
    INITIAL = "INITIAL"
    TRYING = "TRYING"
    RINGING = "RINGING"
    ESTABLISHED = "ESTABLISHED"
    FAILED = "FAILED"
    FINISHED = "FINISHED"

class CallMonitor(QObject):
    """Centraliza la lógica de monitoreo de llamadas"""
    
    call_updated = pyqtSignal(str, CallState)  # call_id, new_state
    stats_updated = pyqtSignal(int, int, int)  # active, failed, total

    STATE_COLORS = {
        CallState.INITIAL: "#FFFFFF",
        CallState.TRYING: "#FFFF00",
        CallState.RINGING: "#FFA500", 
        CallState.ESTABLISHED: "#00FF00",
        CallState.FAILED: "#FF0000",
        CallState.FINISHED: "#888888"
    }

    def __init__(self):
        super().__init__()
        self.active_calls = {}
        self.stats = {"active": 0, "failed": 0, "total": 0}

    def add_call(self, call_data: CallData):
        self.active_calls[call_data.call_id] = call_data
        self.stats["active"] += 1
        self.stats["total"] += 1
        self._emit_updates(call_data.call_id, call_data.state)

    def update_call_state(self, call_id: str, new_state: CallState):
        if call_id not in self.active_calls:
            return
            
        call = self.active_calls[call_id]
        old_state = call.state
        call.state = new_state
        
        if new_state in [CallState.FAILED, CallState.FINISHED]:
            self.stats["active"] -= 1
            if new_state == CallState.FAILED:
                self.stats["failed"] += 1
                
        self._emit_updates(call_id, new_state)

    def _emit_updates(self, call_id: str, state: CallState):
        self.call_updated.emit(call_id, state)
        self.stats_updated.emit(
            self.stats["active"],
            self.stats["failed"],
            self.stats["total"]
        )

class CallMonitorTable(QTableWidget):
    """Tabla mejorada para mostrar llamadas"""
    
    HEADERS = ["Start Time", "State", "From URI", "To URI", "Direction", "Duration"]

    def __init__(self, call_monitor: CallMonitor, parent=None):
        super().__init__(parent)
        self.call_monitor = call_monitor
        self.setup_table()
        self._connect_signals()

    def setup_table(self):
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #00FF00;
                gridline-color: #004400;
            }
            QHeaderView::section {
                background-color: #002200;
                color: #00FF00;
            }
        """)

    def _connect_signals(self):
        self.call_monitor.call_updated.connect(self._handle_call_update)

    def _handle_call_update(self, call_id: str, state: CallState):
        call = self.call_monitor.active_calls.get(call_id)
        if not call:
            return
            
        # Buscar fila existente o crear nueva
        row = self._find_call_row(call_id)
        if row == -1:
            row = self.rowCount()
            self.insertRow(row)
            
        self._update_row(row, call)