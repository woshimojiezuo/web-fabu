from connet.utils import *

imgdir = 'D:\python_code\web-fabu\static\logo_txt.png'
imgname = 'logo_txt'

# 调用函数进行数据库连接、表创建和保存图像数据
connection = create_connection()
if connection:
    create_images_table(connection)
    # 假设有一个名为 'image.jpg' 的图片文件
    with open(imgdir, "rb") as image_file:
        image_data = image_file.read()
        save_image(connection, imgname, image_data)
    connection.close()
