from PyQt6.QtWidgets import QStyleFactory, QProxyStyle
from PyQt6.QtGui import QPalette
from src.ui.themes.cyber_theme import RetroCyberTheme  # Importación correcta

class RetroStyle(QProxyStyle):
    """Estilo personalizado para widgets."""
    
    def __init__(self):
        super().__init__(QStyleFactory.create("Fusion"))
        # Usar RetroCyberTheme en lugar de RetroTheme
        self._palette = RetroCyberTheme.get_palette()
    
    def polish(self, widget_or_palette):
        """Aplica el estilo cyberpunk a los widgets o paletas."""
        if isinstance(widget_or_palette, QPalette):
            return self._palette
            
        if hasattr(widget_or_palette, 'setFont'):
            # Usar el método del nuevo tema
            widget_or_palette.setFont(RetroCyberTheme.get_font())
        
        return super().polish(widget_or_palette)

    def standardPalette(self) -> QPalette:
        """Retorna la paleta estándar para este estilo."""
        return self._palette