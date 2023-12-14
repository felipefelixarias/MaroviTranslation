import googletrans as gt
from .core import Translator

class GoogleTranslator(Translator):
    """Class to translate text from one language to another using googletrans library
    Attributes
    ----------
    translator : gt.Translator
        Translator object from googletrans library.
    src_lang : str
        Source language.
    dest_lang : str
        Destination language.
    """
    def __init__(self):
        super().__init__()
        self.translator = gt.Translator()

    def translate(self, text):
        """Translates text from one language to another.
        Parameters
        ----------
        paragraph : str
            Text to translate.

        Returns
        -------
        str
            Translated text.
        """
        translation = self.translator.translate(text, src=self.src_lang, dest=self.dest_lang)
        return translation.text
    