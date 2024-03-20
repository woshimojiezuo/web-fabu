# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from test import text_write
from PIL import Image
import numpy as np
import os
LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    text_write()
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def shuru_and_shuchu():
    if 'image' not in st.session_state:
        st.session_state['image']=None
    loadfile = st.file_uploader('图片')
    if loadfile is not None:
        st.session_state['image'] = loadfile
    # 将图像转换为 NumPy 数组
    if st.session_state['image']:
        type = st.session_state['image']
        # print(imgnp.shape)
        image = Image.open(type)
        # 将图像转换为 numpy 数组
        img_array = np.array(image)
        # print(type)
        # logo_image = np.array(st.session_state['image'])
        st.image(img_array)



# '''
# 测试1 目录里的函数文件能不能调用  成功了
# 测试2 目录里的文件能不能调用     用相对路经失败，绝对路经在本地能够运行，在部署后同样不可以
# 测试3 保存文件能不能用
# 测试4 读取文件能不能用
# '''
if __name__ == "__main__":
    run()
    shuru_and_shuchu()
    st.image('images/logo.png')
    #st.markdown("[![Click me](Hello/static/logo.jpg)](https://streamlit.io)")
