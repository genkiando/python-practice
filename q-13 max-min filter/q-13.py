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

size_lank = 4
k_size = (size_lank*2)+1 
result = img.copy()
answer = 0*result
count = 0

#0 padding
H, W = gray.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = gray.copy()

     
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        
        im_max = np.max(out[j : j+k_size, i : i+k_size])
        im_min = np.min(out[j : j+k_size, i : i+k_size])
        dif = im_max - im_min
        answer[j, i] = dif
        count += 1
        print(count)

        
cv2.imwrite("answer.bmp", answer)
cv2.imshow("result", answer)
cv2.waitKey(0)
cv2.destroyAllwindows()