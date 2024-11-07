import cv2 as cv
import numpy as np


def template_demo():
    tpl = cv.imread("./pics/main2.png")
    target = cv.imread("pics/add.jpg")
    cv.imshow("template image", tpl)
    cv.imshow("target image", target)
    method = cv.TM_CCOEFF_NORMED  # 各种匹配算法
    height, width = tpl.shape[:2]  # 获取模板图像的高宽'
    print(height, width)

    result = cv.matchTemplate(target, tpl, method)
    # threshold = 0.7
    # # res大于70%
    # loc = np.where(result >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv.rectangle(tpl, pt, (pt[0] + width, pt[1] + height), (7, 249, 151), 2)

    cv.imshow(f"match-%{method}", target)
    min_val_tgt, max_val_tgt, min_loc_tgt, max_loc_tgt = cv.minMaxLoc(result)
    print(max_val_tgt)
    print(min_loc_tgt, max_loc_tgt)
    print(max_loc_tgt[0] / width, max_loc_tgt[1] / height)
    return (min_loc_tgt[0] + max_loc_tgt[0]) / 2, (min_loc_tgt[1] + max_loc_tgt[1]) / 2


print(template_demo())

cv.waitKey(0)
