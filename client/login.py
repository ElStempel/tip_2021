from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

import client

joined = False

class Login_Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Login_Okno,self).__init__(*args,*kwargs)
        self.setWindowTitle("Dołączanie")
        
        #tytuł
        titleText = QLabel()
        titleText.setText("SquadTalk 4")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setStyleSheet("color: white")
        titleText.setFont(QFont('Arial',45))
        
        #pole nazwy
        self.nameField = QLineEdit()
        self.nameField.setPlaceholderText("Podaj nazwę użytkownika")
        self.nameField.setStyleSheet("color: white")
        
        #pole ip
        self.ipField = QLineEdit()
        self.ipField.setPlaceholderText("Podaj ip serwera")
        self.ipField.setStyleSheet("color: white")
        
        #pole portu
        self.portField = QLineEdit()
        self.portField.setPlaceholderText("Podaj port serwera")
        self.portField.setStyleSheet("color: white")
        
        #join button
        joinButton = QPushButton()
        joinButton.setText("Dołącz")
        joinButton.setStyleSheet("background-color: rgb(0, 191, 178); color: white")
        joinButton.clicked.connect(self.joinClicked)
        
        #save button
        saveButton = QPushButton()
        saveButton.setStyleSheet("background-color: rgb(72, 61, 63); color: white")
        saveButton.setText("Zapisz ustawienia")
        
        #load button
        loadButton = QPushButton()
        loadButton.setStyleSheet("background-color: rgb(72, 61, 63); color: white")
        loadButton.setText("Wczytaj ustawienia")
        
        #layout
        mainMenu = QVBoxLayout()
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(self.nameField)
        mainMenu.addWidget(self.ipField)
        mainMenu.addWidget(self.portField)
        mainMenu.addWidget(joinButton)
        mainMenu.addWidget(saveButton)
        mainMenu.addWidget(loadButton)
        mainMenu.setAlignment(Qt.AlignCenter)
        
        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)
        
        self.setCentralWidget(mainMenuW)
    
    def joinClicked(self):
        print("Join button clicked")
        global joined
        joined = True
        

#app = QApplication(sys.argv)

#login_window = Login_Okno()
#login_window.setFixedSize(400,400)
#login_window.setStyleSheet("background-color: rgb(37,37,37)")
#login_window.show()

#stream_window = Stream_Okno()
#stream_window.setFixedSize(400,690)
#stream_window.setStyleSheet("background-color: rgb(37,37,37)")
#stream_window.show()

#app.exec_()