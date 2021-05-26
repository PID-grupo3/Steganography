import cv2
from extractionAuxiliar import decode_image
import matplotlib.pyplot as plt
def extraction(imagen):
    mensage,heatMap,imgBlock,EncriptedImg= decode_image(imagen)

    print(mensage)
    plt.plot(heatMap)
    print(imgBlock)
    print(EncriptedImg)
    return mensage

photo="images/saved.png"
dct_img = cv2.imread(photo, -1)

extraction(dct_img)