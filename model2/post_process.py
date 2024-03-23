import torch
import numpy as np
import torch.nn.functional as F
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt
import math
import random


def threshold(tensor, thresh):
    '''

    :param tensor: [1,1,255,255]
    :param thresh: 阈值
    :return: 【1,1,255,255】
    '''
    tensor = tensor * 255
    tensort = torch.where(tensor < thresh, 0, 255)
    return tensort


def find_threshold(tensor):
    '''
    找到最佳的阈值范围
    :param tensor: 【1,1,255,255】
    :return: threshold
    '''
    tensor = tensor.cpu() * 255
    tensor_arr = tensor.detach().numpy()
    hist, bins = np.histogram(tensor_arr, bins=50, density=True)
    min_index = np.argmin(hist[5:-5])
    min_value = bins[min_index + 5]
    # if 4 < min_index < 46:
    #     return min_value
    # else:
    #     print('最小值：', min_value, '索引数：', min_index)
    #     raise ValueError("索引太偏向一边了")
    return min_value


def save_tensor(tensor, savedir):
    '''

    :param tensor: [1,1,255,255]
    :param savedir: str,dir
    :return: save file
    '''
    tensor = tensor.squeeze(0)
    tensor = tensor.permute(1, 2, 0)
    tensor = tensor.cpu()
    array = tensor.detach().numpy()
    array = np.uint8(array)
    im = Image.fromarray(array[:, :, 0])
    im.save(savedir)
    print(savedir, '已保存')

def show_tensor(tensor, name):
    '''
    :param tensor: [1,1,255,255] tensor
    :param name: str
    :return: showimg
    '''
    tensor = tensor.squeeze(0)
    tensor = tensor.permute(1, 2, 0)
    tensor = tensor.cpu()
    array = tensor.detach().numpy()
    array = np.uint8(array)
    im = Image.fromarray(array[:, :, 0])
    im.show(name)


def open_close(image_np, lopnumber,):
    '''
    :param tensor:  [1,1,255,255]
    :param lopnumber: 腐蚀膨胀循环次数
    :return: 【255,255】
    '''
    reverse = False
    # 定义结构元素（卷积核）
    kernel = np.ones((3, 3), np.uint8)
    for i in range(lopnumber):
        if reverse:
            # 膨胀操作
            image_np = cv2.dilate(image_np, kernel, iterations=2)
            # 腐蚀操作
            image_np = cv2.erode(image_np, kernel, iterations=2)
        else:
            # 腐蚀操作
            image_np = cv2.erode(image_np, kernel, iterations=2)
            # 膨胀操作
            image_np = cv2.dilate(image_np, kernel, iterations=2)
    return image_np


def anas_binary(img_binary):
    '''
    通过轮廓检测，获得轮廓的物理信息，返回一个数据列表
    :param img_binary: [h,w],bin
    :return: data colorimg
    '''

    # canny = cv2.Canny(np.uint8(img_binary), 100, 200)
    # cv2.imshow('aftercanny',canny)
    # cv2.waitKey(0)
    img_binary = np.uint8(img_binary)
    shape = img_binary.shape
    filled_image = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
    # 轮廓检测
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 4.轮廓绘制
    for i in range(len(contours)):
        # 生成随机颜色
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # 绘制填充轮廓
        filled_image = cv2.drawContours(filled_image, contours, i, color, thickness=cv2.FILLED)

    # cv2.imshow('filled_image',filled_image)
    # cv2.imshow('imag',img_binary)
    # cv2.waitKey(0)
    data = {
        '面积': [],
        '周长': [],
        '等效粒径': []
    }
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, closed=True)
        equivalent_particle = calculation(area, perimeter) if area != 0 else 0
        data['面积'].append(area)
        data['周长'].append(perimeter)
        data['等效粒径'].append(equivalent_particle)
    return data, filled_image


def calculation(area, zhouchang):
    pi = math.pi
    s = area
    p = zhouchang
    a = 1 / 2 * (p / pi + ((p * p / pi / pi) - (4 * s / pi)) ** 0.5)
    b = 1 / 2 * (p / pi - ((p * p / pi / pi) - (4 * s / pi)) ** 0.5)
    d = 29 / 25 * b * (27 / 20 * a / b) ** 0.5
    return d


