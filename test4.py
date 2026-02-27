import sys
import math
from PySide6.QtWidgets import QApplication, QDial, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PySide6.QtCore import Qt, QRectF, QPointF

class CustomDial(QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.valueChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Size calculations
        w, h = self.width(), self.height()
        side = min(w, h)
        center = QPointF(w/2, h/2)
        margin = side * 0.05
        outer_r = side/2 - margin
        inner_r = outer_r * 0.65

        painter.translate(center)

        # Draw outer circle (black, only for labels)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), outer_r, outer_r)

        # Draw tick marks slightly shorter, pushed outward
        tick_inner = inner_r + 5
        tick_outer = outer_r - 5
        painter.setPen(QPen(Qt.black, 1))
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            x1 = math.sin(rad) * tick_inner
            y1 = -math.cos(rad) * tick_inner
            x2 = math.sin(rad) * tick_outer
            y2 = -math.cos(rad) * tick_outer
            painter.drawLine(x1, y1, x2, y2)

        # Draw inner circle (black fill, white border)
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawEllipse(QPointF(0, 0), inner_r, inner_r)

        # Draw central percentage text
        value = self.value()
        percent_text = f"{int(value)}%"
        font = painter.font()
        font.setPointSizeF(inner_r * 0.3)
        font.setBold(True)
        painter.setFont(font)
        metrics = painter.fontMetrics()
        text_w = metrics.horizontalAdvance(percent_text)
        text_h = metrics.height()
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(-text_w/2, -text_h/2, text_w, text_h),
                         Qt.AlignCenter, percent_text)

        # Draw numeric labels on outer circle
        labels = {0: "48", 120: "48", 180: "96", 240: "48"}
        painter.setPen(QPen(Qt.black))
        label_radius = outer_r + 10
        for angle, label in labels.items():
            rad = math.radians(angle)
            x = label_radius * math.sin(rad)
            y = -label_radius * math.cos(rad)
            lw = metrics.horizontalAdvance(label)
            lh = metrics.height()
            painter.drawText(QRectF(x - lw/2, y - lh/2, lw, lh),
                             Qt.AlignCenter, label)

        # Draw full-length needle (spans entire dial)
        painter.setPen(QPen(QColor(200, 200, 200), 3))
        angle_deg = (value - self.minimum()) / (self.maximum() - self.minimum()) * 360
        rad = math.radians(angle_deg)
        needle_len = outer_r
        nx = math.sin(rad) * needle_len
        ny = -math.cos(rad) * needle_len
        # Draw from one edge across center to opposite edge
        painter.drawLine(-nx, -ny, nx, ny)

class DialDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Dial Demo")
        layout = QVBoxLayout(self)
        self.dial = CustomDial(self)
        self.dial.setValue(50)
        layout.addWidget(self.dial)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DialDemo()
    demo.resize(300, 300)
    demo.show()
    sys.exit(app.exec())
