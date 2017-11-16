import urllib2
import requests

# with open('valid_ids.txt') as f:
	# mylist = f.read().splitlines()
	# for i in mylist:
for i in range(10000, 99999):
	try:
		url = 'https://evaluations.scu.edu/?vclass=' + str(i) + '&vtrm=3820'
		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'SimpleSAMLAuthToken=_ac3c423cb0d8be186d3c3061eb522f3fac57efb4ad; PHPSESSID=fee8859aed42ee0821ff8cd295994cab'))
		response = opener.open(url)
		read = response.read()

		if len(read) >= 10000:
			print 'ID: ' + str(i) + ' downloaded as ' + str(i) + '.pdf'
			filename = str(i) + '.pdf'
			print filename
			file = open(filename, "wb")
			file.write(read)
			file.close()	
		else:
			print 'ID: '+ str(i) + ' invalid'

	except KeyboardInterrupt:
		exit()
	except:
		print 'Error'