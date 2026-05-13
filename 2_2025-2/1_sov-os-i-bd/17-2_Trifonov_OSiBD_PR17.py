# main.py – для практической работы №3

import csv
import random
import sys

# 1. Создание CSV с рандомными репликами
def create_csv():
    characters = ['Neo', 'Trinity', 'Morpheus', 'Agent Smith', 'Oracle', 'Cypher']
    with open('the-matrix-reloaded.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Speaker', 'Line'])
        for i in range(60):  # 60 строк — достаточный объём для lab
            speaker = random.choice(characters)
            line = ''.join(random.choices('abcdef ', k=random.randint(10, 40)))
            writer.writerow([speaker, line])

# 2. Функция, которая как lab3.py: читает свой же CSV и выводит блок реплик
def emulate_lab3():
    with open('the-matrix-reloaded.csv', newline='', encoding='utf-8') as f:
        dialog_lines = list(csv.reader(f))[1:]  # без заголовка

    # Выбираем случайный блок строк
    chunk_min, chunk_max = 10, 20
    line_num = len(dialog_lines)
    chunk_size = random.randrange(chunk_min, chunk_max)
    slice_start = random.randrange(0, line_num - chunk_size)
    slice_end = slice_start + chunk_size
    chosen_lines = dialog_lines[slice_start:slice_end]

    streams = [sys.stdout, sys.stderr]

    # Выводим случайные реплики в stdout/stderr
    for line in chosen_lines:
        speaker, text = line
        stream = random.choice(streams)
        print(f'{speaker}: {text}', file=stream, flush=True)

# 3. Функция, имитирующая lab3_2.py (генерация задания)
def emulate_lab3_2():
    variants = [
        'Neo, Trinity, love, .',
        'Neo, Morpheus, matrix, ?',
        'Trinity, Neo, kiss, !',
        'Morpheus, Neo, choice, .',
    ]
    parts = random.choice(variants).split(', ')
    saying_char   = parts[0].strip()
    about_char    = parts[1].strip()
    subject       = parts[2].strip()
    punc          = parts[3].strip()

    print(f'a) The character that says a phrase is "{saying_char}"')
    print(f'b) The character that is talked with/about is "{about_char}"')
    print(f'c) Should contain punctuation "{punc}"')
    print(f'd) The subject that is talked about "{subject}"')

# 4. Основной запуск
if __name__ == '__main__':
    # Создаём CSV
    create_csv()
    print("Создан файл the-matrix-reloaded.csv", file=sys.stderr)

    # Вариант лабораторной:
    # - если вызывать как `python main.py` — эмулируем логику lab3.py
    # - если вызывать с --task2 — эмулируем lab3_2.py
    if len(sys.argv) > 1 and sys.argv[1] == "--task2":
        emulate_lab3_2()
    else:
        emulate_lab3()