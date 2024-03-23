import torch
from torch.utils.data import Dataset, DataLoader
from .dataset import Mytest_for_uploadfile
from .MSBA import *
from torchvision import transforms
import os
import json
from .post_process import *
from connet.get import get_pt
import streamlit as st

@st.cache_data
def houduan_msba(stateupload):
    cuda = torch.cuda.is_available()
    #模型参数加载中
    pt = 'msba_pkl'
    pt_data = get_pt(pt)
    if cuda:
        model = Msba().cuda()
        model.load_state_dict(torch.load(r'D:\python_code\web-fabu\model2\model4best.pkl',))
    else:
        model = Msba()
        model.load_state_dict(torch.load(pt_data, map_location=torch.device('cpu')), )
    #模型加载完成


    data_transform = transforms.Compose(
                [
                transforms.Resize((512,512)),#transforms.RandomCrop(512),
                ])#transforms.Normalize(0.5, 0.229)
    TEST = Mytest_for_uploadfile(stateupload, transform=data_transform)
    test_loader = DataLoader(TEST, batch_size=1, shuffle=False)
    datas = []
    colorimgs=[]
    names = []
    for step, (test, name) in enumerate(test_loader):
        # 预测
        pred_tensor1, pred_tensor2 = model(test)
        # post-processing
        data, colorimg = post_process(pred_tensor1, pred_tensor2, show=False)
        datas.append(data)
        colorimgs.append(colorimg)
        names.append(name)
    return datas,colorimgs,names
if __name__=='__main__':
    houduan_msba()