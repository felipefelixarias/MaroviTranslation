from .core import PDFParser

class NeurIPSParser(PDFParser):
    def extract_section(self, section_title):
        text = self.extract_text()
        start_idx = text.find(section_title)
        end_idx = text.find("Background", start_idx)
        return text[start_idx:end_idx]