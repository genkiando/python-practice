

import cv2
import numpy as np

def ave(img , p_s = 8):
    res = img.copy()
    h, w, c = img.shape
    w_p = int(w/(p_s))
    h_p = int(h/(p_s))
    
    for m in range(h_p):
        for n in range(w_p):
            for C in range(c):
                res[m*p_s : m*p_s + p_s , n*p_s : n*p_s + p_s , C] = np.mean(img[m*p_s : m*p_s + p_s , n*p_s : n*p_s + p_s , C].astype(np.int)) 
    return res 

img = cv2.imread("Koala_small.bmp")
result = ave(img)


cv2.imwrite("answer.bmp", result)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllwindows()