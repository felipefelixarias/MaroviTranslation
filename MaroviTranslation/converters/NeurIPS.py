import os
import re
from MaroviTranslation.parsing.NeurIPSParser import NeurIPSParser
from MaroviTranslation.markdown.core import Markdown

class NeurIPSPDFToSpanishMarkdown:
    """Class to convert a NeurIPS PDF to a Spanish Markdown file.

    Attributes
    ----------
    pdf_path : str
        Path to the PDF file.
    output_dir : str
        Path to the output directory.
    translator : Translator
        Translator object used to translate the text.
    project_name : str
        Name of the project.
    image_dir : str
        Path to the image directory.
    image_dir_relative : str
        Relative path to the image directory.
    output_md_en : str
        Path to the output English Markdown file.
    output_md_es : str
        Path to the output Spanish Markdown file.
    image_map : dict
        Dictionary mapping image tags to image paths.
    pattern : str   
        Regex pattern for image tags.
    """
    def __init__(self, pdf_path, output_dir, translator):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.translator = translator
        self.project_name = os.path.basename(pdf_path).split('.')[0]
        self.image_dir = os.path.join(output_dir, f"{self.project_name}_images")
        self.image_dir_relative = f"{self.project_name}_images"
        self.output_md_en = os.path.join(output_dir, f"{self.project_name}_en.md")
        self.output_md_es = os.path.join(output_dir, f"{self.project_name}_es.md")
        self.image_map = {}
        self.pattern = r"<image: .+?>|<Imagen: .+?>"

        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def parse_pdf(self):
        """Parses the PDF file and extracts the images."""
        parser = NeurIPSParser(self.pdf_path)
        self.sections = parser.sections
        self.image_paths = parser.extract_images(self.image_dir, self.image_dir_relative)
        parser.close()

    def create_image_map(self):
        """Creates a dictionary mapping image tags to image paths."""
        self.image_map = {f'image_{i}': f'![Image {i}]({path})' for i, path in enumerate(self.image_paths)}

    def convert_images_to_html_with_width(self, text, width=300):
        """Converts image tags to HTML tags with a specified width.

        Parameters
        ----------
        text : str
            Text to convert.
        width : int
            Width of the image.
        
        Returns
        -------
        str
            Converted text.
        """
        def replace_md_with_html(match):
            alt_text, img_src = match.groups()
            return f'\n<img src="{img_src}" alt="{alt_text}" width="{width}px">\n'

        pattern = r'!\[(.*?)\]\((.*?)\)'
        return re.sub(pattern, replace_md_with_html, text)

    def generate_markdown(self):
        """Generates the Markdown files."""
        markdown_en = Markdown()
        markdown_es = Markdown()

        for title, section_data in self.sections:
            spanish_title = self.translator.translate(title)
            if not spanish_title:
                spanish_title = title

            num_periods = title.count('.')
            markdown_en.add_title(title, level=num_periods+2)
            markdown_es.add_title(spanish_title, level=num_periods+2)

            if section_data:
                section_data = section_data.replace('\n', ' ')
                section_data_en = self.convert_images_to_html_with_width(
                    markdown_en.replace_image_tags(section_data, self.image_map, self.pattern))
                markdown_en.add_text(section_data_en)

                section_data_es = self.convert_images_to_html_with_width(
                    markdown_es.replace_image_tags(self.translator.translate(section_data), self.image_map, self.pattern))
                markdown_es.add_text(section_data_es)

        markdown_en.save_markdown(self.output_md_en)
        markdown_es.save_markdown(self.output_md_es)