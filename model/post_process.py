import cv2
import numpy as np
import torch
import os
import math


class Post_processing_single(object):
    #单个图像的后处理类
    #接受的results为单个元素的列表
    def __init__(self,results,show_color=True,water=False,show=False,save=True,save_dir='D:\python_code\web_system_detect\Predict\result'):
        self.result = results[0]
        self.filename = self.result.path.split('\\')[-1]
        self.boxes = self.result.boxes  # Boxes object for bbox outputs
        self.masks = self.result.masks.data.cpu()  # Masks object for segment masks outputs
        self.probs = self.result.probs  # Class probabilities for classification output
        self.num = self.masks.shape[0]
        self.shape1 = self.masks.shape[1]
        self.shape2 = self.masks.shape[2]
        self.save_dir = save_dir
        #all color and all bin
        if show_color==True:
            self.all_color = self.show_color()
        self.all_bin = self.show_mask()
        #data
        self.data = []
        for i in range(self.num):
            self.data.append(self.anas_binary(255*self.masks[i, :, :]))
        self.dlist = []
        for i in self.data:
            dlist = i['等效粒径']
            for j in range(len(dlist)):
                if dlist[j] != 0:
                    self.dlist.append(dlist[j])
        #watershed part
        if water == True:
            masklist = self.split_mask()
            self.all_bin_water, self.infor_list_water = self.watershed(masklist,threshold=0.5)

        if show:
            self.show()
        if save:
            self.save()


    def show(self):
        self.all_bin = np.array(self.all_bin, dtype=np.uint8)
        cv2.imshow('color',self.all_color)
        cv2.imshow('bin', self.all_bin)
        cv2.waitKey(0)

    def save(self):
        savedir = self.save_dir
        self.check_and_create_folder(savedir, self.filename)
        basedir =os.path.join(savedir,self.filename)
        cv2.imwrite(os.path.join(basedir,'color.jpg'),self.all_color)
        cv2.imwrite(os.path.join(basedir, 'bin.jpg'), self.all_bin)
        cv2.imwrite(os.path.join(basedir, 'afterwater.jpg'), self.all_bin_water)
        print(self.filename,'彩色图，黑白图，分水岭后黑白图已保存')

    def show_mask(self):
        # 传入mask，将所有mask组成一个图
        # 返回值 图像二值化矩阵，或者空列表
        masks = self.masks.cpu()
        mk = torch.zeros((self.shape1, self.shape2))
        for i in range(self.num):
            mk += masks[i, :, :]
        mkk = torch.where(mk>0,255,0)
        mkk = np.array(mkk, dtype=np.uint8)
        # for i in range(shape[1]):
        #     for j in range(shape[2]):
        #         if mk[i, j] != 0:
        #             mk[i, j] = 255
        return mkk

        # cv2.imshow('a',mk)
        # key = cv2.waitKey(0)

    def show_color(self):
        # 展示最初的检测效果,汇总的实例分割--彩色图像
        all_color = np.zeros((self.shape1, self.shape2, 3))
        for j in range(self.num):
            img = self.masks[j, :, :]
            img = img.unsqueeze(0)
            bimg = torch.where(img > 0, int(255 * np.random.rand(1)), 0)
            rimg = torch.where(img > 0, int(255 * np.random.rand(1)), 0)
            yimg = torch.where(img > 0, int(255 * np.random.rand(1)), 0)
            colorimg = torch.cat((bimg, rimg, yimg), 0)
            colorimg = colorimg.permute(1, 2, 0).numpy()
            all_color = all_color + colorimg
        all_color = np.array(all_color, dtype=np.uint8)
        # cv2.imshow('color',all_color)
        # cv2.waitKey(0)
        return all_color

    def watershed(self, masklist, threshold):
        if isinstance(masklist, list):
            h, w = masklist[0].shape
            infor_list = []
            all_masks_img = np.zeros((h, w), dtype=np.uint8)
            for mask in masklist:
                mask = np.array(mask, np.uint8)
                img_ = np.zeros((h, w, 3), dtype=np.uint8)
                img_[:, :, 0] = mask
                img_[:, :, 1] = mask
                img_[:, :, 2] = mask
                # cv2.imshow('img_',img_)
                # cv2.waitKey(0)
                dist_transfrom = cv2.distanceTransform(mask, cv2.DIST_L2, 5)  # 生成距离矩阵
                dist_transfrom = np.array(dist_transfrom, np.uint8)

                ret, sure_fg = cv2.threshold(dist_transfrom, threshold * dist_transfrom.max(), 255,
                                             0)  # 距离矩阵进行阈值处理，剩余核心部分
                # Finding unknown region
                sure_fg = np.uint8(sure_fg)
                unknown = cv2.subtract(mask, sure_fg)  # 原始二值图像与核心图像相减，得到部分不确定边界

                # cv2.imshow('a',dist_transfrom)
                # cv2.imshow('sure_fg',sure_fg)
                # cv2.imshow('unknow', unknown)
                # cv2.waitKey(0)

                # Marker labelling
                ret, markers = cv2.connectedComponents(sure_fg)  # 核心区域进行标记0 1 2
                markers = np.array(markers, np.uint8)
                # Add one to all labels so that sure background is not 0, but 1
                markers = markers + 1  # 1 2 3
                # Now, mark the region of unknown with zero
                markers[unknown == 255] = 0  # 未知区域 0 背景1 物体2 物体3
                markers = np.array(markers, np.int32)
                markers = cv2.watershed(img_, markers)
                mask[markers == -1] = [0]
                all_masks_img += mask
                # cv2.imshow('watershed', mask)
                # cv2.waitKey(0)
                ##mask继续算边缘值
                infor_list.append(self.anas_binary(mask))
            # cv2.imshow('all',all_masks_img)
            # cv2.waitKey(0)
            #print('图片轮廓信息\n', infor_list)
            return all_masks_img, infor_list

    def split_mask(self):
        all_bin_img = np.array(self.all_bin, np.uint8)
        h, w = all_bin_img.shape
        imgz = np.zeros((h, w))
        contours, hierarchy = cv2.findContours(all_bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        masklist = []
        for i in range(len(contours)):
            imgz = np.zeros((h, w))
            imgz = cv2.drawContours(imgz, contours, i, (255, 255, 255), thickness=cv2.FILLED)
            # cv2.imshow('a',imgz)
            # cv2.waitKey(0)
            masklist.append(imgz)
        return masklist

        # if kwargs['watershed']:
        #     bin_img,information = watershed(masklist,kwargs['threshold'])
        #     list.append(information)

    def anas_binary(self,img_binary):
        #通过轮廓检测，获得轮廓的物理信息，返回一个数据列表
        #边缘检测
        canny = cv2.Canny(np.uint8(img_binary), 100, 200)
        # cv2.imshow('aftercanny',canny)
        # cv2.waitKey(0)
        #轮廓检测
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # 4.轮廓绘制
        img = cv2.drawContours(canny, contours, -1, (255, 255, 255), thickness=3)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        data = {
            '面积':[],
            '周长':[],
            '等效粒径':[]
        }
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, closed=True)
            equivalent_particle = self.calculation(area, perimeter) if area != 0 else 0
            data['面积'].append(area)
            data['周长'].append(perimeter)
            data['等效粒径'].append(equivalent_particle)
        return data

    def calculation(self,area,zhouchang):
        pi = math.pi
        s = area
        p = zhouchang
        a = 1/2*(p/pi+((p*p/pi/pi)-(4*s/pi))**0.5)
        b = 1/2*(p/pi-((p*p/pi/pi)-(4*s/pi))**0.5)
        d = 29/25*b*(27/20*a/b)**0.5
        return d

    def check_and_create_folder(self, path, folder_name):
        # 拼接文件夹路径
        folder_path = os.path.join(path, folder_name)

        # 判断文件夹是否存在
        if not os.path.exists(folder_path):
            # 如果不存在，创建文件夹
            os.makedirs(folder_path)
            print(f"文件夹 '{folder_name}' 已创建成功.")
        else:
            print(f"文件夹 '{folder_name}' 已存在.")


