import os

from MaroviTranslation.parsing.GrobidParser import GrobidParser

parser = GrobidParser()
curr_dir = os.path.dirname(os.path.realpath(__file__))
pdf_path = os.path.join(curr_dir, "../../data/pdf/the_llama_3_heard_of_models.pdf")
output_directory = os.path.join(curr_dir, "../../data/tei")

print(f"PDF path: {pdf_path}")
print(f"Output directory: {output_directory}")

output_file = parser.parse_pdf(pdf_path, output_dir=output_directory, 
                                consolidate_citations=True, include_raw_citations=True,
                                include_raw_affiliations=True, tei_output=True, force=True)

print(f"Output file: {output_file}")