# encoding='utf-8'

import cv2
import scipy as sp

file_path = '/Users/apple/PycharmProjects/company-image/feature/dataset/'

import datetime

starttime = datetime.datetime.now()

result = {}

img1 = cv2.imread(file_path + '1.png')  # query

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)


for i in range(2, 10000):
    print(i)
    try:
        img2 = cv2.imread(file_path + str(i) + '.png')  # train
        # sift = cv2.SIFT()
        # 计算描述子 其中kp表示关键点，des是指关键点的特征描述
        kp2, des2 = orb.detectAndCompute(img2, None)

        # kp2, des2 = sift.detectAndCompute(img2, None)

        # print('des1:',des1)
        # print('len(des1):',len(des1[0]))
        # print('des2:',des2)
        # print('len(des2):',len(des2[0]))

        # FLANN_INDEX_KDTREE = 0
        # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # search_params = dict(checks=50)
        # flann = cv2.FlannBasedMatcher(index_params, search_params)
        # matches = flann.knnMatch(des1, des2, k=2)
        # print('matches....',len(matches))

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # good = []
        #
        # for m, n in matches:
        #     if m.distance < 0.75 * n.distance:
        #         good.append(m)

        result[str(i)] = len(matches)
        # print('good',len(good))

    except:
        print('except......:', i)

endtime = datetime.datetime.now()

print((endtime - starttime).seconds)

result = sorted(result.items(), key=lambda x: x[1], reverse=True)
print('result:', result)