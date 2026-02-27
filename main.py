import threading
import asyncio
from bellows.zigbee.application import ControllerApplication
from zigpy.config import (
    CONF_DEVICE,
    CONF_DEVICE_PATH,

)
from PySide6.QtGui import Qt, QColor, QFontDatabase, QFont 
import sys
from PySide6.QtCore import QUrl,Qt,QTimer 
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget,
    QGridLayout, QDial, QProgressBar, QVBoxLayout, QStackedWidget,QPushButton, QSizePolicy)
from customDial import CustomDial
from fontGlowEffect import FontGlowEffect

def run_loop(loop):
    loop.run_forever()

CONFIG = {
    CONF_DEVICE: {
        CONF_DEVICE_PATH: "COM6",  # adjust if needed
    },
    "database_path": "G:/zigpy_db/zigbee.db",
    
}

ieees = "a4:c1:38:06:f7:07:ff:ff"
endpoints = {}  # global

async def main():
    global endpoints
    app = ControllerApplication(CONFIG)
    await app.startup(auto_form=False)
    await app.permit(20)
    
    print("Put your Sonoff plugs into pairing mode now...")
    await asyncio.sleep(20)

    for ieee, dev in app.devices.items():
        print(ieee, dev.manufacturer, dev.model)
        if "SONOFF" == dev.manufacturer:
            endpoints[ieee] = dev.endpoints[1]

    print("All endpoints ready:")
    changeSetuMessage("Found Smart Plugs : " + str(len(endpoints)))
    print(len(endpoints))


listOfValues = [0,0,0,0]

def sumForListValues(list:list):
    result = 0
    for i in list:       
        result += i
    return result

async def checkEffects():
   secondPuzzle = 3
   for ieee, ep in endpoints.items():
        if listOfValues[0]  == 32 and listOfValues[1] == 22 and listOfValues[2] == 22 and listOfValues[3] == 24:
            changeCurrentPage(secondPuzzle)
        elif listOfValues[0] > 31 and sumForListValues(list=listOfValues) <= 100:
            await ep.on_off.on()
        else:
            await ep.on_off.off()

async def changeValue(value , i ):
    listOfValues[i] = value
    await checkEffects()

def changeCurrentPage(page:int):
        stack.setCurrentIndex(page)

def changeSetuMessage(text:str):
    labelSetupScreen.setText(text)

labelSetupScreen:QLabel = None
stack = None



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(main())
threading.Thread(target=run_loop,args=(loop,),daemon=True).start()

class MainWindow(QMainWindow):
    
    def __init__(self):
        global stack
        global labelSetupScreen
        stack = QStackedWidget()
        super().__init__()
        self.setWindowTitle("My App")
        QFontDatabase.addApplicationFont("fonts/Geostar-Regular.ttf")
        layout = QGridLayout()
        self.showFullScreen()
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
            
            dial.valueChanged.connect(
                lambda value, i=i-1: asyncio.run_coroutine_threadsafe(
                    changeValue(value,i),loop
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
            QTimer.singleShot(5000, lambda: stack.setCurrentIndex(2))
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
            background-color: #000000;
        """)
        labelTmp = QLabel("Second Puzzle")
        labelTmp.setFont(QFont("Geostar",70,QFont.Weight.Bold))
        labelTmp.setStyleSheet("color: #FFFFFF")
        labelTmp.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelTmp,QColor(255,255,255),15,20)
        layoutSecondPuzzle = QGridLayout()
        layoutSecondPuzzle.addWidget(labelTmp)
        secondPuzzle.setLayout(layoutSecondPuzzle)
        stack.addWidget(secondPuzzle)


        self.setCentralWidget(stack)
        stack.setCurrentIndex(0)
        

       # QTimer.singleShot(5000,lambda v = 1: stack.setCurrentIndex(v)) # change to 28000 for production 

    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



