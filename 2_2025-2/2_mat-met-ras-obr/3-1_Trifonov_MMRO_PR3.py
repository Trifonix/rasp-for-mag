from PIL import Image
import matplotlib.pyplot as plt
import os


def task1_replace_channels(image_path):
    """
    Задание 1.
    Замена каналов с использованием getpixel и putpixel
    """

    print("=== Задание 1: Замена каналов ===")

    img = Image.open(image_path)
    img = img.convert("RGB")
    img.show(title="Исходное изображение")

    width, height = img.size

    # Создаём копию, чтобы не портить оригинал
    new_img = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            # Меняем каналы местами (B, R, G)
            new_img.putpixel((x, y), (b, r, g))

    new_img.show(title="Изображение с заменёнными каналами")
    print("Замена каналов выполнена.\n")

    return new_img


def task2_split_and_merge(image_path):
    """
    Задание 2.
    Разделение каналов и сборка изображения
    """

    print("=== Задание 2: Split и Merge ===")

    img = Image.open(image_path)
    img = img.convert("RGB")

    # Разделяем каналы
    r, g, b = img.split()

    r.show(title="Красный канал")
    g.show(title="Зелёный канал")
    b.show(title="Синий канал")

    # Собираем обратно
    merged = Image.merge("RGB", (r, g, b))
    merged.show(title="Собранное изображение")

    print("Каналы выделены и изображение собрано.\n")

    return merged


def task3_histogram(image_path):
    """
    Задание 3.
    Построение гистограммы изображения
    """

    print("=== Задание 3: Гистограмма ===")

    img = Image.open(image_path)
    img = img.convert("RGB")

    histogram = img.histogram()

    # Гистограмма RGB состоит из 256*3 значений
    r_hist = histogram[0:256]
    g_hist = histogram[256:512]
    b_hist = histogram[512:768]

    plt.figure()
    plt.plot(r_hist)
    plt.plot(g_hist)
    plt.plot(b_hist)

    plt.title("Гистограмма изображения (RGB)")
    plt.xlabel("Значение пикселя")
    plt.ylabel("Количество пикселей")
    plt.show()

    print("Гистограмма построена.\n")


def main():
    image_path = "3-2_flowers.jpeg"

    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден в текущей папке.")
        return

    task1_replace_channels(image_path)
    task2_split_and_merge(image_path)
    task3_histogram(image_path)


if __name__ == "__main__":
    main()
    