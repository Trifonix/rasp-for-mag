import pandas as pd
import json
import re
from datetime import datetime
import numpy as np # Для работы с NaN

# Соответствие номера пары времени
pair_times = {
    "1": "09:00-10:30", "2": "10:40-12:10", "3": "12:30-14:00",
    "4": "14:10-15:40", "5": "15:50-17:20", "6": "17:40-19:10",
    "7": "19:20-20:50"
}

def clean(s):
    """
    Очищает строковое значение, преобразуя NaN или числа (которые могут быть 
    пустыми ячейками, включая 0/0.0) в пустую строку.
    """
    if pd.notna(s):
        s_str = str(s).replace("\n", " ").strip()
        # Гарантируем, что 0 или 0.0 становятся пустыми строками
        if s_str in ["0", "0.0", "0.00"]:
            return ""
        return s_str
    return ""

def fix_pair(pair_text: str) -> str:
    """Извлекает номер пары и добавляет временной интервал."""
    pair_text = clean(pair_text)
    if not pair_text:
        return ""
    
    m = re.search(r"(\d+)", pair_text)
    if m:
        num = m.group(1)
        time_str = pair_times.get(num, '')
        return f"{num} пара {time_str}"
        
    return pair_text.strip()

def join_teacher(record, teacher_key, degree_key):
    """Объединяет имя преподавателя и ученую степень."""
    prep = clean(record.get(teacher_key))
    title = clean(record.get(degree_key))
    
    if title:
        title = title.replace("д-р наук", "д-р. наук") 
        title = title.replace("канд. наук", "канд. наук")
        return (prep + " " + title).strip()
        
    return prep.strip()

def normalize_day(day_text):
    """Нормализует формат даты и дня недели в 'DD.MM.YYYY день_недели'."""
    t = clean(day_text)
    if not t:
        return None
        
    # 1. Пытаемся найти исходный формат: "DD.MM.YYYY день_недели"
    parts = t.split()
    if len(parts) >= 2 and re.match(r'\d{2}\.\d{2}\.\d{4}', parts[0]):
        return parts[0] + " " + parts[1].strip()
        
    # 2. Обрабатываем строку, которая выглядит как вывод datetime-объекта
    if re.match(r'\d{4}-\d{2}-\d{2}', t):
        try:
            date_part = t.split()[0] # YYYY-MM-DD
            dt_obj = pd.to_datetime(date_part)
            return dt_obj.strftime('%d.%m.%Y') 
        except:
             return None 
             
    return t 

# --- читаем XLSM ---
try:
    df = pd.read_excel(
        "0_parse-from-pdf/parse-from-xlsm/new.xlsm", 
        header=10, 
        # Принудительно читаем столбцы с датами как строки
        converters={'Дни недели': str, 'Дни недели.1': str}
    )
except FileNotFoundError:
    print("Ошибка: Файл new.xlsm не найден. Укажите правильный путь.")
    exit()

# Удаляем строки, которые полностью пусты
df = df.dropna(how='all')

# Удаляем первую строку, которая часто содержит дубликат заголовков
if not df.empty:
    df = df.iloc[1:]

# --- Определяем наборы колонок для двух расписаний ---
COL_RENAME_MAP = {
    # Неделя 1 (A-H)
    'Дни недели': 'W1_День', 'пара': 'W1_Пара', 'Вид занятий': 'W1_Вид_занятий',
    'Дисциплина': 'W1_Дисциплина', 'Преподаватель': 'W1_Преподаватель',
    'Unnamed: 5': 'W1_Ученая_степень', 'Ссылка': 'W1_Ссылка',
    
    # Неделя 2 (I-P)
    'Дни недели.1': 'W2_День', 'пара.1': 'W2_Пара', 'Вид занятий.1': 'W2_Вид_занятий',
    'Дисциплина.1': 'W2_Дисциплина', 'Преподаватель.1': 'W2_Преподаватель',
    'Unnamed: 12': 'W2_Ученая_степень', 'Ссылка.1': 'W2_Ссылка'
}

df.columns = [clean(c) for c in df.columns]
df.rename(columns=COL_RENAME_MAP, inplace=True)

