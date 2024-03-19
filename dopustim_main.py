import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(0,0,1920,1000)
        self.label = QLabel(self)
        self.label.setGeometry(0,0,1900,800)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.intro = QPushButton("Intro", self)
        self.intro.setGeometry(300, 300, 180, 40)
        self.intro.clicked.connect(self.intro_button_was_clicked)
        self.quit = QPushButton("Exit", self)
        self.quit.setGeometry(300,340,180,40)
        self.quit.clicked.connect(self.quit_button_was_clicked)

    def intro_button_was_clicked(self):
        with open('./intro.txt', 'r', encoding="utf-8") as file:
            self.text=file.read()
            self.i=0
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateText)
            self.timer.start(25)

    def quit_button_was_clicked(self):
        game.app.quit()


    
    def updateText(self):
        if self.text:
            self.label.setText(self.label.text() + self.text[0])
            self.text = self.text[1:]
        else:
            self.timer.stop()

class game:
    def __init__(self):
        self.player_choices = {}
        self.app = QApplication([])
        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    path = './intro.txt'
    game=game()
    game.app.exec()
    
