import mysql.connector
import numpy as np
from PIL import Image
from io import BytesIO

# 配置数据库连接信息
host = "mysql.sqlpub.com"
port = "3306"
database = "pt_and_staticfile"
user = "wuqiong"
password = "GNmSVafbQJMrDLgs"


# 建立与数据库的连接
def create_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred while connecting to MySQL database")
    return conn


# 查询数据库中的图像数据
def query_image(conn, name):
    try:
        cursor = conn.cursor()
        query = '''
            SELECT data FROM images WHERE name = %s
        '''
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        if result:
            image_data = result[0]
            image = Image.open(BytesIO(image_data))
            image_np = np.array(image)
            return image_np
        else:
            print(f"No image found with name '{name}'")
            return None

        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred while querying image data")


# 使用示例函数进行查询和转换
connection = create_connection()
if connection:
    # 假设要查询名为 'image.jpg' 的图片
    image_name = "image.jpg"
    image_np = query_image(connection, image_name)
    if image_np is not None:
        print("Image data successfully retrieved and converted into NumPy array")
        print("Shape of the image:", image_np.shape)
    connection.close()
