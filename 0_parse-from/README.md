# Обновление расписания

## Единый цикл (рекомендуется)

Положите новый `.xlsm` в `0_parse-from/` и запустите:

```bash
pip install -r 0_parse-from/requirements.txt
python 0_parse-from/update_schedule.py
```

Или с явным путём:

```bash
python 0_parse-from/update_schedule.py "0_parse-from/Расписание_ИИТ_1-2_неделя.xlsm"
```

Скрипт делает:

1. **excel** — парсит лист `12-25РПм`
2. **json** — дополняет `schedule3.json` (фронтенд / GitHub Pages)
3. **date_excel** — переносит файл в `0_parse-from/YYYY-MM-DD/YYYY-MM-DD.xlsm`

Публикация:

```bash
git add schedule3.json 0_parse-from/
git commit -m "update schedule3"
git push
```

Сайт: https://trifonix.github.io/rasp-for-mag/

## Только парсер (без архива)

```bash
python 0_parse-from/parse-from-xlsm/main.py "0_parse-from/2026-09-05/2026-09-05.xlsm" --merge
```

| Параметр | Описание |
|----------|----------|
| `input` | Путь к `.xlsm` / `.xlsx` |
| `--group` | Лист группы (по умолчанию `12-25РПм`) |
| `--output` | JSON (по умолчанию `schedule3.json`) |
| `--merge` | Дополнить существующий JSON |
| `--dry-run` | Показать результат без записи |
| `--no-archive` | В `update_schedule.py`: не переносить Excel |

## Зависимости

```bash
pip install -r 0_parse-from/requirements.txt
```
