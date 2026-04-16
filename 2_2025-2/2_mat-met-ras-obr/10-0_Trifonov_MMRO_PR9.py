import torch
from torch import nn

torch.manual_seed(0)

print("=== PyTorch demo ===")

# 1. Данные: простая регрессия y = 2x - 1 + шум
x = torch.linspace(-1, 1, steps=100).unsqueeze(1)      # shape (100, 1)
y = 2 * x - 1 + 0.2 * torch.randn_like(x)

# 2. Модель: минимальный однослойный перцептрон
model = nn.Sequential(
    nn.Linear(1, 1)  # y_hat = w * x + b
)

# 3. Функция потерь и оптимизатор
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

def describe_tensor(name, t):
    print(f"{name:>8}: shape={tuple(t.shape)}, "
          f"mean={t.mean().item():+.3f}, std={t.std().item():+.3f}")

print("\nInitial parameters:")
for name, p in model.named_parameters():
    describe_tensor(name, p.data)

# 4. Обучение
for epoch in range(1, 101):
    y_hat = model(x)                  # прямой проход
    loss = loss_fn(y_hat, y)          # скалярная потеря

    optimizer.zero_grad()             # обнулить градиенты
    loss.backward()                   # автодифференцирование
    optimizer.step()                  # шаг оптимизации

    if epoch in {1, 2, 5, 10, 20, 50, 100}:
        print(f"epoch {epoch:3d} | loss = {loss.item():.4f}")

print("\nLearned parameters:")
for name, p in model.named_parameters():
    describe_tensor(name, p.data)

# 5. Демонстрация предсказания
with torch.no_grad():
    test_x = torch.tensor([[-1.0], [0.0], [1.0]])
    test_y = model(test_x)
    print("\nPredictions:")
    for xi, yi in zip(test_x, test_y):
        print(f"x = {xi.item():+4.1f} -> y_hat = {yi.item():+6.3f}")