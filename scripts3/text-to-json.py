import os
import time
import errno

json_dir = '/mnt/c/Users/zachb/Documents/GitHub/scu-course-eval/json'
txt_dir = '/mnt/c/Users/zachb/Documents/GitHub/scu-course-eval/txts'

for subdir, dirs, files in os.walk(txt_dir):
    for file in files:
    	
        txt_path = os.path.join(subdir, file)

        json_folder = subdir.replace('txts', 'json')
        json_file = file.replace('.txt', '.json')
        json_path = os.path.join(json_folder, json_file)

        try:
          os.makedirs(json_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print('Directory already exists.')

        with open(txt_path) as fp:
            name = fp.readline()
            # print(name)

        json_output_file = open(json_path, 'w')
        json_output_file.write(name)
        json_output_file.close()

        # print(txt_path)
