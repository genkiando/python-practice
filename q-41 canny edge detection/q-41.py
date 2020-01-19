import cv2
import numpy as np

def gray(img):
    red = img[:, :, 2].copy()
    green = img[:, :, 1].copy() 
    blue = img[:, :, 0].copy()
    Y = 0.21626*red + 0.7152*green + 0.0722*blue 
    return Y.astype(np.uint8)

img = cv2.imread("test_image1_small.jpg")
gray = gray(img)

#################### Gaussian ####################
size_lank = 2
k_size = (size_lank*2)+1 
result = gray.copy()
answer = 0*result


#0 padding
H, W = gray.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = gray.copy().astype(np.float)

#kernel
sig = 1.4
k = np.zeros((k_size, k_size), dtype = np.float)
for x in range(-size_lank,k_size-size_lank):
    for y in range(-size_lank,k_size-size_lank):
        k[x + size_lank, y + size_lank] = np.exp(-(x**2 + y**2)/(2*sig**2))
       
k = k*(1/(2*np.pi*sig*sig))
k = k/k.sum() 

for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        im_c = out[:, :].copy()
        im_k = np.sum(im_c[j : j+k_size, i : i+k_size]*k)
        answer[j, i] = im_k

cv2.imshow("result0",answer)
##################################################

####################  sobel   ####################

size_lank = 1 
k_size = (size_lank*2)+1 
result = answer.copy()
ans_k1 = 0*result
ans_k2 = 0*result

#0 padding
H, W = answer.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float)
out[size_lank:size_lank + H, size_lank:size_lank + W] = answer.copy()

k1 = np.array([[ 1, 2, 1],[0, 0, 0],[-1, -2, -1]]) 
k2 = np.array([[ 1, 0, -1],[2, 0, -2],[1, 0, -1]])
     
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        
        im_k1 = np.sum(out[j : j+k_size, i : i+k_size]*k1)
        im_k2 = np.sum(out[j : j+k_size, i : i+k_size]*k2)
            
        ans_k1[j, i] = im_k1
        ans_k2[j, i] = im_k2

##################################################

edge = np.sqrt(np.power(ans_k1, 2) + np.power(ans_k2, 2)).astype(np.uint8)
ans_k1 = np.maximum(ans_k1, 1e-5) ##arctanを計算するときに0だと困る

angle = np.arctan(ans_k2/ans_k1).astype(np.uint8)
angle_degree = angle*(180/(np.pi))

angle_degree[angle_degree < -22.5] = 180 + angle_degree[angle_degree < -22.5]
_angle = np.zeros_like(angle_degree, dtype = np.uint8)
_angle[np.where(angle_degree <= 22.5)] = 0
_angle[np.where((angle_degree > 22.5)&(angle_degree <= 67.5))] = 45
_angle[np.where((angle_degree > 67.5)&(angle_degree <= 112.5))] = 90
_angle[np.where((angle_degree > 112.5)&(angle_degree <= 157.5))] = 135

print(_angle)
print(edge)


cv2.imwrite("answer1.bmp", edge)
cv2.imshow("result1", edge)

cv2.imwrite("answer2.bmp", _angle)
cv2.imshow("result2", _angle)

cv2.waitKey(0)
cv2.destroyAllwindows()