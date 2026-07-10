import pickle
import json
import faiss
import numpy as np

print("Загружаем index.pkl...")

with open("index.pkl", "rb") as f:
    data = pickle.load(f)

print("Товаров:", len(data))

vectors = []
meta = []

for item in data:
    vectors.append(item["vector"])

    meta.append({
        "channel": item["channel"],
        "post_id": item["post_id"],
        "url": item["url"],
        "text": item["text"]
    })

matrix = np.array(vectors).astype("float32")

print("Размер матрицы:", matrix.shape)

dim = matrix.shape[1]

index = faiss.IndexFlatIP(dim)
index.add(matrix)

faiss.write_index(index, "index.faiss")

with open("meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False)

print()
print("ГОТОВО")
print("Товаров в FAISS:", index.ntotal)
