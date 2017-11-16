# from PyPDF2 import PdfFileReader

# filename = 'download.pdf'

# pdfReader = PdfFileReader(file(filename, 'rb'))
# title = pdfReader.getDocumentInfo().title
# print pdfReader.getNumPages()
# print pdfReader.getPage(0).extractText()
# pdfReader.stream.close()

import textract

filename = '0aceb3b3-0111-40cf-92ce-7d5db86d8b99.pdf'

extracted_text = textract.process(filename)

output_text_file = open('output.txt', 'w')
output_text_file.write(extracted_text)
output_text_file.close()