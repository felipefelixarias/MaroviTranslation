class Translator:
    """Class to translate text, parent class to use with different translation APIs.
    Attributes
    ----------
    translator : None
        Translator object from translation API.
    src_lang : str
        Source language.
    dest_lang : str
        Destination language.
    """
    def __init__(self):
        self.translator = None
        self.src_lang = 'en'
        self.dest_lang = 'es'

    def set_translator(self, translator):
        """Set translator object from translation API.
        Parameters
        ----------
        translator : object
            Translator object from translation API.
        """
        self.translator = translator

    def translate(self, text):
        """Translate text from source language to destination language.
        Parameters
        ----------
        text : str
            Text to translate.
        Returns
        -------
        str
            Translated text.
        """
        if self.translator is None:
            raise NotImplementedError('Translator not implemented')
    
        return self.translator.translate(text)
    
    