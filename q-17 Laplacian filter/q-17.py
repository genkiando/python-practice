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
result = gray.copy().astype(np.float)
answer = 0*result
count = 0

#0 padding
H, W = gray.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = gray.copy()

#kernel
k = np.array([[ 0, 1, 0],[1, -4, 1],[0, 1, 0]]) 
     
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        im = out.copy()
        im_k = np.sum(out[j : j+k_size, i : i+k_size]*k)
        answer[j, i] = im_k
        count += 1
        print(count)

        
cv2.imwrite("answer1.bmp", answer)
cv2.imshow("result1", answer)

cv2.waitKey(0)
cv2.destroyAllwindows()