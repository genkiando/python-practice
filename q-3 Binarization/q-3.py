import cv2
import numpy as np

def gray(img):
    red = img[:, :, 2].copy()
    green = img[:, :, 1].copy() 
    blue = img[:, :, 0].copy()
    Y = 0.21626*red + 0.7152*green + 0.0722*blue 
    return Y.astype(np.uint8)
    
img = cv2.imread("test1.jpg")
gray = gray(img)

gray[gray < 128] = 0
gray[gray > 128] = 255
    
    
cv2.imwrite("answer1.bmp",gray)
cv2.imshow("result1",gray)

cv2.waitKey(0)
cv2.destroyAllwindows()