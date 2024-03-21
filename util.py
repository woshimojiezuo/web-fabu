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
