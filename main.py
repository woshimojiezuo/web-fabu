import os.path
import streamlit as st
import numpy as np
from PIL import Image
###########################################################
page_title = "颗粒识别分析系统"
page_icon="🧊",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"}

#########################################################
if 'jincheng' not in st.session_state:
    st.session_state['jincheng'] = 0
if 'file_change_flag' not in st.session_state:
    st.session_state['file_change_flag'] = 0
if 'file_add_flag' not in st.session_state:
    st.session_state['file_add_flag']=False
if 'loged' not in st.session_state:
    st.session_state['loged'] = False
st.set_page_config(
    page_title="颗粒识别分析系统",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
if not st.session_state['loged']:
    with st.sidebar:
        st.markdown('尚未登陆的函数')
#布局部分------------------------------------------------------------------
##头目布局
title_col1,title_col2,buttons = st.columns((0.4,0.2,0.6),gap="small")
with buttons:
    button_col1, button_col2, button_col3, button_col4 = st.columns(4, gap="small")
##内容文件布局
file_bar,contains = st.columns((0.2,0.8),gap="small")
###filebar布局
file_container = file_bar.container(height=700, border=True)
with file_container:
    file_container1_1,file_container1_2 = st.columns(2)
###contains布局
with contains:
    contain_col11,contain_col12 = st.columns(2,gap="small")
    contain_col21,contain_col22 = st.columns(2,gap="small")
with contain_col11:
    c11_container = contain_col11.container(height=340, border=True)
with contain_col12:
    c12_container = contain_col12.container(height=340, border=True)
with contain_col21:
    c21_container = contain_col21.container(height=340, border=True)
with contain_col22:
    c22_container = contain_col22.container(height=340, border=True)
##尾部布局
foot_col1,foot_col2,foot_col3 = st.columns((1,0.5,1),gap="small")
#-----------------------------------------------------------------------
# state逻辑 或者静态的内容
## 头部
with title_col1:
    st.markdown('这是一张logo图片')
    st.markdown('# **粒子图像识别系统**')
    # st.image(logo_image,use_column_width="always")
with title_col2:
    st.markdown(' ')
    # st.header('粒子图像识别系统')
with button_col1:
    if st.button('图 片 载 入'):
        st.session_state['jincheng'] = 1
with button_col2:
    if st.button('粒 子 识 别'):
        st.session_state['jincheng'] = 2
with button_col3:
    if st.button('识 别 结 果'):
        st.session_state['jincheng'] = 3
with button_col4:
    if st.button('系 统 退 出'):
        st.session_state['jincheng'] = 0

###filebar
with file_container1_1:
    if st.button('添加文件'):
        st.session_state['file_add_flag'] = True
with file_container1_2:
    if st.button('删除图片'):
        st.markdown('删除函数')
with file_container:
    st.markdown('***当前文件：***')
    st.write('- 暂无图片，请添加')
###foot
with foot_col1:
    st.write(' ')
with foot_col2:
    st.write('版权所有：中国矿业大学')
with foot_col3:
    st.write(' ')
#------------------------------------------------------
#根据state逻辑实施
##头部静止无变化
##filebar
if st.session_state['file_add_flag']:
    with file_container:
        image_file = st.file_uploader("插入识别图片：", type=["jpg", "jpeg", "png"],
                                      label_visibility="collapsed")
##contents
if st.session_state['jincheng']>=1:
    with c11_container:
        st.markdown('阶段一')
if st.session_state['jincheng']>=2:
    with c12_container:
        st.markdown('阶段二')
if st.session_state['jincheng']>=3:
    with c21_container:
        st.markdown('阶段三')
    with c22_container:
        st.markdown('阶段三')
if st.session_state['jincheng']>=4:
    st.write('系统退出')



