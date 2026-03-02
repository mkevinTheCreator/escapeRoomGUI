from PySide6.QtGui import Qt, QColor, QPainter, QPen
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class FontGlowEffect:
    def __init__(self, label: QLabel, glow_color=QColor(0, 200, 255), steps=15, intensity=15):
        self.label = label
        self.glow_color = glow_color
        self.steps = steps          # Number of glow layers
        self.intensity = intensity  # Alpha multiplier
        # Replace the label's paintEvent with our custom one
        self.original_paint = label.paintEvent
        label.paintEvent = self._paint_with_glow

    def _paint_with_glow(self, event):
        painter = QPainter(self.label)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.label.rect()

        text = self.label.text()
        font = self.label.font()

        # Draw glow layers
        for i in range(self.steps, 0, -1):
            alpha = min(255, int(self.intensity * i))
            pen = QPen(QColor(self.glow_color.red(),
                               self.glow_color.green(),
                               self.glow_color.blue(), alpha))
            pen.setWidth(i)  # Wider stroke for outer glow
            painter.setPen(pen)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, text)

        # Draw the original text on top
        painter.setPen(QPen(self.label.palette().color(self.label.foregroundRole()), 1))
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, text)