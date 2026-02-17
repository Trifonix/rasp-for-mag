# main.py - Практическая работа 2: Цветовые модели, создание и сохранение изображений с PIL
# Установка: pip install Pillow
from PIL import Image
import os

print("=== ЗАДАНИЕ 1: Получение и изменение цвета пикселя ===")

# Открываем изображение из текущей папки
img = Image.open("foto.jpeg")  # Замените на имя вашего файла
print(f"Режим цвета изображения: {img.mode}")  # Проверяем цветовую модель [web:1]

# 1. Метод load()
print("\n1. Работа с методом load():")
obj = img.load()  # Создаем объект для прямого доступа к пикселям
print(f"Цвет пикселя [25, 45]: {obj[25, 45]}")  # Получаем цвет пикселя

# Изменяем цвет пикселя на красный
obj[25, 45] = (255, 0, 0)
print(f"Новый цвет пикселя [25, 45]: {obj[25, 45]}")
img.show()  # Показываем измененное изображение

# 2. Методы getpixel() и putpixel()
print("\n2. Работа с getpixel() и putpixel():")
original_color = img.getpixel((25, 45))
print(f"Цвет пикселя через getpixel(): {original_color}")

# Меняем на синий
img.putpixel((25, 45), (0, 0, 255))
print(f"Цвет после putpixel(): {img.getpixel((25, 45))}")
img.show()

print("\n=== ЗАДАНИЕ 2: Переход между цветовыми моделями ===")

# Сбрасываем изменения, открываем заново
img = Image.open("foto.jpeg")
print(f"Исходный режим: {img.mode}")

# 1. Преобразование RGB -> RGBA через split() и merge()
print("\n1. Через split() и merge():")
r, g, b = img.split()  # Разделяем на каналы R, G, B
rgba_channels = (r, g, b, Image.new("L", img.size, (128,)))  # Добавляем альфа-канал (полупрозрачный)
img_rgba_split = Image.merge("RGBA", rgba_channels)
print(f"Новый режим после merge: {img_rgba_split.mode}")
img_rgba_split.show()

# 2. Преобразование через convert()
print("\n2. Через convert():")
img_rgba = img.convert("RGBA")
print(f"Режим после convert RGBA: {img_rgba.mode}")
img_rgba.show()

# 3. В градации серого
print("\n3. Конвертация в градации серого:")
img_gray = Image.open("foto.jpeg").convert("L")  # L = градации серого
print(f"Режим градаций серого: {img_gray.mode}")
img_gray.show()

# 4. RGB -> P (палитровый режим, 128 цветов)
print("\n4. Конвертация в палитровый режим P:")
img_p = img.convert("P", palette=Image.ADAPTIVE, colors=128)
print(f"Режим палитровый: {img_p.mode}")
img_p.show()

print("\n=== ЗАДАНИЕ 3: СОХРАНЕНИЕ ИЗОБРАЖЕНИЙ ===")

# Сохранение в текущую папку
img.save("result_rgb.jpg", "JPEG", quality=95)  # JPEG с высоким качеством [web:1]
img_rgba.save("result_rgba.png")  # PNG для RGBA
img_gray.save("result_gray.jpg")  # Градации серого
img_p.save("result_palette.gif")  # Палитровый режим лучше в GIF

print("\nСохраненные файлы:")
print("- result_rgb.jpg (исходное)")
print("- result_rgba.png (RGBA)")
print("- result_gray.jpg (градации серого)") 
print("- result_palette.gif (палитровый)")

# Дополнительно: сохранение в другую папку
try:
    save_path = "./folder/saved_image.jpg"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save("./folder/saved_image.jpg", "JPEG")  # В папку выше
    print("- saved_image.jpg (в папку ниже)")
except:
    print("Папка ./folder/ не найдена")

print("\n=== РАБОТА ЗАВЕРШЕНА ===")
