import streamlit as st
import mysql.connector
from mysql.connector import Error
# 连接到MySQL数据库
def connect_db():
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

# 验证用户
def authenticate_user(username, password):
    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"发生错误：{e}")
        return False
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# 注册用户
def register_user(username, password):
    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # 用户名重复
    except Exception as e:
        st.error(f"发生错误：{e}")
        return False
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

#
# if 'loged' not in st.session_state:
#     st.session_state['loged'] = False
# if 'sb_state' not in st.session_state:
#     st.session_state['sb_state'] = True
#
# if not st.session_state['loged']:
#     if st.session_state['sb_state']:
#         st.sidebar.title("登录")
#         username = st.sidebar.text_input("用户名")
#         password = st.sidebar.text_input("密码", type="password")
#         a = st.sidebar.empty()
#         button1 = st.sidebar.button("登录")
#         button2 = st.sidebar.button("注册")
#         if button1:
#             # 验证用户
#             if username and password and authenticate_user(username, password):
#                 st.sidebar.success("登录成功！")
#                 st.session_state['loged']=True
#             else:
#                 st.sidebar.error("登录失败，请检查用户名和密码。")
#
#         if button2:
#             st.session_state['sb_state'] = False
#     else:
#         st.sidebar.title("注册")
#         username = st.sidebar.text_input("用户名")
#         password = st.sidebar.text_input("密码", type="password")
#         jigou = st.sidebar.text_input("授权的机构")
#         button_regi = st.sidebar.button("确定注册")
#         button_signin = st.sidebar.button('登录')
#         if button_regi:
#             if username and password and register_user(username, password) and jigou=='矿大':
#                 st.sidebar.success("注册成功！")
#                 st.session_state['sb_state'] = True
#             else:
#                 st.sidebar.error("注册失败")
#         if button_signin:
#             st.session_state['sb_state']=True

def log_part():
    if 'loged' not in st.session_state:
        st.session_state['loged'] = False
    if 'sb_state' not in st.session_state:
        st.session_state['sb_state'] = True

    if not st.session_state['loged']:
        st.markdown('''
        # 颗粒识别分析系统
        _____
        ## 操作流程
        ### 依次点击
        - 添加文件
        - 图片载入
        - 粒子识别
            - 选择模型
        - 识别结果
        - 退出登录
        _____
        ## 注册
        授权机构：矿大
        
        ''')
        if st.session_state['sb_state']:
            st.sidebar.title("登录")
            username = st.sidebar.text_input("用户名")
            password = st.sidebar.text_input("密码", type="password")
            a = st.sidebar.empty()
            button1 = st.sidebar.button("登录")
            button2 = st.sidebar.button("注册")
            if button1:
                # 验证用户
                if username and password and authenticate_user(username, password):
                    st.sidebar.success("登录成功！")
                    st.session_state['loged'] = True
                    st.rerun()
                else:
                    st.sidebar.error("登录失败，请检查用户名和密码。")

            if button2:
                st.session_state['sb_state'] = False
                st.rerun()
        else:
            st.sidebar.title("注册")
            username = st.sidebar.text_input("用户名")
            password = st.sidebar.text_input("密码", type="password")
            jigou = st.sidebar.text_input("授权的机构")
            button_regi = st.sidebar.button("确定注册")
            button_signin = st.sidebar.button('登录')
            if button_regi:
                if username and password and register_user(username, password) and jigou == '矿大':
                    st.sidebar.success("注册成功！")
                    st.session_state['sb_state'] = True
                    st.rerun()
                else:
                    st.sidebar.error("注册失败")
            if button_signin:
                st.session_state['sb_state'] = True
                st.rerun()

