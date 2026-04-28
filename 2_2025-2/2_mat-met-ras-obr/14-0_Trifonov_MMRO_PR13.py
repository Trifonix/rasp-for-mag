import torch
from torch import nn

# 1. Создаём входные данные: 3 условных изображения 4x4
input_data = torch.rand(3, 4, 4)
print("Original input:")
print(f"Shape: {input_data.size()}")
print(input_data)

# 2. nn.Flatten: преобразуем 4x4 изображения в векторы длины 16
flatten = nn.Flatten()
flattened = flatten(input_data)
print("\nFlattened input:")
print(f"Shape: {flattened.size()}")
print(flattened)

# 3. nn.Linear: линейное преобразование 16 -> 4
layer1 = nn.Linear(in_features=16, out_features=4)
hidden1 = layer1(flattened)
print("\nAfter Linear (16 -> 4):")
print(f"Shape: {hidden1.size()}")
print(f"Before ReLU:\n{hidden1}")

# 4. nn.ReLU: нелинейность, отрицательные значения становятся 0
relu = nn.ReLU()
hidden1_relu = relu(hidden1)
print("\nAfter ReLU:")
print(hidden1_relu)

# 5. nn.Sequential: собираем всю сеть в один контейнер
neural_network = nn.Sequential(
    nn.Flatten(),
    nn.Linear(in_features=16, out_features=4),
    nn.ReLU(),
    nn.Linear(4, 2)
)

# Прогоняем данные через всю сеть
logits = neural_network(input_data)
print("\nOutput of neural网络 (logits):")
print(f"Shape: {logits.size()}")
print(logits)

# 6. nn.Softmax: преобразуем logits в вероятности по классам (dim=1)
softmax = nn.Softmax(dim=1)
probabilities = softmax(logits)
print("\nPredicted probabilities (Softmax):")
print(f"Shape: {probabilities.size()}")
print(probabilities)

# Проверка: сумма вероятностей по каждому образцу должна быть ≈ 1
print("\nSum of probabilities for each sample (should be ~1):")
print(probabilities.sum(dim=1))