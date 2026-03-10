"""
Выполнил Дмитрий Трифонов
Студент 1 курса
группы 12-25РПм
Программная инженерия
"""

from PIL import Image, ImageDraw
import random

# Загрузка исходного изображения
img_path = "5-2_foto20260310.jpg"
img = Image.open(img_path)
width, height = img.size
print(f"Размер изображения: {width}x{height}")
print()

# Задание 1. Закраска части и всего изображения
print("=== Задание 1 ===")

# 1. Закраска области красным (0,0,100,100)
img1 = img.copy()
img1.paste((255, 0, 0), (0, 0, 100, 100))
print("1. Область закрашена красным")

img1.show()

# 2. Заливка всего зеленым
img2 = img.copy()
img2.paste((0, 128, 0), img2.getbbox())
print("2. Все изображение залито зеленым")

img2.show()
print()

# Задание 2. Комбинированные манипуляции
print("=== Задание 2 ===")

# 1. Уменьшенная копия с красной рамкой, вставка в исходное
small_size = (width // 3, height // 3)
img_small = img.resize(small_size)
frame_w = 8
frame_img = Image.new('RGB', (small_size[0] + 2 * frame_w, small_size[1] + 2 * frame_w), (255, 0, 0))
frame_img.paste(img_small, (frame_w, frame_w))
img21 = img.copy()
paste_x, paste_y = 50, 50
img21.paste(frame_img, (paste_x, paste_y))
print("1. Уменьшенная копия с красной рамкой вставлена")

img21.show()

# 2. Белая полупрозрачная горизонтальная полоса 100px - исправлено
strip_h = 100
strip_pos_y = height // 2 - strip_h // 2
img22 = img.copy()
# Создаем маску для прозрачности
mask = Image.new('L', (width, strip_h), 128)  # полупрозрачность
strip_color = Image.new('RGB', (width, strip_h), (255, 255, 255))
img22.paste(strip_color, (0, strip_pos_y), mask)
print("2. Белая полупрозрачная полоса показана")

img22.show()

# 3. Повернутая часть изображения
crop_box = (width//4, height//4, 3*width//4, 3*height//4)
part = img.crop(crop_box).rotate(30, expand=True)
img23 = img.copy()
paste_pos = (width - part.width - 20, 20)
img23.paste(part, paste_pos)
print("3. Повернутая центральная часть вставлена")

img23.show()
print()

# Задание 3. Симуляция кликов - ввод координат вручную
print("=== Задание 3 ===")
print("Случайный выбор координат (x y, например 150 200):")
points = []
for i in range(3):
    print(f"Точка {i+1} (x y): ")
    coords = [random.randint(0, 1000), random.randint(0, 1000)]
    x, y = int(coords[0]), int(coords[1])
    points.append((x, y))
    print(f"Точка {i+1}: ({x}, {y})")

# Показываем точки на изображении
img3 = img.copy()
draw3 = ImageDraw.Draw(img3)
for x, y in points:
    draw3.ellipse((x-5, y-5, x+5, y+5), fill='red', outline='yellow', width=20)
print("Изображение с отмеченными точками")

img3.show()
print()

# Задание 4. Рисование точек и линий
print("=== Задание 4 ===")
img4 = img.copy()
draw4 = ImageDraw.Draw(img4)

# Точки
points4 = [(100, 100), (300, 150), (200, 300), (400, 200)]
colors = ['red', 'blue', 'green', 'magenta']
for i, (x, y) in enumerate(points4):
    draw4.ellipse((x-8, y-8, x+8, y+8), fill=colors[i])

# Линии между точками
for i in range(len(points4)):
    x1, y1 = points4[i]
    x2, y2 = points4[(i+1) % len(points4)]
    draw4.line((x1, y1, x2, y2), fill='yellow', width=4)

print("4. Точки и линии нарисованы")

img4.show()

print("\nВсе задания выполнены!")
