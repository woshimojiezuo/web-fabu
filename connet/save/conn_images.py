import mysql.connector

# 配置数据库连接信息
host = "mysql.sqlpub.com"
port = "3306"
database = "pt_and_staticfile"
user = "wuqiong"
password = "GNmSVafbQJMrDLgs"

# 建立与数据库的连接
connection = mysql.connector.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# 创建游标对象
cursor = connection.cursor()

# 定义创建表的SQL语句
create_table_query = '''
    CREATE TABLE employees (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        salary DECIMAL(10, 2)
    );
'''

# 执行创建表的SQL语句
cursor.execute(create_table_query)

# 提交事务
connection.commit()

# 关闭游标和数据库连接
cursor.close()
connection.close()
