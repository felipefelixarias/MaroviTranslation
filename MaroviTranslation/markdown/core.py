import markdown2 as md2
import os
import re

class Markdown:
    def __init__(self):
        """Class to generate and save Markdown files.
        Attributes
        ----------
        content : str
            Markdown content.
        """
        self.content = ""
        self.image_counter = 0

    def add_title(self, title, level=1):
        """Adds a title to the Markdown file.
        Parameters
        ----------
        title : str
            Title text.
        level : int
            Title level, from 1 to 6.
        """
        self.content += f"{'#' * level} {title}\n\n"

    def add_image(self, image_path, alt_text=""):
        """Adds an image to the Markdown file.

        Parameters
        ----------
        image_path : str
            Path to image file.
        alt_text : str, optional
            Alternative text for image, by default "".

        Raises
        ------
        FileNotFoundError
            _description_
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        self.content += f"![{alt_text}]({image_path})"

    def add_equation(self, equation):
        """Adds an equation to the Markdown file.

        Parameters
        ----------
        equation : str
            LaTeX equation string.
        """
        self.content += f"$$\n{equation}\n$$\n\n"

    def add_text(self, text, image_map=None, pattern=None):
        """Adds text to the Markdown file.

        Parameters
        ----------
        text : str
            Text to add.
        image_map : dict, optional
            Map of image tags to Markdown image syntax, by default None.
        """
        if image_map:
            text = self.replace_image_tags(text, image_map, pattern)
        self.content += f"{text}\n\n"

    def replace_image_tags(self, text, image_map, pattern):
        """Replaces image tags with Markdown image syntax.

        Parameters
        ----------
        text : str
            Text to replace image tags in.
        image_map : dict
            Map of image tags to Markdown image syntax.
        pattern : str
            Regular expression pattern to match image tags.
            
        Returns
        -------
        str
            Text with image tags replaced.
        """
        def replace_func(match):
            img_tag = f'image_{self.image_counter}'
            self.image_counter += 1  # Increment the counter after each match
            return image_map.get(img_tag, "")
        return re.sub(pattern, replace_func, text)
    
    def save_markdown(self, filename):
        """Saves the Markdown file.

        Parameters
        ----------
        filename : str
            Path to save Markdown file to.
        """
        with open(filename, 'w') as file:
            file.write(self.content)