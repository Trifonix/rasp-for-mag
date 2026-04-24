import torch
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Загрузка обучающего набора FashionMNIST
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

# Создание DataLoader для обучения (batch_size=64, shuffle=True)
train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)

# Получение первого батча
features, labels = next(iter(train_dataloader))

print(f"Размер батча признаков: {features.size()}")
print(f"Размер батча меток: {labels.size()}")

# Визуализация первого изображения из батча
img = features[0].squeeze()
label = labels[0].item()
plt.figure()
plt.imshow(img, cmap="gray")
plt.title(f"Метка: {label}")
plt.show()

# Проход по всем данным в DataLoader
print("\nПроход по всем батчам:")
for batch_idx, (images, batch_labels) in enumerate(train_dataloader):
    print(f"Батч {batch_idx + 1}:")
    print(f"  Тензор изображений: {images.shape}")
    print(f"  Тензор меток: {batch_labels.shape}")
    if batch_idx >= 2:  # Показываем только первые 3 батча для краткости
        break
print("Демонстрация завершена.") [web:1][web:2][page:1]