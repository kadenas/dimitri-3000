from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, 
                        QRadialGradient)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty
from src.ui.themes.cyber_theme import RetroCyberTheme

class LedIndicator(QWidget):
    """Indicador LED cyberpunk con soporte para temas dinámicos y animaciones"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración inicial con valores del tema
        self._on_color = QColor(RetroCyberTheme.PRIMARY)
        self._off_color = QColor(RetroCyberTheme.SURFACE)
        self._border_color = QColor(RetroCyberTheme.PRIMARY)
        self._active = False
        self._blink = False
        self._opacity = 1.0  # Valor inicial de opacidad

        # Configurar animación de parpadeo
        self._blink_animation = QPropertyAnimation(self, b"opacity")
        self._blink_animation.setDuration(1000)
        self._blink_animation.setStartValue(1.0)
        self._blink_animation.setEndValue(0.3)
        self._blink_animation.finished.connect(self._reset_blink)

    # Propiedad opacity para la animación
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()

    def _reset_blink(self):
        """Restablece la opacidad al finalizar la animación"""
        if self._blink:
            self._blink_animation.start()

    @pyqtProperty(QColor)
    def onColor(self):
        return self._on_color

    @onColor.setter
    def onColor(self, color):
        self._on_color = QColor(color)
        self.update()

    @pyqtProperty(QColor)
    def offColor(self):
        return self._off_color

    @offColor.setter
    def offColor(self, color):
        self._off_color = QColor(color)
        self.update()

    @pyqtProperty(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, color):
        self._border_color = QColor(color)
        self.update()

    def setActive(self, active: bool):
        """Establece el estado activo/inactivo del LED"""
        if self._active != active:
            self._active = active
            self.update()
            if self._blink:
                self.toggle_blink(active)

    def toggle_blink(self, enable: bool):
        """Activa/desactiva el efecto de parpadeo"""
        self._blink = enable
        if enable:
            self._blink_animation.start()
        else:
            self._blink_animation.stop()
            self.opacity = 1.0  # Restablecer opacidad

    def sizeHint(self) -> QSize:
        """Tamaño preferido del widget"""
        return QSize(24, 24)

    def paintEvent(self, event):
        """Renderizado personalizado del LED"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity)  # Usar la propiedad de opacidad

        # Tamaño dinámico basado en las dimensiones del widget
        size = min(self.width(), self.height()) - 4
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2

        # Configuración de colores según el estado
        base_color = self._on_color if self._active else self._off_color
        glow_color = base_color.lighter(150) if self._active else self._border_color

        # Dibujar borde neón
        painter.setPen(QPen(glow_color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(x, y, size, size)

        # Gradiente radial para efecto 3D
        gradient = QRadialGradient(x + size/2, y + size/2, size/2)
        gradient.setColorAt(0.0, base_color.lighter(200))
        gradient.setColorAt(0.7, base_color)
        gradient.setColorAt(1.0, base_color.darker(200))

        # Dibujar cuerpo principal del LED
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(x + 2, y + 2, size - 4, size - 4)

        # Efecto de brillo central
        if self._active:
            painter.setBrush(QBrush(glow_color))
            painter.setOpacity(0.4 * self._opacity)  # Combinar con opacidad de animación
            painter.drawEllipse(x + size/3, y + size/3, size/3, size/3)