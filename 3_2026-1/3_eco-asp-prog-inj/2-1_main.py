#!/usr/bin/env python3
"""
Генерация горизонтальной PDF-презентации по дисциплине
«Экономические аспекты программной инженерии».

Запуск:
    pip install reportlab
    python main.py
"""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------------------
# Заполните перед запуском
# ---------------------------------------------------------------------------
TEACHER_FIO = "САМЧИНСКАЯ Ярослава Борисовна. Кандидат экономических наук, доцент"  # например: "Иванова И. И."
STUDENT_FIO = "Трифонов Д.С., студент группы 12-25РПм"  # например: "Петров П. П."
TOPIC = "Экономические аспекты программной инженерии"
OUTPUT_PDF = Path(__file__).with_name("presentation.pdf")

# ---------------------------------------------------------------------------
# Оформление
# ---------------------------------------------------------------------------
PAGE = landscape(A4)  # 297 × 210 мм
WIDTH, HEIGHT = PAGE

BG = HexColor("#0F2744")
ACCENT = HexColor("#3D8BDB")
ACCENT_SOFT = HexColor("#1A3A5C")
TITLE_COLOR = white
TEXT_COLOR = HexColor("#E8EEF5")
MUTED = HexColor("#9BB0C7")
CARD_BG = HexColor("#163552")


def register_fonts() -> tuple[str, str]:
    """Подключает системные шрифты с кириллицей (Windows / Linux / macOS)."""
    candidates = [
        (
            Path(r"C:\Windows\Fonts\arial.ttf"),
            Path(r"C:\Windows\Fonts\arialbd.ttf"),
        ),
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ),
        (
            Path("/Library/Fonts/Arial.ttf"),
            Path("/Library/Fonts/Arial Bold.ttf"),
        ),
        (
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ),
    ]
    for regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("AppSans", str(regular)))
            pdfmetrics.registerFont(TTFont("AppSans-Bold", str(bold)))
            return "AppSans", "AppSans-Bold"
    raise FileNotFoundError(
        "Не найден шрифт с кириллицей. Установите Arial или DejaVu Sans."
    )


FONT, FONT_BOLD = register_fonts()


def draw_background(c: canvas.Canvas) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # декоративная полоса слева
    c.setFillColor(ACCENT)
    c.rect(0, 0, 6 * mm, HEIGHT, fill=1, stroke=0)
    # мягкий акцент внизу
    c.setFillColor(ACCENT_SOFT)
    c.rect(0, 0, WIDTH, 8 * mm, fill=1, stroke=0)


def draw_footer(c: canvas.Canvas, page_num: int, total: int) -> None:
    c.setFont(FONT, 9)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, 3 * mm, TOPIC)
    c.drawRightString(WIDTH - 12 * mm, 3 * mm, f"{page_num} / {total}")


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    *,
    font: str,
    size: float,
    color: Color,
    max_width: float,
    leading: float | None = None,
) -> float:
    leading = leading or size * 1.35
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_bullets(
    c: canvas.Canvas,
    items: list[str],
    x: float,
    y: float,
    *,
    max_width: float,
    size: float = 20.8,
    leading: float = 28.8,
    gap: float = 12.8,
) -> float:
    bullet_x = x
    text_x = x + 7 * mm
    for item in items:
        c.setFillColor(ACCENT)
        c.circle(bullet_x + 1.5 * mm, y + size * 0.25, size * 0.17, fill=1, stroke=0)
        y = draw_wrapped(
            c,
            item,
            text_x,
            y,
            font=FONT,
            size=size,
            color=TEXT_COLOR,
            max_width=max_width - 7 * mm,
            leading=leading,
        )
        y -= gap
    return y


def draw_title_block(c: canvas.Canvas, title: str, subtitle: str | None = None) -> float:
    y = HEIGHT - 28 * mm
    y = draw_wrapped(
        c,
        title,
        18 * mm,
        y,
        font=FONT_BOLD,
        size=24,
        color=TITLE_COLOR,
        max_width=WIDTH - 36 * mm,
        leading=30,
    )
    if subtitle:
        y -= 4 * mm
        c.setStrokeColor(ACCENT)
        c.setLineWidth(2)
        c.line(18 * mm, y + 10, 50 * mm, y + 10)
        y -= 4 * mm
        y = draw_wrapped(
            c,
            subtitle,
            18 * mm,
            y,
            font=FONT,
            size=12,
            color=MUTED,
            max_width=WIDTH - 36 * mm,
            leading=16,
        )
    return y - 8 * mm


