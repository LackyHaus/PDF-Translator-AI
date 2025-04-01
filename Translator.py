from g4f.client import Client
import json

class Translator_Class:
    def __init__(self, source_lang='auto', target_lang='ru', prompt=''):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.prompt = prompt
        self.gpt_client = Client()

        self.Model = 'gpt-4o-mini'
    
    def translate_text(self, input_text):
        '''
        Переводит текст с одного языка на другой.
        Возвращает переведенный текст.
        '''
        if not input_text:
            print("No text to translate!")
            return None
        
        text = str(input_text)
        
        SystemText = "".join([
            "You are a translator of PDF books and documents. Keep in mind that it is impossible to ",
            "extract the entire text safely, so you will receive an array of words and symbols — these ",
            "will be separate text fragments. You have to translate them while keeping them as ",
            "fragments. It is important that the order of the fragments remains the same, and the ",
            "context is clear. The array will contain the full text so that you understand correctly how to ",
            "translate fragments.\n\n",
            "The format of your reply must strictly match the format of the received message! Your ",
            "answer should be exactly the same array, but with the translated text instead of the original!\n",
            "AN EXAMPLE OF YOUR RESPONSE: {'text': ['Hello', 'world!'], 'full_text_page': 'Hello world!'}!!!\n\n",
            f"Just for context, about what this PDF file is about: {self.prompt}"
        ])

        message = [
            {"role": "user", "content": "The text is in auto and must be translated into ru.\nSAVE THE NUMBER OF FRAGMENTS!\n\n{'text': ['Hello', 'world!'], 'full_text_page': 'Hello world!'}"},
            {"role": "assistant", "content":"{'text': ['Привет', 'мир!'], 'full_text_page': 'Привет мир!'}"},
            {"role": "user", "content": "The text is in auto and must be translated into en.\nSAVE THE NUMBER OF FRAGMENTS!\n\n{'text': ['Wie', 'geht es', 'dir?'], 'full_text_page': 'Wie geht es dir?'}"},
            {"role": "assistant", "content":"{'text': ['How', 'are you', 'doing?'], 'full_text_page': 'How are you doing?'}"},
            {"role": "user", "content": "The text is in en and must be translated into ru.\nSAVE THE NUMBER OF FRAGMENTS!\n\n{'text': ['I want to', 'explore', 'the binary search', 'tree.'], 'full_text_page': 'I want to explore the binary search tree.'}"},
            {"role": "assistant", "content":"{'text': ['Я хочу', 'изучить', 'дерево бинарного', 'поиска.'], 'full_text_page': 'Я хочу изучить дерево бинарного поиска.'}"},
            {"role": "user", "content": f"The text is in {self.source_lang} and must be translated into {self.target_lang}.\nSAVE THE NUMBER OF FRAGMENTS!\n\n{text}"}
        ]

        response = self.gpt_client.chat.completions.create(
        model=self.Model,
        messages=[{"role": "system", "content": SystemText}] + message
        )

        print(f"\n\n{response}\n\n")

        response_text = response.choices[0].message.content.strip()
        response_text = response_text.replace("'", '"')
        response_text = response_text.replace("\n", ' ')
        print(type(response_text))
        print(f"\n\ntext: {text}\n\nresponse_text: {response_text}")
        translated_text = json.loads(response_text)


        
        
        
        return translated_text