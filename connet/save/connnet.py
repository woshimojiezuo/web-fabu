import mysql.connector
#https://www.mysql.sqlpub.com
#https://chatapi.chat86.cn/#/home?from=lg
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

# 使用连接执行数据库操作
# ...
# 执行查询数据的SQL语句
select_query = "SELECT * FROM employees;"
cursor.execute(select_query)

# 获取查询结果
results = cursor.fetchall()
# 输出查询结果
for row in results:
    print(row)
# 关闭游标和数据库连接
cursor.close()
connection.close()

# 输出查询结果
for row in results:
    print(row)
