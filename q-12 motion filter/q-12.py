import cv2
import numpy as np

img = cv2.imread("Koala_small.bmp")


size_lank = 3
k_size = (size_lank*2)+1 
amount = 1/k_size
result = img.copy()
answer = 0*result

#0 padding
H, W, C = img.shape
out = np.zeros((H + size_lank*2, W + size_lank*2, C), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = img.copy()

#kernel
k = np.eye(k_size)*amount
     
for c in [0, 1, 2]:
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
        
            im_c = out[:,:,c].copy()
            h = np.sum(np.multiply(im_c[j : j+k_size, i : i+k_size],k))
            answer[j, i, c] = h 

        

cv2.imwrite("answer.bmp",answer)
cv2.imshow("result",answer)
cv2.waitKey(0)
cv2.destroyAllwindows()