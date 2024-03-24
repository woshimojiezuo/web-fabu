from connet.utils import *
import pickle

def save1():
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
def save2():
    msba_pt = 'D:\python_code\web-fabu\model2\model4best.pkl'
    name = 'msba_pkl'
    connection = create_connection()
    if connection:
        create_model_canshu_table(connection)
        # 假设有一个名为 'image.jpg' 的图片文件
        with open(msba_pt, "rb") as pt_file:
            ptk_data = pt_file.read()
            # save_pt(connection, name, ptk_data)
        connection.close()
    with open("D:\python_code\web-fabu\static\src\msba_cabshu.py", "w") as file:
        file.write(f'msba_cabshu = {pickle.dumps(ptk_data)}')
if __name__=="__main__":
    save2()
