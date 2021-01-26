from run_over_images import *
import numpy as np
import cv2

for file in get_next_image(TEST_DIR):
    img = cv2.imread(file,cv2.IMREAD_COLOR)
    filtered = cv2.pyrMeanShiftFiltering(img, )