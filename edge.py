import cv2
import numpy as np
import glob

def calc_edges(img, tresh1=100, tresh2=200):
    blur = cv2.GaussianBlur(img,(3,3),0.5)
    out = cv2.Canny(blur, tresh1, tresh2)
    return cv2.morphologyEx(out,cv2.MORPH_CLOSE,(2,2))


def sort_numbered_fname(e):
    import re
    match = re.search('([^0-9]*)([0-9]+)(.*)', e)
    num = int(match[2])
    return num


if __name__ == "__main__":
    # Get list of images
    img_dir = 'test_data/img/'
    fname = glob.glob(img_dir + '*.jpg')
    fname.sort(key=sort_numbered_fname)

    CANNY_TRS1 = 60
    CANNY_TRS2 = CANNY_TRS1 * 2

    for i in range(len(fname)):
        img = cv2.imread(fname[i], cv2.IMREAD_GRAYSCALE)
        edges = calc_edges(img, CANNY_TRS1, CANNY_TRS2)
        out = img
        out[edges != 0] = 0
        cv2.imshow('out', out)
        cv2.imshow('edges', edges)
        if cv2.waitKey() == ord('q'):
            break

    cv2.destroyAllWindows()
