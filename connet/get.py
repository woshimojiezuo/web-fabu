
from connet.utils import *

image_name = 'logo'

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
imgdata = get_img(image_name)
print(0)

