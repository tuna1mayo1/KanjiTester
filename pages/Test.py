import sys
import random
import numpy as np

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QFormLayout, QGroupBox, QScrollArea, QRadioButton, QButtonGroup
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QRect, QMargins

from buttons.BackButton import BackButton
from .Result import Result
from windows.DefaultWindow import DefaultWindow

# Test users on their understanding of Kanji. 
# Show users kanjis, and ask for their meaning in multiple choice (4 choices per question)

class Test():

    def __init__(self, stack, kanjilist):

        self.stack = stack
        self.num_qs = 10

        self.widget  = self._get_widget(kanjilist)
        # Initialize buttons that allow user to go back (to difficulty selection) and finished (pressed after user finishes the test)
        BackButton(self.widget, self.stack, 1)
        FinishedButton = QPushButton("Finished", self.widget)
        FinishedButton.move(1090, 10)
        FinishedButton.clicked.connect(self._load_results)
    
        self.stack.addWidget(self.widget)
        self.stack.setCurrentWidget(self.widget)
        self.stack.show()
    
    # Once finished button is pressed, Get the text data on which radio buttons were selected per question
    # And pass the information to Result. Invoke Result after along with above information to be analyzed
    def _load_results(self):

        # Initialize a string array of user's attempts
        self.attempt = [""] * self.num_qs

        # Find out which # the user selected for each question
        checked_options = [button_grp.checkedId() for button_grp in self.button_grps]
        #print(checked_options)

        for n in range(self.num_qs):
            if checked_options[n] != -1:
                self.attempt[n] = self.button_grps[n].button(checked_options[n]).text()
            else:
                self.attempt[n] = None
        
        self.Result = Result(self.stack, self.num_qs, self.kanjis_asked, self.attempt, self.answerkey)

    # Generate a test from given kanjilist
    # Per each kanji, 4 options of radio button will be given (including one correct answer)
    def _get_widget(self, kanjilist):

        widget = QWidget()
        form_layout = QFormLayout()
        group = QGroupBox()

        font_kanji = QFont("Times", 50, QFont.Bold)
        layout_margins = QMargins(50, 50, 50, 50)
        question_margins = QMargins(50, 30, 0, 0)

        end = len(kanjilist)
        kanjis = [list(entry.keys())[0] for entry in kanjilist]
        meanings = [list(entry.values())[0]["meanings"] for entry in kanjilist]
        meanings = [", ".join(meaning) for meaning in meanings]

        # Randomly select kanji_nums number of kanji indexes to create a test set
        possible_kanjis = list(range(end))
        selected_indexes = random.sample(possible_kanjis, self.num_qs)
        
        self.answerkey = []
        self.kanjis_asked = []
        self.button_grps = []
    
        for index in selected_indexes: 

            kanji = kanjis[index]
            self.kanjis_asked.append(kanji)
            kanji = QLabel(kanji)
            kanji.setFont(font_kanji)

            answer = meanings[index]
            self.answerkey.append(answer)

            # Generate 4 possible answer options including a correct one
            answers = [answer]
            possible_indexes = list(range(1, index)) + list(range(index+1, end))
            random_indexes = random.sample(possible_indexes, 3)
            answers = answers + [meanings[i] for i in random_indexes]
            random.shuffle(answers)

            # Generate a box of 4 shuffled radio buttons
            r0 = QRadioButton(answers[0])
            r1 = QRadioButton(answers[1])
            r2 = QRadioButton(answers[2])
            r3 = QRadioButton(answers[3])

            button_layout = QVBoxLayout()
            button_layout.addWidget(r0)
            button_layout.addWidget(r1)
            button_layout.addWidget(r2)
            button_layout.addWidget(r3)

            # The box of 4 shuffled radio buttons, including one correct option is one group (one question)
            button_grp = QButtonGroup()
            button_grp.addButton(r0, 0)
            button_grp.addButton(r1, 1)
            button_grp.addButton(r2, 2)
            button_grp.addButton(r3, 3)    

            self.button_grps.append(button_grp)

            button_layout.setContentsMargins(question_margins)
            form_layout.addRow(kanji, button_layout)
        
        group.setLayout(form_layout)
        scroll = QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(layout_margins)
        layout.addWidget(scroll)
        
        widget.setLayout(layout)
        return widget