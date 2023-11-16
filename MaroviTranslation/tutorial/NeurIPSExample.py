from MaroviTranslation.parsing.NeurIPSParser import NeurIPSParser
from MaroviTranslation.markdown.core import Markdown
from MaroviTranslation.translation.core import Translator


neurips_paper = NeurIPSParser("MaroviTranslation/pdfs/attention.pdf")

# Extracting Introduction section
introduction = neurips_paper.extract_section("Introduction")
print(introduction)

neurips_paper.close()

# Creating Markdown file
markdown = Markdown()
markdown.add_section("Introduction")
markdown.add_text(introduction)
markdown.save_markdown("MaroviTranslation/outputs/attention.md")

# Translating pdf
translator = Translator()
translated_introduction = translator.translate_paragraph(introduction)
markdown = Markdown()
markdown.add_section("Introducción")
markdown.add_text(translated_introduction)
markdown.save_markdown("MaroviTranslation/outputs/atencion.md")