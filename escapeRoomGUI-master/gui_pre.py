

class FontGlowEffect:
    """
    Apply a glow effect to any QLabel text.
    Usage:
        label = QLabel("Glowing Text")
        FontGlowEffect(label, glow_color=QColor(0,200,255), steps=15, intensity=15)
    """
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
        # Draw from one edge across center to opposite edge
        painter.drawLine(-nx , -ny ,  int(math.copysign((abs(nx)-10),nx)), (abs(ny)-10)* int(math.copysign(1,ny)))

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
from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRectF

class FadingProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(True)
        self.radius = 15
        self.bg_glow_color = QColor(46, 53, 81, 80)  # soft faded background glow

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # Draw fading box background
        painter.setBrush(QBrush(self.bg_glow_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, self.radius, self.radius)

        # Draw the chunk (filled portion)
        progress_width = int(rect.width() * (self.value() - self.minimum()) / (self.maximum() - self.minimum()))
        chunk_rect = QRectF(rect.x(), rect.y(), progress_width, rect.height())
        gradient_color = QColor(46, 83, 151)  # example gradient base color
        painter.setBrush(QBrush(gradient_color))
        painter.drawRoundedRect(chunk_rect, self.radius, self.radius)

        # Draw text on top
        painter.setPen(QPen(Qt.white))
        painter.drawText(rect, Qt.AlignCenter, f"{self.value()}%")



listOfValues = [0,0,0,0]
def sumForListValues(list:list):
    result = 0
    for i in list:       
        result += i
    return result
def checkEffects():
    if listOfValues[0] > 32 and sumForListValues(list=listOfValues) <= 100:
        print("aight")
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        QFontDatabase.addApplicationFont("fonts/Geostar-Regular.ttf")
        layout = QGridLayout()
        #self.showFullScreen()
        # --- 1. ADD THE HEADLINE ---
        headline = QLabel("Voltarium")
        headline.setStyleSheet("""
            QLabel{
                color: #E5791B;


            }
        """)
        headline_font = QFont("Geostar", 36)

        headline_font.setBold(True)
        headline.setFont(headline_font)
        headline.setAlignment(Qt.AlignCenter)
        FontGlowEffect(headline,glow_color=QColor(2,170,50),steps=25,intensity=15)
        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns
        layout.addWidget(headline, 0, 0, 1, 6)
        # ---------------------------

        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile("dial2.wav"))
        self.effect.setVolume(0.5)
        labels = ["Licht","platz","halter","platzhalter"]
       
        for i in range(1,5,1):
            # --- 1. CONTAINER BOX ---
            title = QLabel(labels[i-1])
            title.setAlignment(Qt.AlignLeft)

            titleFont = QFont("Geostar", 18)
            titleFont.setBold(True)
            title.setFont(titleFont)
            title.setFixedHeight(30)
            title.setStyleSheet("""
                QLabel {border: none;
                        color:#6C80C1;
                        background: transparent;
                        padding-bottom: 0px; 
                        padding-left: 24px;
                        height: 20px;
                   



            }""")

            # BOX
            box = QWidget()
            box.setMinimumWidth(350)
            boxLayout = QVBoxLayout(box)
            boxLayout.setSpacing(-4)

            boxLayout.setContentsMargins(0, 0, 0, 0)  # zero top margin

            box.setStyleSheet("""
                QWidget {
                    border-right: 3px solid #6C80C1;
                    border-left: 3px solid #6C80C1;
                    border-radius: 18px;
                }
            """)



            # --- ADD TO GRID ---



            # --- 2. LABEL (NO BOX) ---
            label = QLabel("0%")
            label.setAlignment(Qt.AlignCenter)
            font = QFont("Geostar", 36)

            font.setBold(True)

            FontGlowEffect(label,glow_color=QColor(229, 121, 27),steps=15,intensity=20)
            label.setFont(font)
            label.setFixedHeight(36)
            label.setContentsMargins(0,0,0,0)

            label.setStyleSheet("""
            QLabel { 
                    color: #E5791B;
                    padding: 0px;
                    border: none; 
                    margin: 0px;
            }""")

            # --- 3. PROGRESS BAR (UNCHANGED SIZE) ---
            # --- PROGRESS BAR: FIX SIZE + CORNERS ---
            progressBar = QProgressBar()
            progressBar.setOrientation(Qt.Orientation.Vertical)
            progressBar.setFixedSize((int)(box.width()/3.5), (int)(box.height()/1.1))  # restore height
            progressBar.setTextVisible(False)

            progressBar.setStyleSheet("""
            QProgressBar:vertical {
                border: 2px solid transparent;
                background-color: #2E3551;
                border-radius: 0px;
                
            

            }

            QProgressBar::chunk:vertical {
                background:
                    qlineargradient(
                        x1:0, y1:1, x2:0, y2:0,
                        stop:0 #ECA376,
                        stop:1 #F3B2B3);
                margin-bottom: 20px; 
                margin-left: 10px; 
                margin-right: 10px;
                box-shadow: 0px 0px 235px 31px rgba(243,178,179,0.9);
                border-radius: 20px; 
                
            }
            """)

            #

            # --- 4. DIAL ---
            dial2 = QDial()
            dial = CustomDial(dial2)

            dial.setRange(0, 100)
            dial.setSingleStep(1)
            dial.setFixedSize((int)(box.width()/2),(int)(box.width()/2))


            dial.valueChanged.connect(lambda v, l=label: l.setText(f"{v}%"))
            dial.valueChanged.connect(progressBar.setValue)
            dial.valueChanged.connect(lambda value, i=i-1: listOfValues.__setitem__(i, value))
            dial.valueChanged.connect(self.effect.play)
            dial.valueChanged.connect(checkEffects)

            # --- 5. PACK INTO BOX ---
            boxLayout.addWidget(label,0, alignment=Qt.AlignCenter)
            boxLayout.addWidget(progressBar,0, alignment=Qt.AlignCenter)
            boxLayout.addWidget(dial,0, alignment=Qt.AlignCenter)
            layout.setHorizontalSpacing(60)
            layout.setVerticalSpacing(0)
            layout.setContentsMargins(0,0,0,100)
            layout.addWidget(title, 1, i)  # row above
            # --- 6. ADD TO GRID ---
            layout.addWidget(box, 2, i, 3, 1)

        # Row 3
        container = QWidget()
        container.setObjectName("MainContainer")  # Give it a unique ID
        container.setLayout(layout)

        container.setStyleSheet("""
            #MainContainer {
                background-color: #1B2024;
            }
            QLabel {
                background-color: rgba(0, 0, 0, 0); /* Keep labels transparent */
                color: white;
            }
        """)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



