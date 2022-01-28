# a simple test of template matching in Cookie clicker using OpenCV
# tutorial available at: https://www.youtube.com/watch?v=vXqKniVe6P8
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

# read the source images
haystack_img = cv2.imread('haystack.png', cv2.IMREAD_UNCHANGED)
ones_img = cv2.imread('one.png', cv2.IMREAD_UNCHANGED)
twos_img = cv2.imread('two.png', cv2.IMREAD_UNCHANGED)
threes_img = cv2.imread('three.png', cv2.IMREAD_UNCHANGED)
print("Found haystack and needle(s)...")

# show the farm image, close on keypress
cv2.imshow('Haystack', haystack_img)
cv2.waitKey()
cv2.destroyAllWindows()

# template match
print("Matching to template(s)...")
result_ones = cv2.matchTemplate(haystack_img, ones_img, cv2.TM_CCOEFF_NORMED)
result_twos = cv2.matchTemplate(haystack_img, twos_img, cv2.TM_CCOEFF_NORMED)
result_threes = cv2.matchTemplate(haystack_img, threes_img, cv2.TM_CCOEFF_NORMED)

# show the result
#cv2.imshow('Result', result)
#cv2.waitKey()
#cv2.destroyAllWindows()

# get the matching positions from result
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_ones)
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_twos)
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_threes)

# get the dimensions of the template image
w_ones = ones_img.shape[1]
h_ones = ones_img.shape[0]
w_twos = twos_img.shape[1]
h_twos = twos_img.shape[0]
w_threes = threes_img.shape[1]
h_threes = threes_img.shape[0]


# set a match threshold and filter the results
# yloc and xloc will be arrays with matches that are withing the threshold
threshold_ones = .70
threshold_twos = .90
threshold_threes = .80
yloc_ones, xloc_ones = np.where(result_ones >= threshold_ones)
yloc_twos, xloc_twos = np.where(result_twos >= threshold_twos)
yloc_threes, xloc_threes = np.where(result_threes >= threshold_threes)
print(f"{len(yloc_ones)} + {len(yloc_twos)} + {len(yloc_threes)} matches found.")

# now, there might be multiple rectangles on each match
# to fix this, we group them using cv2
# we also double them, to make sure that there is 
# at least 2 rectangles per match
# otherwise the grouping fails...
rectangles_ones = []
rectangles_twos = []
rectangles_threes = []
for (x, y) in zip(xloc_ones, yloc_ones):
    rectangles_ones.append([int(x), int(y), int(w_ones), int(h_ones)])
    rectangles_ones.append([int(x), int(y), int(w_ones), int(h_ones)])
for (x, y) in zip(xloc_twos, yloc_twos):
    rectangles_twos.append([int(x), int(y), int(w_twos), int(h_twos)])
    rectangles_twos.append([int(x), int(y), int(w_twos), int(h_twos)])
for (x, y) in zip(xloc_threes, yloc_threes):
    rectangles_threes.append([int(x), int(y), int(w_threes), int(h_threes)])
    rectangles_threes.append([int(x), int(y), int(w_threes), int(h_threes)])
rectangles_ones, weights_ones = cv2.groupRectangles(rectangles_ones, 1, 0.2)
rectangles_twos, weights_twos = cv2.groupRectangles(rectangles_twos, 1, 0.2)
rectangles_threes, weights_threes = cv2.groupRectangles(rectangles_threes, 1, 0.2)
print(f"Reduced match(es) to {len(rectangles_ones)} + {len(rectangles_twos)} + {len(rectangles_threes)} rectangle(s).")
for (x, y, w, h) in rectangles_ones:
    cv2.rectangle(haystack_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
for (x, y, w, h) in rectangles_twos:
    cv2.rectangle(haystack_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
for (x, y, w, h) in rectangles_threes:
    cv2.rectangle(haystack_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
# show the farm image with the matches on it
cv2.imshow('Haystack', haystack_img)
cv2.waitKey()
cv2.destroyAllWindows()