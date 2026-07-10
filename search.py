import faiss
import json
import numpy as np
import torch
import open_clip
from PIL import Image

device = "cpu"

# --- CLIP model ---
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)
model = model.to(device)
model.eval()

# --- load FAISS index ---
index = faiss.read_index("index.faiss")

# --- load metadata ---
with open("meta.json", "r") as f:
    meta = json.load(f)


def get_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.encode_image(image)
        emb = emb / emb.norm(dim=-1, keepdim=True)

    return emb.cpu().numpy().astype("float32")[0]


def search_similar(image_path, top_k=5):
    vec = get_embedding(image_path)
    vec = np.array([vec]).astype("float32")

    scores, ids = index.search(vec, top_k)

    results = []

    for score, idx in zip(scores[0], ids[0]):

        if score < 0.65:
            continue

        item = meta[idx]

        results.append({
            "score": float(score),
            "url": item["url"],
            "text": item["text"],
            "channel": item["channel"],
            "post_id": item["post_id"]
        })

    return results
