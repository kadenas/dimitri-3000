from PyQt6.QtGui import QColor, QPalette, QFont, QFontDatabase

class RetroCyberTheme:
    """Tema retro-moderno con elementos cyberpunk mejorados"""
    
    # Paleta de colores
    PRIMARY = "#00FF9F"    # Verde neón brillante
    SECONDARY = "#FF0090"  # Rosa neón
    BACKGROUND = "#0A0A12" # Negro azulado oscuro
    FOREGROUND = "#E0E0FF" # Texto principal claro
    SURFACE = "#1A1A2F"    # Superficie oscura con tono azul
    ERROR = "#FF003C"      # Rojo neón para alertas
    HIGHLIGHT = PRIMARY    # Alias para consistencia
    BORDER = PRIMARY       # Borde principal

    # Parámetros de diseño
    BORDER_RADIUS = "4px"
    BORDER_WIDTH = "2px"
    GLOW_EFFECT = "0 0 8px {color}"

    @classmethod
    def get_palette(cls) -> QPalette:
        """Retorna la paleta de colores cyberpunk"""
        palette = QPalette()
        
        # Roles base
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.FOREGROUND))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.FOREGROUND))
        
        # Roles interactivos
        palette.setColor(QPalette.ColorRole.Highlight, QColor(cls.PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(cls.SURFACE))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(cls.PRIMARY))
        
        # Roles de estado
        palette.setColor(QPalette.ColorRole.Base, QColor(cls.SURFACE))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#252542"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(cls.BACKGROUND))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(cls.PRIMARY))
        
        return palette

    @classmethod
    def get_font(cls) -> QFont:
        """Configura la fuente cyberpunk con fallbacks seguros"""
        font_preferences = [
            "Roboto Mono",
            "DejaVu Sans Mono",
            "Consolas",
            "Courier New",
            "Monospace"
        ]
        
        # Obtener todas las fuentes disponibles
        available_families = QFontDatabase.families()  # <-- Método correcto
        
        # Tamaño y peso configurable
        font_size = 12
        font_weight = QFont.Weight.Normal

        for font_name in font_preferences:
            if font_name in available_families:  # <-- Verificación directa
                font = QFont(font_name, font_size, font_weight)
                font.setStyleHint(QFont.StyleHint.TypeWriter)
                return font

        # Fallback ultra seguro
        fallback_font = QFont()
        fallback_font.setStyleHint(QFont.StyleHint.Monospace)
        fallback_font.setPointSize(font_size)
        return fallback_font

    @classmethod
    def get_stylesheet(cls) -> str:
        """Retorna los estilos QSS completos"""
        return f"""
            /* Estilos generales */
            QWidget {{
                background-color: {cls.BACKGROUND};
                color: {cls.FOREGROUND};
                selection-background-color: {cls.PRIMARY};
                selection-color: {cls.BACKGROUND};
                font-family: "{cls.get_font().family()}";
            }}

            /* Grupos y paneles */
            QGroupBox {{
                border: {cls.BORDER_WIDTH} solid {cls.PRIMARY};
                border-radius: {cls.BORDER_RADIUS};
                margin-top: 1.5em;
                padding-top: 12px;
            }}

            QGroupBox::title {{
                color: {cls.SECONDARY};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}

            /* Elementos de entrada */
            QLineEdit, QTextEdit, QComboBox, QSpinBox {{
                background: {cls.SURFACE};
                border: {cls.BORDER_WIDTH} solid {cls.PRIMARY};
                border-radius: {cls.BORDER_RADIUS};
                padding: 5px 8px;
                selection-background-color: {cls.PRIMARY};
            }}

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border-color: {cls.SECONDARY};
                border: {cls.BORDER_WIDTH} solid {cls.SECONDARY};
            }}

            /* Botones */
            QPushButton {{
                background: {cls.SURFACE};
                border: {cls.BORDER_WIDTH} solid {cls.PRIMARY};
                border-radius: {cls.BORDER_RADIUS};
                color: {cls.PRIMARY};
                padding: 8px 20px;
                min-width: 100px;
            }}

            QPushButton:hover {{
                background: {cls.PRIMARY}33;
                border-color: {cls.SECONDARY};
            }}

            QPushButton:pressed {{
                background: {cls.PRIMARY};
                color: {cls.BACKGROUND};
            }}

            /* Pestañas */
            QTabWidget::pane {{
                border: {cls.BORDER_WIDTH} solid {cls.PRIMARY};
                border-radius: {cls.BORDER_RADIUS};
                margin-top: -1px;
            }}

            QTabBar::tab {{
                background: {cls.SURFACE};
                border: {cls.BORDER_WIDTH} solid {cls.PRIMARY};
                border-bottom: none;
                border-top-left-radius: {cls.BORDER_RADIUS};
                border-top-right-radius: {cls.BORDER_RADIUS};
                color: {cls.PRIMARY};
                padding: 8px 20px;
                margin-right: 2px;
            }}

            QTabBar::tab:selected {{
                background: {cls.BACKGROUND};
                color: {cls.SECONDARY};
            }}

            /* Barra de estado */
            QStatusBar {{
                border-top: 2px solid {cls.PRIMARY};
                color: {cls.FOREGROUND};
                font-size: 12px;
            }}

            /* Terminal personalizada */
            TerminalWidget {{
                border: 2px solid {cls.SECONDARY};
                border-radius: {cls.BORDER_RADIUS};
                font-family: "Roboto Mono";
            }}

            /* LED Indicator */
            LedIndicator {{
                qproperty-onColor: {cls.PRIMARY};
                qproperty-offColor: {cls.SURFACE};
                qproperty-borderColor: {cls.PRIMARY};
            }}

            /* Mensajes de error */
            QMessageBox {{
                background: {cls.BACKGROUND};
            }}

            QMessageBox QLabel {{
                color: {cls.FOREGROUND};
            }}
        """