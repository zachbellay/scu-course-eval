import urllib.request
import requests
import os


def download_range(quarter, year, id, low, high, cookie):

	# Progress bar for nice CLI UI
	# bar = progressbar.ProgressBar(redirect_stdout=True)

	# Create new directory to download PDFs in
	# pdf_dir = 'C:\\Users\\Zach\\Documents\\GitHub\\scu-course-eval\\pdfs'
	
	rel_pdf_dir = '../pdfs'
	cd = os.getcwd()
	pdf_dir = os.path.abspath(os.path.join(cd, rel_pdf_dir))

	# download_dir = pdf_dir + '\\' + str(quarter) + '_' + str(year) + '\\'
	download_dir = os.path.join(pdf_dir, str(quarter) + '_' + str(year))

	os.makedirs(download_dir, exist_ok=True)

	# Iterate from low to high and download all eval PDFs
	for i in range(int(low), int(high)+1):
		try:
			# Construct URL path to PDF and read response
			url = 'https://evaluations.scu.edu/?vclass=' + str(i) + '&vtrm=' + str(id)
			opener = urllib.request.build_opener()
			opener.addheaders.append(('Cookie', cookie))
			response = opener.open(url)
			read = response.read()

			# Determine whether recieved page is a PDF
			if len(read) >= 10000:
				print('ID: ' + str(i) + ' downloaded as ' + str(i) + '.pdf')
				filename = str(i) + '.pdf'
				# print(filename)
				file = open(download_dir + filename, "wb")
				file.write(read)
				file.close()	
			else:
				print('ID: '+ str(i) + ' invalid')

		except KeyboardInterrupt:
			exit()
		except:
			print('Error')