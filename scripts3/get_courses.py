import re


f = open('courses.txt', "r")
lines = f.readlines()
f.close()


subjects = re.findall(r'value="(.*?)"', lines[0])

subjects = [i for i in subjects if len(i) > 0]

print(subjects)
