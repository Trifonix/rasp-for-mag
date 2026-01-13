import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

# --- 1. Регистрация шрифтов ---
fonts_dir = r"C:\Windows\Fonts"
font_regular = os.path.join(fonts_dir, "times.ttf")
font_bold = os.path.join(fonts_dir, "timesbd.ttf")

pdfmetrics.registerFont(TTFont('TimesNewRoman', font_regular))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', font_bold))
pdfmetrics.registerFontFamily('TimesNewRoman', normal='TimesNewRoman', bold='TimesNewRoman-Bold')

# --- 2. Загрузка ДВУХ файлов ---
with open("title.json", "r", encoding="utf-8") as f:
    title_data = json.load(f)

with open("report.json", "r", encoding="utf-8") as f:
    report_data = json.load(f)

# --- 3. Настройка PDF ---
pdf_file = "Report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=20, leftMargin=60, topMargin=40, bottomMargin=40)
story = []

# --- 4. Стили ---
styles = {
    'Info': ParagraphStyle('Info', fontName='TimesNewRoman', fontSize=14, alignment=TA_CENTER, leading=14),
    'Subject': ParagraphStyle('Subject', fontName='TimesNewRoman-Bold', fontSize=14, alignment=TA_CENTER, leading=16, spaceBefore=16),
    'Title': ParagraphStyle('Title', fontName='TimesNewRoman-Bold', fontSize=18, alignment=TA_CENTER, leading=22, spaceAfter=16),
    'Header': ParagraphStyle('Header', fontName='TimesNewRoman-Bold', fontSize=16, spaceBefore=18, spaceAfter=12, leading=18, keepWithNext=True),
    'SubHeader': ParagraphStyle('SubHeader', fontName='TimesNewRoman-Bold', fontSize=14, spaceBefore=12, spaceAfter=10, keepWithNext=True),
    'Normal': ParagraphStyle('Normal', fontName='TimesNewRoman', fontSize=14, alignment=TA_JUSTIFY, leading=16, spaceAfter=10),
    'RightAlignBlock': ParagraphStyle('RightAlignBlock', fontName='TimesNewRoman', fontSize=16, alignment=TA_LEFT, leading=14)
}

# --- 5. Функция титульного листа ---
def add_title_page(info):
    story.append(Paragraph(info['institution'], styles['Info']))
    story.append(Paragraph(info['specialty'].replace('\n', '<br/>'), styles['Info']))
    story.append(Paragraph(info['study_form'], styles['Info']))
    story.append(Paragraph(info['course'], styles['Info']))
    story.append(Paragraph(info['city'], styles['Info']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(info['subject'].replace('\n', '<br/>'), styles['Subject']))
    story.append(Spacer(1, 60))

    student_t = info['student'].replace('\n', '<br/>')
    teacher_t = info['teacher'].replace('\n', '<br/>')
    table_data = [['', Paragraph(student_t, styles['RightAlignBlock'])], ['', Spacer(1, 15)], ['', Paragraph(teacher_t, styles['RightAlignBlock'])]]
    t = Table(table_data, colWidths=[200, 280])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (1, 0), (1, -1), 0), # Убираем лишние отступы внутри ячейки
    ]))
    story.append(t)
    story.append(Spacer(1, 40))

# --- 6. Функции контента с защитой от разрыва ---
def create_list(items):
    flow_items = [ListItem(Paragraph(str(i), styles['Normal'])) for i in items]
    return ListFlowable(flow_items, bulletType='bullet', bulletText='\u2022', 
                              leftIndent=35, bulletIndent=20, spaceBefore=5, spaceAfter=10)

def create_numbered_list(items):
    flow_items = []
    for i in items:
        text = str(i).replace('\n', '<br/>')
        flow_items.append(ListItem(Paragraph(text, styles['Normal'])))
    return ListFlowable(
        flow_items,
        bulletType='1',   # нумерация
        start='1',
        leftIndent=35,
        bulletIndent=20,
        spaceBefore=5,
        spaceAfter=10
    )

def process_section(section):
    section_elements = [] # Временный список для текущей секции
    
    if 'header' in section:
        section_elements.append(Paragraph(section['header'], styles['Header']))
    
    if 'content' in section:
        if isinstance(section['content'], list):
            section_elements.append(create_list(section['content']))
        else:
            section_elements.append(
                Paragraph(str(section['content']).replace('\n', '<br/>'), styles['Normal'])
            )

    if 'content-ordered' in section:
        section_elements.append(create_numbered_list(section['content-ordered']))

    
    # Оборачиваем заголовок + основной текст в KeepTogether, чтобы они не разрывались
    story.append(KeepTogether(section_elements))

    if 'subsections' in section:
        for sub in section['subsections']:
            sub_elements = []
            if 'subheader' in sub:
                sub_elements.append(Paragraph(sub['subheader'], styles['SubHeader']))
            if 'content' in sub:
                if isinstance(sub['content'], list):
                    sub_elements.append(create_list(sub['content']))
                else:
                    sub_elements.append(
                        Paragraph(str(sub['content']).replace('\n', '<br/>'), styles['Normal'])
                    )

            if 'content-ordered' in sub:
                sub_elements.append(create_numbered_list(sub['content-ordered']))
            
            if 'factors' in sub:
                sub_elements.append(Paragraph("<b>Ключевые факторы системы:</b>", styles['Normal']))
                sub_elements.append(create_list(sub['factors']))
            
            if 'relations' in sub:
                sub_elements.append(Paragraph("<b>Причинно-следственные связи:</b>", styles['Normal']))
                sub_elements.append(create_list(sub['relations']))
            
            # Оборачиваем подсекцию, чтобы она не разрывалась
            story.append(KeepTogether(sub_elements))

# --- 7. Запуск сборки ---
add_title_page(title_data)
story.append(Paragraph(report_data.get("title", ""), styles['Title']))

for section in report_data.get("sections", []):
    process_section(section)

doc.build(story)
print(f"Готово! Полный отчет сохранен в {pdf_file}")
