import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore
import pickle


def save_game(func, char):
    with open("saved_games/char_stat.save", 'wb') as file:
        pickle.dump(char,file)
    with open("saved_games/saved_game.save", 'wb') as file:
        pickle.dump(func, file)
    


def load_game():
    with open("saved_games/char_stat.save", 'rb') as file:
        char = pickle.load(file)
    with open("saved_games/saved_game.save", 'rb') as file:
        func = pickle.load(file)

    return func, char


class Progress:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.intro_passed = False
        self.ch1_carpet_key = False
        self.ch1_lockpick = False
        self.ch1_UGA_BUGA = False
        self.ch1_vent = False
        

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
        self.progress = Progress(self)
        self.setWindowTitle("My App")
        self.choises = [QPushButton(self) for _ in range(4)]
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

        self.label.setGeometry(0,0,1900,400)
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


    
    def updateText(self, label, buttons = 0, func=0):
        if self.text:
            label.setText(label.text() + self.text[0])
            self.text = self.text[1:]
        else:
            for i,button in enumerate(buttons):
                button.clicked.connect(lambda _, x = i : func(x))
                button.show()
            self.timer.stop()
            
    def hide_buttons(self, buttons):
        for button in buttons:
            button.hide()
            button.disconnect()
            
    def print_text(self, label, buttons = [], func = lambda x:x):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda : self.updateText(label, buttons, func))
        self.timer.start(0)
        
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


    def ch1_near_apart(self, restart = 0):
        if not restart:
            self.hide_buttons(self.statsbuttons)
            for i,stat in enumerate(self.character.stats):
                self.names_labels[i].hide()
                self.value_labels[i].hide()
            
        self.menu_buttons[0].hide()
        self.label.setText("")
        self.label.show()
        
        with open('./data/chapter1/first_decision.txt', 'r', encoding = "utf-8") as file:
            self.text=file.read()
        self.print_text(self.label,self.choises[0:3], self.first_decision_variant)
        with open('./data/chapter1/first_decision_variants.txt','r',encoding = "utf-8") as file:
            for i,string in enumerate(file): 
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(100,400+i*40,240,40)


    def first_decision_variant(self,i):
        self.label.setText('')
        self.hide_buttons(self.choises[0:3])
        if (i==0):
            self.progress.ch1_carpet_key = True
            with open('./data/chapter1/key_under_carpet.txt', 'r', encoding = 'utf-8') as file:
                self.text=file.read()
            
        if (i==1):
            self.progress.ch1_lockpick = True
            with open('./data/chapter1/use_lockpick.txt', 'r', encoding = 'utf-8') as file:
                self.text=file.read()
                    
        if (i==2):
            self.progress.ch1_UGA_BUGA = True
            with open('./data/chapter1/break_door.txt', 'r', encoding = 'utf-8') as file:
                self.text=file.read()

                
        self.print_text(self.label, self.choises, self.ch1_in_the_flat)
        
        with open('./data/chapter1/key_under_carpet_variants.txt', 'r', encoding = 'utf-8') as file:
            for i,string in enumerate(file):
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(100,400+i*40,240,40)

            
    def ch1_in_the_flat(self,i):
        dex = self.character.stats[list(self.character.stats.keys())[2]]
        path = ''
        if (not i==1 or dex > 4):
            self.label.setText('')
            self.hide_buttons(self.choises)
        if(i==0):
            self.progress.ch1_under_bed = True
            path ='./data/chapter1/hide_under_bed_variants.txt'
            with open('./data/chapter1/hide_under_bed.txt', 'r', encoding = 'utf-8') as file:
                self.text=file.read()
            
        if(i==1):
            
            if(dex>3):
                self.progress.ch1_vent = True
                with open('./data/chapter1/climb_into_vent.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
                self.print_text(self.label)
                self.menu_buttons[0].show()

        if(i==2):
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda _:self.ch1_near_apart(1))
            with open('./data/chapter1/jump_from_window.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            self.menu_buttons[0].show()
        if(i==3):
            path = './data/chapter1/stay_variants.txt'
            self.progress.ch1_stay = True
            with open('./data/chapter1/stay.txt', 'r', encoding='utf-8') as file:
                self.text.file.read()
        if not (i==1 or i == 2):
            self.print_text(self.label, self.choises)
            with open(path,'r',encoding = "utf-8") as file:
                for i,string in enumerate(file): 
                    if not (string == '\n'):
                        self.choises[i].setText(string)
                        self.choises[i].setGeometry(100,400+i*40,240,40)
            
        


  

                
            

        

        

class game:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        self.window.show()
        self.player_choices = {}


        

if __name__ == "__main__":
    game=game()
    game.app.exec()
    
