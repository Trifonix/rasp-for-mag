import pdfplumber
import json
import re

header_fix = {
    "Дни\nнедели": "Дни недели",
    "пара": "Пара",
    "диВ йитяназ": "Вид занятий",
    "Дисциплина": "Дисциплина",
    "Преподователь": "Преподаватель",
    "Ссылка": "Ссылка"
}

pair_times = {
    "1": "09:00-10:30",
    "2": "10:40-12:10",
    "3": "12:30-14:00",
    "4": "14:10-15:40",
    "5": "15:50-17:20",
    "6": "17:40-19:10",
    "7": "19:20-20:50"
}

schedule = {}

def normalize_date_string(date_string):
    cleaned_string = date_string.replace('\n', ' ')
    parts = cleaned_string.strip().split(' ')
    return f"{parts[1]} {parts[0]}"[::-1]

def fix_pair(pair_text: str) -> str:
    if not pair_text:
        return ""
    m = re.match(r"(\d)\s*пара", pair_text)
    if m:
        num = m.group(1)
        return f"{num} пара {pair_times.get(num, '')}"
    return pair_text.strip()

def clean_link(link: str) -> str:
    if not link:
        return ""
    cleaned_link = link.replace(" ", "")
    return cleaned_link

with pdfplumber.open("0_parse-from-pdf/12-25РПм.pdf") as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue

        headers = [header_fix.get(h, h) for h in table[0]]
        current_day = None

        for row in table[1:]:
            record = dict(zip(headers, row))
            day_value = record.get("Дни недели")

            if day_value and day_value.strip():
                current_day = normalize_date_string(day_value.strip())

            record["Дни недели"] = current_day

            if not record.get("Дисциплина"):
                continue

            clean_record = {k: (v.replace("\n", " ").strip() if v else "") for k, v in record.items()}
            clean_record["Пара"] = fix_pair(clean_record.get("Пара", ""))
            clean_record["Ссылка"] = clean_link(clean_record["Ссылка"])

            day = clean_record.pop("Дни недели", "Неизвестный день")
            schedule.setdefault(day, []).append(clean_record)

with open("schedule.json", "w", encoding="utf-8") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

print("✅ Готово")
