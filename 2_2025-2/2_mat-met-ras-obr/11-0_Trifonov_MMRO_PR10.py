import torch

def main():
    # 1. Создание тензора из обычных данных
    data = [[1, 2],
            [3, 4]]
    tensor = torch.tensor(data)
    print("Тензор из данных:\n", tensor, "\n")

    # 2. Размерность (shape), тип данных (dtype), устройство (device)
    print("Форма:", tensor.shape)
    print("Тип данных:", tensor.dtype)
    print("Устройство:", tensor.device, "\n")

    # 3. Создание разных тензоров
    shape = (2, 3)

    zeros_tensor = torch.zeros(shape)
    ones_tensor = torch.ones(shape)
    rand_tensor = torch.rand(shape)
    full_tensor = torch.full(shape, 7)

    print("Zeros:\n", zeros_tensor, "\n")
    print("Ones:\n", ones_tensor, "\n")
    print("Random:\n", rand_tensor, "\n")
    print("Full (7):\n", full_tensor, "\n")

    # 4. Тензоры на основе другого тензора
    new_zeros = torch.zeros_like(tensor)
    new_rand = torch.rand_like(tensor, dtype=torch.float32)

    print("Zeros like:\n", new_zeros, "\n")
    print("Rand like:\n", new_rand, "\n")

    # 5. Простая операция
    a = torch.tensor([[1.0, 2.0],
                      [3.0, 4.0]])
    b = torch.tensor([[5.0, 6.0],
                      [7.0, 8.0]])

    print("Сложение тензоров:\n", a + b)


if __name__ == "__main__":
    main()