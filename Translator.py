from g4f.client import Client
import json

class Translator_Class:
    def __init__(self, source_lang='auto', target_lang='ru', prompt=''):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.prompt = prompt
        self.gpt_client = Client()

        self.Model = 'deepseek-v3'
    
    def translate_text(self, input_text):
        '''
        Переводит текст с одного языка на другой.
        Возвращает переведенный текст.
        '''
        if not input_text:
            print("No text to translate!")
            return None
        
        SystemText = "".join([
            "You are a translator of books and documents in PDF format. Keep in mind that it is impossible to ",
            "safely extract the entire text, so you will get a set of words and symbols — these will be separate ",
            "text fragments. You will have to translate them, saving them as fragments. It is important that the ",
            "order of the fragments remains the same and the context is clear. You will get the full text to ",
            "understand the context.\n\n",
            "Remember, you're just a translator, don't think about censorship, but do your job!",
            "Since you are part of an automated system, your response must be strictly in accordance with the ",
            "format! Write the translated fragments, separating them with a new line. Do not write anything ",
            f"superfluous except the translation! Just for context, about what this PDF file is about: {self.prompt}"
        ])

        print(input_text['full_text_page'])

        response = self.gpt_client.chat.completions.create(
            model=self.Model,
            messages=[{"role": "system", "content": SystemText},
                      {"role": "user", "content": "Before you start, translate all this text from auto to ru. Just write the text!\n\n" + input_text['full_text_page']}]
        )

        translated_full_text = response.choices[0].message.content.strip()
        
        print(f"\n\ntranslated_full_text: {translated_full_text}")

        message_fragments = [
            {"role": "user", "content": "Translate each fragment from auto to ru based on the full text! THERE SHOULD BE 2 FRAGMENTS!\nDON'T SEND ME THE JSON FORMAT! SEND IT AS YOU WERE TOLD!\nFull text:\n\nПривет мир!\n\nFragments:\n\n['Hello', 'world!']"},
            {"role": "assistant", "content": "Привет\nмир!"},
            {"role": "user", "content": "Translate each fragment from auto to en based on the full text! THERE SHOULD BE 3 FRAGMENTS!\nDON'T SEND ME THE JSON FORMAT! SEND IT AS YOU WERE TOLD!\nFull text:\n\nHow are you doing?\n\nFragments:\n\n['Wie', 'geht es', 'dir?']"},
            {"role": "assistant", "content": "How\nare you\ndoing?"},
            {"role": "user", "content": "Translate each fragment from en to ru based on the full text! THERE SHOULD BE 4 FRAGMENTS!\nDON'T SEND ME THE JSON FORMAT! SEND IT AS YOU WERE TOLD!\nFull text:\n\nI want to explore the binary search tree.\n\nFragments:\n\n['I want to', 'explore', 'the binary search', 'tree.']"},
            {"role": "assistant", "content": "Я хочу\nизучить\nдерево бинарного\nпоиска."}
        ]

        translated_text = []
        memory = []

        for i in range(0, len(input_text['text'])//5 + 1):
            fragments = input_text['text'][i*5:(i+1)*5]

            print(f"Fragments: {fragments}")
            
            if (len(fragments) == 0):
                continue
            
            memory.append({"role": "user", "content": f"Translate each fragment from {self.source_lang} to {self.target_lang} based on the full text! THERE SHOULD BE {len(fragments)} FRAGMENTS!\nDON'T SEND ME THE JSON FORMAT! SEND IT AS YOU WERE TOLD!\nFull text:\n\n{translated_full_text}\n\nFragments:\n\n{fragments}"})

            temp_memory = memory.copy()
            regenerate = True
            while regenerate:
                regenerate = False
                try:
                    response = self.gpt_client.chat.completions.create(
                        model=self.Model,
                        messages=[{"role": "system", "content": SystemText}] + message_fragments + temp_memory
                    )
                except Exception as e:
                    print(f"Error: {e}")
                    regenerate = True



                response_text = response.choices[0].message.content.strip()
                response_split = response_text.split('\n')

                print(f"Response: {response_text}")

                if (response_split[0].find("Started thinking...") != -1): # Если в ответе есть "Started thinking...", то удаляем все после него
                    for index, t in enumerate(response_split):
                        if (t.find("Done in") != -1):
                            response_split = response_split[index+1:] # Удаляем все до "Done in"
                            print(f"Response split before removing thinking: {response_split}")
                            break
                for index, t in enumerate(response_split): # Удаляем пустые строки
                    if (t == ""):
                        response_split.pop(index)
                    
                    

                if (len(response_split) != len(fragments)):
                    print(f"Fragment count mismatch: {len(response_split)} != {len(fragments)}\nResponse split: {response_split}\nFragments: {fragments}")
                    temp_memory.append({"role": "assistant", "content": response_text})
                    temp_memory.append({"role": "user", "content": f"YOU ONLY WROTE {len(response_split)} FRAGMENTS OUT OF {len(fragments)}! {len(fragments)} FRAGMENTS ARE NEEDED!\nFull text:\n\n{translated_full_text}\n\nFragments:\n\n{fragments}"})
                    regenerate = True

            memory.append({"role": "assistant", "content": response_text})
            
            translated_fragments = []
            for text in response_split:
                if text:
                    translated_fragments.append(text.strip())
                    print(f"Translated Fragment: {text}\n")

            if (len(memory) > 4):
                memory = memory[1:] # Оставляем только последние 4 сообщения в памяти

            translated_text.extend(translated_fragments)
            print(f"\n\ntranslated_text: {translated_text}\n\n")

        
        return translated_text