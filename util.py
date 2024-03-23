import streamlit as st
from PIL import Image
import numpy as np
@st.cache_data
def get_images_name_strings(loads):
    all = ''
    for load in loads:
        all = all + '- ' + load.name + '\n'
    return all
@st.cache_data
def chart1(loads):
    imgs = []
    caps = []
    for load in loads:
        # st.write(load.name)
        image = Image.open(load)
        img_array = np.array(image)
        imgs.append(img_array)
        caps.append(load.name)
    return imgs,caps
@st.cache_data
def chart3(datas):
    hist_datas = []
    for data in datas:
        sizes = data['等效粒径']
        hist_data = histogram(sizes,20)
        hist_datas.append(hist_data)
    return hist_datas
@st.cache_data
def chart4(datas):
    line_datas = []
    for data in datas:
        sizes = data['等效粒径']
        line_data = plot_cumulative_distribution(sizes,20)
        line_datas.append(line_data)
    return line_datas


###------------------------------------------------
#统计相关的函数
def histogram(data, num):
    '''
    data list
    '''
    # 计算直方图
    hist, bins = np.histogram(data, bins=num)

    # 获取每个分组的范围
    bin_ranges = [f"{bins[i]:.2f}-{bins[i+1]:.2f}" for i in range(len(bins)-1)]

    # 生成bar_chart所需的数据格式
    hist_data = {bin_range: count for bin_range, count in zip(bin_ranges, hist)}

    # 绘制直方图
    return hist_data

def plot_cumulative_distribution(data, num):
    '''
    data list
    '''
    # 计算数据的概率分布
    sorted_data = np.sort(data)
    n = sorted_data.size
    # 获取均匀间隔的横坐标
    x = np.linspace(min(sorted_data), max(sorted_data), num)
    cumulative_percentages = []
    for value in x:
        percentage = np.sum(sorted_data <= value) / n
        cumulative_percentages.append(percentage)
    # 将数据转换为适合st.line_chart的格式
    line_chartdata = {bin_range: count for bin_range, count in zip(x, cumulative_percentages)}
    # # 绘制概率分布曲线
    # st.line_chart(hist_data)
    return line_chartdata