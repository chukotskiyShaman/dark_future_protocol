import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore


class Char:
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.points = 10 
        self.stats = {"Сила":3,"Технология":3,"Ловкость":3,"Харизма":3,"Интелект":3}
    def choose_params(self, i, cnt):
        if (((self.stats[list(self.stats.keys())[i]]!=3 and cnt==-1) or (self.stats[list(self.stats.keys())[i]]!=10 and cnt==1)) and (self.points!=0 or cnt==-1)):
            self.stats[list(self.stats.keys())[i]] += cnt
            self.parent.value_labels[i].setText(f"{list(self.stats.values())[i]}")
            self.points-=cnt
        if(self.points==0):
            self.parent.menu_buttons[0].show()
        else:
            self.parent.menu_buttons[0].hide()
         
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character=Char(self)
        self.setWindowTitle("My App")
        self.choises = [QPushButton(self),QPushButton(self),QPushButton(self),QPushButton(self)]
        for choise in self.choises:
            choise.hide()
        self.setGeometry(0,0,1920,1000)

        self.label = QLabel(self)
        self.names_labels = [QLabel(self) for _ in range(len(self.character.stats))]
        self.value_labels = [QLabel(self) for _ in range(len(self.character.stats))]
        self.statsbuttons = [QPushButton(self) for _ in range(len(self.character.stats)*2)]

        for i in range(10):
            if (i%2==0):
                self.statsbuttons[i].setText("-")
            else:
                self.statsbuttons[i].setText("+")
            self.statsbuttons[i].hide()
        for stats,vals in zip(self.names_labels,self.value_labels):
            stats.hide()
            vals.hide()

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
            self.text="a" #file.read()
            self.i=0
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateText)
            self.timer.start(25)
            # self.menu_buttons[2].hide()
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
        self.menu_buttons[0].hide()
        
        for i,stat in enumerate(self.character.stats):
            self.names_labels[i].setText(stat)
            self.value_labels[i].setText(f"{self.character.stats[stat]}")


            
            self.statsbuttons[i*2].clicked.connect(lambda _,x = i : self.character.choose_params(x,-1))
            self.statsbuttons[i*2+1].clicked.connect(lambda _,x = i : self.character.choose_params(x,+1))

            

            self.names_labels[i].setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            self.value_labels[i].setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

            self.names_labels[i].setGeometry(0,100+i*20,100,20)
            self.value_labels[i].setGeometry(120,100+i*20,20,20)    
            self.statsbuttons[i*2].setGeometry(100,100+i*20,20,20)
            self.statsbuttons[i*2+1].setGeometry(140, 100+i*20,20,20)

            self.names_labels[i].show()
            self.value_labels[i].show()
            self.statsbuttons[i*2].show()
            self.statsbuttons[i*2+1].show()

        

        

class game:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        self.window.show()
        self.player_choices = {}


class progress:
    def __init__(self):
        super().init()
        self.intro_passed = False
        

if __name__ == "__main__":
    game=game()
    game.app.exec()
    
