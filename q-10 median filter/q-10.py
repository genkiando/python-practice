import cv2
import numpy as np

img = cv2.imread("Koala_small.bmp")

size_lank = 5
k_size = (size_lank*2)+1 
result = img.copy()
answer = 0*result
count = 0

#0 padding
H, W, C = img.shape
out = np.zeros((H + size_lank*2, W + size_lank*2, C), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = img.copy()
print(out.shape)

for c in [0,1,2]:    
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
            im_c = out[:, :, c].copy()
            im = np.mean(im_c[j : j + k_size, i : i + k_size])
            answer[j, i, c] = im
            count += 1
            print(count)

cv2.imwrite("answer1.bmp", answer)
cv2.imshow("result1", answer)

cv2.waitKey(0)
cv2.destroyAllwindows()