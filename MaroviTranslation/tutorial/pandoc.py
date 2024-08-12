import os

import pypandoc 

def convert(input_file, output_file, format):
    pypandoc.convert_file(input_file, format, outputfile=output_file)

curr_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(curr_dir, "../../data/output.tei.xml")
output_file = os.path.join(curr_dir, "../../data/output.md")
format = "markdown"
output_directory = os.path.join(curr_dir, "../../data/tei")

convert(input_file, output_file, format)