class Post_processing_all(object):
    def __init__(self):
        self.pos = []

    def add_po(self,po):
        self.pos.append(po)

    def dlist(self):
        ds_dic={}
        for po in self.pos:
            i = po.filename[0]
            dlist = po.dlist
            if i not in ds_dic:
                ds_dic[i] = dlist
            else:
                ds_dic[i].extend(dlist)
        return ds_dic

    def jipei(self,dlist, name, countdot=20):
        dlist = np.array(dlist)
        num = len(dlist)
        dlist = sorted(dlist)
        dmax = max(dlist)
        dmin = min(dlist)
        d_ = (dmax - dmin) / countdot
        x = [dmin + i * d_ for i in range(countdot + 1)]
        x_ = [math.log10(j) for j in x]
        y = [np.sum(dlist <= (dmin + i * d_)) for i in range(countdot + 1)]
        y_precent = np.array(y).astype(float) / num
        return x, y_precent

    def creat_matplotlib_figure(self,x, y, name):
        # 创建散点图
        # plt.scatter(x_, y_precent, label='数据点')
        # 连线
        fig, ax = plt.subplots()
        y_precent = y
        ax.plot(x, y_precent, label='连线', color='r')
        # 添加标题和标签
        title = 'Gradation curve' + str(name)
        ax.set_title(title)
        ax.set_xlabel('Particle size')
        ax.set_ylabel('Particle size ratio')
        return fig