def slide_title(c: canvas.Canvas) -> None:
    draw_background(c)
    c.setFont(FONT, 12)
    c.setFillColor(ACCENT)
    c.drawString(18 * mm, HEIGHT - 30 * mm, "Практическая работа")

    y = draw_wrapped(
        c,
        TOPIC,
        18 * mm,
        HEIGHT - 48 * mm,
        font=FONT_BOLD,
        size=28,
        color=TITLE_COLOR,
        max_width=WIDTH - 50 * mm,
        leading=34,
    )
    y -= 6 * mm
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2.5)
    c.line(18 * mm, y, 70 * mm, y)

    y -= 20 * mm
    c.setFont(FONT, 13)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, y, "Преподаватель:")
    c.setFont(FONT_BOLD, 16)
    c.setFillColor(TEXT_COLOR)
    c.drawString(18 * mm, y - 9 * mm, TEACHER_FIO)

    y -= 28 * mm
    c.setFont(FONT, 13)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, y, "Студент:")
    c.setFont(FONT_BOLD, 16)
    c.setFillColor(TEXT_COLOR)
    c.drawString(18 * mm, y - 9 * mm, STUDENT_FIO)

    questions = [
        "1) В чем состоит основная идея определения рыночной цены на ПП на основе точки безубыточности?",
        "2) Метрики процесса, метрики проекта, метрики продукта.",
        "3) Обзор основных принципов оценивания стоимости разработки программного обеспечения.",
        "4) Охарактеризуйте основные проблемы ценообразования на ПП.",
    ]
    card_x = 18 * mm
    card_w = WIDTH - 36 * mm
    pad_x = 6 * mm
    pad_y = 5 * mm
    title_size = 14
    q_size = 11
    q_leading = 15
    q_gap = 3
    inner_w = card_w - 2 * pad_x

    # высота: заголовок + вопросы (с переносами) + отступы
    content_h = title_size + 6
    for q in questions:
        content_h += len(wrap_text(q, FONT, q_size, inner_w)) * q_leading + q_gap
    content_h -= q_gap
    card_h = content_h + 2 * pad_y

    y -= 18 * mm
    card_bottom = y - card_h
    c.setFillColor(CARD_BG)
    c.roundRect(card_x, card_bottom, card_w, card_h, 6, fill=1, stroke=0)

    text_y = card_bottom + card_h - pad_y - title_size
    c.setFont(FONT_BOLD, title_size)
    c.setFillColor(ACCENT)
    c.drawString(card_x + pad_x, text_y, "Вопросы")

    text_y -= title_size + 4
    for q in questions:
        text_y = draw_wrapped(
            c,
            q,
            card_x + pad_x,
            text_y,
            font=FONT,
            size=q_size,
            color=TEXT_COLOR,
            max_width=inner_w,
            leading=q_leading,
        )
        text_y -= q_gap


