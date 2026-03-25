import json
import re

notebook_file = "input.ipynb"  # замените на ваш путь
output_file = "clean_notebook.txt"

def clean_line(line):
    """Удаляем лишние спецсимволы JSON/Jupyter, оставляем текст, код и вывод"""
    # Убираем явные JSON-символы, но сохраняем точки, скобки кода, знаки операций
    line = re.sub(r'[\\]+', '', line)  # убираем экранирование
    line = re.sub(r'^\s*[*#^`]+\s*', '', line)  # убираем Markdown спецсимволы в начале
    line = re.sub(r'\s+', ' ', line)  # лишние пробелы
    return line.strip()

with open(notebook_file, "r", encoding="utf-8") as f:
    notebook = json.load(f)

clean_lines = []

for cell in notebook.get("cells", []):
    # Сохраняем все ячейки
    source_lines = cell.get("source", [])
    if not source_lines:
        continue
    for line in source_lines:
        clean_lines.append(clean_line(line))
    
    # Для output в коде (вывод)
    if cell.get("cell_type") == "code" and "outputs" in cell:
        for output in cell["outputs"]:
            # Текстовые выводы
            if "text" in output:
                for line in output["text"]:
                    clean_lines.append(clean_line(line))
            # Вывод в виде data, например stdout/stderr
            if "data" in output:
                for key in ["text/plain", "text/html"]:
                    if key in output["data"]:
                        for line in output["data"][key]:
                            clean_lines.append(clean_line(line))

# Сохраняем в txt
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(clean_lines))

print(f"Чистый текст с кодом и выводами сохранён в {output_file}")