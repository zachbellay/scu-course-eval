#!/usr/bin/python
# URL that generated this code:
# http://txt2re.com/index-python.php3?s=Mixed%20Media%20Painting(ARTS148-99999)%20Winter%20-%202017&9

import re

txt='some other stuff Mixed Media Painting(ARTS148-12345) Winter - 2017 hello world'

regex = '.*?(\\-(\\d+)\\))'

rg = re.compile(regex, re.DOTALL)
m = rg.search(txt)
if m:
    int1=m.group(2)
    print int1