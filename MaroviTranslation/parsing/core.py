import fitz  # PyMuPDF

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
        """Extracts text from PDF file.

        Returns
        -------
        str
            Text from PDF file.
        """
        text = ""
        for page in self.doc:
            text += page.get_text()
        return text

    def extract_images(self):
        """Extracts images from PDF file.

        Returns
        -------
        list
            List of images from PDF file.
        """
        images = []
        for page_num, page in enumerate(self.doc):
            for img_num, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                images.append(image_bytes)
        return images

    def close(self):
        self.doc.close()
