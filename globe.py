from PySide6.QtCore import Signal
from PySide6.QtGui import QFontDatabase, QPainter, QPen, Qt, QColor, QMovie
from PySide6.QtWidgets import QWidget


class globe(QMovie):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start()
        self.setFileName("media/textures/globe.gif")

