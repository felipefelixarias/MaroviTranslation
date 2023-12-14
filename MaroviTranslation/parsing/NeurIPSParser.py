import re
from .core import PDFParser

class NeurIPSParser(PDFParser):
    """Class to parse NeurIPS PDF files. Inherits from PDFParser.
    Note: Likely not to work if used on non-NeurIPS PDF files.

    Attributes
    ----------
    file_path : str
        Path to PDF file.
    doc : fitz.Document 
        PDF document.
    sections : list
        List of sections in the PDF file.
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        self.sections = self.extract_sections()

    def extract_sections(self):
        """Extracts sections from PDF file.

        Returns
        -------
        list
            List of sections in the PDF file. Each section is a list with the section title
            as the first element and the section content as the second element.
        """
        text = self.extract_text()
        pattern = r'\n(\d+(\.\d+)*)\s*([A-Za-z][^\n.]*)?(\n[^\n\d]+)?'
        matches = list(re.finditer(pattern, text))

        # Filter and process sections
        filtered_sections = []
        for match in matches:
            section_number = match.group(1)
            section_title = match.group(3) or (match.group(4).strip() if match.group(4) else '')

            # Apply pre-filtering criteria
            # Title must be between 5 and 50 characters and start with a capital letter
            if len(section_title) > 50 or len(section_title) < 5 or section_title[0].islower():
                continue

            filtered_sections.append((section_number, section_title, match.start(), match.end()))

        processed_sections = self.post_process_sections(filtered_sections)

        # Extract section content
        extracted_sections = []
        for i, (section_number, section_title, start, end) in enumerate(processed_sections):
            start_content = start
            # End of content is start of next title or end of text
            end_content = processed_sections[i + 1][2] if i + 1 < len(processed_sections) else len(text)
            section_content = text[start_content:end_content].strip()

            full_title = f"{section_number} {section_title}"
            #Remove first two lines since they are the title
            section_content = section_content.split('\n', 2)[2:]
            section_content = '\n'.join(section_content)
            extracted_sections.append([full_title, section_content])

        #For last section, remove all lines following "References"
        extracted_sections[-1][1] = extracted_sections[-1][1].split("\nReferences")[0]

        return extracted_sections

    
    def post_process_sections(self, sections_with_spans):
        """Post-processes sections to ensure they follow a logical order.

        Parameters
        ----------
        sections_with_spans : list
            List of tuples with section numbers, titles, and their text spans.

        Returns
        -------
        list
            Filtered and ordered list of section tuples.
        """
        valid_sections = []
        for num, title, start, end in sorted(sections_with_spans, key=lambda x: [int(part) for part in x[0].split('.')]):
            if not valid_sections:
                valid_sections.append((num, title, start, end))
            else:
                # Check for large gap or invalid transition
                if self.is_large_gap(valid_sections[-1][0], num) or not self.is_valid_section_transition(valid_sections[-1][0], num):
                    continue
                valid_sections.append((num, title, start, end))

        return valid_sections