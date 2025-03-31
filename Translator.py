from g4f.client import Client

class Translator_Class:
    def __init__(self, source_lang='auto', target_lang='ru', prompt=''):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.prompt = prompt
        self.gpt_client = Client()
    
    def translate_text(self, text):
        '''
        Переводит текст с одного языка на другой.
        Возвращает переведенный текст.
        '''
        if not text:
            print("No text to translate!")
            return None
        
        SystemText = "".join([
            "You are a translator of PDF books and documents. Keep in mind that it is impossible to ",
            "extract the entire text safely, so you will receive an array of words and symbols — these ",
            "will be separate text fragments. You have to translate them while keeping them as ",
            "fragments. It is important that the order of the fragments remains the same, and the ",
            "context is clear. The array will contain the full text so that you understand correctly how to ",
            "translate fragments.\n\n",
            "The format of your reply must strictly match the format of the received message! Your ",
            "answer should be exactly the same array, but with the translated text instead of the original!\n\n",
            f"The text is in {self.source_lang} and must be translated into {self.target_lang}.\n\n",
            f"Just for context, about what this PDF file is about: {self.prompt}"
        ])

        print(SystemText)


        
        
        
        return