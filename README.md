# Marovi Translation

A tool for translating PDF documents to Spanish in Markdown format, specifically tailored for NeurIPS papers.

## Installation

### Prerequisites

- Anaconda or Miniconda (recommended for managing dependencies and environments)
- Python 3.12.0

### Setup

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:felipefelixarias/MaroviTranslation.git
   cd MaroviTranslation
   ```

2. **Create and Activate Conda Environment:**
   ```bash
   conda create --name your_env_name python=3.12.0
   conda activate your_env_name
   ```

3. **Install Dependencies:**
   ```bash
   pip install .
   ```

   This will install all the dependencies listed in `requirements.txt`.

## Usage

1. **PDF to Markdown Conversion:**
   A working example is available in `MaroviTranslation/tutorial/NeurIPSExample.py`. 
   Run it with the following command.
   ```python MaroviTranslation/tutorial/NeurIPSExample.py```
   The markdowns will be saved in `MaroviTranslation/outputs/`
   More generally, use the `NeurIPSPDFToSpanishMarkdown` class to convert a PDF file into a Spanish Markdown file. Example usage:
   ```python
    from MaroviTranslation.converters.NeurIPS import NeurIPSPDFToSpanishMarkdown
    from MaroviTranslation.translation.core import Translator
    from MaroviTranslation.translation.GoogleTranslator import GoogleTranslator

    # Initialize translator and converter
    translator = Translator()
    translator.set_translator(GoogleTranslator())
    converter = NeurIPSPDFToSpanishMarkdown("path_to_pdf", "path_to_output_folder", translator)

    # Parse PDF, create image map, and generate Markdown
    converter.parse_pdf()
    converter.create_image_map()
    converter.generate_markdown()
   ```

   This will generate Markdown files with translated content and images in the specified output directory.

## Project Structure

- `MaroviTranslation/`
  - `converters/`: Modules for parsing, translation, and markdown generation.
    - `NeurIPS.py`:
  - `markdown/`: Modules for handling Markdown generation.
    - `core.py`: Core functionalities for Markdown manipulation.
  - `outputs/`: Output directory for generated Markdown files and images.
  - `parsing/`: Modules for parsing PDF files.
    - `core.py`: 
    - `NeurIPSParser.py`: Parser specific for NeurIPS papers.
  - `pdfs/`: Directory to place PDF files for conversion.
  - `translation/`: Translation modules.
    - `core.py`: Core translation class.
    - `GoogleTranslator.py`: Google Translator API wrapper.
  - `tutorial`
    - `NeurIPSExample.py`: Script with example usage.
- `requirements.txt`: List of project dependencies.
- `setup.py`: Setup script for installing the project.
- `README.md`: Documentation for the project (this file).

