import os
import fitz  # PyMuPDF

def convert_pdfs_to_txt():
    files = os.listdir('.')
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("PDF-файлы не найдены.")
        return

    for pdf_file in pdf_files:
        try:
            print(f"Обработка файла: {pdf_file}...")
            
            # Читаем PDF
            doc = fitz.open(pdf_file)
            full_text = []
            
            # Перебираем все страницы и извлекаем текст
            for page in doc:
                text = page.get_text()
                if text.strip():
                    full_text.append(text.strip())
            
            doc.close()
            
            # Формируем имя для текстового файла
            txt_filename = os.path.splitext(pdf_file)[0] + ".txt"
            
            # Сохраняем результат
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write("\n\n".join(full_text))
                
            print(f"Готово! Текст сохранен в {txt_filename}")
            
        except Exception as e:
            print(f"Ошибка при чтении файла {pdf_file}: {e}")

if __name__ == "__main__":
    convert_pdfs_to_txt()
