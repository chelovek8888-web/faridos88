import os
import json
import torch
import faiss
import numpy as np
from PIL import Image
from telethon import TelegramClient
import open_clip

# ---------------- CONFIG ----------------
API_ID = 37796988
API_HASH = "c39ecb6e2931af61e8b2b2397148e1f3"
CHANNEL = "Safrano_opt"

LIMIT = 300  # тестовый лимит

# ---------------- DEVICE ----------------
device = "cpu"

# ---------------- TELEGRAM ----------------
client = TelegramClient("session", API_ID, API_HASH)

# ---------------- CLIP ----------------
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)
model = model.to(device)
model.eval()

# ---------------- STORAGE ----------------
vectors = []
meta = []

# ---------------- EMBEDDING ----------------
def get_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.encode_image(image)
        emb = emb / emb.norm(dim=-1, keepdim=True)

    return emb.cpu().numpy().astype("float32")[0]

# ---------------- MAIN ----------------
async def main():
    await client.start()

    channel = await client.get_entity(CHANNEL)

    count = 0

    async for msg in client.iter_messages(channel, limit=LIMIT):

        if not msg.photo:
            continue

        file_path = f"tmp_{msg.id}.jpg"

        try:
            await client.download_media(msg.photo, file=file_path)

            vec = get_embedding(file_path)

            vectors.append(vec)

	meta.append({
    		"channel": CHANNEL,
    		"post_id": msg.id,
    		"url": f"https://t.me/{CHANNEL}/{msg.id}",
    		"text": msg.message or "",
	 	"date": msg.date.strftime("%Y-%m-%d %H:%M:%S") if msg.date else None,
    		"vector": vector
	})
            count += 1
            print(f"[OK] {count}")

        except Exception as e:
            print("[ERROR]", e)

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    # -------- FAISS INDEX --------
    dim = len(vectors[0])

    index = faiss.IndexFlatIP(dim)  # cosine similarity (after normalization)

    matrix = np.array(vectors).astype("float32")
    index.add(matrix)

    faiss.write_index(index, "index.faiss")

    with open("meta.json", "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\nГОТОВО")
    print("Товаров:", len(meta))

    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
