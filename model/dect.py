import os
import numpy as np
from ultralytics import YOLO
from model import post_process
import math
import json
import torch
from PIL import Image

import streamlit as st
def jipei(dlist, name,countdot=20):
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
    return x,y_precent
    # zhenlv = 12/(end_time-start_time)
    # post_process(results ,save = True,save_dir = r'D:\gimodels\yolov8\seg_rock\runs\Post-processing',watershed = True,threshold=0.96)

@st._cache_data
def houduan(state):
    ptdir = r'D:\python_code\web-fabu\model\Parameter\best.pt'
    # Load a model
    model = YOLO(ptdir)  # load a pretrained model (recommended for training)
    dlists = []
    colorimgs = []
    names=[]
    for load in state:
        image = Image.open(load)
        img_array = np.array(image)
        # dectfile = r'C:\Users\Administrator\Desktop\wq\web-fabu\model\0jpg_00.jpg'
        results = model(img_array, save=False)
        a = post_process.Post_processing_single(results=results, show_color=True, water=True, show=False,save =False,save_dir='')
        data2 = {'周长':[],
                 '等效粒径':[],
                 '面积':[]}
        for i in a.data:
            data2['周长'].append(i['周长'][0])
            data2['等效粒径'].append(i['等效粒径'][0])
            data2['面积'].append(i['面积'][0])
        dlists.append(data2)
        colorimgs.append(a.all_color)
        names.append(load.name)
    return dlists,colorimgs,names
if __name__ == '__main__':
    houduan([1,2])
