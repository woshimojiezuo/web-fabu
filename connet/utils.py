import mysql.connector
from mysql.connector import Error
import mysql.connector
import numpy as np
from PIL import Image
from io import BytesIO
# 建立与数据库的连接
def create_connection():
    # 配置数据库连接信息
    host = "mysql.sqlpub.com"
    port = "3306"
    database = "pt_and_staticfile"
    user = "wuqiong"
    password = "GNmSVafbQJMrDLgs"
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
# 创建图像数据表
def create_images_table(conn):
    try:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE images (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                data LONGBLOB
            )
        '''
        cursor.execute(create_table_query)
        print("Images table created successfully")
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred while creating 'images' table")

# 保存图像数据到数据库
def save_image(conn, name, image_data):
    try:
        cursor = conn.cursor()
        insert_query = '''
            INSERT INTO images (name, data) VALUES (%s, %s)
        '''
        cursor.execute(insert_query, (name, image_data,))
        conn.commit()
        print("Image data saved successfully")
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred while saving image data")

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