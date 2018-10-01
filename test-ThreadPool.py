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
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            result[str(i)] = len(matches)
            # print('good',len(good))
        except:
            print('except......:', i)

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    return result


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    file_path = '/Users/apple/PycharmProjects/company-image/feature/dataset/'

    starttime = datetime.datetime.now()

    img1 = cv2.imread(file_path + '1.png')  # query
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)

    # pool = threadpool.ThreadPool(10)
    # task_param_list = [[1,1000],[1001,2000],[2001,3000],[3001,4000],[4001,5000],[5001,6000],[6001,7000],[7001,8000],[8001,9999]]
    task_param_list = [[1,500],[501,1000],[1001,1500],[1501,2000],[2001,2500],[2501,3000],[3001,3500],[3501,4000],[4001,4500],[4501,5000],
                       [5001,5500],[5501,6000],[6001,6500],[6501,7000],[7001,7500],[7501,8000],[8001,8500],[8501,9000],[9500,9999]]

    result2 = {}
    with ThreadPoolExecutor(20) as executor:
        [executor.submit(match,x) for x in task_param_list]

    print("dispose finished")

    endtime = datetime.datetime.now()

    print((endtime - starttime).seconds)



