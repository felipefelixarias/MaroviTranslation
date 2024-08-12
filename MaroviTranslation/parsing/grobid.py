import os
from grobid_client.grobid_client import GrobidClient

class GrobidParser:
    def __init__(self, grobid_server='http://localhost:8070', api_version='v1'):
        self.client = GrobidClient(grobid_server=grobid_server)

    def parse_pdf(self, pdf_file_path, output_dir=None, process_type="processFulltextDocument",
                  consolidate_citations=True, include_raw_citations=False, include_raw_affiliations=False,
                  tei_output=True, force=True):
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"The file {pdf_file_path} does not exist.")
        
        # Debugging: Ensure the output directory exists
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Debugging: Print paths and options
        print(f"Processing PDF: {pdf_file_path}")
        print(f"Output directory: {output_dir}")

        # Execute the GROBID parsing process
        self.client.process(process_type, pdf_file_path, output=output_dir)

        # Determine the output file path
        if output_dir:
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file_path))[0] + ".tei.xml")
        else:
            output_file = os.path.splitext(pdf_file_path)[0] + ".tei.xml"

        # Debugging: Confirm the output file
        if os.path.exists(output_file):
            print(f"Output file was successfully created: {output_file}")
        else:
            print(f"Output file was not found: {output_file}")

        return output_file