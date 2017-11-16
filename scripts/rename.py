import os,sys
folder = 'C:\Users\Zach\Desktop\Classes\downloads'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.tmp', '.pdf')
       output = os.rename(infilename, newname)