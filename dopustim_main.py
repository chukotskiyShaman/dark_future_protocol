import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore

class Char:
    def __init__(self):
        super().__init__()
        self.stre = 3
        self.tech = 3
        self.dex = 3
        self.ch = 3 #Святослав, е***, это харизма
        self.intelegence = 3
    def choose_params():
        self.points = 10 
        print("Распределите свободные очки характеристик")
        print("Введите значение силы")
        self.stre = int(input())

class MainWindow(QMainWindow):
    def __init__(self, char):
        super().__init__()
        self.character=char
        self.setWindowTitle("My App")
        self.choises = [QPushButton(self),QPushButton(self),QPushButton(self),QPushButton(self)]
        for choise in self.choises:
            choise.hide()
        self.setGeometry(0,0,1920,1000)
        self.label = QLabel(self)
        self.label.setGeometry(0,0,1900,800)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.menu_buttons = [QPushButton(self),QPushButton(self),QPushButton(self)]
        self.menu_buttons[1].hide()
        self.menu_buttons[0].setText("Start game")
        self.menu_buttons[0].setGeometry(300, 300, 180, 40)
        self.menu_buttons[0].clicked.connect(self.new_game_button_was_clicked)
        self.menu_buttons[2].setText("Exit")
        self.menu_buttons[2].setGeometry(300, 340, 180, 40)
        self.menu_buttons[2].clicked.connect(self.quit_button_was_clicked)

    def new_game_button_was_clicked(self):
        with open('./intro.txt', 'r', encoding="utf-8") as file:
            self.text=file.read()
            self.i=0
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateText)
            self.timer.start(25)
            self.menu_buttons[2].hide()
            self.menu_buttons[0].hide()
            self.menu_buttons[0].disconnect()

    def quit_button_was_clicked(self):
        game.app.quit()


    
    def updateText(self):
        if self.text:
            self.label.setText(self.label.text() + self.text[0])
            self.text = self.text[1:]
        else:
            self.menu_buttons[0].setText("Continue")
            self.menu_buttons[0].show()
            self.menu_buttons[0].clicked.connect(self.player_char)
            self.timer.stop()

    def player_char(self):
        self.label.hide()
        

class game:
    def __init__(self):
        self.app = QApplication([])
        char = Char()
        self.window = MainWindow(char)
        self.window.show()
        self.player_choices = {}


class progress:
    def __init__(self):
        super().init()
        self.intro_passed = False
        

if __name__ == "__main__":
    path = './intro.txt'
    game=game()
    game.app.exec()
    
