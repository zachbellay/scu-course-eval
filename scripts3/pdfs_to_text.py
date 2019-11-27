import os
import subprocess
import sys
from tqdm import tqdm

# Get current dir
cd = os.getcwd()

# Relative filepaths
rel_pdf_dir = '../pdfs'
rel_txt_dir = '../txts'

# Full filepaths
abs_pdf_dir = os.path.abspath(os.path.join(cd, rel_pdf_dir))
abs_txt_dir = os.path.abspath(os.path.join(cd, rel_txt_dir))

# Check that pdfs are available
if not os.path.exists(abs_pdf_dir):
    sys.exit('pdfs directory not found.')

# Create txt folder is not already created
if not os.path.exists(abs_txt_dir):
    os.makedirs(abs_txt_dir)

# Get number of files in directory recursively
num_files = sum([len(files) for _, _, files in os.walk(abs_pdf_dir)])

with tqdm(total=num_files) as pbar:
    # Iterate over all Quarters/Years in the PDF directory
    for subdir, dirs, files in os.walk(abs_pdf_dir):
        
        # Iterate over every PDF file
        for file in files:

            # Ignore non-pdf files
            if(".pdf" not in file):
                continue

            abs_pdf_file = os.path.abspath(os.path.join(subdir, file))
            
            abs_txt_file = subdir.replace('pdfs', 'txts')

            txt_file = file.replace('.pdf', '.txt')

            # Create txt directory
            if(not os.path.exists(abs_txt_file)):
                os.mkdir(abs_txt_file)

            # Append file name to end of directory path
            abs_txt_file = os.path.abspath(os.path.join(abs_txt_file, txt_file))

            # If the text file already exists, go to the next file
            if(os.path.exists(abs_txt_file)):
                continue

            # Call pdftotext utility
            subprocess.call(['pdftotext', abs_pdf_file, abs_txt_file])

            # Update progress bar
            pbar.update(1)