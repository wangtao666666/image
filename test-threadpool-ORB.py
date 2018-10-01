# encoding='utf-8'

import cv2
import scipy as sp
import datetime
import threadpool

def match(num):
    result = {}
    for i in range(num[0],num[1]):
        print(i)
        try:
            img2 = cv2.imread(file_path + str(i) + '.png')  # train
            kp2, des2 = orb.detectAndCompute(img2, None)

            #knn匹配
            # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            # matches = bf.knnMatch(des1,des2,k=1)
            # good = [m for (m,n) in matches if m.distance < 0.75*n.distance]
            # result[str(i)] = len(good)

            #bf 暴力匹配
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            result[str(i)] = len(matches)
            # print('good',len(good))

            #FLANN匹配器
            # FLANN_INDEX_KDTREE ＝ 0
            # Flann_index_kdtree = 0
            # indexParams = dict(algorithm = Flann_index_kdtree,tree = 5)
            # searchParams = dict(checks = 50)
            # flann = cv2.FlannBasedMatcher(indexParams,searchParams)
            # des1 = des1.convertTo(des1,CV_32F)
            # des2 = des2.convertTo(des2,CV_32F)
            # matches = flann.knnMatch(des1,des2,k=2)
            # matchesMask = [[0,0] for i in range(matches)]
            #
            # for i,(m,n) in enumerate(matches):
            #     if m.distance < 0.7*n.distance:
            #         matchesMask[i] = [1,0]
            #
            # print(matchesMask)

        except:
            print('except......:', i)

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    return result


if __name__ == '__main__':

    file_path = '/Users/apple/PycharmProjects/company-image/feature/dataset/'

    starttime = datetime.datetime.now()

    img1 = cv2.imread(file_path + '1.png')  # query
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    pool = threadpool.ThreadPool(20)
    task_param_list = [[1,500],[501,1000],[1001,1500],[1501,2000],[2001,2500],[2501,3000],[3001,3500],[3501,4000],[4001,4500],[4501,5000],
                       [5001,5500],[5501,6000],[6001,6500],[6501,7000],[7001,7500],[7501,8000],[8001,8500],[8501,9000],[9500,9999]]

    task_list = threadpool.makeRequests(match, task_param_list)
    [pool.putRequest(x) for x in task_list]

    pool.wait()
    print("dispose finished")

    endtime = datetime.datetime.now()

    print((endtime - starttime).seconds)



