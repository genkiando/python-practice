import cv2
import numpy as np

img = cv2.imread("Koala_small.bmp")

size_lank = 13
k_size = (size_lank*2)+1 
result = img.copy()
answer = 0*result
count = 0

#0 padding
H, W, C = img.shape
out = np.zeros((H + size_lank*2, W + size_lank*2, C), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = img.copy().astype(np.float)


#kernel
sig = 1.3
k = np.zeros((k_size, k_size), dtype = np.float)
for x in range(-size_lank,k_size-size_lank):
    for y in range(-size_lank,k_size-size_lank):
        k[x + size_lank, y + size_lank] = np.exp(-(x**2 + y**2)/(2*sig**2))
        
k = k*(1/(2*np.pi*sig*sig))
k = k/k.sum() 


for c in [0,1,2]:    
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
            im_c = out[:, :, c].copy()
            im_k = np.sum(im_c[j : j+k_size, i : i+k_size]*k)
            answer[j, i, c] = im_k
            count += 1
            print(count)

        
cv2.imwrite("answer1.bmp", answer)
cv2.imshow("result1", answer)

cv2.waitKey(0)
cv2.destroyAllwindows()