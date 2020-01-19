import cv2
import numpy as np

def gray(img):
    red = img[:, :, 2].copy()
    green = img[:, :, 1].copy() 
    blue = img[:, :, 0].copy()
    Y = 0.21626*red + 0.7152*green + 0.0722*blue 
    return Y.astype(np.uint8)

img = cv2.imread("test_image1_big.bmp") #integer
gray = gray(img) #integer

#################### Gaussian ####################
size_lank = 2
k_size = (size_lank*2)+1 
result = gray.copy() #integer
answer = 0*result #integer


#0 padding
H, W = gray.shape
out = np.zeros((H + size_lank*2, W + size_lank*2), dtype = np.float) #float
out[size_lank:size_lank + H, size_lank:size_lank + W] = gray.copy().astype(np.float) #float

#kernel
sig = 1.4
k = np.zeros((k_size, k_size), dtype = np.float) #float
for x in range(-size_lank,k_size-size_lank):
    for y in range(-size_lank,k_size-size_lank):
        k[x + size_lank, y + size_lank] = np.exp(-(x**2 + y**2)/(2*sig**2))
       
k = k*(1/(2*np.pi*sig*sig))
k = k/k.sum() #float

for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        im_c = out[:, :].copy() #float
        im_k = np.sum(im_c[j : j+k_size, i : i+k_size]*k) #float
        answer[j, i] = im_k #integerに丸めている

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
out[size_lank:size_lank + H, size_lank:size_lank + W] = answer.copy() #floatの箱にint

k1 = np.array([[ 1, 2, 1],[0, 0, 0],[-1, -2, -1]]) 
k2 = np.array([[ 1, 0, -1],[2, 0, -2],[1, 0, -1]])
     
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        
        im_k1 = np.sum(out[j : j+k_size, i : i+k_size]*k1)
        im_k2 = np.sum(out[j : j+k_size, i : i+k_size]*k2)
            
        ans_k1[j, i] = im_k1
        ans_k2[j, i] = im_k2

################### edge and angle ###############################

#ans_k1,k2はinteger
#一度floatに変換→2乗計算

ans_k1 = ans_k1.astype(np.float)
ans_k2 = ans_k2.astype(np.float)
edge = np.sqrt((ans_k1)**2 + (ans_k2)**2) #float

ans_k1 = np.maximum(ans_k1, 1e-5) ##arctanを計算するときに0だと困る
angle = np.arctan(ans_k2/ans_k1) #float
angle_degree = 180*angle / np.pi #float

angle_degree[angle_degree < -22.5] = 180 + angle_degree[angle_degree < -22.5]
_angle = np.zeros_like(angle_degree, dtype = np.uint8)
_angle[np.where(angle_degree <= 22.5)] = 0
_angle[np.where((angle_degree > 22.5) & (angle_degree <= 67.5))] = 45
_angle[np.where((angle_degree > 67.5) & (angle_degree <= 112.5))] = 90
_angle[np.where((angle_degree > 112.5) & (angle_degree <= 157.5))] = 135

#0 padding
H, W = _angle.shape
out = np.zeros((H + 2, W + 2), dtype = np.float)
out[1:1 + H, 1:1 + W] = _angle.copy()
new_angle = np.zeros_like(_angle, dtype = np.uint8)


for x in range(_angle.shape[1]):
    for y in range(_angle.shape[0]):
        kx = x + 1
        ky = y + 1  
        if out[ky, kx] == 0:
            if (out[ky, kx] >= out[ky, kx-1]) and (out[ky, kx] >= out[ky, kx+1]):
                new_angle[y, x] = out[ky, kx]          
            else:
                new_angle[y, x] = 0

        if out[ky, kx] == 45:
            if (out[ky, kx] >= out[ky-1, kx+1]) and (out[ky, kx] >= out[ky+1, kx-1]):
                new_angle[y, x] = out[ky, kx]         
            else:
                new_angle[y, x] = 0
   
        if out[ky, kx] == 90:
            if (out[ky, kx] >= out[ky+1, kx]) and (out[ky, kx] >= out[ky-1, kx]):
                new_angle[y, x] = out[ky, kx]              
            else:
                new_angle[y, x] = 0   
  
        if out[ky, kx] == 135:
            if (out[ky, kx] >= out[ky+1, kx+1]) and (out[ky, kx] >= out[ky-1, kx-1]):
                new_angle[y, x] = out[ky, kx]     
            else:
                new_angle[y, x] = 0   

##################### thrshold processing ################################ 

HT = 100 #high thoreshold
LT = 30 #low thoreshold
edge[edge >= HT] =255
edge[edge <= LT] =0

H, W = edge.shape
out = np.zeros((H + 2, W + 2), dtype = np.float)
out[1:1 + H, 1:1 + W] = edge.copy()
new_edge = np.zeros_like(edge, dtype = np.uint8)

for h in range(H):
    for w in range(W):
        mat = out[h:h+2,w:w+2]
        if LT < out[h+1,w+1] < HT:
            if mat.max() > HT:
                new_edge[h,w] = 255
            else:
                new_edge[h,w] = 0

cv2.imwrite("answer1.bmp", new_edge)
cv2.imshow("result1", new_edge)


cv2.waitKey(0)
cv2.destroyAllwindows()
