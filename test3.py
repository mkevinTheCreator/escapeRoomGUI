from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QRadialGradient, QBrush, QFontDatabase
from PySide6.QtCore import Qt, QRectF
import sys

class RadiantGlowLabel(QLabel):

    def __init__(self, text="", parent=None):
        QFontDatabase.addApplicationFont("fonts/Geostar-Regular.ttf")
        super().__init__(text, parent)
        self.setFont(QFont("Geostar", 50, QFont.Bold))
        self.glow_color = QColor(0, 200, 255)  # Base glow color
        self.glow_radius = 120                  # Smaller radius -> tighter glow
        self.text_opacity = 1.0
        self.steps = 20                          # More steps for smoother glow
        self.bg_opacity = 100                     # stronger background glow

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # --- Soft radial background glow (tighter) ---
        bg_gradient = QRadialGradient(rect.center(), self.glow_radius)
        bg_gradient.setColorAt(0.0, QColor(self.glow_color.red(), self.glow_color.green(),
                                           self.glow_color.blue(), self.bg_opacity))
        bg_gradient.setColorAt(1.0, QColor(self.glow_color.red(), self.glow_color.green(),
                                           self.glow_color.blue(), 0))
        painter.setBrush(QBrush(bg_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        # --- Multi-layer glowing text (tighter glow) ---
        for i in range(self.steps, 0, -1):
            alpha = int(15 * i)                   # Fading glow
            pen = QPen(QColor(self.glow_color.red(), self.glow_color.green(),
                               self.glow_color.blue(), alpha))
            pen.setWidth(i)                        # narrower for tighter glow
            painter.setPen(pen)
            painter.setFont(self.font())
            painter.drawText(rect, Qt.AlignCenter, self.text())

        # --- Main text on top ---
        painter.setPen(QPen(QColor(255, 255, 255, int(255 * self.text_opacity)), 1))
        painter.drawText(rect, Qt.AlignCenter, self.text())

# Preview window
class PreviewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tighter Radiant Glow Text Preview")
        layout = QVBoxLayout()

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setSpacing(40)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Blue tight glow
        blue_glow = RadiantGlowLabel("Bright Blue Glow")
        blue_glow.glow_color = QColor(0, 200, 255)
        scroll_layout.addWidget(blue_glow)

        # Pink tight glow
        pink_glow = RadiantGlowLabel("Bright Pink Glow")
        pink_glow.glow_color = QColor(255, 0, 200)
        scroll_layout.addWidget(pink_glow)

        # Green tight glow
        green_glow = RadiantGlowLabel("Bright Green Glow")
        green_glow.glow_color = QColor(0, 255, 100)
        scroll_layout.addWidget(green_glow)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_container)
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.resize(1000, 700)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreviewWindow()
    window.show()
    sys.exit(app.exec())
