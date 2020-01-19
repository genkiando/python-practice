import cv2
import numpy as np

def gray(img):
    red = img[:, :, 2].copy()
    green = img[:, :, 1].copy() 
    blue = img[:, :, 0].copy()
    Y = 0.21626*red + 0.7152*green + 0.0722*blue 
    return Y.astype(np.uint8)
    
    
img = cv2.imread("Koala_small.bmp")
gray = gray(img)
size_lank = 1 
k_size = (size_lank*2)+1 
result = img.copy()
ans_k1 = 0*result
ans_k2 = 0*result
count = 0

#0 padding
H, W = gray.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = gray.copy()


k1 = np.array([[ 0, -1, 0],[0, 1, 0],[0, 0, 0]]) 
k2 = np.array([[ 0, 0, 0],[-1, 1, 0],[0, 0, 0]])
     
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        im_k1 = np.sum(out[j : j+k_size, i : i+k_size]*k1)
        im_k2 = np.sum(out[j : j+k_size, i : i+k_size]*k2)
            
        ans_k1[j, i] = im_k1
        ans_k2[j, i] = im_k2
        count += 1
        print(count)

        
cv2.imwrite("answer1.bmp",ans_k1)
cv2.imshow("result1",ans_k1)

cv2.imwrite("answer2.bmp",ans_k2)
cv2.imshow("result2",ans_k2)

cv2.waitKey(0)
cv2.destroyAllwindows()