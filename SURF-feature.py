# encoding='utf-8'

import cv2
import scipy as sp

file_path = '/Users/apple/PycharmProjects/company-image/feature/dataset/'

import datetime

starttime = datetime.datetime.now()

result = {}

img1 = cv2.imread(file_path + '1.png')  # query

gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
surf = cv2.xfeatures2d.SURF_create()
kp1, des1 = surf.detectAndCompute(gray1, None)

for i in range(2, 10000):
    print(i)
    try:
        img2 = cv2.imread(file_path + str(i) + '.png')  # train
        # sift = cv2.SIFT()
        # 计算描述子 其中kp表示关键点，des是指关键点的特征描述
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        surf = cv2.xfeatures2d.SURF_create()
        kp2, des2 = surf.detectAndCompute(gray2, None)
        # kp2, des2 = sift.detectAndCompute(img2, None)

        # print('des1:',des1)
        # print('len(des1):',len(des1[0]))
        # print('des2:',des2)
        # print('len(des2):',len(des2[0]))

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # print('matches....',len(matches))

        good = []

        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        result[str(i)] = len(good)
        # print('good',len(good))

    except:
        print('except......:', i)

endtime = datetime.datetime.now()

print((endtime - starttime).seconds)

result = sorted(result.items(), key=lambda x: x[1], reverse=True)
print('result:', result)