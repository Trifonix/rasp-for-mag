# Обновление расписания 3 семестра

## Как пользоваться

1. Скачанный `.xlsx` / `.xlsm` положить **рядом** с `update_schedule.py` (в эту папку `0_parse-from/`).
2. Запустить одним из способов:

```bash
python 0_parse-from/update_schedule.py
```

или двойной клик по `0_parse-from/update_schedule.bat`.

Скрипт сам:

1. Возьмёт самый новый Excel в этой папке (не из архивных `YYYY-MM-DD/`).
2. Спарсит лист `12-25РПм`.
3. Сравнит с `schedule3.json`.
4. Добавит **только новое**: новые дни и новые пары; изменившиеся пары обновит.
5. Учтёт ручной перенос библиодня (`02.10` → `30.09`).
6. После успеха перенесёт файл в `0_parse-from/YYYY-MM-DD/YYYY-MM-DD.xlsx`.

Если новых занятий нет, JSON не трогает, Excel всё равно архивирует, чтобы папка снова была пустой.

Публикация:

```bash
git add schedule3.json 0_parse-from/
git commit -m "upd schedule 3"
git push
```

Сайт: https://trifonix.github.io/rasp-for-mag/

## Опции

```bash
python 0_parse-from/update_schedule.py "0_parse-from/файл.xlsm"
python 0_parse-from/update_schedule.py --dry-run
python 0_parse-from/update_schedule.py --no-archive
```

| Параметр | Описание |
|----------|----------|
| `input` | Явный путь к Excel; иначе — самый новый файл в `0_parse-from/` |
| `--dry-run` | Показать, что добавилось бы, без записи и архива |
| `--no-archive` | Не переносить Excel в папку по дате |
| `--group` | Лист группы (по умолчанию `12-25РПм`) |
| `--output` | JSON (по умолчанию `schedule3.json`) |

## Только парсер

```bash
python 0_parse-from/parse-from-xlsm/main.py "0_parse-from/2026-10-05/2026-10-05.xlsm" --merge
```

## Зависимости

```bash
pip install -r 0_parse-from/requirements.txt
```
