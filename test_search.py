import sys
from search import search_similar

image_path = "test1.jpg"

if len(sys.argv) > 1:
    image_path = sys.argv[1]

results = search_similar(image_path, top_k=5)

print("\nНайденные товары:\n")

for r in results:
    print("URL:", r["url"])
    print("TEXT:", r["text"])
    print("SCORE:", round(r["score"], 3))
    print("-" * 40)
