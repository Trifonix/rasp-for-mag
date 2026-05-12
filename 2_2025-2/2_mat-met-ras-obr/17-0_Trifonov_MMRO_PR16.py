import torch

def demonstrate_gradients_and_autograd():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ГРАДИЕНТОВ И АВТОМАТИЧЕСКОГО ДИФФЕРЕНЦИРОВАНИЯ")
    print("=" * 60)

    # Пример 1: Простой пример с одной переменной
    print("\n1. ПРОСТЫЕ ГРАДИЕНТЫ: y = x² + 4x + 11")
    print("- " * 40)

    x = torch.tensor([1.5], requires_grad=True)
    print(f"Исходный тензор x: {x}")
    print(f"x.requires_grad: {x.requires_grad}")

    y = x ** 2 + 4 * x + 11
    print(f"Результат вычисления y = x² + 4x + 11: {y}")
    print(f"y.grad_fn (функция для обратного прохода): {y.grad_fn}")

    # Вычисляем градиент
    y.backward()
    print(f"Градиент dy/dx в точке x=1.5: {x.grad}")

    # Проверяем вручную: dy/dx = 2x + 4, при x=1.5 → 2*1.5 + 4 = 7
    manual_gradient = 2 * 1.5 + 4
    print(f"Ручная проверка (2x + 4): {manual_gradient}")
    print(f"Совпадают ли значения? {torch.allclose(x.grad, torch.tensor([manual_gradient]))}")

    # Пример 2: Многомерный тензор
    print("\n2. МНОГОМЕРНЫЙ ПРИМЕР")
    print("- " * 30)

    x_multi = torch.tensor([2.0, 3.0, 4.0], requires_grad=True)
    print(f"Многомерный тензор x: {x_multi}")

    # Функция от нескольких переменных
    y_multi = x_multi ** 2 + 2 * x_multi + 5
    print(f"y = x² + 2x + 5: {y_multi}")

    # Суммируем, чтобы получить скаляр для backward()
    scalar_y = y_multi.sum()
    print(f"Сумма элементов y (скаляр): {scalar_y}")

    scalar_y.backward()
    print(f"Градиенты для каждого элемента x: {x_multi.grad}")
    print("Проверка вручную:")
    for i, val in enumerate(x_multi):
        manual_grad = 2 * val + 2
        print(f"  x[{i}] = {val}: dy/dx = {manual_grad} (ручной расчёт)")

    # Пример 3: Простая нейронная сеть
    print("\n3. ПРИМЕР С НЕЙРОННОЙ СЕТЬЮ")
    print("- " * 35)

    # Входные данные
    x_nn = torch.ones(5)  # входной вектор из 5 единиц
    y_true = torch.zeros(3)  # целевые значения (3 нуля)

    print(f"Входные данные x_nn: {x_nn}")
    print(f"Целевые значения y_true: {y_true}")

    # Параметры сети (обучаемые)
    w = torch.randn(5, 3, requires_grad=True)  # веса
    b = torch.randn(3, requires_grad=True)   # смещения

    print(f"Матрица весов w (5×3):\n{w}")
    print(f"Вектор смещений b (3): {b}")

    # Прямой проход (Forward Pass)
    z = torch.matmul(x_nn, w) + b  # линейное преобразование
    print(f"Результат линейного преобразования z: {z}")

    # Функция потерь
    loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y_true)
    print(f"Значение функции потерь: {loss:.6f}")

    print(f"Функция для обратного прохода для z: {z.grad_fn}")
    print(f"Функция для обратного прохода для loss: {loss.grad_fn}")

    # Обратное распространение (Backward Pass)
    loss.backward()

    print("\nГРАДИЕНТЫ ПОСЛЕ ОБРАТНОГО РАСПРОСТРАНЕНИЯ:")
    print(f"Градиенты весов w.grad:\n{w.grad}")
    print(f"Градиенты смещений b.grad: {b.grad}")

    # Пример 4: Визуализация градиентного спуска
    print("\n4. ВИЗУАЛИЗАЦИЯ ГРАДИЕНТНОГО СПУСКА")
    print("- " * 38)

    # Начальная точка
    x_gd = torch.tensor([3.0], requires_grad=True)
    learning_rate = 0.1
    steps = 10

    print(f"Начальная точка x = {x_gd.item()}, скорость обучения = {learning_rate}")

    for step in range(steps):
        # Функция для минимизации: y = (x - 2)²
        y_gd = (x_gd - 2) ** 2

        # Обнуляем градиенты
        if x_gd.grad is not None:
            x_gd.grad.zero_()

        # Вычисляем градиент
        y_gd.backward()

        # Обновляем параметр в направлении, противоположном градиенту
        with torch.no_grad():
            x_gd -= learning_rate * x_gd.grad

        print(f"Шаг {step + 1}: x = {x_gd.item():.4f}, loss = {y_gd.item():.6f}, grad = {x_gd.grad.item():.4f}")

    print(f"\nФинальное значение x: {x_gd.item():.6f} (теоретический минимум при x = 2)")


    # Пример 5: Проверка вычислительного графа
    print("\n5. СТРУКТУРА ВЫЧИСЛИТЕЛЬНОГО ГРАФА")
    print("- " * 37)

    a = torch.tensor(2.0, requires_grad=True)
    b = torch.tensor(3.0, requires_grad=True)

    c = a ** 2
    d = b ** 3
    e = c + d
    f = e * 2

    print(f"a = {a}, b = {b}")
    print(f"c = a² = {c}")
    print(f"d = b³ = {d}")
    print(f"e = c + d = {e}")
    print(f"f = e × 2 = {f}")

    f.backward()

    print(f"Градиент a.grad = {a.grad}")
    print(f"Градиент b.grad = {b.grad}")

    # Проверка правил дифференцирования
    print("\nПроверка правил дифференцирования:")
    print(f"∂f/∂a = ∂f/∂e × ∂e/∂c × ∂c/∂a = 2 × 1 × 2a = 8 (при a=2)")
    print(f"∂f/∂b = ∂f/∂e × ∂e/∂d × ∂d/∂b = 2 × 1 × 3b² = 54 (при b=3)")



if __name__ == "__main__":
    try:
        demonstrate_gradients_and_autograd()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Убедитесь, что установлен PyTorch: pip install torch")
