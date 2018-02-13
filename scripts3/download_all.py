import csv
import os
# import progressbar

from download_range import download_range

csv_dir = 'C:\\Users\\Zach\\Documents\\GitHub\\scu-course-eval\\class_ids.csv'
pdf_dir = 'C:\\Users\\Zach\\Documents\\GitHub\\scu-course-eval\\pdfs'
ck = 'SimpleSAMLAuthToken=_d14ae85f84a7cc2bb58f359efe34cdc9dfec01f8ca; PHPSESSID=730a05654a0a02d70606e9218bad6c3e'

# bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, redirect_stdout=True)

with open(csv_dir) as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		# Fetch info from CSV file
		quarter = row['Quarter']
		year = row['Year']
		id = int(row['Id'])
		low = int(row['Low'])
		high = int(row['High'])

		download_dir = pdf_dir + '\\' + str(quarter) + '_' + str(year) + '\\'

		# Check whether the current quarter & year already has a directory
		if(os.path.isdir(download_dir)):

			print(str(quarter) + ' '+ str(year) + ' directory found!')
			
			# Get the index of the last PDF that was downloaded in this directory
			last_pdf_index = int(max(os.listdir(download_dir)).replace('.pdf',''))

			# If the last index that was downloaded was also the high from the CSV, then this directory is complete
			if(last_pdf_index == high):
				print(quarter + ' ' + year + ' directory already completed!')
			else:
				low = last_pdf_index
				print(quarter + ' ' + year + ' downloads resuming from ' + str(low))
				download_range(quarter, year, id, low, high, ck)	
		else:
			print('Downloading evals from ' + str(quarter) + ' ' + str(year))
			download_range(quarter, year, id, low, high, ck)