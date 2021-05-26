import numpy as np
import cv2
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE 
                    [12,12,14,19,26,58,60,55],    
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

class DCT():    
    def __init__(self): 
        self.message = None
        self.messageInBits = None
        self.oriCol = 0
        self.oriRow = 0
        self.numBits = 0   

    def incrustation(self,img,secret):
        
        # Save message data in local variables
        self.message = str(len(secret))+'*'+secret
        self.messageInBits = self.toBits()

        # Get size of image in pixels
        row,col = img.shape[:2]
        self.oriRow, self.oriCol = row, col  

        # Calculate if message fits in the image
        if((col/8)*(row/8)<len(secret)):
            print("Error: Message too large to encode in image")
            return      
        
        # Make divisible by 8x8 adding padding if needed
        if row%8 != 0 or col%8 != 0:
            img = self.addPadd(img, row, col)
        
        # Take number of rows and cols
        row,col = img.shape[:2]
        
        # Split image into RGB channels
        bImg,gImg,rImg = cv2.split(img)
        
        # Get the encrypted image and get the heatMap from the quantized DCT matrix
        sImg, heatMap = self.incrustationCore(bImg,row,col)
        
        # Message will be hide in blue channel
        encryptedImage = cv2.merge((sImg,gImg,rImg))
        
        #Calculate blue channel error image and numeric value
        blueErrorDiff = sImg - bImg
        blueNumericalError = np.mean(blueErrorDiff**2)
        blueNumericalError
        
        #Calculate total (3 channels) error and numeric value
        totalDiff = encryptedImage - img
        totalNumericError = np.mean(totalDiff**2)
        totalNumericError

        return encryptedImage, sImg, heatMap, blueErrorDiff, blueNumericalError, totalDiff, totalNumericError

    ## Functions used for the image reconstruction after the message incrustation in blue channel
    def chunks(self, l, n):
        m = int(n)
        for i in range(0, len(l), m):
            yield l[i:i + m]
    def addPadd(self,img, row, col):
        img = cv2.resize(img,(col+(8-col%8),row+(8-row%8)))    
        return img
    def toBits(self):
        bits = []
        for char in self.message:
            binval = bin(ord(char))[2:].rjust(8,'0')
            bits.append(binval)
        self.numBits = bin(len(bits))[2:].rjust(8,'0')
        return bits
    ##

    def incrustationCore(self, bImg, row,col):
        
        # Change image to float32 to fit DCT values
        bImg = np.float32(bImg)

        # Break into 8x8 blocks
        imgBlocks = [np.round(bImg[j:j+8, i:i+8]+128) for (j,i) in itertools.product(range(0,row,8),
                                                                       range(0,col,8))]

        # Blocks are run through DCT function
        dctBlocks = [np.round(cv2.dct(img_Block)) for img_Block in imgBlocks]
        
        # Blocks then run through quantization table
        quantizedDCT = [np.round(dct_Block/quant) for dct_Block in dctBlocks]
        
        # Set LSB in DC value corresponding bit of message
        messIndex = 0
        letterIndex = 0

        # Calculate the heatmap of the matrix
        heatMap = sns.heatmap(quantizedDCT[0])

        # Incrustation of the message in blue channel
        for quantizedBlock in quantizedDCT:
            # Find LSB in DCT coeff and replace with message bit
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)

            # Introduce the next letter of the message
            DC = np.unpackbits(DC)
            DC[7] = self.messageInBits[messIndex][letterIndex]
            DC = np.packbits(DC)
            
            # Modify old quantizedBlock with the new one that has the message
            DC = np.float32(DC)
            DC= DC-255
            quantizedBlock[0][0] = DC

            # Adds 1 to the letter reader index (mod 8)
            letterIndex = letterIndex+1
            if letterIndex == 8:
                letterIndex = 0
                messIndex = messIndex + 1
                if messIndex == len(self.message):
                    break
        

        # Blocks run inversely through quantization table
        sImgBlocks = [quantizedBlock *quant-128 for quantizedBlock in quantizedDCT]
        
        # Puts the new image back together
        sImg=[]
        for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    sImg.extend(block[rowBlockNum])
        sImg = np.array(sImg).reshape(row, col)
        
        
        # Converted from type float32 to uint8 again to return it and save
        sImg = np.uint8(sImg)
        
        return sImg,heatMap