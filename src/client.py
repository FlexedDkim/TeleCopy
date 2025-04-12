from pyrogram import Client as PyrogramClient
from dotenv import load_dotenv
import os
from typing import List

from src.console import Console
from src.intro import Intro
from src.barProgress import BarProgress

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

class Client():
    def __init__(self):
        self.client = PyrogramClient(name="mysession", api_id=api_id, api_hash=api_hash)
    
    async def start(self):
        await self.client.start()
    
    async def download_media(self, links: List[str]):
        try:
            for i, link in enumerate(links):
                message = await self._get_media_by_link(link)
                if not message: continue

                def get_progress(current, total):
                    Console.clear()
                    Intro.create()
                    print(f"Загружаемые медиа {i+1}/{len(links)}:")
                    print(BarProgress.create(current, total))

                await self.client.download_media(message, progress=get_progress)
            
            print("     ** Завершено **")
        
        except Exception as e:
            print(f"Скачивание было завершено с ошибкой: {e}")

    async def _get_media_by_link(self, link: str):
        if "/s/" in link: 
            return await self._get_story_by_link(link)
        else:
            return await self._get_message_by_link(link)

    async def _get_story_by_link(self, link: str):
        try:
            base = link.split("https://t.me/")[-1]
            parts = base.split("/s/")
            username = parts[0]
            story_id = parts[1]

            return await self.client.get_stories(
                story_sender_chat_id=username,
                story_ids=int(story_id)
            )

        except Exception as e:
            print(f"Что-то пошло не так при попытке получить этот файл: {e}")

    
    async def _get_message_by_link(self, link: str):
        try:
            group_id: str | int
            message_id: str | int

            if link.startswith("https://t.me/c/"):
                base = link.split("https://t.me/c/")[-1]
                parts = base.split("/")

                if len(parts) == 3:
                    topic_id = parts[1]
                    message_id = parts[2]
                else:
                    message_id = parts[1]

                group_id = int(f"-100{parts[0]}")
            
            else:
                base = link.split("https://t.me/")[-1]
                parts = base.split("/")

                group_id = parts[0]
                message_id = parts[1]

            message_id = int(message_id) if not "?" in message_id else int(message_id.split("?")[0])

            return await self.client.get_messages(
                chat_id=group_id, 
                message_ids=message_id
            )

        except Exception as e:
            print(f'Что-то пошло не так при попытке получить этот файл: {e}')
