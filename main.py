from PDF import PDF_Class
from Translator import Translator_Class

pdf = PDF_Class("Тест.pdf")
translator = Translator_Class(source_lang='auto', target_lang='ru', prompt='')

# translator.translate_text("Тест")


for page_index in range(pdf.start_page, pdf.pages):
    page_text = pdf.extract_textdata(page_index)
    print(f"Page {page_index}:")
    print(page_text)
    print("\n")
    pdf.insert_text(page_index, translator.translate_text(page_text))
    input("Press Enter to continue...")
    #break  # Удалите эту строку, чтобы обработать все страницы