import threading
import time
import asyncio
from typing import List

from src.intro import Intro
from src.console import Console
from src.client import Client

links = []
running = True

def input_links():
    global running, links

    while running:
        try:
            current_text = input("Введите ссылку на сообщение с контентом: ").strip()

            if current_text.lower() == "done":
                break

            if not current_text.startswith("https://t.me/"):
                print("Странная ссылка. Она должна начинаться с https://t.me/")
                continue

            if not current_text:
                print("Поле пустое :(")
                continue

            if current_text in links:
                print("Ссылка уже добавлена.")
                continue

            links.append(current_text)

            if len(links) == 1:
                Console.clear()
                Intro.create()
                print("\n  >> Добавленные ссылки <<\n")

            print(f"{len(links)}) {current_text}")

        except Exception as e:
            print(f"Ошибка: {e}")

async def main():
    global running, links

    client = Client()
    await client.start()

    Console.clear()
    Intro.create()

    input_thread = threading.Thread(target=input_links, daemon=True)
    input_thread.start()

    while running:
        command = input("").strip().lower()

        if command == "":
            if not len(links):
                print("Нужны только ссылки на медиа...")
                continue

            print("Начинаю загрузку...")

            await client.download_media(links)
            links = []

            Console.clear()
            Intro.create()

        elif command == "r":
            links = []

            Console.clear()
            Intro.create()

        elif command == "exit":
            print("Выхожу...")
            running = False

        else:
            print("Я не знаю, что ты мне прислал...")

if __name__ == "__main__":
    asyncio.run(main())