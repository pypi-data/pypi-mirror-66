import cv2
import math


def judge_similar_area(img, x1, y1, x2, y2):
    """
    判断区域(x1, y1, x2, y2)是否相似（是否轮廓突变，边界为轮廓突变）
    :param im: 背景图片
    :param x1:  区域起始列
    :param y1:  区域起始行
    :param x2:  区域结束
    :param y2:  区域结束行
    :return:    True:该区域为空白区域, False:该区域非空白区域
    """

    # img = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
    height, width = img.shape[:2]
    if x1 < 0 or y1 < 0 or x2 > width - 1 or y2 > height - 1 or x1 > x2 or y1 > y2:
        # 是否超出im范围
        return False

    crop = img[y1:y2, x1:x2]
    crop = cv2.Canny(crop, 64, 128)  # 检查阈值边缘差距
    contours, _ = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        return False
    return True


def spreading_area(img, rect, align, offset, direct, limit=None):
    """
    对一个区域，向上下移动，找到安全的区域（区域不突变）
    :param rect:
    :param align:
    :param offset: 2
    :param direct: 0 y，1 x
    :param limit:
    :return:
    """
    if limit:
        limit = min([limit, img.shape[direct]])
    else:
        limit = img.shape[direct]
    index_1, index_2 = (0, 2) if direct else (1, 3)
    temp_rect = cur_rect = rect.copy()
    while True:
        is_similar_area = judge_similar_area(img, *temp_rect)
        if is_similar_area:
            cur_rect = temp_rect.copy()
            if align == 0:  # 做对齐
                ymax = temp_rect[index_2] + offset
                if ymax - temp_rect[index_1] + 1 > limit:
                    break
                temp_rect[index_2] = ymax
            elif align == 1:
                ymin, ymax = temp_rect[index_1] - offset, temp_rect[index_2] + offset
                if ymin < 0 or ymax - ymin + 1 > limit:
                    break
                temp_rect[index_1] = ymin
                temp_rect[index_2] = ymax
            else:
                ymin = temp_rect[index_1] - offset
                if ymin < 0 and temp_rect[index_2] - ymin + 1 > limit:
                    temp_rect[index_1] = ymin
                temp_rect[index_1] = ymin
        else:
            cur_rect[index_1] = max(cur_rect[index_1], 0)
            # cur_rect[index_2] = min(cur_rect[index_2], limit - 1)
            break
    return cur_rect


def multi_spreading_area(img, rect, factor_info):
    temp_rect = rect.copy()
    while True:
        cur_rect = temp_rect.copy()
        for index, factor in factor_info.items():
            temp_rect[index] += factor * (1 if index >= 2 else -1)
        is_similar_area = judge_similar_area(img, *rect)
        if not is_similar_area:
            break
    return cur_rect


def par_relarge_area(img, rect, xy_align, par):
    x_align, y_align = xy_align
    x_center, y_center = rect[0] + rect[2], rect[1] + rect[3]
    temp_rect = cur_rect = rect.copy()
    while True:
        is_similar_area = judge_similar_area(img, *temp_rect)
        if not is_similar_area:
            break

        cur_rect = temp_rect.copy()
        if par > 1:
            if y_align == 0:
                temp_rect[3] += 2
            elif y_align == 1:
                temp_rect[1] -= 1
                temp_rect[3] += 1
            else:
                temp_rect[1] -= 2

            req = math.ceil((temp_rect[3] - temp_rect[1] + 1) * par)
            if x_align == 0:
                temp_rect[2] = temp_rect[0] + req - 1
            elif x_align == 1:
                temp_rect[0] = int((x_center - req) / 2) + 1
                temp_rect[2] = req + temp_rect[0] - 1
            else:
                temp_rect[0] = temp_rect[2] - req + 1
        else:
            if x_align == 0:
                temp_rect[2] += 2
            elif x_align == 1:
                temp_rect[0] -= 1
                temp_rect[2] += 1
            else:
                temp_rect[0] -= 2

            req = math.ceil((temp_rect[2] - temp_rect[0] + 1) * par)
            if y_align == 0:
                temp_rect[3] = temp_rect[1] + req - 1
            elif y_align == 1:
                temp_rect[1] = int((y_center - req) / 2)
                temp_rect[3] = req + temp_rect[1] - 1
            else:
                temp_rect[1] = temp_rect[3] - req + 1

    return cur_rect