def slide_q1_idea(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "1) В чем состоит основная идея определения рыночной цены на ПП на основе точки безубыточности?",
        "Основная идея подхода",
    )
    draw_bullets(
        c,
        [
            "Точка безубыточности (BEP) — объём продаж, при котором выручка "
            "покрывает все постоянные и переменные затраты.",
            "Рыночная цена задаётся так, чтобы при ожидаемом спросе "
            "обеспечить выход на BEP (или выше) в приемлемый срок.",
            "Цена связывает экономику разработки с рынком: затраты + маржа "
            "должны «окупаться» реалистичным числом лицензий/подписок.",
            "Если цена слишком высока — спрос падает и BEP недостижима; "
            "слишком низка — даже большой объём не покрывает инвестиции.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
    )


def slide_q1_logic(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "1) В чем состоит основная идея определения рыночной цены на ПП на основе точки безубыточности?",
        "Логика расчёта и практический смысл",
    )
    draw_bullets(
        c,
        [
            "Упрощённо: BEP (шт.) ≈ Постоянные затраты / (Цена − Переменные "
            "затраты на единицу).",
            "Отсюда: при известном целевом объёме продаж можно вывести "
            "минимально допустимую цену.",
            "Для ПП постоянные затраты часто велики (разработка, инфраструктура), "
            "а переменные на копию — малы → критична оценка ёмкости рынка.",
            "Идея метода: цена — не «из воздуха», а инструмент достижения "
            "безубыточности при заданных затратах и прогнозе спроса.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
    )


def slide_q2_process(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "2) Метрики процесса, метрики проекта, метрики продукта.",
        "Метрики процесса",
    )
    draw_bullets(
        c,
        [
            "Характеризуют сам процесс разработки и его эффективность "
            "(как работаем), а не только итоговый продукт.",
            "Примеры: длительность циклов, доля дефектов, найденных на этапах; "
            "производительность (LOC/FP на человека-месяц); соблюдение сроков.",
            "Помогают улучшать процесс: выявлять узкие места, сравнивать "
            "практики, оценивать эффект внедрения новых методов.",
            "Используются менеджментом для планирования ресурсов и "
            "управления качеством процесса.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
    )


def slide_q2_project_product(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "2) Метрики процесса, метрики проекта, метрики продукта.",
        "Различие уровней измерения",
    )
    draw_bullets(
        c,
        [
            "Метрики проекта — касаются конкретного проекта: трудозатраты, "
            "бюджет, отклонения от плана, риски, загрузка команды, прогресс.",
            "Цель: контроль сроков/стоимости и принятие управленческих "
            "решений в рамках одного проекта.",
            "Метрики продукта — свойства результата: размер (LOC, FP), "
            "сложность, надёжность, дефектность, удобство сопровождения, "
            "производительность ПО.",
            "Цель: оценка качества и ценности продукта для заказчика/рынка; "
            "сравнение версий и альтернатив.",
            "Связь: метрики продукта и процесса питают оценку стоимости "
            "и ценообразование ПП.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
        size=20,
        leading=27.2,
        gap=9.6,
    )


def slide_q3_principles(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "3) Обзор основных принципов оценивания стоимости разработки программного обеспечения.",
        "Основные принципы",
    )
    draw_bullets(
        c,
        [
            "Опираться на измеримые факторы: объём/сложность, требования, "
            "технологии, опыт команды, ограничения качества и сроков.",
            "Разделять оценки: сверху вниз (аналогии, экспертные) и снизу "
            "вверх (декомпозиция работ, WBS).",
            "Учитывать неопределённость: диапазоны, риски, резервы; "
            "пересматривать оценку по мере уточнения требований.",
            "Связывать оценку с жизненным циклом: ранняя оценка грубее, "
            "поздняя — точнее (конус неопределённости).",
            "Документировать допущения: иначе оценка несопоставима "
            "и непроверяема.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
        size=20,
        leading=27.2,
        gap=9.6,
    )


def slide_q3_methods(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "3) Обзор основных принципов оценивания стоимости разработки программного обеспечения.",
        "Подходы и ориентиры",
    )
    draw_bullets(
        c,
        [
            "Экспертные методы: Delphi, трёхточечная оценка (оптимист / "
            "реалист / пессимист).",
            "Аналоговые и параметрические модели: сравнение с прошлыми "
            "проектами; модели вида COCOMO (стоимость от размера и драйверов).",
            "Оценка через функциональный размер (Function Points) или "
            "User Stories / story points с калибровкой velocity.",
            "Стоимость ≈ трудозатраты × ставка + накладные + риски; "
            "для рынка дополнительно учитывают TCO и модель монетизации.",
            "Принцип: нет «одной верной цифры» — есть обоснованная оценка "
            "при явных предпосылках.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
        size=20,
        leading=27.2,
        gap=9.6,
    )


def slide_q4_pricing(c: canvas.Canvas) -> None:
    draw_background(c)
    y = draw_title_block(
        c,
        "4) Охарактеризуйте основные проблемы ценообразования на ПП.",
        "Ключевые особенности рынка ПО",
    )
    draw_bullets(
        c,
        [
            "Высокие постоянные затраты на создание и низкие предельные "
            "издержки копирования → классическая «себестоимость единицы» "
            "плохо задаёт цену.",
            "Неосязаемость и сложность оценки ценности до использования; "
            "информационная асимметрия между продавцом и покупателем.",
            "Быстрое устаревание, пиратство, конкуренция с open-source "
            "и «бесплатными» моделями (freemium, реклама).",
            "Разнообразие моделей: лицензия, подписка (SaaS), pay-per-use — "
            "цена зависит от сегмента и готовности платить (value-based).",
            "Сетевые эффекты и lock-in искажают «справедливую» цену; "
            "сложно учесть затраты на поддержку и обновления.",
        ],
        36 * mm,
        y,
        max_width=WIDTH - 42 * mm,
        size=20,
        leading=27.2,
        gap=9.6,
    )


def slide_thanks(c: canvas.Canvas) -> None:
    draw_background(c)
    text = "Благодарю за внимание!"
    c.setFont(FONT_BOLD, 36)
    c.setFillColor(TITLE_COLOR)
    tw = pdfmetrics.stringWidth(text, FONT_BOLD, 36)
    c.drawString((WIDTH - tw) / 2, HEIGHT / 2 + 4 * mm, text)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2.5)
    line_w = 40 * mm
    c.line((WIDTH - line_w) / 2, HEIGHT / 2 - 4 * mm, (WIDTH + line_w) / 2, HEIGHT / 2 - 4 * mm)
    c.setFont(FONT, 12)
    c.setFillColor(MUTED)
    sub = TOPIC
    sw = pdfmetrics.stringWidth(sub, FONT, 12)
    c.drawString((WIDTH - sw) / 2, HEIGHT / 2 - 16 * mm, sub)


def build_presentation(path: Path) -> None:
    slides = [
        slide_title,
        slide_q1_idea,
        slide_q1_logic,
        slide_q2_process,
        slide_q2_project_product,
        slide_q3_principles,
        slide_q3_methods,
        slide_q4_pricing,
        slide_thanks,
    ]
    total = len(slides)
    c = canvas.Canvas(str(path), pagesize=PAGE)
    c.setTitle(TOPIC)
    c.setAuthor(STUDENT_FIO)

    for i, slide in enumerate(slides, start=1):
        slide(c)
        draw_footer(c, i, total)
        c.showPage()

    c.save()
    print(f"Готово: {path.resolve()} ({total} слайдов)")


if __name__ == "__main__":
    build_presentation(OUTPUT_PDF)
