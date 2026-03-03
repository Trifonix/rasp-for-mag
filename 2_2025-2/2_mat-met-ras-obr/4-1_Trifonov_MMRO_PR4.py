from PIL import Image

def task1_copy_and_resize():
    print("=== Задание 1: Копирование и изменение размера ===")

    # Открываем изображение
    img = Image.open("4-2_foto.png")
    print("Исходный размер:", img.size)

    # 1. Копирование
    img_copy = img.copy()
    img_copy.show()

    # 2. Пропорциональное уменьшение (thumbnail)
    img_thumb = img.copy()
    img_thumb.thumbnail((400, 300), Image.Resampling.LANCZOS)
    print("Размер после thumbnail (400x300):", img_thumb.size)
    img_thumb.show()

    img_thumb2 = img.copy()
    img_thumb2.thumbnail((400, 100), Image.Resampling.LANCZOS)
    print("Размер после thumbnail (400x100):", img_thumb2.size)
    img_thumb2.show()

    # 3. Изменение до точного размера (resize)
    new_size = (400, 400)
    img_resized = img.resize(new_size)
    print("Размер после resize:", img_resized.size)
    img_resized.show()


def task2_crop_and_resize():
    print("\n=== Задание 2: Вырезка области и изменение размеров ===")

    img = Image.open("4-2_foto.png")
    print("Исходный размер:", img.size)
    img.show()

    # Вырезаем прямоугольную область
    box = (100, 100, 300, 300)
    img_crop = img.crop(box)

    # Изменяем размер вырезанной области
    new_size = (400, 400)
    img_crop_resized = img_crop.resize(new_size)

    print("Размер вырезанной области после resize:", img_crop_resized.size)
    img_crop_resized.show()


def task3_rotate_and_mirror():
    print("\n=== Задание 3: Вращение и зеркальное отражение ===")

    img = Image.open("4-2_foto.png")
    print("Исходный размер:", img.size)

    # Поворот на 90 градусов
    img_rotate_90 = img.rotate(90, expand=True)
    print("Размер после поворота на 90°:", img_rotate_90.size)
    img_rotate_90.show()

    # Поворот на 45 градусов без expand
    img_rotate_45 = img.rotate(45)
    print("Размер после поворота на 45° (без expand):", img_rotate_45.size)
    img_rotate_45.show()

    # Поворот на 45 градусов с expand
    img_rotate_45_expand = img.rotate(45, expand=True)
    print("Размер после поворота на 45° (expand=True):", img_rotate_45_expand.size)
    img_rotate_45_expand.show()

    # Горизонтальное отражение
    img_flip_horizontal = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_flip_horizontal.show()

    # Вертикальное отражение
    img_flip_vertical = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_flip_vertical.show()


if __name__ == "__main__":
    task1_copy_and_resize()
    task2_crop_and_resize()
    task3_rotate_and_mirror()
