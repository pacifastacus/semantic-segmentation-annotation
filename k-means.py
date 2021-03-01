import numpy as np
import glob
import cv2


def sort_numbered_fname(e):
    import re
    match = re.search('([^0-9]*)([0-9]+)(.*)', e)
    num = int(match[2])
    return num


# Get list of images
img_dir = 'test_data/img/'
fname = glob.glob(img_dir + '*.jpg')
fname.sort(key=sort_numbered_fname)

# false-color-map
colors = np.array([[0, 0, 0],
                   [0, 0, 255],
                   [0, 255, 0],
                   [255, 0, 0],
                   [255, 255, 255],
                   [0, 255, 255],
                   [255, 0, 255],
                   [255, 255, 0],
                   [125, 125, 125],
                   [125, 255, 0],
                   [125, 0, 255]],
                  dtype=np.uint8)

# define criteria, number of clusters(K) to run kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
K = 2

for i in range(len(fname)):
    img = cv2.imread(fname[i],cv2.IMREAD_COLOR)
    img_size = img.shape[0:2]   #Get width and height that independent of pixel information
    img = cv2.GaussianBlur(img,(3,3),1)
    #img = img.reshape((*img.shape,1))
    #coords = np.mgrid[0:img.shape[0],0:img.shape[1]].transpose((1, 2, 0))/5
    #data = np.concatenate((img,coords),axis=2)
    Z = img.reshape((-1, 3))
    #Z = data.reshape((-1,5))
    # convert to np.float32
    Z = np.float32(Z)

    # Perform K-means clustering. Try optimize cluster centroids from previous cycle
    # This is useful only if the images are in sequence
    try:
        ret, label, center = cv2.kmeans(Z, K, label, criteria, 1, cv2.KMEANS_USE_INITIAL_LABELS)
    except NameError:
        print('label not implemented, yet (first run)')
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    #res = center[label.flatten()]
    res = colors[label.flatten()%colors.shape[0]]
    res = res.reshape((*img_size,3))
    #img = np.concatenate((img,img,img),axis=2)
    #out = cv2.addWeighted(img, 0.5, res, 0.5, 0)
    out = res
    cv2.imshow('res2', out)
    if cv2.waitKey() == ord('q'):
        break

cv2.destroyAllWindows()