SCHEDULE_COLUMNS_SETS = [
    {
        "prefix": "W1",
        "day": "W1_День", "pair": "W1_Пара", "activity_type": "W1_Вид_занятий",
        "discipline": "W1_Дисциплина", "teacher": "W1_Преподаватель",
        "degree": "W1_Ученая_степень", "link": "W1_Ссылка",
    },
    {
        "prefix": "W2",
        "day": "W2_День", "pair": "W2_Пара", "activity_type": "W2_Вид_занятий",
        "discipline": "W2_Дисциплина", "teacher": "W2_Преподаватель",
        "degree": "W2_Ученая_степень", "link": "W2_Ссылка",
    }
]

schedule = {}
current_day_w1 = None
current_day_w2 = None

# --- Обработка данных с учетом двух половин ---
for index, row in df.iterrows():
    
    # 1. Обновление текущего дня для Недели 1
    day_raw_w1 = row.get("W1_День")
    if pd.notna(day_raw_w1):
        normalized = normalize_day(day_raw_w1)
        if normalized:
            current_day_w1 = normalized
            
    # 2. Обновление текущего дня для Недели 2
    day_raw_w2 = row.get("W2_День")
    if pd.notna(day_raw_w2):
        normalized = normalize_day(day_raw_w2)
        if normalized:
            current_day_w2 = normalized

    # --- Обработка данных Недели 1 ---
    discipline_w1 = clean(row.get("W1_Дисциплина"))
    activity_w1 = clean(row.get("W1_Вид_занятий"))
    pair_raw_w1 = row.get("W1_Пара")
    teacher_raw_w1 = row.get("W1_Преподаватель")
    
    # Фильтрация W1: проверяем, что все ключевые поля заполнены и есть текущий день W1
    if discipline_w1 and activity_w1 and clean(pair_raw_w1) and clean(teacher_raw_w1) and current_day_w1:
        entry = {
            "Пара": fix_pair(pair_raw_w1),
            "Вид занятий": activity_w1,
            "Дисциплина": discipline_w1,
            "Преподаватель": join_teacher(row, "W1_Преподаватель", "W1_Ученая_степень"),
            "Ссылка": clean(row.get("W1_Ссылка"))
        }
        schedule.setdefault(current_day_w1, []).append(entry)

    # --- Обработка данных Недели 2 ---
    discipline_w2 = clean(row.get("W2_Дисциплина"))
    activity_w2 = clean(row.get("W2_Вид_занятий"))
    pair_raw_w2 = row.get("W2_Пара")
    teacher_raw_w2 = row.get("W2_Преподаватель")
    
    # Фильтрация W2: проверяем, что все ключевые поля заполнены и есть текущий день W2
    if discipline_w2 and activity_w2 and clean(pair_raw_w2) and clean(teacher_raw_w2) and current_day_w2:
        entry = {
            "Пара": fix_pair(pair_raw_w2),
            "Вид занятий": activity_w2,
            "Дисциплина": discipline_w2,
            "Преподаватель": join_teacher(row, "W2_Преподаватель", "W2_Ученая_степень"),
            "Ссылка": clean(row.get("W2_Ссылка"))
        }
        schedule.setdefault(current_day_w2, []).append(entry)

# --- сохраняем JSON (с сортировкой и фильтрацией некорректных ключей) ---
output_path = "0_parse-from-pdf/parse-from-xlsm/schedule.json"
with open(output_path, "w", encoding="utf-8") as f:
    
    def sort_key(date_str):
        """Преобразует строку DD.MM.YYYY [день_недели] в объект datetime для сортировки."""
        date_part = date_str.split()[0]
        try:
            return datetime.strptime(date_part, '%d.%m.%Y')
        except ValueError:
            # Возвращаем максимальное значение для отфильтровки
            return datetime.max 

    # 1. Фильтруем и сортируем ключи
    sorted_keys = [
        key for key in schedule.keys() if sort_key(key) != datetime.max
    ]
    sorted_keys = sorted(sorted_keys, key=sort_key)
    
    # 2. Создаем новый словарь с отсортированными и отфильтрованными ключами
    sorted_schedule = {key: schedule[key] for key in sorted_keys}
    
    json.dump(sorted_schedule, f, ensure_ascii=False, indent=2)

print(f"✅ Расписание успешно создано: {output_path}")
