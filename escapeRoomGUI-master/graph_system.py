from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QFontDatabase, QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget


class graph_system(QWidget):
    mouse_pressed = Signal(float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(20, 122, 16))  # manual background

        w, h = self.width(), self.height()
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(0, 550, w, 550)
        painter.drawLine(w//2, 0, w//2, h)

        for n in range(50,700,100):
            painter.drawLine(w//2+25, n, w//2-25, n)

        for n in range(100,1800,100):
            painter.drawLine(n, 550+25, n,550-25)
        i = -700
        for n in range(100,1500,100):
            painter.drawText(QPoint(n-15, 590), str(i))
            i+=100
        i = 500
        for n in range(50,800,100):
            if i != 0:
                painter.drawText(QPoint(w//2-55, n+5), str(i))
            i-=100

        painter.setPen(QPen(Qt.black, 2))
        for n in range(50,700,50):
            painter.drawLine(w//2+15, n, w//2-15, n)

        for n in range(50,1800,50):
            painter.drawLine(n, 550+15, n,550-15)



    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.mouse_pressed.emit(pos.x(), pos.y())#




