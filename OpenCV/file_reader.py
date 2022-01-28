from os import listdir
from os.path import isfile, join


PATH = '/home/mac/Documents/python_projects/OpenCV/cards'
filenames = [f for f in listdir(PATH) if isfile(join(PATH, f))]
print(sorted(filenames, key = str.lower))