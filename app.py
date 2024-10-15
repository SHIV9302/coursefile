import json
import os
from PyPDF2 import PdfMerger
from difflib import SequenceMatcher  # Importing difflib for similarity check

# Define the paths
index_file_path = r'F:\cltcourse_file\index.json'
course_files_path = r'F:\cltcourse_file\course_files'
output_file_path = r'F:\cltcourse_file\final_course_file.pdf'

# Function to check file validity
def is_pdf(file_path):
    return file_path.lower().endswith('.pdf')

# Function to calculate similarity between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Load the index.json file
try:
    with open(index_file_path, 'r') as f:
        index_data = json.load(f)
except FileNotFoundError:
    print(f"ERROR: The file '{index_file_path}' was not found.")
    exit()
except json.JSONDecodeError:
    print("ERROR: The file 'index.json' is not a valid JSON.")
    exit()

# Initialize the PDF merger
merger = PdfMerger()

# Get a list of all files in the course_files directory
all_files = os.listdir(course_files_path)

# Loop through each section in the index.json file
for section in index_data.get('sections', []):
    expected_filename = section.get('filename')
    if not expected_filename:
        print("WARNING: An entry in 'index.json' does not have a 'filename'.")
        continue

    # Try to find a file that matches at least 80% with the expected filename
    matched_file = None
    for file in all_files:
        if similar(expected_filename, file) >= 0.75:
            matched_file = file
            break

    if matched_file:
        file_path = os.path.join(course_files_path, matched_file)

        # Check if the file exists and is a PDF
        if is_pdf(file_path):
            print(f"Adding file: {file_path}")
            # Append the PDF to the merger
            merger.append(file_path)
        else:
            print(f"WARNING: File '{file_path}' is not a PDF.")
    else:
        print(f"WARNING: No file matching '{expected_filename}' found with at least 80% similarity.")

# Write the merged PDF to a new file
try:
    with open(output_file_path, 'wb') as output_pdf:
        merger.write(output_pdf)
    print(f"PDF merging complete! The final file is '{output_file_path}'.")
except Exception as e:
    print(f"ERROR: Could not write the final PDF. {e}")
