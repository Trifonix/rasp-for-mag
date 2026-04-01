"""
ПРАКТИЧЕСКАЯ РАБОТА:
ИСПОЛЬЗОВАНИЕ PYTHON И БИБЛИОТЕКИ OPEN CV ДЛЯ РАСПОЗНАВАНИЯ ОБЪЕКТОВ

Тема примера: обнаружение лиц на статичном изображении с помощью
каскада Хаара из библиотеки OpenCV.

Требуемые зависимости:
    pip install opencv-python
"""

import cv2  # основная библиотека компьютерного зрения OpenCV [web:6]
import os


def load_cascade(cascade_path: str) -> cv2.CascadeClassifier:
    """
    Загрузка каскада Хаара из файла XML.

    :param cascade_path: путь к файлу каскада (например, haarcascade_frontalface_default.xml)
    :return: объект CascadeClassifier
    """
    if not os.path.exists(cascade_path):
        raise FileNotFoundError(
            f"Файл каскада не найден: {cascade_path}. "
            f"Скачайте, пожалуйста, 'haarcascade_frontalface_default.xml' "
            f"из репозитория OpenCV и разместите рядом с main.py. [web:1]"
        )

    # Создаём объект классификатора и загружаем в него обученный каскад
    cascade = cv2.CascadeClassifier(cascade_path)

    # Проверяем, успешно ли загружен каскад
    if cascade.empty():
        raise RuntimeError(
            "Не удалось загрузить каскад Хаара. "
            "Проверьте корректность файла XML. [web:1]"
        )

    return cascade


def detect_faces_on_image(
    image_path: str,
    cascade: cv2.CascadeClassifier,
    scale_factor: float = 1.1,
    min_neighbors: int = 4,
    min_size: tuple = (30, 30),
):
    """
    Обнаружение лиц на статичном изображении с использованием каскада Хаара.

    :param image_path: путь к исходному изображению
    :param cascade: загруженный каскад Хаара (cv2.CascadeClassifier)
    :param scale_factor: параметр масштабирования для detectMultiScale
    :param min_neighbors: количество соседей для подтверждения прямоугольника
    :param min_size: минимальный размер обнаруживаемого лица
    :return: кортеж (исходное_изображение_BGR, список_прямоугольников_лиц)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Изображение не найдено: {image_path}. "
            f"Положите тестовое изображение (например, 'input.png') рядом с main.py."
        )

    # Читаем исходное цветное изображение в формате BGR
    image = cv2.imread(image_path)

    if image is None:
        raise RuntimeError(
            "Не удалось загрузить изображение. "
            "Проверьте формат и целостность файла."
        )

    # Переводим изображение в оттенки серого.
    # Для каскада Хаара обязательно использовать одноцветное изображение.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем метод detectMultiScale для поиска лиц.
    # scaleFactor – масштабирует окно поиска, minNeighbors – фильтрация ложных срабатываний. [web:2][web:5]
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_size,
    )

    return image, faces


def draw_faces(image, faces):
    """
    Отрисовка прямоугольников вокруг найденных лиц на изображении.

    :param image: исходное изображение BGR
    :param faces: список координат лиц (x, y, w, h)
    :return: изображение с нарисованными прямоугольниками
    """
    # Перебираем все найденные области, соответствующие лицам
    for (x, y, w, h) in faces:
        # Рисуем прямоугольник зелёного цвета толщиной 2 пикселя
        cv2.rectangle(
            image,          # изображение
            (x, y),         # левая верхняя точка
            (x + w, y + h), # правая нижняя точка
            (0, 255, 0),    # цвет в формате BGR (зелёный)
            2               # толщина линии
        )

    return image


def main():
    """
    Точка входа программы.

    Алгоритм работы:
    1. Загружаем каскад Хаара для обнаружения лиц.
    2. Загружаем исходное изображение.
    3. Выполняем обнаружение лиц с помощью detectMultiScale.
    4. Обводим найденные лица прямоугольниками.
    5. Сохраняем результат в файл и отображаем окно с результатом.
    """
    # Имя файла каскада Хаара (должен лежать рядом с main.py).
    # Классический файл для обнаружения лиц: haarcascade_frontalface_default.xml [web:1]
    cascade_path = "9-1_haarcascade_frontalface_default.xml"

    # Имя входного изображения
    input_image_path = "9-2_input.png"  # при необходимости измените на своё изображение

    # Имя выходного изображения с результатом
    output_image_path = "9-3_output_faces.png"

    # 1. Загрузка каскада
    face_cascade = load_cascade(cascade_path)

    # 2–3. Обнаружение лиц
    image, faces = detect_faces_on_image(
        image_path=input_image_path,
        cascade=face_cascade,
        scale_factor=1.1,
        min_neighbors=5,
        min_size=(30, 30),
    )

    print(f"Найдено лиц: {len(faces)}")

    # 4. Рисуем прямоугольники вокруг найденных лиц
    image_with_faces = draw_faces(image, faces)

    # 5. Сохраняем результат в файл
    cv2.imwrite(output_image_path, image_with_faces)
    print(f"Результат сохранён в файл: {output_image_path}")

    # Дополнительно можем показать результат в отдельном окне
    cv2.imshow("Результат обнаружения лиц", image_with_faces)
    print("Нажмите любую клавишу в окне изображения, чтобы завершить программу.")
    cv2.waitKey(0)  # ожидание нажатия клавиши
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()