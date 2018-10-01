#encoding='utf-8'

"""用平均哈希法实现识别相似图片"""
"""
    调研平均哈希法步骤如下：
    1、缩小尺寸 ：将图片缩小到8*8的尺寸，总共64个元素
    作用是去除图片的细节，只保留结构、明暗等基本信息，摒弃不同尺寸、比例带来的图片差异
    2、简化色彩
    将缩小后的图片，转为64级灰度。也就是说，所有像素点总共有64中颜色
    3、计算平均值
    计算所有64个像素的灰度平均值
    4、比较像素的灰度
    将每个像素的灰度，与平均值进行比较。大于或等于平均值，记为1；小于平均值，记为0
    5、计算哈希值
    将上一步的比例结果，组合在一起，就构成一个64位的整数，这就是这张图片的指纹
    得到指纹以后，就可以对比不同的图片，看看64位中有多少位是不一样的－－》等同于计算汉明距离
    如果不相同的数据位数不超过5，就说明两张图片很相似
    如果不相同数据位数大于10，则说明两张图片不相同
"""

from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps

def getCode(img, size):
    pixel = []
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            pixel_value = img.getpixel((x, y))
            pixel.append(pixel_value)

    avg = sum(pixel) / len(pixel)

    cp = []

    for px in pixel:
        if px > avg:
            cp.append(1)
        else:
            cp.append(0)
    return cp


def compCode(code1, code2):
    num = 0
    for index in range(0, len(code1)):
        if code1[index] != code2[index]:
            num += 1
    return num


def classfiy_aHash(image1, image2, size=(8, 8), exact=25):

    """
    image.convert() 图片灰度化处理：将RGB/RGBA->L
    image.filter() 图像滤波
    API参考链接：https://blog.csdn.net/louishao/article/details/69879981
    """

    image1 = image1.resize(size).convert('L').filter(ImageFilter.BLUR)
    image1 = ImageOps.equalize(image1) #均衡图像直方图，为产生灰色值均匀分布输出图像
    code1 = getCode(image1, size)
    # print(code1)

    image2 = image2.resize(size).convert('L').filter(ImageFilter.BLUR)
    image2 = ImageOps.equalize(image2)
    code2 = getCode(image2, size)

    assert len(code1) == len(code2), "error"

    return compCode(code1,code2)
    # return compCode(code1, code2) <= exact


if __name__ == '__main__':
    import os
    import operator

    filename = os.listdir('/Users/apple/PycharmProjects/company-image/hash-feature/picture')
    print('filename:',filename)

    dict = {}
    image1 = Image.open('./text-image/'+filename[1])

    for i in range(1,20):
        image2 = Image.open('./picture/'+filename[i])
        result = classfiy_aHash(image1, image2)
        dict[str(filename[i])] = result
    listname = sorted(dict.items(),key=operator.itemgetter(1))

    for i in range(len(listname)):
        print(listname[i][0])

