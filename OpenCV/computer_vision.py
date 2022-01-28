# this program captures the mines (minesweeper) window
# tutorial at https://www.youtube.com/watch?v=WymCpVUPWQ4
import cv2
import numpy as np
import pyautogui
from os import listdir
from os.path import isfile, join

# import the filenames to make image objects from
PATH = '/home/mac/Documents/python_projects/OpenCV/cards'
filenames = [f for f in listdir(PATH) if isfile(join(PATH, f))]

# load the needle images
clubs_imgs = []
diamonds_imgs = []
hearts_imgs = []
spades_imgs = []
for f in sorted(filenames):
    if f[0] == 'c':
        clubs_imgs.append(cv2.imread(join(PATH, f), cv2.COLOR_RGB2BGR))
    elif f[0] == 'd':
        diamonds_imgs.append(cv2.imread(join(PATH, f), cv2.COLOR_RGB2BGR))
    elif f[0] == 'h':
        hearts_imgs.append(cv2.imread(join(PATH, f), cv2.COLOR_RGB2BGR))
    elif f[0] == 's':
        spades_imgs.append(cv2.imread(join(PATH, f), cv2.COLOR_RGB2BGR))
facedown_img = cv2.imread(join(PATH, 'facedown.png'), cv2.COLOR_RGB2BGR)

# confidence thresholds (found by trial and error)
threshold_super = .95
threshold_high = .88
threshold_low = .78


def match_template(haystack, needle, threshold, rectColor, name):
    """
    Matches the needle image with a given haystack (screenshot)
    example input:
    threshold = 0.90
    rectColor = (0, 255, 0)
    """
    # template match
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

    # get the dimensions of the template image
    w = needle.shape[1]
    h = needle.shape[0]

    # set a match threshold and filter the results
    # yloc and xloc will be arrays with matches that are withing the threshold
    yloc, xloc = np.where(result >= threshold)

    # now, there might be multiple rectangles on each match
    # to fix this, we group them using cv2
    # we also double them, to make sure that there is 
    # at least 2 rectangles per match
    # otherwise the grouping fails...
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(f"Reduced {len(xloc)} match(es) to {len(rectangles)} rectangle(s).")

    # draw the rectangles and the text label
    for (x, y, w, h) in rectangles:
        cv2.rectangle(screenshot, (x, y), (x + w, y + h), rectColor, 2)
        cv2.putText(screenshot, name, (x, y - 5), cv2.QT_FONT_NORMAL, 0.5, rectColor)

    # show the heatmap
    #cv2.imshow('Result', result)

print("Starting...")
while(True):
    screenshot = pyautogui.screenshot(region=(1010,250,900,610)) # take a screenshot
    screenshot = np.array(screenshot)   # reformat for openCV
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR) # convert from RGB to BGR
    if not screenshot.data:
        print("error")

    # match the screenshot to the needle image(s)
    ci, di, hi, si = 1, 1, 1, 1
    for i in clubs_imgs:
        match_template(screenshot, i, threshold_high, (0, 0, 0), "clubs_" + str(ci))
        ci += 1
    for i in diamonds_imgs:
        match_template(screenshot, i, threshold_high, (0, 0, 255), "diamonds_" + str(di))
        di += 1
    for i in hearts_imgs:
        match_template(screenshot, i, threshold_low, (0, 0, 255), "hearts_" + str(hi))
        hi += 1
    for i in spades_imgs:
        match_template(screenshot, i, threshold_high, (0, 0, 0), "spades_" + str(si))
        si += 1

    match_template(screenshot, facedown_img, threshold_high, (255, 0, 0), "facedown")
    print()

    # update the window
    cv2.imshow('Computer vision', screenshot)

    # press any key with the output window focused to exit
    if cv2.waitKey(5) != -1:
        cv2.destroyAllWindows()
        break

print('...done.')

