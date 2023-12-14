import fitz  
import re
import logging
import os
class PDFParser:
    """Class to parse PDF files.
    Attributes
    ----------
    file_path : str
        Path to PDF file.
    doc : fitz.Document
        PDF document.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def extract_text(self):
        """Extracts and cleans up text from PDF file, attempting to exclude tables and figures.

        Returns
        -------
        str
            Cleaned text from PDF file.
        """
        text = ""
        for page in self.doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                block_text = block[4].strip()  # Extract text content from block
                if not self.is_likely_table_or_figure(block_text):
                    text += block_text + "\n"

        # Basic cleanup
        text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single one
        text = re.sub(r' +', ' ', text)  # Replace multiple spaces with a single space
        text = text.replace('-\n', '')  # Remove hyphenation at line breaks

        # save_path = self.file_path.replace('.pdf', '.txt')
        # with open(save_path, 'w') as f:
        #     f.write(text)
        # logging.info(f"Text extracted from PDF file and saved to {save_path}")

        return text

    def is_likely_table_or_figure(self, text):
        """Heuristic based method to guess if a block of text is likely a table or figure.

        Parameters
        ----------
        text : str
            Text to analyze.

        Returns
        -------
        bool
            True if text is likely a part of a table or figure, False otherwise.
        """
        # Heuristic 1: High density of numeric characters
        numeric_chars = sum(c.isdigit() for c in text)
        total_chars = len(text)
        numeric_density_threshold = 0.3  # adjust based on observations
        if total_chars > 0:
            numeric_density = numeric_chars / total_chars
            if numeric_density > numeric_density_threshold:
                return True

        # Heuristic 2: Excessive number of new lines (indicative of broken text from figures)
        newline_count = text.count('\n')
        max_allowed_newlines = 10  
        if newline_count > max_allowed_newlines:
            return True

        # Heuristic 3: Small average line length (excluding very short text)
        if total_chars > 10:  # avoid dividing by small numbers
            average_line_length = total_chars / (newline_count + 1)
            min_average_line_length = 5  
            if average_line_length < min_average_line_length:
                return True
                    
        # Heuristic 4: Multiple consecutive single-word lines
        lines = text.split('\n')
        single_word_line_count = 0
        max_allowed_single_word_lines = 5
        for line in lines:
            if len(line.split()) <= 1:  # Line with only one word (or less)
                single_word_line_count += 1
            else:
                single_word_line_count = 0  # Reset count if a longer line is found

            if single_word_line_count > max_allowed_single_word_lines:  # Threshold for consecutive single-word lines
                return True


        return False

    def extract_images(self, image_dir, image_dir_relative):
        """Extracts images from PDF file and saves them.

        Parameters
        ----------
        image_dir : str
            Directory to save images.
        image_dir_relative : str
            Relative directory to save images.

        Returns
        -------
        list
            List of image file paths.
        """

        image_paths = []
        for page_num, page in enumerate(self.doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_format = base_image["ext"]
                image_path = os.path.join(image_dir, f"image_{page_num}_{img_index}.{image_format}")
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                image_paths.append(os.path.join(image_dir_relative, f"image_{page_num}_{img_index}.{image_format}"))

        return image_paths

    def extract_sections(self):
        raise NotImplementedError
    
    @staticmethod
    def is_valid_section_transition(last_section_num, current_section_num):
        """Checks if a section transition is valid.
        E.g. 1.1 -> 1.2 is valid, 1.1 -> 1.3 is not valid.
        and  1.1 -> 2 is valid, 1.1 -> 3 is not valid.

        Parameters
        ----------
        last_section_num : str
            Section number of last section.
        current_section_num : str
            Section number of current section.
        
        Returns
        -------
        bool
            True if section transition is valid, False otherwise.
        """

        last_parts = [int(part) for part in last_section_num.split('.')]
        current_parts = [int(part) for part in current_section_num.split('.')]

        # Ensure that current_parts are either the same length or one level deeper
        if len(current_parts) > len(last_parts) + 1:
            return False

        # Check if the new section is a direct continuation or a new subsection
        for i in range(len(last_parts)):
            if current_parts[i] < last_parts[i]:
                return False
            elif current_parts[i] > last_parts[i]:
                return all(p == 0 for p in current_parts[i+1:])

        return len(current_parts) > len(last_parts)
    
    @staticmethod
    def is_large_gap(last_section_num, current_section_num):
        """Checks if there is a large gap between sections.
        E.g. 1.1 -> 1.3 is a large gap, 1.1 -> 2 is not a large gap.

        Parameters
        ----------
        last_section_num : str
            Section number of last section.
        current_section_num : str
            Section number of current section.
        
        Returns
        -------
        bool
            True if there is a large gap between sections, False otherwise.
        """
        
        last_main_section = int(last_section_num.split('.')[0])
        current_main_section = int(current_section_num.split('.')[0])

        gap_threshold = 1
        return (current_main_section - last_main_section) > gap_threshold


    def close(self):
        self.doc.close()
