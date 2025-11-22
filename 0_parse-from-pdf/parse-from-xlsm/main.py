import pandas as pd
import json
import re
from datetime import datetime

WEEKDAYS_MAP = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье'
}

pair_times = {
    "1": "09:00-10:30", "2": "10:40-12:10", "3": "12:30-14:00",
    "4": "14:10-15:40", "5": "15:50-17:20", "6": "17:40-19:10",
    "7": "19:20-20:50"
}

def clean(s):
    if pd.notna(s):
        s_str = str(s).replace("\n", " ").strip()
        if s_str in ["0", "0.0", "0.00"]:
            return ""
        return s_str
    return ""

def fix_pair(pair_text: str) -> str:
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
    prep = clean(record.get(teacher_key))
    title = clean(record.get(degree_key))
    
    if title:
        title = title.replace("д-р наук", "д-р. наук") 
        title = title.replace("канд. наук", "канд. наук")
        return (prep + " " + title).strip()
        
    return prep.strip()


def normalize_day(day_text):
    t = clean(day_text)
    if not t:
        return None
        
    parts = t.split()
    if len(parts) >= 2 and re.match(r'\d{2}\.\d{2}\.\d{4}', parts[0]):
        return parts[0] + " " + parts[1].strip()
        
    if re.match(r'\d{4}-\d{2}-\d{2}', t):
        try:
            date_part = t.split()[0]
            dt_obj = pd.to_datetime(date_part)
            
            weekday_num = dt_obj.weekday()
            weekday_name = WEEKDAYS_MAP.get(weekday_num, '')
            
            return f"{dt_obj.strftime('%d.%m.%Y')} {weekday_name}"
        except:
             return None 
             
    if len(parts) == 1 and parts[0].lower() in WEEKDAYS_MAP.values():
        return None 
             
    return t 

try:
    df = pd.read_excel(
        "0_parse-from-pdf/parse-from-xlsm/new.xlsm", 
        header=10, 
        converters={'Дни недели': str, 'Дни недели.1': str}
    )
except FileNotFoundError:
    print("Ошибка: Файл new.xlsm не найден. Укажите правильный путь.")
    exit()

df = df.dropna(how='all')

if not df.empty:
    df = df.iloc[1:]

COL_RENAME_MAP = {
    'Дни недели': 'W1_День', 'пара': 'W1_Пара', 'Вид занятий': 'W1_Вид_занятий',
    'Дисциплина': 'W1_Дисциплина', 'Преподаватель': 'W1_Преподаватель',
    'Unnamed: 5': 'W1_Ученая_степень', 'Ссылка': 'W1_Ссылка',
    
    'Дни недели.1': 'W2_День', 'пара.1': 'W2_Пара', 'Вид занятий.1': 'W2_Вид_занятий',
    'Дисциплина.1': 'W2_Дисциплина', 'Преподаватель.1': 'W2_Преподаватель',
    'Unnamed: 12': 'W2_Ученая_степень', 'Ссылка.1': 'W2_Ссылка'
}

df.columns = [clean(c) for c in df.columns]
df.rename(columns=COL_RENAME_MAP, inplace=True)

schedule = {}
current_day_w1 = None
current_day_w2 = None

for index, row in df.iterrows():
    
    # Обновление дня W1
    day_raw_w1 = row.get("W1_День")
    if pd.notna(day_raw_w1):
        normalized = normalize_day(day_raw_w1)
        if normalized:
            current_day_w1 = normalized
            
    # Обновление дня W2
    day_raw_w2 = row.get("W2_День")
    if pd.notna(day_raw_w2):
        normalized = normalize_day(day_raw_w2)
        if normalized:
            current_day_w2 = normalized

    # Обработка Недели 1
    discipline_w1 = clean(row.get("W1_Дисциплина"))
    activity_w1 = clean(row.get("W1_Вид_занятий"))
    pair_raw_w1 = row.get("W1_Пара")
    teacher_raw_w1 = row.get("W1_Преподаватель")
    
    if discipline_w1 and activity_w1 and clean(pair_raw_w1) and clean(teacher_raw_w1) and current_day_w1:
        entry = {
            "Пара": fix_pair(pair_raw_w1),
            "Вид занятий": activity_w1,
            "Дисциплина": discipline_w1,
            "Преподаватель": join_teacher(row, "W1_Преподаватель", "W1_Ученая_степень"),
            "Ссылка": clean(row.get("W1_Ссылка"))
        }
        schedule.setdefault(current_day_w1, []).append(entry)

    # Обработка Недели 2
    discipline_w2 = clean(row.get("W2_Дисциплина"))
    activity_w2 = clean(row.get("W2_Вид_занятий"))
    pair_raw_w2 = row.get("W2_Пара")
    teacher_raw_w2 = row.get("W2_Преподаватель")
    
    if discipline_w2 and activity_w2 and clean(pair_raw_w2) and clean(teacher_raw_w2) and current_day_w2:
        entry = {
            "Пара": fix_pair(pair_raw_w2),
            "Вид занятий": activity_w2,
            "Дисциплина": discipline_w2,
            "Преподаватель": join_teacher(row, "W2_Преподаватель", "W2_Ученая_степень"),
            "Ссылка": clean(row.get("W2_Ссылка"))
        }
        schedule.setdefault(current_day_w2, []).append(entry)

# --- Сохранение JSON с сортировкой ---
output_path = "0_parse-from-pdf/parse-from-xlsm/schedule.json"
with open(output_path, "w", encoding="utf-8") as f:
    
    def sort_key(date_str):
        date_part = date_str.split()[0]
        try:
            return datetime.strptime(date_part, '%d.%m.%Y')
        except ValueError:
            return datetime.max 

    sorted_keys = [
        key for key in schedule.keys() if sort_key(key) != datetime.max
    ]
    sorted_keys = sorted(sorted_keys, key=sort_key)
    
    sorted_schedule = {key: schedule[key] for key in sorted_keys}
    
    json.dump(sorted_schedule, f, ensure_ascii=False, indent=2)

print(f"✅ Расписание успешно создано: {output_path}")
