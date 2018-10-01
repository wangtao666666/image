#encoding='utf-8'

from PIL import Image

def calculate(image1, image2):
    g = image1.histogram()
    s = image2.histogram()
    assert len(g) == len(s), "error"

    data = []

    for index in range(0, len(g)):
        if g[index] != s[index]:
            data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
        else:
            data.append(1)

    return sum(data) / len(g)


def split_imgae(image, part_size):
    pw, ph = part_size
    w, h = image.size

    sub_image_list = []

    assert w % pw == h % ph == 0, "error"

    for i in range(0, w, pw):
        for j in range(0, h, ph):
            sub_image = image.crop((i, j, i + pw, j + ph)).copy()
            sub_image_list.append(sub_image)

    return sub_image_list


def classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64)):

    image1 = image1.resize(size).convert("RGB")
    sub_image1 = split_imgae(image1, part_size)

    image2 = image2.resize(size).convert("RGB")
    sub_image2 = split_imgae(image2, part_size)

    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)

    x = size[0] / part_size[0]
    y = size[1] / part_size[1]

    pre = round((sub_data / (x * y)), 3)
    return pre

if __name__ == '__main__':
    image1 = Image.open("./image1.jpg")
    image2 = Image.open("./image2.jpg")
    result = classfiy_histogram_with_split(image1, image2)
    print(result)