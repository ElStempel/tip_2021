from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

import client

joined = False

class Stream_Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Stream_Okno,self).__init__(*args,*kwargs)
        self.setWindowTitle("Pokój rozmów")
        
        #tytuł (ip i port)
        titleText = QLabel()
        titleText.setText("127.0.0.1:5000")
        titleText.setStyleSheet("color: white")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Arial',30))
        
        #leave button
        leaveButton = QPushButton()
        leaveButton.setText("Wyjdź")
        leaveButton.setStyleSheet("background-color: rgb(213, 88, 98); color: white")
        leaveButton.clicked.connect(self.leaveClicked)
        
        #mute button
        muteButton = QPushButton()
        muteButton.setText("Wycisz")
        muteButton.setStyleSheet("background-color: rgb(2, 128, 144); color: white")
        muteButton.clicked.connect(self.leaveClicked)
        
        #users
        
        users = []
        tmpstring = ""
        for i in range(25):
            users.append("user" + str(i+1))
        
        user1 = QTextEdit("")
        user1.setStyleSheet("color: white")
        user1.setReadOnly(True)
        user1.setFont(QFont('Arial', 16))
        
        for u in users:
            tmpstring += u + "\n"
        
        user1.setText(tmpstring)
            
        # user2 = QTextEdit("User 2")
        # user2.setReadOnly(True)
        # user3 = QTextEdit("User 3")
        # user3.setReadOnly(True)
        # user4 = QTextEdit("User 4")
        # user4.setReadOnly(True)
        # user5 = QTextEdit("User 5")
        # user5.setReadOnly(True)
        # user6 = QTextEdit("User 6")
        # user6.setReadOnly(True)
        # user7 = QTextEdit("User 7")
        # user7.setReadOnly(True)
        # user8 = QTextEdit("User 8")
        # user8.setReadOnly(True)
        # user9 = QTextEdit("User 9")
        # user9.setReadOnly(True)
        # user10 = QTextEdit("User 10")
        # user10.setReadOnly(True)
        # user11 = QTextEdit("User 11")
        # user11.setReadOnly(True)
        # user12 = QTextEdit("User 12")
        # user12.setReadOnly(True)
        # user13 = QTextEdit("User 13")
        # user13.setReadOnly(True)
        # user14 = QTextEdit("User 14")
        # user14.setReadOnly(True)
        # user15 = QTextEdit("User 15")
        # user15.setReadOnly(True)
        # user16 = QTextEdit("User 16")
        # user16.setReadOnly(True)
        # user17 = QTextEdit("User 17")
        # user17.setReadOnly(True)
        # user18 = QTextEdit("User 18")
        # user18.setReadOnly(True)
        # user19 = QTextEdit("User 19")
        # user19.setReadOnly(True)
        # user20 = QTextEdit("User 20")
        # user20.setReadOnly(True)
        # user21 = QTextEdit("User 21")
        # user21.setReadOnly(True)
        # user22 = QTextEdit("User 22")
        # user22.setReadOnly(True)
        # user23 = QTextEdit("User 23")
        # user23.setReadOnly(True)
        # user24 = QTextEdit("User 24")
        # user24.setReadOnly(True)
        # user25 = QTextEdit("User 25")
        # user25.setReadOnly(True)
        
        #userBox
        userBox = QGroupBox("Użytkownicy")
        userBox.setStyleSheet("color: white")
        
        #userBox layout
        boxLayout = QVBoxLayout()
        boxLayout.addWidget(user1)
        # boxLayout.addWidget(user2)
        # boxLayout.addWidget(user3)
        # boxLayout.addWidget(user4)
        # boxLayout.addWidget(user5)
        # boxLayout.addWidget(user6)
        # boxLayout.addWidget(user7)
        # boxLayout.addWidget(user8)
        # boxLayout.addWidget(user9)
        # boxLayout.addWidget(user10)
        # boxLayout.addWidget(user11)
        # boxLayout.addWidget(user12)
        # boxLayout.addWidget(user13)
        # boxLayout.addWidget(user14)
        # boxLayout.addWidget(user15)
        # boxLayout.addWidget(user16)
        # boxLayout.addWidget(user17)
        # boxLayout.addWidget(user18)
        # boxLayout.addWidget(user19)
        # boxLayout.addWidget(user20)
        # boxLayout.addWidget(user21)
        # boxLayout.addWidget(user22)
        # boxLayout.addWidget(user23)
        # boxLayout.addWidget(user24)
        # boxLayout.addWidget(user25)
        userBox.setLayout(boxLayout)
        
        #title layout
        titleLayout = QVBoxLayout()
        titleLayout.setAlignment(Qt.AlignTop)
        titleLayout.addWidget(titleText)
        titleLayoutV = QWidget()
        titleLayoutV.setLayout(titleLayout)
        
        #button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(muteButton)
        buttonLayout.addWidget(leaveButton)
        buttonLayout.setAlignment(Qt.AlignCenter)
        buttonLayoutH = QWidget()
        buttonLayoutH.setLayout(buttonLayout)
        
        mainMenu = QVBoxLayout()
        #mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleLayoutV)
        mainMenu.addWidget(userBox)
        mainMenu.addWidget(buttonLayoutH)
        
        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)
        
        self.setCentralWidget(mainMenuW)
    
    def leaveClicked(self):
        print("Leave button clicked")
        global joined
        joined = False