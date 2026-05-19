"""
Демонстрация сохранения/загрузки в PyTorch без создания реальных файлов:
- torch.save / torch.load с io.BytesIO
- сохранение и загрузка объекта модели целиком
- сохранение и загрузка state_dict (весов)
При запуске вы увидите вывод, подтверждающий корректность операций.
"""

import io
import torch
from torch import nn

# Пример 1: сохранение и загрузка простого тензора через BytesIO
def demo_tensor_save_load():
    x = torch.tensor([0, 1, 2, 3, 4])
    buf = io.BytesIO()
    # Сохраняем в "файлоподобный" объект
    torch.save(x, buf)
    # Перемещаем курсор в начало и загружаем
    buf.seek(0)
    y = torch.load(buf)
    print("Tensor loaded equals original:", torch.equal(x, y), "| value:", y)

# Простая модель для демонстрации
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(4, 2),
            nn.ReLU(),
            nn.Linear(2, 1),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# Пример 2: сохранение и загрузка всей модели (pickle-serialized object)
def demo_model_save_load():
    model = NeuralNetwork()
    # заполним веса детерминировано для воспроизводимости
    with torch.no_grad():
        for i, p in enumerate(model.parameters()):
            p.fill_(i + 1.0)

    buf = io.BytesIO()
    torch.save(model, buf)    # сохраняем объект модели
    buf.seek(0)
    loaded_model = torch.load(buf, weights_only=False)  # загружаем модель целиком
    # Проверим совпадение state_dict
    same = all(torch.equal(a, b) for a, b in zip(model.state_dict().values(), loaded_model.state_dict().values()))
    print("Full model loaded equals original:", same)
    # Печатаем state_dict для наглядности (кратко)
    print("Original state_dict keys:", list(model.state_dict().keys()))
    print("Loaded  state_dict keys: ", list(loaded_model.state_dict().keys()))

# Пример 3: сохранение и загрузка state_dict (только веса)
def demo_state_dict_save_load():
    model1 = NeuralNetwork()
    model2 = NeuralNetwork()  # новая модель с отличающимися весами

    # Инициализируем model1 весами отличными от model2
    with torch.no_grad():
        for i, p in enumerate(model1.parameters()):
            p.fill_(i + 2.0)
        for i, p in enumerate(model2.parameters()):
            p.fill_(i + 10.0)

    # Сохраняем только state_dict в буфер
    buf = io.BytesIO()
    torch.save(model1.state_dict(), buf)
    buf.seek(0)

    # Загружаем веса в model2
    loaded_state = torch.load(buf, weights_only=True)
    model2.load_state_dict(loaded_state, strict=True)
    model2.eval()  # переводим в режим оценки
    # Проверим что теперь веса совпадают
    same_after = all(torch.equal(a, b) for a, b in zip(model1.state_dict().values(), model2.state_dict().values()))
    print("State dict loaded into model2, equal to model1:", same_after)

# Запускаем все демонстрации
if __name__ == "__main__":
    print("Demo: tensor save/load via BytesIO")
    demo_tensor_save_load()
    print("\nDemo: full model save/load via BytesIO")
    demo_model_save_load()
    print("\nDemo: state_dict save/load via BytesIO")
    demo_state_dict_save_load()
    print("\nAll demos completed.")