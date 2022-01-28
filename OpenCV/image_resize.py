from PIL import Image
from os import listdir
from os.path import isfile, join

PATH = '/home/mac/Documents/python_projects/OpenCV/cards'
filenames = [f for f in listdir(PATH) if isfile(join(PATH, f))]
for i in sorted(filenames):
    print(i)
    im = Image.open(join(PATH, i))
    imc = im.crop((0, 0, 15, 30))
    imc.save(join(PATH, i))