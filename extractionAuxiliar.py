import cv2
import math
import numpy as np
import itertools

quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

 
def decode_image(img):
    row,col = img.shape[:2]

    sizeOfMessage = None
    messageInBits = []
    buff = 0
    
    # Split image into RGB channels
    bImg,gImg,rImg = cv2.split(img)

    # Message hid in blue channel so converted to type float32 for dct function
    bImg = np.float32(bImg)

    # Break into 8x8 blocks
    imgBlocks = [bImg[j:j+8, i:i+8]-128 for (j,i) in itertools.product(range(0,row,8),
                                                                    range(0,col,8))]    
    # Blocks run through quantization table
    quantizedDCT = [img_Block/quant for img_Block in imgBlocks]

    i=0
    # Message extracted from LSB of DCT coeff
    for quantizedBlock in quantizedDCT:
        DC = quantizedBlock[0][0]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        if DC[7] == 1:
            buff+=(0 & 1) << (7-i)
        elif DC[7] == 0:
            buff+=(1&1) << (7-i)
        i=1+i
        if i == 8:
            messageInBits.append(chr(buff))
            buff = 0
            i =0
        
            if messageInBits[-1] == '*' and sizeOfMessage is None:
                try:
                    sizeOfMessage = int(''.join(messageInBits[:-1]))
                except:
                    pass
        if len(messageInBits) - len(str(sizeOfMessage)) - 1 == sizeOfMessage:
            return ''.join(messageInBits)[len(str(sizeOfMessage))+1:]
    
    return ''
