import numpy as np
import cv2
import itertools
import matplotlib.pyplot as plt
from incrustationAuxiliar import * 

def incrustation(source,dest,message):
    encryptedImage, bluePart, heatMap, blueErrorDiff, blueNumericalError, totalDiff, totalNumericError = DCT().incrustation(source,message)
    cv2.imwrite(dest,encryptedImage)
    return encryptedImage, bluePart, heatMap, blueErrorDiff, blueNumericalError, totalDiff, totalNumericError


filename = 'images/saved.png'    
photo="images/lenna.png"
dct_img = cv2.imread(photo, -1)

message = "Test message"
#of breeding and deilcacy could not but feel some inwrd qualms when he reached the Father Superiors with Ivan he felt ashamed of havin lost his temper He felt that he ought to have disdaimed that despicable wretch Fyodor Pavlovitch too much to have been upset by him in Father Zossimas cell and so to have forgotten himself Teh monks were not to blame in any case he reflceted on the steps And if theyre decent people here and the Father Superior I understand is a nobleman why not be friendly and courteous withthem I wont argue Ill fall in with everything Ill win them by politness and show them that Ive nothing to do with that Aesop thta buffoon that Pierrot and have merely been takken in over this affair just as they have."
encryptedImage, bluePart, heatMap, blueErrorDiff, blueNumericalError, totalDiff, totalNumericError = incrustation(dct_img, filename, message)