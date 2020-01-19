import cv2
import numpy as np
import math

#直線検出したい画像を入力
img_ori = cv2.imread("test_image1_big.bmp") #integer

#q-44ではきだされた細線画像を入力
img = cv2.imread("answer1-big.bmp") #integer

########################　細線画像の各画素をハフ空間で描画　#########################
_img = img[:,:,0]
H, W = _img.shape
#対角線の長さの導出
rmax = math.ceil(np.sqrt(H**2 + W**2))
ind = np.where(img == 255)
bort = np.zeros((2*rmax, 180), dtype = np.int)

for y, x in zip(ind[0], ind[1]):
    for t in range(0, 180, 1):
            
            th = np.pi/180*t
            rho = int(x*np.cos(th) + y*np.sin(th))
            #rho の極値は角度がrhoのt微分が0になるとき
            #rhoが最大なのは対角線の長さ
            #微分とかしなくても直感的に対角線が最大になるのは理解できる
            #ｔの範囲は0～180° rhoの範囲は-rmax ~ rmax このように範囲をとればすべての直線を網羅
            #t=270°で直線を引きたい場合は、t=90で、rの値がマイナスになったのと実質同じ
            bort[rho+rmax, t] = bort[rho+rmax, t] + 1 

bort.astype(np.uint8)

Hb, Wb = bort.shape
for l in range(Hb):
    for m in range(180):
        #画像の端を選んだときの対処
        y1 = max(l-1, 0)
        x1 = max(m-1, 0)
        x2 = min(m+2, 180)
        y2 = min(l+2, Hb-1)
        if np.max(bort[y1:y2, x1:x2]) == bort[l, m] and bort[l, m] != 0:
            pass
        else:
            bort[l, m] = 0

###############################################################################

####################### ハフ空間で画素値上位20のインデックスを取得　###################
#######################　→該当箇所を白く埋める ####################################
ind_x = np.argsort(bort.ravel())[::-1][:10]
# rabel()で配列を1次元に並べる
#→argsortで値が低い順番からインデックスを返す
#→[::-1]で値が高い順番に変更
#→[:20]で左から20個の値を取得。上位20のx方向のインデックスが得られる
ind_y = ind_x.copy()
thetas = ind_x % 180
rhos = (ind_y // 180) - rmax


# //は切り捨て除算
#ind_xは180の行が一列に並んでいる状態で、20位までインデックスが記録されている
#だから180で割れば何分割目か出てくる→何行目かわかる
#その余りは×分割目の○番目→列番号が分かる

#hough = np.zeros_like(bort, dtype = np.int)
#hough[rhos, thetas] = 255

###############################################################################
################################## 逆変換 #####################################
print(rhos)
print(thetas)
for r, t in zip(rhos, thetas):
    th = np.pi/180.*t
    for x in range(img_ori.shape[1]):
        if np.sin(th) != 0:
            y = -(np.cos(th)/np.sin(th))*x + (r/np.sin(th))
            y = int(y)
            if y>=img_ori.shape[0] or y<0:
                continue
            img_ori[y, x] = [0, 0, 255] 
    for y in range(img_ori.shape[0]):
        if np.cos(th) != 0:
            x = -(np.sin(th)/np.cos(th))*y + (r/np.cos(th))
            x = int(x)
            if x>=img_ori.shape[1] or x<0:
                continue
            img_ori[y, x] = [0, 0, 255] 

###############################################################################

cv2.imwrite("result.bmp", img_ori)
cv2.imshow("result", img_ori)

cv2.waitKey(0)
cv2.destroyAllwindows()
