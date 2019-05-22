import re
from tika import parser
raw = parser.from_file('../pdfs/Winter_2017/46003.pdf')
parsed_pdf = raw['content']

print(len(parsed_pdf))

matches = re.findall(r'/n=([0-9.]+).*av\.=([0-9.]+).*md=([0-9.]+).*dev\.=([0-9.]+)/g', parsed_pdf)

for match in matches:
    print(match)