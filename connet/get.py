import streamlit as st
from connet.utils import *
import io

@st.cache_data
def get_img(image_name):
    # 使用示例函数进行查询和转换
    connection = create_connection()
    if connection:
        # 假设要查询名为 'image.jpg' 的图片
        image_np = query_image(connection, image_name)
        if image_np is not None:
            print("Image data successfully retrieved and converted into NumPy array")
            print("Shape of the image:", image_np.shape)
            return (image_np)
        connection.close()
    else:
        print('数据库获取图片失败')

@st.cache_data
def get_pt(name):
    # 使用示例函数进行查询和转换
    connection = create_connection()
    if connection:
        ptdata = query_pt(connection, name)
        if ptdata is not None:
            print('数据库模型参数成功')
            return ptdata
        connection.close()
    else:
        print('数据库模型参数失败')
if __name__=="__main__":
    import torch
    image_name = 'logo'
    # imgdata = get_img(image_name)
    pt = 'msba_pkl'
    pt_data = get_pt(pt)
    a = torch.load(pt_data,map_location=torch.device('cpu'))
    print(0)

