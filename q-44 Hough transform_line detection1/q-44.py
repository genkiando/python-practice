import cv2
import numpy as np
import math
img = cv2.imread("answer1.bmp") #integer
_img = img[:,:,0]
H, W = _img.shape
rmax = math.ceil(np.sqrt(H**2 + W**2))

bort = np.zeros((2*rmax,180), dtype = np.float)
for t in range(180):
    for x in range(W):
        for y in range(H):
            if _img[y, x] != 0:
                tr = t * np.pi/180 
                rho = int(x*np.cos(tr) + y*np.sin(tr))
                #rho の極値は角度がrhoのt微分が0になるとき
                #rhoが最大なのは対角線の長さ
                #微分とかしなくても直感的に対角線が最大になるのは理解できる
                #ｔの範囲は0～180° rhoの範囲は-rmax ~ rmax このように範囲をとればすべての直線を網羅
                #t=270°で直線を引きたい場合は、t=90で、rの値がマイナスになったのと実質同じ
                bort[rho+rmax, t] = bort[rho+rmax, t] + 1 
print(bort)
bort.astype(np.uint8)
cv2.imwrite("answer-hough.bmp", bort)
cv2.imshow("result1", bort)


cv2.waitKey(0)
cv2.destroyAllwindows()
