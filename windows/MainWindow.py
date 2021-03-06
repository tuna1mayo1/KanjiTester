import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtGui import QFont

from .DefaultWindow import DefaultWindow
from pages.GroupSelect import GroupSelect
from pages.About import About

class MainWindow():

    def __init__(self, stack):
        stack.setCurrentIndex(0)
        self.stack = stack
        self.widget = self.stack.currentWidget()
        self.stack.show()

        self.learnButton = self.widget.findChild(QPushButton, 'learnButton')
        self.learnButton.clicked.connect(self.clicked_learn)
        
        self.testButton = self.widget.findChild(QPushButton, 'testButton')
        self.testButton.clicked.connect(self.clicked_test)

        self.aboutButton = self.widget.findChild(QPushButton, 'aboutButton')
        self.aboutButton.clicked.connect(self.clicked_about)

    def clicked_learn(self):
        self.GS = GroupSelect(self.stack, mode="learn")
    
    def clicked_test(self):
        self.GS = GroupSelect(self.stack, mode="test")
    
    def clicked_about(self):
        self.About = About(self.stack)

