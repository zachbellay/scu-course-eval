import textract
import os
import time
import errno

pdf_dir = 'C:\\Users\\Zach\\Documents\\GitHub\\scu-course-eval\\pdfs'
txt_dir = 'C:\\Users\\Zach\\Documents\\GitHub\\scu-course-eval\\txts'

for subdir, dirs, files in os.walk(pdf_dir):
    for file in files:
    	
        pdf_path = os.path.join(subdir, file)

        txt_folder = subdir.replace('pdfs', 'txts')
        txt_file = file.replace('.pdf', '.txt')
        txt_path = os.path.join(txt_folder, txt_file)

        try:
            os.makedirs(txt_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print('Directory already exists.')

        text = textract.process(pdf_path)
        text_output_file = open(txt_path, 'wb')
        text_output_file.write(text)
        text_output_file.close()

        print(txt_path)
