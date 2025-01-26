from PyQt6.QtGui import QColor, QPalette, QFont

class RetroTheme:
    """Tema retro estilo terminal con soporte completo"""
    
    # Colores
    BACKGROUND = "#000000"  # Negro
    FOREGROUND = "#00FF00"  # Verde
    HIGHLIGHT = "#00AA00"   # Verde oscuro
    BORDER = "#004400"      # Borde verde

    @classmethod
    def get_palette(cls) -> QPalette:
        """Retorna la paleta de colores retro"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.FOREGROUND))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.FOREGROUND))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(cls.HIGHLIGHT))
        return palette

    @classmethod
    def get_font(cls) -> QFont:
        """Fuente estilo terminal"""
        return QFont("Courier New", 10)

    @classmethod
    def get_stylesheet(cls) -> str:  # <-- ¡Método faltante!
        """Estilos QSS para componentes específicos"""
        return f"""
            QStatusBar {{
                border-top: 2px solid {cls.HIGHLIGHT};
                color: {cls.FOREGROUND};
                font-family: "Courier New";
            }}
            QTabBar::tab {{
                background: {cls.BACKGROUND};
                border: 1px solid {cls.HIGHLIGHT};
                color: {cls.FOREGROUND};
                padding: 5px;
            }}
        """