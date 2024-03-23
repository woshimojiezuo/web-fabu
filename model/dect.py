import os
import numpy as np
from ultralytics import YOLO
from model import post_process
import math
import json
import torch
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

def houduan(basedir):
    ptdir = r'D:\python_code\web-fabu\model\Parameter\best.pt'
    weights_path = ptdir
    checkpoint = torch.load(weights_path)
    jsonfilename = os.path.join(basedir, r'model/size/sizes.json')
    # Load a model
    model = YOLO(ptdir)  # load a pretrained model (recommended for training)

    filelist = [r'D:\python_code\web-fabu\model\0jpg_00.jpg']
    ds_dic = {}
    for file in filelist:
        dectfile = file

        results = model(dectfile, save=False)
        a = post_process.Post_processing_single(results=results, show_color=True, water=True, show=False,save =False,save_dir='')
        dlist = a.dlist
        ds_dic[file] = dlist
        # i = file[0]
        # if i not in ds_dic:
        #     ds_dic[i] = dlist
        # else:
        #     ds_dic[i].extend(dlist)
    # ds_dic = a.dlist()#根据文件名生成字典
    # for key, value in ds_dic.items():
    #     x, y = pop.jipei(value, key)
    #
    #     str_ = '级配曲线：' + key
    #     st.text(str_)
    #
    #     fig = pop.creat_matplotlib_figure(x, y, key)
    #     st.pyplot(fig)
    #     st.image(pop.pos[0].all_color)


    with open(jsonfilename, 'w') as json_file:
        json.dump(ds_dic, json_file)
        print('粒径信息已保存到json文件', jsonfilename)
    # jipei(ds_dic['0'])
    return 0

if __name__ == '__main__':
    houduan('D:\python_code\web-fabu')
