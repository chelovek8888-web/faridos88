import torch
import open_clip
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

device = "cpu"
model = model.to(device)

def get_embedding(path):
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)

    with torch.no_grad():
        features = model.encode_image(image)
        features /= features.norm(dim=-1, keepdim=True)

    return features

img1 = get_embedding("test1.jpg")
img2 = get_embedding("test2.jpg")
img3 = get_embedding("test3.jpg")

sim12 = (img1 @ img2.T).item()
sim13 = (img1 @ img3.T).item()
sim23 = (img2 @ img3.T).item()

print(f"test1 ↔ test2 = {sim12:.4f}")
print(f"test1 ↔ test3 = {sim13:.4f}")
print(f"test2 ↔ test3 = {sim23:.4f}")
