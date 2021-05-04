import cv2
from extractionAuxiliar import * 

def extraction(imagen):
    mensage =DCT().decode_image(imagen)
    print(mensage)
    return mensage



photo="images/saved.png"
dct_img = cv2.imread(photo, cv2.IMREAD_UNCHANGED)
extraction(dct_img)