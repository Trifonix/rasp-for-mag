import torch
from torch import nn


# -------------------------------
# Определение модели
# -------------------------------

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(784, 512),    # 28*28 = 784
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


# -------------------------------
# Функция обучения (без зависимости от FashionMNIST)
# -------------------------------

def train_loop(dataloader, model, loss_fn, optimizer, device):
    """
    dataloader: должен выдавать пакеты (X, y) в виде тензоров.
    Здесь нет загрузки данных из файлов/датасетов.
    """
    size = len(dataloader.dataset) if hasattr(dataloader, "dataset") else -1
    model.train()

    for batch, (X, y) in enumerate(dataloader):
        X = X.to(device)
        y = y.to(device)

        # Forward pass
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backward pass
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Необязательный вывод прогресса
        if batch % 100 == 0 and size != -1:
            loss_val = loss.item()
            current = batch * X.size(0) + X.size(0)
            print(f"loss: {loss_val:>7f}  [{current:>5d}/{size:>5d}]")


# -------------------------------
# Функция тестирования
# -------------------------------

def test_loop(dataloader, model, loss_fn, device):
    """
    То же самое: dataloader — просто итератор по (X, y); без загрузки файлов.
    """
    model.eval()
    size = len(dataloader.dataset) if hasattr(dataloader, "dataset") else -1
    num_batches = len(dataloader) if hasattr(dataloader, "dataset") else -1
    test_loss = 0.0
    correct = 0

    with torch.no_grad():
        for X, y in dataloader:
            X = X.to(device)
            y = y.to(device)

            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(dim=1) == y).type(torch.float).sum().item()

    # Если можем посчитать средние метрики
    if num_batches > 0:
        test_loss /= num_batches
    if size > 0:
        correct /= size

    print(f"Test Error:\n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f}\n")


# -------------------------------
# Основная часть (пример запуска)
# -------------------------------

if __name__ == "__main__":
    # Определение устройства
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = NeuralNetwork().to(device)

    learning_rate = 1e-3
    epochs = 10  # можно уменьшить/увеличить как нужно

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    # Пример: здесь ты сам подставляешь dataloader (например, из своего скрипта или ноутбука)
    # Ниже строка закомментирована, чтобы не требовать загрузки FashionMNIST:
    # train_dataloader = ...
    # test_dataloader  = ...

    # Тестовый вызов функций (если передашь свои даталоадеры):
    # for t in range(epochs):
    #     print(f"Epoch: {t+1}\n-------------------------------")
    #     train_loop(train_dataloader, model, loss_fn, optimizer, device)
    #     test_loop(test_dataloader, model, loss_fn, device)

    print("Model and training loop defined, no data files loaded.")