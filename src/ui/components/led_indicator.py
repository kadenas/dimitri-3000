from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QRadialGradient)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty, QTimer
from src.ui.themes.cyber_theme import RetroCyberTheme

class LedIndicator(QWidget):
   def __init__(self, parent=None):
       super().__init__(parent)
       self._on_color = QColor(RetroCyberTheme.PRIMARY)
       self._off_color = QColor(RetroCyberTheme.SURFACE)
       self._border_color = QColor(RetroCyberTheme.PRIMARY)
       self._active = False
       self._blink = False
       self._opacity = 1.0
       self._timer = QTimer()
       self._timer.timeout.connect(self._update_blink)
       self.setFixedSize(16, 16)
       
       self._blink_animation = QPropertyAnimation(self, b"opacity")
       self._blink_animation.setDuration(1000)
       self._blink_animation.setStartValue(1.0)
       self._blink_animation.setEndValue(0.3)
       self._blink_animation.finished.connect(self._reset_blink)

   @pyqtProperty(float)
   def opacity(self):
       return self._opacity

   @opacity.setter
   def opacity(self, value):
       self._opacity = value
       self.update()

   def _reset_blink(self):
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

   def setActive(self, active: bool, blink: bool = False):
       self._active = active
       self._blink = blink
       if blink and active:
           self._timer.start(500)
       else:
           self._timer.stop()
       self.update()

   def _update_blink(self):
       self.opacity = 0.3 if self.opacity == 1.0 else 1.0

   def sizeHint(self) -> QSize:
       return QSize(24, 24)

   def paintEvent(self, event):
       painter = QPainter(self)
       painter.setRenderHint(QPainter.RenderHint.Antialiasing)
       painter.setOpacity(self._opacity)

       size = int(min(self.width(), self.height()) - 4)
       x = int((self.width() - size) / 2)
       y = int((self.height() - size) / 2)

       base_color = self._on_color if self._active else self._off_color
       glow_color = base_color.lighter(150) if self._active else self._border_color

       painter.setPen(QPen(glow_color, 2))
       painter.setBrush(Qt.BrushStyle.NoBrush)
       painter.drawEllipse(x, y, size, size)

       gradient = QRadialGradient(x + size/2, y + size/2, size/2)
       gradient.setColorAt(0.0, base_color.lighter(200))
       gradient.setColorAt(0.7, base_color)
       gradient.setColorAt(1.0, base_color.darker(200))

       painter.setPen(Qt.PenStyle.NoPen)
       painter.setBrush(QBrush(gradient))
       painter.drawEllipse(x + 2, y + 2, size - 4, size - 4)

       if self._active:
           painter.setBrush(QBrush(glow_color))
           painter.setOpacity(0.4 * self._opacity)
           painter.drawEllipse(int(x + size/3), int(y + size/3), int(size/3), int(size/3))
       
       painter.end()