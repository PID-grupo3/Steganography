import cv2
import numpy as np
photo = "images/lenna.png"
dct_img = cv2.imread(photo, cv2.IMREAD_UNCHANGED)
bImg = dct_img[:,:,0]
print(np.mean(bImg))