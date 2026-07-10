import os
import json
import pickle
import asyncio

from PIL import Image
from telethon import TelegramClient

import torch
import open_clip

from channels import CHANNELS

import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = "session.session"

INDEX_FILE = "index.pkl"
PROGRESS_FILE = "progress.json"

client = TelegramClient(SESSION, API_ID, API_HASH)

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

device = "cpu"
model = model.to(device)
model.eval()


def get_embedding(image_path):
    with Image.open(image_path) as img:
        image = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        features = model.encode_image(image)
        features /= features.norm(dim=-1, keepdim=True)

    return features.cpu().numpy()[0]


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_index(index):
    tmp_file = INDEX_FILE + ".tmp"

    with open(tmp_file, "wb") as f:
        pickle.dump(index, f)

    os.replace(tmp_file, INDEX_FILE)


async def process_channel(channel_name, index, progress, existing_ids):
    print(f"\n=== {channel_name} ===")

    channel = await client.get_entity(channel_name)

    last_processed = progress.get(channel_name, 0)
    print(f"Последний обработанный ID: {last_processed}")

    added = 0

    async for msg in client.iter_messages(channel):

        if not msg.photo:
            continue

        if msg.id <= last_processed:
            continue
        file_name = f"tmp_{channel_name}_{msg.id}.jpg"

        if (channel_name, msg.id) in existing_ids:
            continue

        try:
            await client.download_media(msg.photo, file=file_name)

            vector = get_embedding(file_name)

            index.append({
                "channel": channel_name,
                "post_id": msg.id,
                "url": f"https://t.me/{channel_name}/{msg.id}",
                "text": msg.message or "",
                "vector": vector
            })

            existing_ids.add((channel_name, msg.id))

            if msg.id > progress.get(channel_name, 0):
                progress[channel_name] = msg.id

            added += 1

            if added % 100 == 0:
                save_index(index)
                save_progress(progress)
                print(f"{channel_name}: +{added}")

        except Exception as e:
            print("Ошибка:", e)

        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

    save_index(index)
    save_progress(progress)

    print(f"Добавлено: {added}")


async def main():
    index = load_index()
    progress = load_progress()

    print("Товаров в индексе:", len(index))

    existing_ids = {
        (item["channel"], item["post_id"])
        for item in index
    }

    await client.start()

    for channel_name in CHANNELS:
        await process_channel(
            channel_name,
            index,
            progress,
            existing_ids
        )

    await client.disconnect()

    print("\nГОТОВО")
    print("Всего товаров:", len(index))


asyncio.run(main())
