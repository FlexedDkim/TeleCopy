import os

class Console:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')