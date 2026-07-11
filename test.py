import os

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

with TelegramClient("session", api_id, api_hash) as client:
    print("Успешно подключились!")
    me = client.get_me()
    print(me)
