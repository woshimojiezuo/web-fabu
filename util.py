import streamlit as st

@st.cache_data
def get_images_name_strings(loads):
    all = ''
    for load in loads:
        all = all + '- ' + load.name + '\n'
    return all
@st.cache_data
def chart1(loads):
    for load in loads:
        st.write(load.name)