def watershed(img_bin, threshold, show: bool):
    '''
    img_bin [255,255]
    return mask
    '''
    h, w = img_bin.shape
    mask = np.array(img_bin, np.uint8)
    img_ = np.zeros((h, w, 3), dtype=np.uint8)
    img_[:, :, 0] = mask
    img_[:, :, 1] = mask
    img_[:, :, 2] = mask
    # cv2.imshow('img_',img_)
    # cv2.waitKey(0)
    dist_transfrom = cv2.distanceTransform(mask, cv2.DIST_L2, 5)  # 生成距离矩阵
    dist_transfrom = np.array(dist_transfrom, np.uint8)

    ret, sure_fg = cv2.threshold(dist_transfrom,threshold, 255,
                                 0)  # 距离矩阵进行阈值处理，剩余核心部分threshold * dist_transfrom.max()
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(mask, sure_fg)  # 原始二值图像与核心图像相减，得到部分不确定边界
    if show:
        cv2.imshow('first', img_bin)
        cv2.imshow('sure_fg', sure_fg)
        cv2.waitKey(0)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)  # 核心区域进行标记0 1 2
    markers = np.array(markers, np.uint8)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1  # 1 2 3
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0  # 未知区域 0 背景1 物体2 物体3
    markers = np.array(markers, np.int32)
    markers = cv2.watershed(img_, markers)

    mask__ = np.zeros((h, w,), dtype=np.uint8)
    mask__[markers ==-1] = [255]
    mask__ = cv2.dilate(mask__,kernel=np.ones((3, 3), np.uint8),iterations=1)
    mask[mask__==255]=[0]
    # cv2.imshow('mask__',mask__)
    # cv2.imshow('mask',mask)
    # cv2.waitKey(0)
    #mask[markers == -1] = [0]
    return mask


def tensor_to_numpy(tensor):
    '''
    [0-1] to [0-255]
    :param tensor: [1,1,255,255]
    :return: [255,255]
    '''
    tensor = tensor.squeeze(0).squeeze(0)
    #tensor = tensor.permute(1, 2, 0)
    tensor = tensor.cpu()
    image_np = tensor.detach().numpy().astype(np.uint8)
    return image_np


def post_process(pred1, pred2, show=False, ):
    '''

    :param pred1: 【1，1，512，512】  region
    :param pred2: 【1，1，512，512】  contour
    :param show: bool
    :return: data colorimg
    '''
    # 阈值分割 and 拼接
    process_by_cv = False
    if process_by_cv:
        pred1_np = tensor_to_numpy(pred1)
        ret1, bin1 = cv2.threshold(pred1_np, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        pred2_np = tensor_to_numpy(pred2)
        ret2, bin2 = cv2.threshold(pred2_np, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        all1 = np.where(bin2 > 0, 0, bin1)

    else:
        threshold1 = find_threshold(pred1)
        region_tensor_threshold = threshold(pred1, threshold1 * 2)
        outline_tensor_threshold = threshold(pred2, 25)
        all1 = torch.where(outline_tensor_threshold > 0, 0, region_tensor_threshold)


    # 先分水+膨胀腐蚀操作
    image_np1 = tensor_to_numpy(tensor=all1)
    image1 = watershed(image_np1, 13, show=False)
    image1 = open_close(image1, 4)

    # # 膨胀 +分水
    # image_np2 = tensor_to_numpy(tensor=all1)
    # image2 = open_close(image_np2, 4)
    # image2 = watershed(image2, 13, show=False)
    # cv2.imshow('a1', image1)
    # cv2.imshow('a2', image2)
    # 轮廓检测 和轮廓参数
    data, colorimg = anas_binary(image1)

    # 展示阶段
    if show:
        show_tensor(region_tensor_threshold, '1')
        show_tensor(outline_tensor_threshold, '2')
        im1 = Image.fromarray(image)
        im1.show('after open and close')
        im = Image.fromarray(colorimg)
        im.show('color')
    return data, colorimg


if __name__ == '__main__':
    print(0)