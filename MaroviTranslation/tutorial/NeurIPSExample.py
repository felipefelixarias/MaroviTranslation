from MaroviTranslation.converters.NeurIPS import NeurIPSPDFToSpanishMarkdown
from MaroviTranslation.translation.core import Translator
from MaroviTranslation.translation.GoogleTranslator import GoogleTranslator

# Initialize translator and converter
translator = Translator()
translator.set_translator(GoogleTranslator())
converter = NeurIPSPDFToSpanishMarkdown("MaroviTranslation/pdfs/attention.pdf", "MaroviTranslation/outputs", translator)

# Parse PDF, create image map, and generate Markdown
converter.parse_pdf()
converter.create_image_map()
converter.generate_markdown()