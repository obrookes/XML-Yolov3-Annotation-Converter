import os
import sys

test_val_file = sys.argv[1]

with open(test_val_file, "a") as a:
    for path, subdirs, files in os.walk('.'):
        for filename in files:
            if(filename.lower().endswith('.jpg') or filename.lower().endswith('.png')):
                f = '/content/darknet/train-dataset/' + filename
                a.write(str(f) + '\n')
