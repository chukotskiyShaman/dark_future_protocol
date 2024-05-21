import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore
import pickle

def save_game(func, char):
    game_stat = {
        'func': func,
        'char': char
    }

    with open('./saved_games/game_state.save', 'wb') as file:
        pickle.dump(game_stat, file)
    


def load_game():
    with open('./saved_games/game_state.save', 'rb') as file:
        game_stat = pickle.load(file)
    return game_stat['func'], game_stat['char']


class Progress:
    def __init__(self):
        super().__init__()
        self.intro_passed = False
        self.ch1_carpet_key = False
        self.ch1_lockpick = False
        self.ch1_UGA_BUGA = False
        self.ch1_vent = False
        self.ch1_stay = False
        self.ch1_under_bad = False
        

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
        self.kastil = False
        self.func = self.quit_button_was_clicked
        self.progress = Progress()
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
        self.menu_buttons = [QPushButton(self) for _ in range(4)]
        self.menu_buttons[2].hide()
        self.menu_buttons[2].setText("Save game")
        self.menu_buttons[2].setGeometry(1740, 40, 180, 40)
        self.menu_buttons[2].clicked.connect(self.save_last_game)
        self.menu_buttons[0].setText("Start game")
        self.menu_buttons[0].setGeometry(1740, 0, 180, 40)
        self.menu_buttons[0].clicked.connect(self.new_game_button_was_clicked)
        self.menu_buttons[1].setText("Load game")
        self.menu_buttons[1].setGeometry(1740, 40, 180, 40)
        self.menu_buttons[1].clicked.connect(self.load_last_game)
        self.menu_buttons[3].setText("Exit")
        self.menu_buttons[3].setGeometry(1740, 80, 180, 40)
        self.menu_buttons[3].clicked.connect(self.quit_button_was_clicked)
        # self.setStyleSheet("""
        #     QWidget {
        #         background-color: #333333;
        #         color: #ffffff;
        #     }
        #     QPushButton {
        #         background-color: #555555;
        #         color: #ffffff;
        #         border: none;
        #         padding: 5px;
        #     }А
        #     QPushButton:hover {
        #         background-color: #666666;
        #     }
        #     QLineEdit {
        #         background-color: #444444;
        #         color: #ffffff;
        #     }
        # """)

    def save_last_game(self):
        save_game(self.func, self.character)
        
    def load_last_game(self):
        func, char =  load_game()
        self.char = char
        self.menu_buttons[1].hide()
        self.menu_buttons[0].disconnect()
        self.menu_buttons[0].setText("Continue")
        self.menu_buttons[0].clicked.connect(func)
    def new_game_button_was_clicked(self):
        with open('./data/intro.txt', 'r', encoding="utf-8") as file:
            self.text = file.read()# self.text="a"
        self.print_text(self.label)
        self.menu_buttons[1].hide()
        self.menu_buttons[2].show()
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
                    self.choises[i].setGeometry(1470,600+i*40,450,40)
        self.func = self.ch1_near_apart


    def first_decision_variant(self,i):
        stren = self.character.stats[list(self.character.stats.keys())[0]]
        if (stren>3 or not i==2):
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
            if (stren>3):
                self.progress.ch1_UGA_BUGA = True
                with open('./data/chapter1/break_door.txt', 'r', encoding = 'utf-8') as file:
                    self.text=file.read()
                self.print_text(self.label)

        if (not i == 2) or stren>3 :
            self.print_text(self.label, self.choises, self.ch1_in_the_flat)
            
            with open('./data/chapter1/key_under_carpet_variants.txt', 'r', encoding = 'utf-8') as file:
                for i,string in enumerate(file):
                    if not (string == '\n'):
                        self.choises[i].setText(string)
                        self.choises[i].setGeometry(1470,600+i*40,450,40)

        self.func = self.first_decision_variant

            
    def ch1_in_the_flat(self,i):
        dex = self.character.stats[list(self.character.stats.keys())[2]]
        path = ''
        if (not i==1 or dex > 3):
            self.label.setText('')
            self.hide_buttons(self.choises)
        if(i==0):
            self.progress.ch1_under_bad = True
            path ='./data/chapter1/hide_under_bed_variants.txt'
            with open('./data/chapter1/hide_under_bed.txt', 'r', encoding = 'utf-8') as file:
                self.text=file.read()
            
        if(i==1):
            
            if(dex>3):
                path ='./data/chapter2/climb_into_vent_variants.txt'
                self.progress.ch1_vent = True
                with open('./data/chapter2/climb_into_vent.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()

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
                self.text = file.read()
        if not (i == 2):
            if i==0:
                self.print_text(self.label, self.choises[0:2],self.they_are_here)
            if i==1:
                self.print_text(self.label, self.choises[0:2], self.ne_poyman)
            if i == 3:
                self.print_text(self.label, self.choises,self.they_are_here)
            with open(path,'r',encoding = "utf-8") as file:
                for i,string in enumerate(file): 
                    if not (string == '\n'):
                        self.choises[i].setText(string)
                        self.choises[i].setGeometry(1470,600+i*40,450,40)

        self.func = self.ch1_in_the_flat

    def they_are_here(self, i):
        ch = self.character.stats[list(self.character.stats.keys())[3]]
        path=''
        if not (i==1 and ch<8 and self.progress.ch1_stay==True):
            self.label.setText('')
            if self.kastil == False:
                if self.progress.ch1_under_bad:
                    self.hide_buttons(self.choises[0:2])
                else:
                    self.hide_buttons(self.choises)
        if i == 0:
            if self.progress.ch1_stay == True:
                self.kastil=False
                path = './data/chapter2/hands_up_variants.txt'
                with open('./data/chapter2/hands_up.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()

            else:
                if(self.kastil==True):
                    path = './data/chapter2/hands_up_variants.txt'
                    with open('./data/chapter2/captured_under_bed.txt', 'r', encoding='utf-8') as file:
                        self.text=file.read()
                    self.kastil=False

                elif self.progress.ch1_UGA_BUGA==True:
                    with open('./data/chapter1/stay_under_bad_door_breaked.txt', 'r', encoding='utf-8') as file:
                        self.text=file.read()
                        self.print_text(self.label)
                        self.menu_buttons[0].disconnect()
                        self.kastil=True
                        self.menu_buttons[0].clicked.connect(lambda x: self.they_are_here(0))
                        self.menu_buttons[0].show()

                else:
                    path = './data/chapter2/climb_into_vent_variants.txt'
                    with open('./data/chapter1/stay_under_bad_door_still.txt', 'r', encoding='utf-8') as file:
                        self.text=file.read()
                        self.print_text(self.label, self.choises[0:2], self.ne_poyman)
                        with open(path,'r',encoding = "utf-8") as file:
                            for i,string in enumerate(file):
                                if not (string == '\n'):
                                    self.choises[i].setText(string)
                                    self.choises[i].setGeometry(1470,600+i*40,450,40)
                        return


        if i == 1:
            if self.progress.ch1_under_bad == True:
                with open('./data/chapter1/get_out_from_underbed.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
                    self.print_text(self.label)
                    self.menu_buttons[0].disconnect()
                    self.kastil=True
                    self.menu_buttons[0].clicked.connect(lambda x: self.they_are_here(0))
                    self.menu_buttons[0].show()

            else:
                if ch>7:
                    if self.kastil == True:
                        path = './data/chapter2/climb_into_vent_variants.txt'
                        with open('./data/chapter2/on_da_street.txt', 'r', encoding='utf-8') as file:
                            self.text=file.read()
                        self.kastil=False

                    else:
                        with open('./data/chapter1/try_to_talk.txt', 'r', encoding='utf-8') as file:
                            self.text=file.read()
                            self.print_text(self.label)
                            self.menu_buttons[0].disconnect()
                            self.kastil=True
                            self.menu_buttons[0].clicked.connect(lambda x: self.they_are_here(1))
                            self.menu_buttons[0].show()

        if i == 2:
            if(self.kastil==True):
                    path = './data/chapter2/hands_up_variants.txt'
                    with open('./data/chapter2/captured_under_bed.txt', 'r', encoding='utf-8') as file:
                        self.text=file.read()
                    self.kastil=False
            else:
                with open('./data/chapter1/try_to_run.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
                    self.print_text(self.label)
                    self.menu_buttons[0].disconnect()
                    self.kastil=True
                    self.menu_buttons[0].clicked.connect(lambda x: self.they_are_here(2))
                    self.menu_buttons[0].show()

        if i == 3:
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda _:self.ch1_near_apart(1))
            with open('./data/chapter1/jump_from_window.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            self.menu_buttons[0].show()
            self.kastil=True

        if ((self.progress.ch1_stay==True and not self.kastil) or not self.kastil) and not ( i==1 and ch<8 and self.progress.ch1_stay):
            if (not i == 1 and self.progress.ch1_stay == True) or (i==0 and self.progress.ch1_under_bad==True):
                self.print_text(self.label, self.choises[0:3], self.we_are_fucked_up)
            else:
                self.print_text(self.label, self.choises[0:2], self.ne_poyman)
            with open(path,'r',encoding = "utf-8") as file:
                for i,string in enumerate(file):
                    if not (string == '\n'):
                        self.choises[i].setText(string)
                        self.choises[i].setGeometry(1470,600+i*40,450,40)

        self.func = self.they_are_here

    def we_are_fucked_up(self,i):
        stren = self.character.stats[list(self.character.stats.keys())[0]]
        dex =  self.character.stats[list(self.character.stats.keys())[2]]
        if not ((i==0 and stren <8) or (i==1 and dex <8)):
            # if self.progress.ch1_under_bad == True:
            self.hide_buttons(self.choises[0:3])
            # else:
            #     self.hide_buttons(self.choises)
            self.label.setText('')
        path = './data/chapter2/rip_the_ropes_variants.txt'
        if i == 0:
            if stren > 7:
                with open('./data/chapter2/rip_the_ropes.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
            else:
                return
        if i == 1:
            if dex > 7:
                with open('./data/chapter2/i_am_a_worm.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
            else:
                return
        if i == 2:
            with open('./data/chapter2/break_chair.txt', 'r', encoding='utf-8') as file:
                    self.text=file.read()
        
        self.print_text(self.label,self.choises[0:3], self.saved_by_god)
        with open(path,'r',encoding = "utf-8") as file:
            for i,string in enumerate(file): 
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(1470,600+i*40,450,40)

    def saved_by_god(self,i):
        stren = self.character.stats[list(self.character.stats.keys())[0]]
        tech =  self.character.stats[list(self.character.stats.keys())[1]]
        if not ((i==0 and stren <8) or (i==2 and tech <8)):
            # if self.progress.ch1_under_bad == True:
            if not i ==3:
                self.hide_buttons(self.choises[0:3])
            # else:
            #     self.hide_buttons(self.choises)
            self.label.setText('')
        with open('./data/chapter2/saved_by_someone.txt', 'r', encoding='utf-8') as file:
            self.text=file.read()
        if i == 0:
            if stren > 7:
                i=0
            else:
                return
        if i == 1:
            i=1
        if i == 2:
            if tech >7:
                i=2
            else: 
                return
        if i==3:
            with open('./data/chapter2/keep_going.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
        self.print_text(self.label)
        if not i == 3:
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda x: self.saved_by_god(3))
            self.menu_buttons[0].show()

    
    def ne_poyman(self, i):
        path =''
        self.hide_buttons(self.choises[0:2])
        self.label.setText('')
        if i == 0:
            path = './data/chapter2/follow_the_instructions_variants.txt'
            with open('./data/chapter2/follow_the_instructions.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label,self.choises[0:2], self.opposition)

        if i == 1:
            path = './data/chapter2/turn_to_police_variants.txt'
            with open('./data/chapter2/turn_to_police.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label,self.choises[0:2], self.police)

        with open(path,'r',encoding = "utf-8") as file:
            for i,string in enumerate(file): 
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(1470,600+i*40,450,40)

    def police(self,i):
        path=''
        self.hide_buttons(self.choises[0:2])
        self.label.setText('')

        if i == 0:
            return
        else:
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda _:self.ch1_near_apart(1))
            with open('./data/chapter2/run.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            self.menu_buttons[0].show()
            return
                
    def opposition(self, i):
        path=''
        if not i == 2:
            self.hide_buttons(self.choises[0:2])
        self.label.setText('')

        if i == 0:
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda _:self.opposition(2))
            with open('./data/chapter2/allow.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            self.menu_buttons[0].show()
            return

        if i ==2:
            with open('./data/chapter2/help_partisans.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            return
        
        if i == 1:
            path = './data/chapter2/decline_variants.txt'
            with open('./data/chapter2/decline.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label,self.choises[0:2], self.decline)

        with open(path,'r',encoding = "utf-8") as file:
            for i,string in enumerate(file): 
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(1470,600+i*40,450,40)

    def decline(self,i):
        path=''
        self.hide_buttons(self.choises[0:2])
        self.label.setText('')
        if i == 0:
            self.menu_buttons[0].disconnect()
            self.menu_buttons[0].clicked.connect(lambda _:self.ch1_near_apart(1))
            with open('./data/chapter2/go_home.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label)
            self.menu_buttons[0].show()
            return
        
        else:
            path = './data/chapter2/turn_to_police_variants.txt'
            with open('./data/chapter2/turn_to_police.txt', 'r', encoding='utf-8') as file:
                self.text=file.read()
            self.print_text(self.label,self.choises[0:2], self.police)

        with open(path,'r',encoding = "utf-8") as file:
            for i,string in enumerate(file): 
                if not (string == '\n'):
                    self.choises[i].setText(string)
                    self.choises[i].setGeometry(1470,600+i*40,450,40)


class game:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        self.window.show()
        self.player_choices = {}


        

if __name__ == "__main__":
    game=game()
    game.app.exec()
    
