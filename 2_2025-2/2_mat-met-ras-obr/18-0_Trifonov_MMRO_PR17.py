import torch
import torch.nn.functional as F

# 1) Пример: y = x^2 + 4x + 11
x = torch.tensor([1.5], requires_grad=True)
y = x**2 + 4 * x + 11
print("y:", y.item(), "y.grad_fn:", type(y.grad_fn).__name__)  # grad_fn у y
y.backward()
print("dy/dx (x.grad):", x.grad.item())  # ожидается 2*x + 4 = 7

# Отдельный раздел для небольшого однослойного примера
# 2) Однослойная сеть (x, w, b) -> z -> бинарная кросс-энтропия с logits
x_in = torch.ones(5)                       # вход (вектор единиц)
y_true = torch.zeros(3)                    # целевые метки (все нули)
w = torch.randn(5, 3, requires_grad=True) # веса
b = torch.randn(3, requires_grad=True)    # смещение

z = x_in @ w + b                           # логиты (прямой проход)
loss = F.binary_cross_entropy_with_logits(z, y_true)  # loss
print("z.grad_fn:", type(z.grad_fn).__name__, "loss.grad_fn:", type(loss.grad_fn).__name__)

loss.backward()                            # обратное распространение
print("w.grad:\n", w.grad)                 # градиенты по весам
print("b.grad:\n", b.grad)                 # градиенты по смещению
