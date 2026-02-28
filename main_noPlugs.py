from rocket import Rocket
from graph_system import graph_system
from PySide6.QtGui import Qt, QColor, QFontDatabase, QFont, QShortcut, QKeySequence, QPainter, QPen, QMouseEvent, QMovie
from globe import globe
import sys
from PySide6.QtCore import QUrl, Qt, QTimer, Signal, QPoint, QSize
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget,
    QGridLayout, QDial, QProgressBar, QVBoxLayout, QStackedWidget,QPushButton, QSizePolicy)
from customDial import CustomDial
from fontGlowEffect import FontGlowEffect


listOfValues = [0,0,0,0]

def sumForListValues(list:list):
    result = 0
    for i in list:       
        result += i
    return result

def checkEffects():
    secondPuzzle = 3
    if listOfValues[0] == 32 and listOfValues[1] == 22 and listOfValues[2] == 22 and listOfValues[3] == 24:
        labelCheckingInput.setText("Correct Input")
        window.effectSolved.play()
        changeCurrentPage(secondPuzzle)
    elif listOfValues[0] > 31 and sumForListValues(list=listOfValues) <= 100:
        print("lamp on")
        labelCheckingInput.setText("Invalid Input")
    else:
        print("lamp off")
        labelCheckingInput.setText("Invalid Input")

def changeValue(value , i ):
    listOfValues[i] = value
    checkEffects()

def changeCurrentPage(page: int):
    window.changePageSignal.emit(page)
   
def changeSetuMessage(text:str):
    labelSetupScreen.setText(text)

labelCheckingInput:QLabel = None
labelSetupScreen:QLabel = None
stack = None





