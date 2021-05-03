from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

#import client

import sys
import re, os

#replace with tcp connected z klienta
joined = False

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):       
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("SquadTalk 4")
 
        # LOGIN
        
        #tytuł
        nameText = QLabel()
        nameText.setText("SquadTalk 4")
        nameText.setAlignment(Qt.AlignCenter)
        nameText.setStyleSheet("color: white")
        nameText.setFont(QFont('Arial',45))
        
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
        saveButton.setText("Zapisz konfigurację")
        saveButton.clicked.connect(self.saveConf)
        
        #load button
        loadButton = QPushButton()
        loadButton.setStyleSheet("background-color: rgb(72, 61, 63); color: white")
        loadButton.setText("Wczytaj konfigurację")
        loadButton.clicked.connect(self.loadConf)
        
        #settings button
        settingsButton = QPushButton()
        settingsButton.setStyleSheet("background-color: rgb(72, 61, 63); color: white")
        settingsButton.setFont(QFont('Arial', 20))
        settingsButton.setFixedSize(40,40)
        settingsButton.setText("\u2699")
        settingsButton.clicked.connect(self.settingsClicked)
        
        #layout
        self.loginMenu = QVBoxLayout()
        self.loginMenu.addWidget(nameText)
        self.loginMenu.addWidget(self.nameField)
        self.loginMenu.addWidget(self.ipField)
        self.loginMenu.addWidget(self.portField)
        self.loginMenu.addWidget(joinButton)
        self.loginMenu.addWidget(saveButton)
        self.loginMenu.addWidget(loadButton)
        self.loginMenu.addWidget(settingsButton)
        self.loginMenu.setAlignment(Qt.AlignCenter)
        
        self.loginMenuW = QWidget()
        self.loginMenuW.setLayout(self.loginMenu)
        
        # STREAM
        
        #tytuł (ip i port)
        titleText = QLabel()
        titleText.setText("127.0.0.1:5000")
        titleText.setStyleSheet("color: white")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Arial',30))
        
        #leave button
        self.leaveButton = QPushButton()
        self.leaveButton.setText("Wyjdź")
        self.leaveButton.setStyleSheet("background-color: rgb(213, 88, 98); color: white")
        self.leaveButton.clicked.connect(self.leaveClicked)
        
        #mute button
        self.muteButton = QPushButton()
        self.muteButton.setText("Wycisz")
        self.muteButton.setStyleSheet("background-color: rgb(2, 128, 144); color: white")
        self.muteButton.clicked.connect(self.muteClicked)
        
        #second settings button
        second_settingsButton = QPushButton()
        second_settingsButton.setStyleSheet("background-color: rgb(72, 61, 63); color: white")
        second_settingsButton.setFont(QFont('Arial', 20))
        second_settingsButton.setFixedSize(40,40)
        second_settingsButton.setText("\u2699")
        second_settingsButton.clicked.connect(self.settingsClicked)
        
        #users
        
        userList = []
        tmpstring = ""
        for i in range(25):
            userList.append("user" + str(i+1))
        
        users = QTextEdit("")
        users.setStyleSheet("color: white")
        users.setReadOnly(True)
        users.setFont(QFont('Arial', 16))
        
        for u in userList:
            tmpstring += u + "\n"
        
        users.setText(tmpstring)
            
        #userBox
        userBox = QGroupBox("Użytkownicy")
        userBox.setStyleSheet("color: white")
        
        #userBox layout
        boxLayout = QVBoxLayout()
        boxLayout.addWidget(users)
        userBox.setLayout(boxLayout)
        
        #title layout
        titleLayout = QVBoxLayout()
        titleLayout.setAlignment(Qt.AlignTop)
        titleLayout.addWidget(titleText)
        titleLayoutV = QWidget()
        titleLayoutV.setLayout(titleLayout)
        
        #button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.muteButton)
        buttonLayout.addWidget(self.leaveButton)
        buttonLayout.setAlignment(Qt.AlignCenter)
        buttonLayoutH = QWidget()
        buttonLayoutH.setLayout(buttonLayout)
        
        self.streamMenu = QVBoxLayout()
        #self.streamMenu.setAlignment(Qt.AlignCenter)
        self.streamMenu.addWidget(titleLayoutV)
        self.streamMenu.addWidget(userBox)
        self.streamMenu.addWidget(buttonLayoutH)
        self.streamMenu.addWidget(second_settingsButton)
        
        self.streamMenuW = QWidget()
        self.streamMenuW.setLayout(self.streamMenu)
        
        self.setCentralWidget(self.streamMenuW)
        
        # USTAWIENIA
        
        #ustawienie 1
        f_settingText = QLabel()
        f_settingText.setText("Nagrywanie dźwięku")
        f_settingText.setAlignment(Qt.AlignCenter)
        f_settingText.setStyleSheet("color: white")
        f_settingText.setFont(QFont('Arial',20))
        
        #ComboBox 1
        self.cb1 = QComboBox()
        self.cb1.addItems(["Mic1", "Mic2", "Mic3"])
        self.cb1.currentIndexChanged.connect(self.rec_selectionchange)
        self.cb1.setStyleSheet("color: white")
        
        #ustawienie 2
        s_settingText = QLabel()
        s_settingText.setText("Odtwarzanie dźwięku")
        s_settingText.setAlignment(Qt.AlignCenter)
        s_settingText.setStyleSheet("color: white")
        s_settingText.setFont(QFont('Arial',20))
        
        #ComboBox 2
        self.cb2 = QComboBox()
        self.cb2.addItems(["Spk1", "Spk2", "Spk3"])
        self.cb2.currentIndexChanged.connect(self.play_selectionchange)
        self.cb2.setStyleSheet("color: white")
        
        #return button
        
        returnButton = QPushButton()
        returnButton.setText("Powrót")
        returnButton.setStyleSheet("background-color: rgb(0, 191, 178); color: white")
        returnButton.clicked.connect(self.returnClicked)
        
        #layout
        self.settingsMenu = QVBoxLayout()
        self.settingsMenu.addWidget(f_settingText)
        self.settingsMenu.addWidget(self.cb1)
        self.settingsMenu.addWidget(s_settingText)
        self.settingsMenu.addWidget(self.cb2)
        self.settingsMenu.addWidget(returnButton)
        self.settingsMenu.setAlignment(Qt.AlignCenter)
        
        self.settingsMenuW = QWidget()
        self.settingsMenuW.setLayout(self.settingsMenu)
        
        #Stack
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.loginMenuW)
        self.Stack.addWidget(self.streamMenuW)
        self.Stack.addWidget(self.settingsMenuW)
        self.setCentralWidget(self.Stack)
    
    #ustawienia
    def rec_selectionchange(self, i):
        print("Indeks wybranej opcji nagrywania:" + str(i))
    
    def play_selectionchange(self, i):
        print("Indeks wybranej opcji odtwarzania:" + str(i))
        
    #odtwarzanie
    def leaveClicked(self):
        print("Leave button clicked")
        global joined
        joined = False
        self.Stack.setCurrentIndex(0)
    
    def muteClicked(self):
        print("Mute button clicked")
    
    #logowanie
    def joinClicked(self):
        print("Join button clicked")
        global joined
        joined = True
        self.Stack.setCurrentIndex(1)
    
    def saveConf(self):
        file = open("config.txt", "w")
        L = [self.nameField.text(),"\n", self.ipField.text(),"\n", self.portField.text(),"\n"]
        file.writelines(L)
        file.close()
    
    def loadConf(self):
        try:
            file = open("config.txt", "r")
            content = file.read().splitlines()
            self.nameField.setText(content[0])
            self.ipField.setText(content[1])
            self.portField.setText(content[2])
            file.close()
        except:
            print("Brak pliku")
    
    #all    
    def settingsClicked(self):
        print("Settings button clicked")
        self.Stack.setCurrentIndex(2)
    
    #ustawienia    
    def returnClicked(self):
        print("Return button clicked")
        global joined
        if(joined == True):
            self.Stack.setCurrentIndex(1)
        else:
            self.Stack.setCurrentIndex(0)
    

#App and window initialization
app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(400, 750)
window.setStyleSheet("background-color: rgb(37,37,37)")
window.show()

app.exec_()
