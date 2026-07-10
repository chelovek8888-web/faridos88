from telethon.sync import TelegramClient

api_id = 37796988
api_hash = "c39ecb6e2931af61e8b2b2397148e1f3"

with TelegramClient("session", api_id, api_hash) as client:
    print("Успешно подключились!")
    me = client.get_me()
    print(me)
