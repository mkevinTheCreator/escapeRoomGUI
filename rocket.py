from PySide6.QtCore import QPoint, QTimer
from PySide6.QtGui import QPainter, QColor, QImage, QPixmap, Qt
from PySide6.QtWidgets import QWidget


class Rocket(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(75, 75)
        self.angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)  # ~60fps

    def rotate(self):
        self.angle = (self.angle + 2) % 360
        self.update()  # triggers paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("media/textures/rocket.png").scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.drawPixmap(-pixmap.width() // 2, -pixmap.height() // 2, pixmap)