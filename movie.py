from PySide6.QtCore import QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QLabel


class movie(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(70, 70)
        movie = QMovie("media/textures/globe.gif")
        movie.setScaledSize(QSize(70, 70))
        movie.setSpeed(70)
        self.setMovie(movie)
        movie.start()
        self.move(300, 300)