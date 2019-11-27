import csv
import os
import urllib.request
import requests
import os

csv_path = '../class_ids.csv'
pdf_dir = '../pdfs'
ck = 'SimpleSAMLAuthToken=_f798a975aa702eb7cd1032252956eb0d71678ea3c3; PHPSESSID=c6e392ef086ae76860fd615dca0ad711'

def download_all():
	with open(csv_path) as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			# Fetch info from CSV file
			quarter = row['Quarter']
			year = row['Year']
			id = int(row['Id'])
			low = int(row['Low'])
			high = int(row['High'])

			download_dir = os.path.join(pdf_dir, str(quarter) + '_' + str(year))

			# Check whether the current quarter & year already has a directory
			if(os.path.isdir(download_dir)):

				print(str(quarter) + ' '+ str(year) + ' directory found!')

				# Get the index of the last PDF that was downloaded in this directory
				_dir = [i.replace('.pdf','') for i in os.listdir(download_dir) if 'pdf' in i]

				if (len(_dir) > 0):
					last_pdf_index = int(max(_dir))
				else:
					last_pdf_index = low

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


def download_range(quarter, year, id, low, high, cookie):

		
	rel_pdf_dir = '../pdfs'
	cd = os.getcwd()
	pdf_dir = os.path.abspath(os.path.join(cd, rel_pdf_dir))

	download_dir = os.path.join(pdf_dir, str(quarter) + '_' + str(year))

	os.makedirs(download_dir, exist_ok=True)

	# Iterate from low to high and download all eval PDFs
	for i in range(int(low), int(high)+1):
		try:
			# Construct URL path to PDF and read response
			url = 'https://www.scu.edu/apps/evaluations/?vclass='+ str(i) + '&vtrm=' + str(id)

			opener = urllib.request.build_opener()
			opener.addheaders.append(('Cookie', cookie))
			response = opener.open(url, timeout=3)
			read = response.read()

			# Determine whether recieved page is a PDF
			if len(read) >= 10000:
				print('ID: ' + str(i) + ' downloaded as ' + str(i) + '.pdf')
				filename = str(i) + '.pdf'
				file = open(os.path.join(download_dir, filename), "wb")
				file.write(read)
				file.close()	
			else:
				print('ID: '+ str(i) + ' invalid')

		except KeyboardInterrupt:
			exit()
		except:
			print('Error')

if __name__ == '__main__':
	download_all()


