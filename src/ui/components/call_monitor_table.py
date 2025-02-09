from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from datetime import datetime

class CallMonitorTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
        
    def setup_table(self):
        headers = ["Start Time", "State", "From URI", "To URI", "Direction", "Duration"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configurar comportamiento de selección
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        self.state_colors = {
            "SETUP": "#FFFF00",
            "RINGING": "#FFA500",
            "CONNECTED": "#00FF00",
            "FAILED": "#FF0000",
            "FINISHED": "#888888"
        }
        
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

    def add_call(self, call_data):
        row = self.rowCount()
        self.insertRow(row)
        
        items = [
            QTableWidgetItem(call_data["timestamp"]),
            QTableWidgetItem(call_data["state"]),
            QTableWidgetItem(call_data["from_uri"]),
            QTableWidgetItem(call_data["to_uri"]),
            QTableWidgetItem(call_data["direction"]),
            QTableWidgetItem(call_data.get("duration", "-"))
        ]
        
        # Aplicar color según estado
        state_color = self.state_colors.get(call_data["state"], "#00FF00")
        for item in items:
            item.setForeground(QColor(state_color))
            
        for col, item in enumerate(items):
            self.setItem(row, col, item)