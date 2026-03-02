import math
from PySide6.QtGui import Qt, QColor, QFontDatabase, QFont, QPainter, QPen, QBrush
from PySide6.QtCore import QRectF, QPointF,Qt
from PySide6.QtWidgets import QDial


class CustomDial(QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.valueChanged.connect(self.update)

    def paintEvent(self, event):
        QFontDatabase.addApplicationFont("fonts/Geostar-Regular.ttf")
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Size calculations
        w, h = self.width(), self.height()
        side = min(w, h)
        center = QPointF(w / 2, h / 2)
        margin = side * 0.05
        outer_r = side / 2 - margin
        inner_r = outer_r * 0.65

        painter.translate(center)

        # Draw outer circle (black, only for labels)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(108, 128, 193)))


        painter.drawEllipse(QPointF(0, 0), outer_r-20, outer_r-20)
        # Draw tick marks slightly shorter, pushed outward
        tick_inner = inner_r + 5
        tick_outer = outer_r - 20
        painter.setPen(QPen(QColor(243, 178, 179), 1))
        for deg in range(0, 360, 4):
            rad = math.radians(deg)
            x1 = math.sin(rad) * tick_inner
            y1 = -math.cos(rad) * tick_inner
            x2 = math.sin(rad) * tick_outer
            y2 = -math.cos(rad) * tick_outer
            painter.drawLine(x1, y1, x2, y2)

        # Draw inner circle (black fill, white border)
        painter.setBrush(QBrush(QColor(27,32,36)))
        painter.setPen(QPen(QColor(108, 128, 193),15))
        painter.drawEllipse(QPointF(0, 0), inner_r, inner_r)

        # Draw central percentage text

        value = self.value()

        painter.setPen(QPen(QColor(229, 121, 27),4))
        angle_deg = (value - self.minimum()) / (self.maximum() - self.minimum()) * 360
        rad = math.radians(angle_deg)
        needle_len = tick_inner
        nx = math.sin(rad) * needle_len
        ny = -math.cos(rad) * needle_len
        nx2 = math.sin(rad) * (needle_len-14)
        ny2 = -math.cos(rad) * (needle_len-14)
        # Draw from one edge across center to opposite edge
        painter.drawLine(-nx , -ny ,  nx2, ny2)
        




        percent_text = f"{int(value)}%"
        font = QFont("Geostar",20)
        font.setPointSizeF(inner_r * 0.3)
        font.setBold(True)
        painter.setFont(font)
        metrics = painter.fontMetrics()
        text_w = metrics.horizontalAdvance(percent_text) + 5
        text_h = metrics.height()
        painter.setPen(QColor(243, 178, 179))
        painter.drawRect(-text_w / 2, -text_h / 2, text_w, text_h)
        painter.setPen(QColor(229, 121, 27))
        painter.drawText(QRectF(-text_w / 2, -text_h / 2, text_w, text_h),
                         Qt.AlignCenter, percent_text)

        # Draw numeric labels on outer circle

        painter.setPen(QPen(Qt.black))