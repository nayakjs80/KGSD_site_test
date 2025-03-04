import streamlit as st
import pandas as pd
import hashlib
import datetime

from Check import is_valid_ssn
from user import clsUser
from Plotting_demo import plotting_demo
from geomatry import triangle_area, rectangle_area

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

import sqlite3 
conn = sqlite3.connect('medical_db_secure.db')
c = conn.cursor()

def create_tableuserlist():
	c.execute('CREATE TABLE IF NOT EXISTS userlist(username TEXT,password TEXT, ssn TEXT PRIMARY KEY)')

def create_tableuser():
	c.execute('''
	CREATE TABLE IF NOT EXISTS user (
		timestamp TEXT PRIMARY KEY,
		ssn TEXT NOT NULL,
		blood_sugar TEXT NOT NULL,
		lactic_acid TEXT NOT NULL,
		FOREIGN KEY(ssn) REFERENCES userlist(ssn)
	)
	''')

def add_userListdata(username,password,ssn):
	c.execute('INSERT INTO userlist(username,password,ssn) VALUES (?,?,?)', (username,password,ssn))
	conn.commit()

def add_user_data(ssn,blood_sugar,lactic_acid):
	timestamp = datetime.datetime.now().isoformat()
	c.execute('INSERT INTO user(timestamp,ssn,blood_sugar,lactic_acid) VALUES (?,?,?,?)', (timestamp,ssn,blood_sugar,lactic_acid))
	conn.commit()

# def login_user(ssn):
# 	c.execute('SELECT * FROM user WHERE ssn = ?', (ssn))
# 	data = c.fetchall()
# 	return data