class MainWindow(QMainWindow):
    changePageSignal = Signal(int)
    def __init__(self):
        
        global stack
        global labelCheckingInput
        global labelSetupScreen
        labelCheckingInput = QLabel("Invalid Input")
        stack = QStackedWidget()
        super().__init__()
        self.changePageSignal.connect(stack.setCurrentIndex)
        self.setWindowTitle("My App")
        QFontDatabase.addApplicationFont("fonts/Geostar-Regular.ttf")
        layout = QGridLayout()
        #self.showFullScreen()
        # --- 1. ADD THE HEADLINE ---
        headline = QLabel("Wattarium")
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
        self.effect.setSource(QUrl.fromLocalFile("G:\\media\\sounds\\dial2.wav"))
        self.effect.setVolume(0.5)
        self.effectSolved = QSoundEffect()
        self.effectSolved.setSource(QUrl.fromLocalFile("G:\\media\\sounds\\solved.wav"))
        self.effectSolved.setVolume(0.5)
        labels = ["Licht","Antrieb","Hitzeschild","Klimaanlage"]

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
            FontGlowEffect(label,glow_color=QColor(229, 121, 27),steps=15,intensity=40)
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
            dial.valueChanged.connect(lambda _,l=labelCheckingInput: l.setText("Checking Input"))
    
            dial.valueChanged.connect(
                lambda value, i=i-1: QTimer.singleShot(
                    2000,
                    lambda:
                    changeValue(value, i)

                )
            )
            dial.valueChanged.connect(self.effect.play)
          

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
        
        labelCheckingInput.setFont(QFont("Geostar",25,QFont.Weight.Bold))
        labelCheckingInput.setStyleSheet("color: #FFFFFF")
        labelCheckingInput.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelCheckingInput,5,0,1,6)
     

        firstPuzzle = QWidget()
        firstPuzzle.setObjectName("MainContainer")  # Give it a unique ID
        firstPuzzle.setLayout(layout)

        firstPuzzle.setStyleSheet("""
            #MainContainer {
                background-color: #1B2024;
            }
            QLabel {
                background-color: rgba(0, 0, 0, 0); /* Keep labels transparent */
                color: white;
            }
        """)
        setupScreen = QWidget()
        setupScreen.setStyleSheet("""
            background-color: #000000;
        """)
        labelSetupScreen = QLabel("Put Sonoff Smart Plug into Pairing Mode")
        labelSetupScreen.setFont(QFont("Geostar",50,QFont.Weight.Bold))
        labelSetupScreen.setStyleSheet("color: #FFFFFF")
        labelSetupScreen.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelSetupScreen,QColor(255,255,255),15,20)
        buttonSetupScreen = QPushButton("Start Escape Room?")
        buttonSetupScreen.setFixedSize(700,300)
        buttonSetupScreen.setFont(QFont("Geostar",30,QFont.Weight.Bold))
        buttonSetupScreen.setStyleSheet("color: #FFFFFF; border: 2px solid white; border-radius: 5px;" )
        buttonSetupScreen.clicked.connect(lambda _: (
            stack.setCurrentIndex(1),
            QTimer.singleShot(5000, lambda: (stack.setCurrentIndex(2),
                        headline.setStyleSheet("""
                            QLabel{
                                color: #E5791B;
                                margin:50px;
                            }
                        """)
                    )
                )
            )
        )
        layoutSetupScreen = QVBoxLayout()
        layoutSetupScreen.setContentsMargins(0, 0, 0, 0)
        layoutSetupScreen.setSpacing(30)


        labelSetupScreen.setFixedHeight(120)
        labelSetupScreen.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        layoutSetupScreen.addStretch(4)

        layoutSetupScreen.addWidget(labelSetupScreen, alignment=Qt.AlignHCenter)
        layoutSetupScreen.addStretch(1)
        layoutSetupScreen.addWidget(buttonSetupScreen, alignment=Qt.AlignHCenter)
        layoutSetupScreen.addStretch(3)
        setupScreen.setLayout(layoutSetupScreen)
        stack.addWidget(setupScreen)


        errorMessage = QWidget()
        errorMessage.setStyleSheet("""
            background-color: #000000;
        """)
        labelErrorMessage = QLabel("ERROR | RESTART WATTARIUM")
        labelErrorMessage.setFont(QFont("Geostar",50,QFont.Weight.Bold))

        labelErrorMessage.setStyleSheet("color: #FD450A; border: 2px solid red;")
        labelErrorMessage.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelErrorMessage,QColor(253,69,10),15,20)
        layoutErrorMessage = QGridLayout()
        layoutErrorMessage.addWidget(labelErrorMessage)
        errorMessage.setLayout(layoutErrorMessage)
        stack.addWidget(errorMessage)
        
        stack.addWidget(firstPuzzle)

        secondPuzzle = QWidget()
        
        secondPuzzle.setStyleSheet("""
            background-color: #1B2024;
        """)
        labelSecondPuzzle = QLabel("Navigation")
        labelSecondPuzzle.setFont(QFont("Geostar",70,QFont.Weight.Bold))
        labelSecondPuzzle.setStyleSheet("color: #FFFFFF")
        labelSecondPuzzle.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelSecondPuzzle,QColor(255,255,255),15,20)
        layoutSecondPuzzle = QGridLayout()
        layoutSecondPuzzle.addWidget(labelSecondPuzzle,1,0,1,9)

        rocket = Rocket(stack)
        rocket.show()

        movieLabel = QLabel(stack)
        movieLabel.resize(70, 70)

        movie = QMovie("media/textures/globe.gif")
        movie.setScaledSize(QSize(70, 70))
        movie.setSpeed(70)
        movieLabel.setMovie(movie)
        movie.start()
        movieLabel.move(300, 300)

        movieLabel.show()

        def on_press(x, y):
            if stack.currentIndex() == 3:
                global_pos = boxSecondPuzzle.mapToGlobal(QPoint(int(x)-27, int(y)-35))
                local_pos = self.centralWidget().mapFromGlobal(global_pos)
                rocket.move(local_pos)
                rocket.raise_()





        boxSecondPuzzle = graph_system()
        boxSecondPuzzle.mouse_pressed.connect(on_press)
        boxSecondPuzzle.setStyleSheet("background-color: white;")
        layoutSecondPuzzle.addWidget(boxSecondPuzzle, 2, 1, 6, 7)
        secondPuzzle.setLayout(layoutSecondPuzzle)
        stack.addWidget(secondPuzzle)


        self.setCentralWidget(stack)

        stack.setCurrentIndex(3) # actually 0
        movieLabel.raise_() # set affter second puzle aopoears


       # QTimer.singleShot(5000,lambda v = 1: stack.setCurrentIndex(v)) # change to 28000 for production 

    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



