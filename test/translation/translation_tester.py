import unittest
from unittest.mock import Mock, patch
from MaroviTranslation.translation.core import Translator
from MaroviTranslation.translation.GoogleTranslator import GoogleTranslator

class TestCore(unittest.TestCase):
    def test_setter(self):
        trans = Translator()
        mock_trans = Mock()
        trans.set_translator(mock_trans)
        self.assertEqual(trans.translator, mock_trans)

    def test_not_implemented(self):
        trans = Translator()
        with self.assertRaises(NotImplementedError):
            trans.translate("Hello")


class TestGoogleTranslation(unittest.TestCase):
    @patch('googletrans.Translator')
    def basic_test(self, MockGTrans):
        mock_trans = MockGTrans.return_value
        mock_trans.translate.return_value.text = "Hola"

        gTrans = GoogleTranslator()
        result = gTrans.translate("Hello")

        self.assertEqual(result, "Hola")
        mock_trans.translate.assert_called_once_with("Hello", src='en', dest='es')


if __name__ == "__main__":
    unittest.main()
