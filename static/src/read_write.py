import pickle
from PIL import Image
import io
import numpy as np
def write():
    # 读取图片并转换为二进制数据
    image_path = "/streamlit/图片1.png"  # 图片路径
    with open(image_path, "rb") as file:
        binary_image_data = file.read()

    # 将二进制数据保存到.py文件中的一个变量中
    with open("binary_image_data.py", "w") as file:
        file.write(f'binary_image_data = {pickle.dumps(binary_image_data)}')

    # 下次调用时，你可以导入该变量，并使用pickle.loads()来获取原始的二进制图片数据
    # from binary_image_data import binary_image_data
    # original_image_data = pickle.loads(binary_image_data)
def read():
    from static.src.binary_image_data import binary_image_data
    original_image_data = pickle.loads(binary_image_data)
    image = Image.open(io.BytesIO(original_image_data))
    image_np = np.array(image)
    return image_np

