#!/usr/bin/env python3
"""
Обновлятор расписания 3 семестра (schedule3.json).

Как пользоваться:
  1. Положить новый .xlsx / .xlsm рядом с этим скриптом (в 0_parse-from/).
  2. Запустить:
       python 0_parse-from/update_schedule.py
     или двойной клик по 0_parse-from/update_schedule.bat

Скрипт:
  - парсит лист группы 12-25РПм;
  - сравнивает с текущим schedule3.json;
  - добавляет только новые дни и новые/изменённые пары;
  - учитывает ручные переносы (библиодень);
  - после успеха переносит Excel в 0_parse-from/YYYY-MM-DD/YYYY-MM-DD.xlsx
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARSE_DIR = Path(__file__).resolve().parent
XLSM_DIR = PARSE_DIR / "parse-from-xlsm"
EXCEL_SUFFIXES = {".xlsm", ".xlsx"}
DATE_FOLDER_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

sys.path.insert(0, str(XLSM_DIR))

from main import (  # noqa: E402
    DEFAULT_GROUP,
    DEFAULT_OUTPUT,
    apply_manual_overrides,
    cleanup_pycache,
    load_json,
    parse_schedule,
    resolve_group_name,
    save_json,
    sort_schedule,
)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def find_newest_inbox_excel() -> Path | None:
    """Незаархивированные .xlsm/.xlsx прямо рядом со скриптом."""
    candidates = [
        path
        for path in PARSE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in EXCEL_SUFFIXES
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def is_already_archived(path: Path) -> bool:
    return DATE_FOLDER_RE.fullmatch(path.parent.name) is not None


def archive_excel(src: Path, archive_date: date | None = None) -> Path:
    if is_already_archived(src):
        print(f"  уже в архиве, не трогаю: {src.relative_to(ROOT)}")
        return src

    day = archive_date or date.today()
    folder_name = day.isoformat()
    dest_dir = PARSE_DIR / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{folder_name}{src.suffix.lower()}"

    if src.resolve() == dest.resolve():
        print(f"  уже в архиве: {dest.relative_to(ROOT)}")
        return dest

    if dest.exists():
        dest.unlink()

    shutil.move(str(src), str(dest))
    print(f"  архив: {src.name} -> {dest.relative_to(ROOT)}")
    return dest


def pair_key(lesson: dict) -> str:
    pair_text = str(lesson.get("Пара", ""))
    match = re.search(r"(\d+)\s*пара", pair_text, re.IGNORECASE)
    if match:
        return match.group(1)
    return pair_text.strip() or repr(lesson)


def pair_sort_key(lesson: dict) -> int:
    match = re.search(r"(\d+)", str(lesson.get("Пара", "")))
    return int(match.group(1)) if match else 99


def sort_day_lessons(lessons: list[dict]) -> list[dict]:
    return sorted(lessons, key=pair_sort_key)


def extend_semester(
    existing: dict[str, list[dict]],
    incoming: dict[str, list[dict]],
) -> tuple[dict[str, list[dict]], dict]:
    """Добавляет новые дни и новые пары, правит изменившиеся пары."""
    incoming = apply_manual_overrides(dict(incoming))
    result = {day: list(lessons) for day, lessons in existing.items()}

    new_days: list[str] = []
    extra_lessons: dict[str, list[dict]] = {}
    changed_lessons: dict[str, list[dict]] = {}
    unchanged_days: list[str] = []

    for day, lessons in incoming.items():
        if day not in result:
            result[day] = sort_day_lessons(list(lessons))
            new_days.append(day)
            continue

        by_pair = {pair_key(lesson): lesson for lesson in result[day]}
        added: list[dict] = []
        changed: list[dict] = []

        for lesson in lessons:
            key = pair_key(lesson)
            current = by_pair.get(key)
            if current is None:
                by_pair[key] = lesson
                added.append(lesson)
            elif current != lesson:
                by_pair[key] = lesson
                changed.append(lesson)

        if added or changed:
            result[day] = sort_day_lessons(list(by_pair.values()))
            if added:
                extra_lessons[day] = added
            if changed:
                changed_lessons[day] = changed
        else:
            unchanged_days.append(day)

    report = {
        "new_days": new_days,
        "extra_lessons": extra_lessons,
        "changed_lessons": changed_lessons,
        "unchanged_days": unchanged_days,
    }
    return sort_schedule(result), report


def has_updates(report: dict) -> bool:
    return bool(report["new_days"] or report["extra_lessons"] or report["changed_lessons"])


def print_lessons(lessons: list[dict], indent: str = "      ") -> None:
    for lesson in lessons:
        pair = lesson.get("Пара", "")
        kind = lesson.get("Вид занятий", "")
        subject = lesson.get("Дисциплина", "")
        teacher = lesson.get("Преподаватель", "")
        print(f"{indent}{pair} | {kind} | {subject} | {teacher}")


def print_report(report: dict, incoming_days: int, existing_days: int, merged_days: int) -> None:
    print(f"  в файле дней: {incoming_days}")
    print(f"  уже было в 3 семестре: {existing_days}")

    if report["new_days"]:
        print(f"  новые дни: {len(report['new_days'])}")
        for day in report["new_days"]:
            print(f"    + {day}")
    else:
        print("  новые дни: нет")

    if report["extra_lessons"]:
        print(f"  новые пары в известных днях: {len(report['extra_lessons'])}")
        for day, lessons in report["extra_lessons"].items():
            print(f"    + {day}")
            print_lessons(lessons)
    else:
        print("  новые пары в известных днях: нет")

    if report["changed_lessons"]:
        print(f"  изменённые пары: {len(report['changed_lessons'])}")
        for day, lessons in report["changed_lessons"].items():
            print(f"    ~ {day}")
            print_lessons(lessons)
    else:
        print("  изменённые пары: нет")

    print(f"  без изменений: {len(report['unchanged_days'])} дней из файла")
    print(f"  после обновления дней всего: {merged_days}")


def run_pipeline(input_path: Path, group: str, output_path: Path, archive: bool, dry_run: bool) -> int:
    print("=== 1/3  excel -> parse ===")
    if not input_path.exists():
        print(f"Ошибка: файл не найден: {input_path}", file=sys.stderr)
        return 1

    resolved_group = resolve_group_name(input_path, group)
    parsed = parse_schedule(input_path, resolved_group)
    if not parsed:
        print("Ошибка: занятий не найдено, файл не архивирую.", file=sys.stderr)
        return 1

    print(f"  лист: {resolved_group}")
    print(f"  файл: {input_path.name}")

    print("=== 2/3  сравнение с schedule3.json ===")
    existing = load_json(output_path)
    merged, report = extend_semester(existing, parsed)
    print_report(report, len(parsed), len(existing), len(merged))

    updated = has_updates(report)
    if dry_run:
        print("  dry-run: JSON и архив не трогаю")
        return 0

    if updated:
        save_json(output_path, merged)
        print(f"  сохранено: {output_path.relative_to(ROOT)}")
    else:
        print("  новых занятий нет — JSON не меняю")

    print("=== 3/3  архив Excel по сегодняшней дате ===")
    if archive:
        archived = archive_excel(input_path)
        print(f"  готово: {archived.relative_to(ROOT)}")
    else:
        print("  пропущено (--no-archive)")

    print()
    if updated:
        print("OK: расписание 3 семестра дополнено, файл архивирован")
        print("Публикация:")
        print(f'  git add {output_path.name} 0_parse-from/')
        print(f'  git commit -m "upd schedule 3 from {date.today().isoformat()}"')
        print("  git push")
    else:
        print("OK: новых занятий не было, исходник архивирован")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Положить xlsx/xlsm рядом со скриптом и запустить: добавит новое в 3 семестр и архивирует файл",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Путь к .xlsm/.xlsx (если не указан — самый новый файл рядом со скриптом)",
    )
    parser.add_argument("--group", default=DEFAULT_GROUP)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Не переносить Excel в папку YYYY-MM-DD",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать, что добавилось бы, без записи и архива",
    )
    return parser


def resolve_input(arg: str | None) -> Path:
    if arg:
        input_path = Path(arg)
        if not input_path.is_absolute():
            input_path = (ROOT / input_path).resolve()
        return input_path

    found = find_newest_inbox_excel()
    if not found:
        raise FileNotFoundError(
            "Положите .xlsx или .xlsm рядом с update_schedule.py "
            f"(папка {PARSE_DIR.relative_to(ROOT)}/) и запустите скрипт снова."
        )
    print(f"Автовыбор файла: {found.relative_to(ROOT)}")
    return found


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()
    exit_code = 1

    try:
        try:
            input_path = resolve_input(args.input)
        except FileNotFoundError as exc:
            print(f"Ошибка: {exc}", file=sys.stderr)
            return 1

        exit_code = run_pipeline(
            input_path=input_path,
            group=args.group,
            output_path=Path(args.output),
            archive=not args.no_archive and not args.dry_run,
            dry_run=args.dry_run,
        )
        return exit_code
    finally:
        cleanup_pycache(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
