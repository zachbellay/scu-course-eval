import os
import subprocess

# Get current directory
cd = os.getcwd()

# Relative filepaths
pdf_loc = '../pdfs/Winter_2017/46003.pdf'
txt_loc = 'test2.txt'

# Full filepaths
full_pdf_loc = os.path.join(cd, pdf_loc)
full_txt_loc = os.path.join(cd, txt_loc)

subprocess.call(['pdftotext', full_pdf_loc, full_txt_loc])