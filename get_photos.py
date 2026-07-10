from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_PATH = 'session.session'  # Путь к твоему файлу сессии

channel_username = 'Safrano_opt'  # Введи юзернейм канала без @

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

async def main():
    await client.start()
    channel = await client.get_entity(channel_username)
    messages = await client.get_messages(channel, limit=20)

    for msg in messages:
        if msg.photo:
            print(f"Пост ID: {msg.id} Дата: {msg.date} Текст: {msg.message}")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
