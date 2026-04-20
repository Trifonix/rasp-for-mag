import torch
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

labels_map = {
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle Boot",
}

data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

fig = plt.figure(figsize=(8, 8))
for i in range(1, 10):
    idx = torch.randint(len(data), (1,)).item()
    img, label = data[idx]
    ax = fig.add_subplot(3, 3, i)
    ax.set_title(labels_map[label], fontsize=10)
    ax.axis("off")
    ax.imshow(img.squeeze(), cmap="gray")

plt.tight_layout()
plt.show()