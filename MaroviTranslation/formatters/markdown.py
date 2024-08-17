from typing import Optional, List, Dict, Any

import re
import json

class ContentElement:
    """
    Represents a content element in a document, such as a paragraph or an image.

    Attributes:
        element_type (str): The type of the content element, e.g., 'paragraph', 'image'.
        text (Optional[str]): The textual content of the element, if applicable.
        path (Optional[str]): The file path of the image, if the element is an image.
        description (Optional[str]): The description of the image, if the element is an image.
        metadata (Dict[str, Any]): Additional metadata associated with the element.
    """

    def __init__(self, 
                 element_type: str, 
                 text: Optional[str] = None, 
                 path: Optional[str] = None,
                 description: Optional[str] = None, 
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initializes a ContentElement with the given attributes.

        Args:
            element_type (str): The type of the content element, e.g., 'paragraph', 'image'.
            text (Optional[str]): The textual content of the element, if applicable.
            path (Optional[str]): The file path of the image, if the element is an image.
            description (Optional[str]): The description of the image, if the element is an image.
            metadata (Optional[Dict[str, Any]]): Additional metadata associated with the element.
        """
        self.element_type = element_type
        self.text = text
        self.path = path
        self.description = description
        self.metadata = metadata if metadata is not None else {}

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the ContentElement to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the ContentElement.
        """
        return {
            "type": self.element_type,
            "text": self.text,
            "path": self.path,
            "description": self.description,
            "metadata": self.metadata
        }

    def to_markdown(self) -> str:
        """
        Converts the ContentElement to a Markdown string.

        Returns:
            str: A string representing the ContentElement in Markdown format.
        """
        if self.element_type == 'paragraph':
            return f"{self.text}\n\n" if self.text else ''
        elif self.element_type == 'image':
            return f"![{self.description}]({self.path})\n\n" if self.path and self.description else ''
        return ''

    def __repr__(self) -> str:
        """
        Returns a string representation of the ContentElement.

        Returns:
            str: A string representation of the ContentElement.
        """
        return (f"ContentElement(element_type={self.element_type!r}, text={self.text!r}, "
                f"path={self.path!r}, description={self.description!r}, metadata={self.metadata!r})")

class Section:
    """
    Represents a section of a document, which can contain content elements and subsections.

    Attributes:
        title (str): The title of the section.
        content (List[ContentElement]): A list of content elements within the section.
        subsections (List['Section']): A list of subsections within the section.
    """

    def __init__(self, title: str):
        """
        Initializes a Section with a title, an empty content list, and an empty subsections list.

        Args:
            title (str): The title of the section.
        """
        self.title = title
        self.content: List[ContentElement] = []
        self.subsections: List[Section] = []

    def add_content(self, content_element: ContentElement) -> None:
        """
        Adds a content element to the section.

        Args:
            content_element (ContentElement): The content element to add to the section.
        """
        self.content.append(content_element)

    def add_subsection(self, subsection: 'Section') -> None:
        """
        Adds a subsection to the section.

        Args:
            subsection (Section): The subsection to add.
        """
        self.subsections.append(subsection)

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the Section and its subsections to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the Section.
        """
        return {
            "title": self.title,
            "content": [elem.to_json() for elem in self.content],
            "subsections": [sub.to_json() for sub in self.subsections]
        }

    def to_markdown(self, level: int = 1, section_number: str = '') -> str:
        """
        Converts the Section and its subsections to a Markdown string.

        Args:
            level (int): The heading level for this section. Default is 1.
            section_number (str): The section number for this section (e.g., '1.2.5'). Default is ''.

        Returns:
            str: A string representing the Section in Markdown format.
        """
        # Construct the heading for the section, with optional section numbering
        heading = f"{self.title}"
        md = f"{'#' * level} {heading}\n"

        # Add content elements
        for elem in self.content:
            md += elem.to_markdown()

        # Add subsections, recursively incrementing the heading level and section numbering
        for index, sub in enumerate(self.subsections, start=1):
            sub_section_number = f"{section_number}{index}." if section_number else f"{index}."
            md += sub.to_markdown(level=level + 1, section_number=sub_section_number)
        
        return md

    def __repr__(self) -> str:
        """
        Returns a string representation of the Section.

        Returns:
            str: A string representation of the Section.
        """
        return f"Section(title={self.title!r}, content={len(self.content)} elements, subsections={len(self.subsections)})"

class Document:
    def __init__(self):
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def to_json(self):
        return [section.to_json() for section in self.sections]

    def to_markdown(self):
        return ''.join(section.to_markdown() for section in self.sections)

    def save_as_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return Document.from_json(data)

    @staticmethod
    def from_json(json_data):
        doc = Document()
        for section_data in json_data:
            section = Section(section_data['title'])
            for content_data in section_data['content']:
                elem = ContentElement(**content_data)
                section.add_content(elem)
            for title, sub_data in section_data.get('subsections', {}).items():
                subsection = Section.from_json(sub_data)
                section.add_subsection(title, subsection)
            doc.add_section(section)
        return doc

class Document:
    """
    Represents a complete document, containing multiple sections.

    Attributes:
        sections (List[Section]): A list of sections in the document.
    """

    def __init__(self):
        """
        Initializes a Document with an empty list of sections.
        """
        self.sections: List[Section] = []

    def add_section(self, section: Section) -> None:
        """
        Adds a section to the document.

        Args:
            section (Section): The section to add to the document.
        """
        self.sections.append(section)

    def to_json(self) -> List[Dict[str, Any]]:
        """
        Converts the Document and its sections to a JSON-serializable list of dictionaries.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the document's sections.
        """
        return [section.to_json() for section in self.sections]

    def to_markdown(self) -> str:
        """
        Converts the Document and its sections to a Markdown string.

        Returns:
            str: A string representing the Document in Markdown format.
        """
        return ''.join(section.to_markdown() for section in self.sections)

    def save_as_json(self, filename: str) -> None:
        """
        Saves the Document as a JSON file.

        Args:
            filename (str): The name of the file to save the JSON data to.
        """
        with open(filename, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

    @staticmethod
    def load_from_json(filename: str) -> 'Document':
        """
        Loads a Document from a JSON file.

        Args:
            filename (str): The name of the file to load the JSON data from.

        Returns:
            Document: A Document object created from the JSON data.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        return Document.from_json(data)

    @staticmethod
    def from_json(json_data: List[Dict[str, Any]]) -> 'Document':
        """
        Creates a Document object from a JSON-serializable list of dictionaries.

        Args:
            json_data (List[Dict[str, Any]]): A list of dictionaries representing the document's sections.

        Returns:
            Document: A Document object populated with sections from the JSON data.
        """
        doc = Document()
        for section_data in json_data:
            section = Section(section_data['title'])
            for content_data in section_data['content']:
                elem = ContentElement(**content_data)
                section.add_content(elem)
            for sub_data in section_data.get('subsections', []):
                subsection = Section.from_json(sub_data)
                section.add_subsection(subsection)
            doc.add_section(section)
        return doc

    def __repr__(self) -> str:
        """
        Returns a string representation of the Document.

        Returns:
            str: A string representation of the Document.
        """
        return f"Document(sections={len(self.sections)})"

    @staticmethod
    def load_from_markdown(filename: str) -> 'Document':
        """
        Loads a Document from a Markdown file.

        Args:
            filename (str): The name of the file to load the Markdown data from.

        Returns:
            Document: A Document object created from the Markdown data.
        """
        with open(filename, 'r') as f:
            markdown = f.read()
        
        return Document.from_markdown(markdown)

    @staticmethod
    def from_markdown(markdown: str) -> 'Document':
        """
        Creates a Document object from a Markdown string.

        Args:
            markdown (str): The Markdown string representing the document.

        Returns:
            Document: A Document object populated with sections from the Markdown.
        """
        doc = Document()
        lines = markdown.splitlines()
        current_section = None
        current_subsection = None
        section_stack = []

        for line in lines:
            line = line.strip()

            # Match headings (sections and subsections)
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()

                # Create a new section or subsection based on heading level
                new_section = Section(title)
                if level == 1:
                    doc.add_section(new_section)
                    current_section = new_section
                    current_subsection = None
                    section_stack = [current_section]
                elif level > 1:
                    current_subsection = new_section
                    while len(section_stack) >= level:
                        section_stack.pop()
                    section_stack[-1].add_subsection(current_subsection)
                    section_stack.append(current_subsection)
            
            # Match image elements
            elif re.match(r'!\[.*\]\(.*\)', line):
                match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                description, path = match.groups()
                content_element = ContentElement(
                    element_type='image',
                    path=path,
                    description=description
                )
                if current_subsection:
                    current_subsection.add_content(content_element)
                elif current_section:
                    current_section.add_content(content_element)

            # Assume all other content is part of a paragraph
            elif line:
                content_element = ContentElement(
                    element_type='paragraph',
                    text=line
                )
                if current_subsection:
                    current_subsection.add_content(content_element)
                elif current_section:
                    current_section.add_content(content_element)

        return doc