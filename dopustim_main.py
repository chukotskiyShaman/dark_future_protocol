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
        if (((self.stats[list(self.stats.keys())[i]]!=2 and cnt==-1) or (self.stats[list(self.stats.keys())[i]]!=10 and cnt==1)) and (self.points!=0 or cnt==-1)):
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
        self.end_print = 0

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
        with open('./data/intro.txt', 'r', encoding="utf-8") as file:
            self.text = file.read()# self.text="a"
        self.print_text(self.label)
        # self.menu_buttons[2].hide()
        # self.menu_buttons[0].hide()
        self.menu_buttons[0].disconnect()
        self.menu_buttons[0].setText("Continue")
        self.menu_buttons[0].clicked.connect(self.player_char)

    def quit_button_was_clicked(self):
        game.app.quit()


    
    def updateText(self, label):
        if self.text:
            label.setText(label.text() + self.text[0])
            self.text = self.text[1:]
        else:
            self.timer.stop()
            self.end_print = 1

            
    def print_text(self, label):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda : self.updateText(label))
        self.timer.start(25)
        
    def player_char(self):
        self.label.hide()
        self.timer.stop()
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
            
        self.menu_buttons[0].disconnect()
        self.menu_buttons[0].clicked.connect(self.ch1_near_apart)

    def ch1_near_apart(self):
        for i,stat in enumerate(self.character.stats):
            self.names_labels[i].hide()
            self.value_labels[i].hide()
            self.statsbuttons[i*2].hide()
            self.statsbuttons[i*2+1].hide()
            
        self.menu_buttons[0].hide()
        self.label.setText("")
        self.label.show()
        
        with open('./data/first_decision.txt', 'r', encoding = "utf-8") as file:
            self.text=file.read()
            self.print_text(self.label)
        print(self.text)
        if self.end_print == 1:
            with open('./data/first_decision_variants.txt','r',encoding = "utf-8") as file:
                for i,string in enumerate(file): 
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(100,200+i*40,240,40)
                    self.choises[i].show()
                
            
            

        

        

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
        self.ch1_carpet_key = False
        self.ch1_lockpick = False
        self.ch1_UGA_BUGA = False
        

if __name__ == "__main__":
    game=game()
    game.app.exec()
    
