from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

import audio, login, settings

import sys
import re, os

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):       
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("SquadTalk 4")
        #self.setWindowIcon(QIcon('Icons/binary.png'))
 
        self.tabs = QTabWidget()
        self.tab1 = login.Login_Okno(self)
        self.tab2 = audio.Stream_Okno(self)
        self.tab3 = settings.Settings_Okno(self)
        self.tabs.addTab(self.tab1, "Dołącz")
        self.tabs.addTab(self.tab2, "Rozmawiaj")
        self.tabs.addTab(self.tab3, "Ustawienia")
        #self.tabs.setStyleSheet("color: white")

        self.setCentralWidget(self.tabs)

#App and window initialization
app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(400, 750)
window.setStyleSheet("background-color: rgb(37,37,37)")
window.show()

app.exec_()
