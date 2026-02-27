from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QFont, QPen
from PySide6.QtCore import Qt
import sys

# Base gradient label
class GradientLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0.0, QColor(255, 0, 200))
        gradient.setColorAt(1.0, QColor(0, 200, 255))

        painter.setFont(self.font())
        painter.setPen(QPen(gradient, 1))
        painter.drawText(rect, Qt.AlignCenter, self.text())

# Outline + fill gradient
class GradientOutlineLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Fill gradient
        fill = QLinearGradient(0, 0, 0, rect.height())
        fill.setColorAt(0, QColor(255, 255, 255))
        fill.setColorAt(1, QColor(160, 160, 160))

        # Outline gradient
        outline = QLinearGradient(0, 0, rect.width(), 0)
        outline.setColorAt(0, QColor(255, 0, 200))
        outline.setColorAt(1, QColor(0, 200, 255))

        painter.setFont(self.font())
        painter.setPen(QPen(outline, 4))
        painter.drawText(rect, Qt.AlignCenter, self.text())

        painter.setPen(QPen(fill, 1))
        painter.drawText(rect, Qt.AlignCenter, self.text())

# Neon / glow effect
class NeonLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Glow
        glow = QLinearGradient(0, 0, rect.width(), rect.height())
        glow.setColorAt(0, QColor(255, 0, 200))
        glow.setColorAt(1, QColor(0, 200, 255))

        painter.setFont(self.font())
        painter.setPen(QPen(glow, 6))
        painter.drawText(rect, Qt.AlignCenter, self.text())

        # Inner text
        painter.setPen(QPen(Qt.white, 2))
        painter.drawText(rect, Qt.AlignCenter, self.text())

# Main preview window
class PreviewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gradient Text Preview")
        layout = QVBoxLayout()

        font = QFont("Arial", 36, QFont.Bold)

        # Gradient label
        grad_label = GradientLabel("Gradient Text")
        grad_label.setFont(font)
        layout.addWidget(grad_label)

        # Gradient outline
        outline_label = GradientOutlineLabel("Gradient Outline")
        outline_label.setFont(font)
        layout.addWidget(outline_label)

        # Neon / glow
        neon_label = NeonLabel("Neon Glow")
        neon_label.setFont(font)
        layout.addWidget(neon_label)

        # Scroll area in case window is small
        container = QWidget()
        container.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.resize(800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreviewWindow()
    window.show()
    sys.exit(app.exec())
