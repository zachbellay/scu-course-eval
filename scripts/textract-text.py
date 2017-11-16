import textract
import os

pdf_dir = 'C:\Users\Zach\Desktop\Classes\scu-course-evals\\'
txt_dir = 'C:\Users\Zach\Desktop\Classes\\text\\'

for pdf_file_name in os.listdir(pdf_dir):
	text = textract.process(pdf_dir + pdf_file_name)
	txt_file_name = pdf_file_name.replace('pdf','txt')
	txt_output_file = open(txt_dir + txt_file_name, 'wb')
	txt_output_file.write(text)
	txt_output_file.close()
	print txt_file_name