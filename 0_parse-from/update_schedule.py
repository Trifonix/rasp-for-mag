#!/usr/bin/env python3
"""
Единый цикл обновления расписания 3 семестра:

  excel -> json (merge schedule3.json) -> archive (date folder)

Использование:
  python 0_parse-from/update_schedule.py "0_parse-from/Расписание_ИИТ_1-2_неделя.xlsm"
  python 0_parse-from/update_schedule.py   # берёт самый новый .xlsm/.xlsx из 0_parse-from/

После успешного запуска:
  git add schedule3.json 0_parse-from/YYYY-MM-DD/
  git commit -m "update schedule3 from YYYY-MM-DD"
  git push
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARSE_DIR = ROOT / "0_parse-from"
XLSM_DIR = PARSE_DIR / "parse-from-xlsm"
sys.path.insert(0, str(XLSM_DIR))

from main import (  # noqa: E402
    DEFAULT_GROUP,
    DEFAULT_OUTPUT,
    load_json,
    merge_schedules,
    parse_schedule,
    resolve_group_name,
    save_json,
)


def find_newest_inbox_excel() -> Path | None:
    """Ищет незаархивированные .xlsm/.xlsx прямо в 0_parse-from/."""
    candidates = [
        p for p in PARSE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".xlsm", ".xlsx"}
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def archive_excel(src: Path, archive_date: date | None = None) -> Path:
    day = archive_date or date.today()
    folder_name = day.isoformat()  # YYYY-MM-DD
    dest_dir = PARSE_DIR / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{folder_name}{src.suffix.lower()}"

    if src.resolve() == dest.resolve():
        print(f"  уже в архиве: {dest}")
        return dest

    if dest.exists():
        dest.unlink()

    shutil.move(str(src), str(dest))
    print(f"  архив: {src.name} -> {dest.relative_to(ROOT)}")
    return dest


def run_pipeline(input_path: Path, group: str, output_path: Path, archive: bool) -> int:
    print("=== 1/3  excel -> parse ===")
    if not input_path.exists():
        print(f"Ошибка: файл не найден: {input_path}", file=sys.stderr)
        return 1

    resolved_group = resolve_group_name(input_path, group)
    parsed = parse_schedule(input_path, resolved_group)
    if not parsed:
        print("Предупреждение: занятий не найдено.", file=sys.stderr)
    else:
        print(f"  лист: {resolved_group}")
        print(f"  дней с занятиями: {len(parsed)}")
        for day, lessons in parsed.items():
            print(f"    {day}: {len(lessons)}")

    print("=== 2/3  json -> schedule3 (frontend / GitHub Pages) ===")
    existing = load_json(output_path)
    merged = merge_schedules(existing, parsed)
    save_json(output_path, merged)
    print(f"  сохранено: {output_path.relative_to(ROOT)} ({len(merged)} дней всего)")
    print("  фронтенд читает этот JSON; после push GitHub Pages обновит сайт")

    print("=== 3/3  date_excel -> архив по дате ===")
    if archive:
        archived = archive_excel(input_path)
        print(f"  готово: {archived.relative_to(ROOT)}")
    else:
        print("  пропущено (--no-archive)")

    print()
    print("OK: цикл excel -> json -> frontend_github -> date_excel завершён")
    print("Дальше для публикации:")
    print(f'  git add {output_path.name} 0_parse-from/')
    print(f'  git commit -m "update schedule3 from {date.today().isoformat()}"')
    print("  git push")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Единый цикл: excel -> schedule3.json -> архив по дате",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Путь к .xlsm/.xlsx (если не указан — самый новый файл в 0_parse-from/)",
    )
    parser.add_argument("--group", default=DEFAULT_GROUP)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Не переносить Excel в папку YYYY-MM-DD",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.input:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = (ROOT / input_path).resolve()
    else:
        found = find_newest_inbox_excel()
        if not found:
            print(
                "Ошибка: укажите файл или положите .xlsm в 0_parse-from/",
                file=sys.stderr,
            )
            return 1
        input_path = found
        print(f"Автовыбор файла: {input_path.relative_to(ROOT)}")

    return run_pipeline(
        input_path=input_path,
        group=args.group,
        output_path=Path(args.output),
        archive=not args.no_archive,
    )


if __name__ == "__main__":
    raise SystemExit(main())
