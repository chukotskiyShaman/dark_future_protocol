import time

class game:
    def __init__(self):
        self.player_choices = {}

    def print(self, file_path):
        with open(file_path, 'r') as file:
            for string in file:
                string = string.strip()
                for symbol in string:
                    print(symbol, end='', flush=True)
                    time.sleep(0.075)
                print()


if __name__ == "__main__":
    path = './intro.txt'
    game=game()

    game.print(path)
    
