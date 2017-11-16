import os
import sys
import textract
import re
import time

directory = 'C:\Users\Zach\Desktop\Classes\downloads\\'
regex = '.*?(\\-(\\d+)\\))'
rg = re.compile(regex)

for file in os.listdir(directory):
	print '====================='
	print 'Old filename: ' + file
	try:

		# Convert the pdf to a string
		extracted_text = textract.process(directory + file)
		
		# Search the extracted pdf file for the course id using the regex expression
		match = rg.search(extracted_text)

		# Gets the second matched regex group (the course id number)
		new_filename = match.group(2) + '.pdf'

		print 'New filename: ' + new_filename

		os.rename(directory + file, directory + new_filename)
		
	except KeyboardInterrupt:
		exit()
	except:
		pass