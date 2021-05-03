from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

import client

class Settings_Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Settings_Okno,self).__init__(*args,*kwargs)
        self.setWindowTitle("Ustawienia")
        
        #tytuł
        titleText = QLabel()
        titleText.setText("Ustawienia")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setStyleSheet("color: white")
        titleText.setFont(QFont('Arial',30))
        
        #ComboBox
        self.cb = QComboBox()
        self.cb.addItems(["Audio1", "Audio2", "Audio3"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.cb.setStyleSheet("color: white")
        
        #layout
        mainMenu = QVBoxLayout()
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(self.cb)
        mainMenu.setAlignment(Qt.AlignCenter)
        
        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)
        
        self.setCentralWidget(mainMenuW)
    
    def selectionchange(self, i):
        print("Indeks wybranej opcji:" + str(i))