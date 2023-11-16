import googletrans as gt

class Translator:
    def __init__(self):
        self.translator = gt.Translator()
        self.src_lang = 'en'
        self.dest_lang = 'es'

    def translate_paragraph(self, paragraph):
        translation = self.translator.translate(paragraph, src=self.src_lang, dest=self.dest_lang)
        return translation.text
    