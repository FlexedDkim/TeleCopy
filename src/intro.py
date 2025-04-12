from IPython.display import clear_output

class Intro:
    @staticmethod
    def create():
        clear_output()
        print("""

Это загрузчик защищённых медиа.

Просто скопируй ссылку на медиа и вставь в меня :3

Нажми enter для загрузки, если ссылок больше нет
Введи exit, если хочешь выйти
    """)