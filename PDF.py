import hashlib
import os
import fitz  # PyMuPDF

class PDF_Class:
    def __init__(self, input_pdf:str):
        self.pdf_file = os.path.join("Book", input_pdf) # Путь в папку Book к PDF-файлу
        self.output_pdf = os.path.join("Book", hashlib.md5(self.pdf_file.encode()).hexdigest() + ".pdf") # Путь в папку Book к выходному PDF-файлу, имя хешируется
        self._font_path = "arialnarrow_bold.ttf"  # Путь к шрифту, который вы хотите использовать
        self.start_page = 1
        self.pages = self.get_pages()

        if os.path.exists(self.output_pdf): # Меняем начальную страницу, если файл уже существует
            doc = fitz.open(self.output_pdf)
            page_count = doc.page_count
            doc.close()
            self.start_page = page_count

    
    def get_pages(self):
        '''
        Возвращает количество страниц в PDF-файле.
        '''
        doc = fitz.open(self.pdf_file)
        page_count = doc.page_count
        doc.close()
        return page_count + 1

    def extract_textdata(self, page_index:int):
        '''
        Извлекает текстовые данные с указанной страницы PDF-файла.
        Возвращает словарь с текстовыми данными и их атрибутами.
        '''
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(page_index - 1)
        page_text_data = {}
        text_instances = page.get_text("dict")
        full_text_page = page.get_text("text")
        page_text_data["text_data"] = []
        
        if not text_instances.get("blocks"):
            return None
        
        for block in text_instances["blocks"]: 
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_data = []
                for span in line["spans"]:
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    line_data.append({
                        'text': text,
                        'bbox': span["bbox"],
                        'origin': span["origin"],
                        'fontsize': span["size"],
                        'color': span["color"]
                    })
                if line_data:
                    page_text_data['text_data'].extend(line_data)
        
        page_text_data["full_text_page"] = full_text_page.strip()
        
        # DeBug
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(str(page_text_data))
        
        doc.close()
        return page_text_data # Возвращает словарь с текстовыми данными и их атрибутами

    def insert_text(self, page_index:int, text_data:dict):
        '''
        Вставляет текст на указанную страницу PDF-файла.
        Удаляет оригинальный текст и добавляет новый.'
        '''
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(page_index - 1)  # загрузка конкретной страницы
        
        if text_data is not None:

            # Удаление оригинального текста
            for item in text_data['text_data']:
                rect = fitz.Rect(item['bbox'])
                page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()

            page.insert_font(fontfile=self._font_path, fontname="F0")
            
            # Вставка текста
            for item in text_data['text_data']:
                x0, y0 = item['origin']
                fontsize = item['fontsize']
                color = item['color']
                text = item['text']
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                normalized_color = (r / 255, g / 255, b / 255)
                page.insert_text((x0, y0), text, fontname="F0", fontsize=fontsize, color=normalized_color)
        
        # Создаем новый документ с одной страницей
        page_doc = fitz.open()
        page_doc.insert_pdf(doc, from_page=page_index - 1, to_page=page_index - 1)
        doc.close()
        
        if os.path.exists(self.output_pdf): # Если файл уже существует, добавляем страницу в конец
            existing_doc = fitz.open(self.output_pdf)
            existing_doc.insert_pdf(page_doc)
            existing_doc.save(self.output_pdf, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            existing_doc.close()
            action_msg = f"Страница {page_index} добавлена в {self.output_pdf}"
        else: # Если файл не существует, сохраняем новый файл
            page_doc.save(self.output_pdf)
            action_msg = f"Страница {page_index} скопирована в {self.output_pdf}"
        page_doc.close()
        
        print(action_msg)

