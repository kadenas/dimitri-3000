from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCursor
from src.ui.themes.cyber_theme import RetroCyberTheme

class TerminalWidget(QTextEdit):
    """Widget que simula una terminal."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFont(RetroCyberTheme.get_font())
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {RetroCyberTheme.BACKGROUND};
                color: {RetroCyberTheme.FOREGROUND};
                border: 1px solid {RetroCyberTheme.HIGHLIGHT};
            }}
        """)
    
    def append_text(self, text: str):
        """Añade texto a la terminal."""
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText(f"\n{text}")
        self.moveCursor(QTextCursor.MoveOperation.End)