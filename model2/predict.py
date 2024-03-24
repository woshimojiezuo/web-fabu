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
from static.src.msba_cabshu import msba_cabshu
import pickle
import io
@st.cache_data
def houduan_msba(stateupload):
    cuda = torch.cuda.is_available()
    #模型参数加载中
    print('加载模型中')
    with st.spinner('加载模型训练参数中，第一次加载时间较长'):
        pt = 'msba_pkl'
        origindata = pickle.loads(msba_cabshu)
        pt_data = io.BytesIO(origindata)
        # a =  torch.load(pt_data, map_location=torch.device('cpu'))
        # pt_data2 = get_pt(pt)
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
    print('预测中')
    for step, (test, name) in enumerate(test_loader):
        # 预测
        pred_tensor1, pred_tensor2 = model(test)
        # post-processing
        data, colorimg = post_process(pred_tensor1, pred_tensor2, show=False)
        datas.append(data)
        colorimgs.append(colorimg)
        names.append(name)
    print('预测结束，返回数据')
    return datas,colorimgs,names
if __name__=='__main__':
    houduan_msba()