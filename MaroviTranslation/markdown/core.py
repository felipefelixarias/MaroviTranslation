import markdown2 as md2
import os

class Markdown:
    def __init__(self):
        self.content = ""

    def add_title(self, title, level=1):
        self.content += f"{'#' * level} {title}\n\n"

    def add_section(self, section, level=2):
        self.add_title(section, level)

    def add_subsection(self, subsection, level=3):
        self.add_title(subsection, level)

    def add_subsubsection(self, subsubsection, level=4):
        self.add_title(subsubsection, level)

    def add_image(self, image_path, alt_text=""):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        self.content += f"![{alt_text}]({image_path})\n\n"

    def add_equation(self, equation):
        self.content += f"$$\n{equation}\n$$\n\n"

    def add_text(self, text):
        self.content += f"{text}\n\n"

    def save_markdown(self, filename):
        with open(filename, 'w') as file:
            file.write(self.content)