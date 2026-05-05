import torch
import torch.nn as nn
from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
from torch.nn import functional as F

# --- Модель ---
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


# --- Произвольные данные (1 изображение 28x28) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
model = NeuralNetwork().to(device)

X = torch.rand(1, 28, 28, device=device)
logits = model(X)
print("logits (1x10):")
print(logits)

softmax = nn.Softmax(dim=1)
pred_probab = softmax(logits)
print("\npred_probab (Softmax, 1x10):")
print(pred_probab)


# --- FashionMNIST через DataLoader ---
print("\n--- FashionMNIST example ---")

training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)
train_features, train_labels = next(iter(train_dataloader))

train_features = train_features.to(device)
logits = model(train_features)

print("logits.shape (batch 64 x 10):", logits.shape)
print("logits (first 3 rows):")
print(logits[:3])
