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


from pyecharts import options as opts
from pyecharts.charts import Bar,Line
from streamlit_echarts import st_pyecharts
import numpy as np
from pyecharts.commons.utils import JsCode
# 定义直方图函数
def histogram2(data, num):
    hist, bins = np.histogram(data, bins=num)
    bin_ranges = [f"{bins[i]:.2f}-{bins[i+1]:.2f}" for i in range(len(bins)-1)]
    return bin_ranges, hist.tolist()  # 将直方图数据转换为原生 Python 列表

# 定义生成柱状图的函数
def bar_chart(data:list, num):
    #用echart做表，此为阶段3的函数
    x_, y = histogram2(data, num)
    b = (
        Bar()
        .add_xaxis(x_)
        .add_yaxis(
            "数量（个）", y
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="粒径统计",
            ),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(name="粒径区间",
                                     name_location="middle",  # 横坐标标题居中
                                     name_gap=30,  # 与坐标轴之间的距离
                                     ),
            yaxis_opts=opts.AxisOpts(name="数量",
                                     name_location="middle",  # 纵坐标标题居中
                                     name_gap=30,  # 与坐标轴之间的距离
                                     type_="value",
                                     ),
        )
    )
    st_pyecharts(b)

def format_axis(value):
    return "{:.2f}".format(value)
def plot_cumulative_distribution2(data, num):
    '''
    data: list
    '''
    # 计算数据的概率分布
    sorted_data = np.sort(data)
    n = sorted_data.size
    # 获取均匀间隔的横坐标
    x = np.linspace(int(min(sorted_data)), int(max(sorted_data)), num)
    cumulative_percentages = []
    for value in x:
        percentage = np.sum(sorted_data >= value) / n
        cumulative_percentages.append(percentage)
    return x.tolist(), cumulative_percentages  # 将结果转换为原生 Python 列表
def line_chart(data:list, num):
    x_, y = plot_cumulative_distribution2(data, num)
    formatter_js = """
    function(params) {
        return params.value.toFixed(2);
    }
    """
    w = (
        Line()
        .add_xaxis(xaxis_data=list(map(format_axis, x_)))
        .add_yaxis(
            series_name="百分比",
            y_axis= y,
            label_opts=opts.LabelOpts(
                is_show=True,
                formatter=JsCode("""
                                    function(params) {
                                    var originalValue = params.value;
                                    var formattedValue = parseFloat(originalValue[1]).toFixed(2);
                                    return formattedValue;
                                    }
                                    """)
            ),
            )

        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="粒径级配累计曲线",
            ),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(name="粒径",
                                     name_location="middle",  # 横坐标标题居中
                                     name_gap=30,  # 与坐标轴之间的距离
                                     type_="value"

                                     ),
            yaxis_opts=opts.AxisOpts(name="小于某粒径的数量百分比",
                                     name_location="middle",  # 纵坐标标题居中
                                     name_gap=30,  # 与坐标轴之间的距离
                                     type_="value",
                                     ),
        )
    )
    st_pyecharts(w)