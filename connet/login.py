import streamlit as st
from utils import create_connection
def login(cnx):
    st.sidebar.subheader('登录界面')
    username = st.sidebar.text_input("用户名")
    password = st.sidebar.text_input("密码", type="password")
    # 处理登录逻辑
    if st.sidebar.button("登录"):
        cursor = cnx.cursor()
        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            st.sidebar.success("登录成功！")
            return True
        else:
            st.sidebar.error("用户名或密码错误。")
            return False
    if st.sidebar.button("注册"):
        cursor = cnx.cursor()
        query = "INSERT INTO login (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        cnx.commit()
        st.sidebar.success("注册成功！")
        cursor.close()



if 'loged' not in st.session_state:
    st.session_state['loged'] = False
conn = create_connection()
mycursor = conn.cursor()
try:
    mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
except:
    print('数据库已经存在')
if st.session_state['loged']:
    st.write('登录成功')
else:
    login(conn)

