# Обновление расписания

## Быстрый старт (3 семестр)

1. Положите новый файл расписания в `0_parse-from/YYYY-MM-DD/` (например, `0_parse-from/2026-09-07/2026-09-07.xlsm`).
2. Запустите парсер с дополнением существующего JSON:

```bash
python 0_parse-from/parse-from-xlsm/main.py "0_parse-from/2026-09-07/2026-09-07.xlsm" --merge
```

3. Закоммитьте и запушьте `schedule3.json` — GitHub Pages обновит сайт.

## Параметры

| Параметр | Описание |
|----------|----------|
| `input` | Путь к `.xlsm` / `.xlsx` (по умолчанию — `0_parse-from/2026-08-31/2026-08-31.xlsm`) |
| `--group` | Лист группы (по умолчанию `12-25РПм`) |
| `--output` | Файл JSON (по умолчанию `schedule3.json`) |
| `--merge` | Дополнить/обновить существующий JSON |
| `--dry-run` | Показать результат без записи |

## Зависимости

```bash
pip install pandas openpyxl
```

## Публикация

Сайт — статические файлы в корне репозитория. После push в `main` GitHub Pages отдаёт:

`https://trifonix.github.io/rasp-for-mag/`

JSON расписания 3 семестра: `https://trifonix.github.io/rasp-for-mag/schedule3.json`
