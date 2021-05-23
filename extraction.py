import cv2
from extractionAuxiliar import decode_image

def extraction(imagen):
    mensage = decode_image(imagen)
    print(mensage)
    return mensage

photo="images/saved.png"
dct_img = cv2.imread(photo, -1)

extraction(dct_img)