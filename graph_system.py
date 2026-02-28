from PySide6.QtCore import Signal
from PySide6.QtGui import QFontDatabase, QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget


class graph_system(QWidget):
    mouse_pressed = Signal(float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("white"))  # manual background

        w, h = self.width(), self.height()
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(0, h-h // 5, w,h- h //5)
        painter.drawLine(w//2, 0, w//2, h)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.mouse_pressed.emit(pos.x(), pos.y())