def login_user(username, password):
	c.execute('SELECT * FROM userlist WHERE username = ? AND password = ?', (username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userlist')
	data = c.fetchall()
	return data

def AddRow(AddRowText, datatype):
	# User 테이블에 blood_pressure 열 추가
	c.execute('''ALTER TABLE user ADD COLUMN (?) ?''', (AddRowText, datatype))	

def get_ssn_by_username(username):
    c.execute('SELECT ssn FROM userlist WHERE username = ?', (username,))
    data = c.fetchone()
    if data:
        return data[0]
    return None

def Info_KGSD():
    st.subheader("KGSD 의료 데이터")
    st.markdown("""
    KGSD 의료 데이터에 오신 것을 환영합니다. 저희는 의료 데이터를 관리하고 분석하는 신뢰할 수 있는 플랫폼입니다.
    
    **특징:**
    - 안전한 사용자 인증 및 데이터 관리
    - 의료 기록을 추가하고 조회할 수 있는 사용하기 쉬운 인터페이스
    - 의료 데이터 통찰력을 위한 분석 도구
    - 의료 동향을 더 잘 이해할 수 있는 데이터 시각화

    **사용 방법:**
    - 새 계정을 등록하거나 기존 자격 증명으로 로그인하세요
    - 메뉴를 통해 다양한 기능에 접근하세요
    - 새로운 의료 데이터를 추가하거나 기존 기록을 조회하세요
    - 분석 도구를 사용하여 데이터에서 통찰력을 얻으세요

    **문의하기:**
    - 지원이나 문의 사항이 있으시면 k.gsd.ric@gmail.com으로 연락해 주세요

    KGSD 의료 데이터를 선택해 주셔서 감사합니다!
    """)

def Login():
		Info_KGSD()
		# st.subheader("Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')

		if st.sidebar.checkbox("Login"):
			create_tableuserlist()
			hashed_pswd = make_hashes(password)
			# result = login_user(username,check_hashes(password,hashed_pswd))
			result = login_user(username,hashed_pswd)
			if result:
				st.success("Logged In as {}".format(username))
				st.success("ssn is {}".format(get_ssn_by_username(username)))

				seluser.username = username
				seluser.password = password
				seluser.ssn = get_ssn_by_username(username)
				seluser.IsLogin = True

				# digit = seluser.ssn.replace('-','')
				# TableInfo(digit)
				# st.success("{}".format(get_table_info(seluser.ssn)))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")
				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password","ssn"])
					st.dataframe(clean_db)

				st.text("username:{}, ssn:{}".format(seluser.username,seluser.ssn))
			else:
				st.warning("Incorrect Username/Password")

def SignUp():
		st.sidebar.subheader("Create New Account")
		new_user = st.sidebar.text_input("Username")
		new_password = st.sidebar.text_input("Password",type='password')
		ssn = st.sidebar.text_input("ssn")
		
		if st.sidebar.button("Signup"):
			# digits = [int(d) for d in ssn.replace('-', '')]
			
			digits = ssn.replace('-','')

			st.text("ssn:{}".format(digits))

			if(is_valid_ssn(ssn)):
				create_tableuserlist()
				create_tableuser()
				add_userListdata(new_user,make_hashes(new_password), ssn)

				st.success("{}".format(get_table_info(digits)))
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
			else:
				st.info("Check your ssn ..")
		else:
			Info_KGSD()

def Test():
		result1 = triangle_area(200, 20)
		result2 = rectangle_area(200, 20)
		st.write(result1)
		st.write(result2)

def get_table_info(table_name):
	# digits = table_name.replace('-','')
    c.execute(f'PRAGMA table_info({table_name})')
    columns = c.fetchall()
    return columns

def TableInfo(table_name):
    # st.subheader("Table Information")
    # table_name = st.text_input("Enter table name")

	c.execute('SELECT * FROM user')
	columns = c.fetchall()

	if columns:
		df = pd.DataFrame(columns, columns=["timestamp", "ssn", "blood_sugar", "lactic_acid"])
		st.dataframe(df)
	else:
		st.warning("Table not found or no columns in table")


    # if st.button("Get Table Info"):
        # columns = get_table_info(table_name)
        # if columns:
        #     df = pd.DataFrame(columns, columns=["timestamp", "ssn", "blood_sugar", "lactic_acid"])
        #     st.dataframe(df)
        # else:
        #     st.warning("Table not found or no columns in table")

# page_names_to_funcs = {
# 	"Home": Home,
# 	"Login": Login,
# 	"SignUp": SignUp,
# 	"Test": Test,
#     "—": intro,
#     "Plotting Demo": plotting_demo,
#     "Mapping Demo": mapping_demo,
#     "DataFrame Demo": data_frame_demo
# }

seluser = clsUser("","","")


def main():
	
	st.set_page_config(
		page_title="MainPage",
		page_icon="👋",
	)

	st.sidebar.header("Hello")
	
	# menu = ["Home","Login","SignUp","Test"]
	# choice = st.sidebar.selectbox("Menu",menu)

    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()

	st.title("Hello .. [KGSD Medical Data]")
	# if(seluser.IsLogin):
	# 	st.markdown("Login Info : not login")
	# else:
	# 	st.markdown("Login Info : user:{}",(seluser.username))

	menu = ["Home","Login","SignUp","InsertData"]
	# menu = ["Home","Login","SignUp","Test","InsertData","plotting_demo"]

	choice = st.sidebar.selectbox("Menu", menu, 1)

	if choice == "Home":
		Info_KGSD()
	elif choice == "Login":
		Login()
	elif choice == "SignUp":
		SignUp()
	elif choice == "Test":
		# intro()
		result1 = triangle_area(200, 20)
		result2 = rectangle_area(200, 20)
		st.write(result1)
		st.write(result2)
	elif choice == "InsertData":
		# InsertData_demo()
		
		blood_sugar = st.number_input("혈당 입력", format="%.2f")
		lactic_acid = st.number_input("락틱산 입력", format="%.2f")

		if(st.button("Add Data")):
			add_user_data(seluser.ssn,blood_sugar,lactic_acid)
	
		if(seluser.IsLogin):
			digit = seluser.ssn.replace('-','')
			TableInfo(digit)

	elif choice == "plotting_demo":
		plotting_demo()

if __name__ == '__main__':
	main()