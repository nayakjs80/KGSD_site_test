import streamlit as st
import pandas as pd
import hashlib
import datetime

from Check import is_valid_ssn
from user import clsUser
from Plotting_demo import plotting_demo
from geomatry import triangle_area, rectangle_area

from PIL import Image
import requests

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

def create_table(tableName):
	c.execute(f'CREATE TABLE IF NOT EXISTS {tableName}()')

def add_column_to_user_table(tableName, column_name, column_type):
    c.execute(f'ALTER TABLE {tableName} ADD COLUMN {column_name} {column_type}')
    conn.commit()

def table_exists(table_name):
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = c.fetchone()
    return result is not None

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
    # st.subheader("한국 당원병 환우회에 오신 것을 환영합니다!")

	st.markdown("""
		<h2 style='color:#2c3e50;'>한국 당원병 환우회에 오신 것을 환영합니다!</h2>
	""", unsafe_allow_html=True)

		# <h2>저희는 당원병 환자와 가족들을 위한 지원과 
		# 	 정보를 제공하는 커뮤니티입니다.</h2>

	st.markdown("""
		<style>
			.card {
				background-color: #f9f9f9;
				padding: 20px;
				margin-bottom: 20px;
				border-radius: 10px;
				box-shadow: 0 2px 5px rgba(0,0,0,0.1);
			}
			.card h3 {
				margin-top: 0;
				color: #333;
			}
			.card p {
				margin: 5px 0;
				color: #555;
			}
			.card a {
				color: #1f77b4;
				text-decoration: underline;
			}
		</style>
	""", unsafe_allow_html=True)


	# st.markdown("""
	# <div class="card">

	# 	특징
	# 	최신 정보: 당원병 관련 최신 연구, 치료법, 뉴스 등을 제공합니다.
	# 	커뮤니티 지원: 환자와 가족들이 서로 경험을 공유하고 
	# 	지원할 수 있는 공간을 제공합니다.
	# 	전문가 연결: 의료 전문가와의 연결을 통해 신뢰할 수 있는 정보를 제공합니다.
	# 	이벤트 및 모임: 정기적인 모임과 이벤트를 통해 	 
	# 	환자와 가족들이 서로 교류할 수 있는 기회를 제공합니다.		 
	# 	자원 및 자료: 당원병 관리에 도움이 되는 다양한 자료와 자원을 제공합니다.
			 
	# 	문의하기<
	# 	지원이나 문의 사항이 있으시면 k.gsd.ric@gmail.com으로 연락해 주세요
			 
	# 	한국 당원 환우회를 방문해 주셔서 감사합니다!
	# </div>
	# """, unsafe_allow_html=True)

	# 
	st.markdown("""
	<div class="card">
		<h3>특징 </h3>
		<p>최신 정보: 당원병 관련 최신 연구, 치료법, 뉴스 등을 제공합니다.</p>
		<p>커뮤니티 지원: 환자와 가족들이 서로 경험을 공유하고</p>
		<p>지원할 수 있는 공간을 제공합니다.</p>
		<p>전문가 연결: 의료 전문가와의 연결을 통해 신뢰할 수 있는 정보를 제공합니다.</p>
		<p>이벤트 및 모임: 정기적인 모임과 이벤트를 통해</p>
		<p>환자와 가족들이 서로 교류할 수 있는 기회를 제공합니다.</p>
		<p>자원 및 자료: 당원병 관리에 도움이 되는 다양한 자료와 자원을 제공합니다.</p>
	</div>
	""", unsafe_allow_html=True)

	# 
	st.markdown("""
	<div class="card">
		<h3>가입 방법 </h3>
		<p>당원병 네이버 카페에 가입해 주세요: </p>
		<p><a href="https://cafe.naver.com/koreagsd" target="_blank">한국 당원병 환우회</a></p>
		<p>가입 요청 글과 연락처를 남겨주세요.</p>
		<p>가입 승인이 완료되면 환우회 활동에 참여하실 수 있습니다.</p>
	</div>
	""", unsafe_allow_html=True)

	# 
	st.markdown("""
	<div class="card">
		<h3>문의하기 </h3>
		<p>지원이나 문의 사항이 있으시면 k.gsd.ric@gmail.com으로 연락해 주세요</p>
		<p>한국 당원 환우회를 방문해 주셔서 감사합니다!</p>
	</div>
	""", unsafe_allow_html=True)


def KGSD_History():
	# st.text("Page 걸어온길")
	st.markdown("""
		<h2 style='color:#2c3e50;'>걸어온 길 페이지</h2>
	""", unsafe_allow_html=True)

	st.markdown("""
		<style>
			.card {
				background-color: #f9f9f9;
				padding: 20px;
				margin-bottom: 20px;
				border-radius: 10px;
				box-shadow: 0 2px 5px rgba(0,0,0,0.1);
			}
			.card h3 {
				margin-top: 0;
				color: #333;
			}
			.card p {
				margin: 5px 0;
				color: #555;
			}
			.card a {
				color: #1f77b4;
				text-decoration: underline;
			}
		</style>
	""", unsafe_allow_html=True)

	# 2025년 카드
	st.markdown("""
	<div class="card">
		<h3>2025년</h3>
		<p>2월 - 질병청 희귀질환 극복의날 행사 참석</p>
		<p>4월 - 성인 환후 간담회(Online)</p>
		<p>6월 - 질병청, 건강보험공단, 당원병 환우회 간담회</p>
		<p>7월 - 경기도 힐링 콘서트(for 희귀질환 가족) 참여</p>
		<p>    - 식약처 간담회 진행</p>			 
		<p>9월 - 당원병 글리코세이드 국가 지원 시작</p>
		<p>    - 최보윤 국회의원 간담회</p>
	</div>
	""", unsafe_allow_html=True)

	# 2024년 카드
	st.markdown("""
	<div class="card">
		<h3>2024년</h3>
		<p>2월 - 당원병 아르고 전분 국가 지원 시작</p>
		<p>  - 질병청 희귀질환 극복의날 활동 발표 진행 (with 김은성)</p>
		<p>3월 - 찾아가는 지역별 간담회 (광주, 전라)</p>
		<p>  - 찾아가는 지역별 간담회 (영남)</p>
		<p>4월 - 찾아가는 지역별 간담회 (충청권)</p>
		<p>5월 - 찾아가는 지역별 간담회 (서울 경기)</p>
		<p>  - 인터랙트 케익 만들기 행사</p>
		<p>10월 - 카카오 헬스케어와 함께하는 당원병 환우회 정기모임</p>
		<p>  <a href="https://www.pointdaily.co.kr/news/articleView.html?idxno=222350" target="_blank">카카헬스케어 / 당원병 환우회 업무 협의 (AI-디지털 기술 활용 솔루션 개발 협력)</a></p>
	</div>
	""", unsafe_allow_html=True)

	# 2023 카드 3
	st.markdown("""
	<div class="card">
		<h3>2023년</h3>
		<p>3월 - 환우회 가입 설문 조사 시작</p>
		<p>5월 - <a href="https://youtu.be/rxfnt7fPUsE" target="_blank">당원병 환우회 발대식</a></p>
		<p>7월 - 질병관리청 연구용역 발주 [희귀질환자 의료비 지원사업 개편방안연구]</p>
		<p>10월 - 강윤구 교수님과 함께하는 당원병이 궁금하세요? (질의 응답 동영상 촬영)</p>
		<p>  <a href="https://m.sports.naver.com/general/article/023/0003796156" target="_blank">춘천 마라톤 대회 참여</a></p>
	</div>
	""", unsafe_allow_html=True)

	# 2022 카드 2
	st.markdown("""
	<div class="card">
		<h3>2022년</h3>
		<p>7월 - 당원병 환우 모임 및 세미나</p>
		<p>12월 - 한국 당원병 환우회 가족 모임 (with 원주세브란스기독병원 희귀질환센터)</p>
	</div>
	""", unsafe_allow_html=True)


	# 2021 카드 2
	st.markdown("""
	<div class="card">
		<h3>2021년</h3>
		<p>12월 - 당원병 이야기 카페 개설</p>
	</div>
	""", unsafe_allow_html=True)


	# st.markdown("<hr>", unsafe_allow_html=True)  # HTML 방식
	# st.subheader("2021년 ~")
	# st.markdown("""			 
	# - 12월 - 당원병 이야기 카페 개설 <br>
	# """, unsafe_allow_html=True)

	# st.markdown("<hr>", unsafe_allow_html=True)  # HTML 방식
	# st.subheader("2022년 ~")
	# st.markdown("""
	# 7월 - 당원병 환우 모임 및 세미나 <br>
	# 12월 - 한국 당원병 환우회 가족 모임 (with 원주세브란스기독병원 희귀질환센터) <br>
	# """, unsafe_allow_html=True)

	# st.markdown("<hr>", unsafe_allow_html=True)  # HTML 방식
	# st.subheader("2023년 ~")
	# st.markdown("""
	#   3월 - 환우회 가입 설문 조사 시작 <br>
	#   5월 - 당원병 환우회 발대식 (영상 링크 : https://youtu.be/rxfnt7fPUsE) <br>
	#   7월 - 질병관리청 연구용역 발주 [ 희귀질한자 의료비 지원사업 개편방안연구 ] <br>
	#   10월 - 강윤구 교수님과 함께하는 당원병이 궁금하세요? (질의 응답 동영상 촬영) <br>
    # 		- 춘천 마라톤 대회 참여 [10 km] (with 강윤구 교수 ) <br>
	# 		  기사링크([당원병 안고 10㎞ 완주… 아이들은 강했다](https://m.sports.naver.com/general/article/023/0003796156))	 <br>
	# """, unsafe_allow_html=True)

	# st.markdown("<hr>", unsafe_allow_html=True)  # HTML 방식
	# st.subheader("2024년 ~")
	# st.markdown("""
	# 2월  - 당원병 아르고 전분 국가 지원 시작 <br>
	# 		- 희귀질환 극복의날 활동 발표 진행 ( with 김은성 ) <br>
	# 3월 - 찾아가는 지역별 간담회 ( 광주, 전라 간담회) <br>
	# 	- 찾아가는 지역별 간담회 ( 영남 간담회) <br>
	# 4월 - 찾아가는 지역별 간담회 ( 충청권 간담회) <br>
	# 5월  - 찾아가는 지역별 간담회 ( 서울 경기 간담회) <br>
	# 		- 인터랙트 케익 만들기 행사 <br>
	# 10월 - 카카오 헬스케어 와 함께 하는 당원병 환우회 정기모임 ( with 카카오 헬스케어 ) <br>
	# 		- 카카오 헬스 케어 / 당원병 환우회 업무 협의 (AI-디지털 기술 활용 솔루션 개발 협력) <br>
	# 			기사 링크(https://www.pointdaily.co.kr/news/articleView.html?idxno=222350) <br>
	# """, unsafe_allow_html=True)

	# st.markdown("<hr>", unsafe_allow_html=True)  # HTML 방식
	# st.subheader("2025년 ~")
	# st.markdown("""
	# 9월 - 당원병 글리코세이드 국가 지원 시작	
	# """, unsafe_allow_html=True)		

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
				# st.success("ssn is {}".format(get_ssn_by_username(username)))

				st.session_state.username = username
				st.session_state.password = password
				st.session_state.ssn = get_ssn_by_username(username)
				st.session_state.IsLogin = True

				# seluser.username = username
				# seluser.password = password
				# seluser.ssn = get_ssn_by_username(username)
				# seluser.IsLogin = True

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

				st.text("username:{}".format(st.session_state.username))
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

			st.text("주민번호:{}".format(digits))

			# if(is_valid_ssn(ssn)):
			if(len(ssn) > 5):
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

def SearchData():
		st.sidebar.subheader("Search Data")

		username = st.sidebar.text_input("Search Name")
		MobileNumber = st.sidebar.text_input("Mobile Number")
		EMailAddr = st.sidebar.text_input("E-Mail Info")

		if st.sidebar.button("Search"):
			file_path = 'ComsAddr_231023.xlsx'
			df = pd.read_excel(file_path, sheet_name='연락망_23.10.23')

			# st.write(df)
			# st.write(df['Unnamed: 3'])
			# st.write(df[3:6])
			# st.write(df.iloc[0].values)
			# st.write(df.columns[1])

			st.success("Search Data")

			# 열 이름이 데이터프레임에 존재하는지 확인
			if 'Unnamed: 3' in df.columns:
				# 해당 열에서 값이 target_value인 행 필터링
				result = df[(df['Unnamed: 3'] == username.strip()) | (df['Unnamed: 6'] == MobileNumber.strip()) | (df['Unnamed: 8'] == EMailAddr.strip())]
				st.write(result)



			# # 0번째 행 가져오기
			# first_row = df.iloc[0].values
			# st.write(first_row)

			# # 0번째 행에서 target_value를 가진 열 이름 찾기
			# column_index = list(first_row).index('성명')
			# st.write(df.columns[column_index].values)


			# if '성명' in df.iloc[0]:
			# 	# 해당 열에서 값이 target_value인 행 필터링
			# 	result = df[df['성명'] == username]
			# 	st.write(result)
			# else:
			# 	st.write(f"'{username}' 열이 존재하지 않습니다.")
			
				# search_result = df[df['성명'] == username]
				# st.write(search_result)

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

	# c.execute('SELECT * FROM user')
	# columns = c.fetchall()

	c.execute('SELECT * FROM user WHERE ssn = ?', (table_name,))
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
# st.text("Execute seluser")


DEFAULT_IMG1_URL = (
	"Image/PageTop_1.jpg"
	# "https://photos.google.com/share/AF1QipN_VeP1rOL91aSnl_q79Xr9p0dand4aTPWx1wjZ9uCqJ_7mkpKhBCiVnMTAvSQTHg/photo/AF1QipN6AR6xNKSuGt659jWij5h45epQ0ladTi_RlYDo?key=TkhaSHU0cGJxemR1bEZvWk8tdlB4MzliYklZX0pn"
	# "https://photos.app.goo.gl/cr9YBqoSch4dYiXX8"
    # "https://juxtapose.knightlab.com/static/img/Sochi_11April2005.jpg"
)

def fetch_img_from_url(url: str) -> Image:
    img = Image.open(requests.get(url, stream=True).raw)
    return img

def main():

	if('IsLogin' not in st.session_state):
		st.session_state.IsLogin = False
		st.session_state.username = ""
		st.session_state.ssn = ""
		st.session_state.password = ""

	st.set_page_config(
		page_title="MainPage",
		page_icon="👋",
	)

	img = Image.open(DEFAULT_IMG1_URL)
	st.image(img, caption="2024 당원병 환우회 정기 모임", width=350, channels="RGB",)

	# st.sidebar.header("KGSD")
	st.sidebar.title("한국 당원병 환우회")

	# Image comparison
	
	# col1, buf, col2 = st.columns([1, 1, 1])
	# with col1:
	# 	img = Image.open(DEFAULT_IMG1_URL)
	# 	st.image(img, caption="Image caption", width=1000, channels="RGB",)
	

	# with col2:
	# 	st.write("This is a Streamlit app.")

	# if table_exists('userlists'):
	# 	st.write("Table 'userlist' exists.")
	# else:
	# 	st.write("Table 'userlist' does not exist.")

	# form = st.form(key="Image comparison")
	# img1_url = form.text_input("Image one url", value=DEFAULT_IMG1_URL)
	# img1 = fetch_img_from_url(DEFAULT_IMG1_URL)
	# submit = form.form_submit_button("Submit")
	
	# menu = ["Home","Login","SignUp","Test"]
	# choice = st.sidebar.selectbox("Menu",menu)

    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()

	# st.title("Hello .. [KGSD]")

	# menu = ["Home", "SearchData"]
	# menu = ["Home","Login","SignUp","InsertData", "SearchData"]
	# menu = ["Home","Login","SignUp","Test","InsertData","plotting_demo"]

	# choice = st.sidebar.selectbox("Menu", menu)
	# selected_page = st.sidebar.radio("이동할 페이지를 선택하세요", ["Home", "소개", "걸어온길"])

	# menu_items = ["Home", "소개", "걸어온길"]

	# # 라디오 버튼으로 선택 기능 유지
	# selected_page = st.sidebar.radio("이동할 페이지를 선택하세요", menu_items)

	# # 선택된 항목에 따라 내용 표시 + 구분선
	# st.sidebar.markdown("---")
	# for item in menu_items:
	# 	if item == selected_page:
	# 		st.sidebar.markdown(f"✅ **{item}** 선택됨")
	# 	else:
	# 		st.sidebar.markdown(f"**{item}**")
	# 	st.sidebar.markdown("---")

	# # 본문에 선택된 페이지 내용 출력
	# if selected_page == "Home":
	# 	st.write("🏠 홈 페이지입니다.")
	# elif selected_page == "소개":
	# 	st.write("📘 소개 페이지입니다.")
	# elif selected_page == "걸어온길":
	# 	st.write("🛤️ 걸어온 길 페이지입니다.")

	# 초기 상태 설정
	if "selected_page" not in st.session_state:
		st.session_state.selected_page = "Home"

	# st.sidebar.markdown("""
	# 	<style>
	# 		.link-button {
	# 			background: none;
	# 			border: none;
	# 			color: #555555;  /* 기본 회색 */
	# 			text-decoration: underline;
	# 			cursor: pointer;
	# 			font-size: 16px;
	# 			padding: 4px 0;
	# 		}
	# 		.link-button:hover {
	# 			color: #888888;  /* hover 시 더 연한 회색 */
	# 		}
	# 	</style>
	# """, unsafe_allow_html=True)

	st.sidebar.markdown("""
		<style>
			button[kind="primary"] {
				background: none !important;
				border: none !important;
				color: #666666 !important;
				text-decoration: underline !important;
				font-size: 16px !important;
				padding: 0 !important;
			}
			button[kind="primary"]:hover {
				color: #999999 !important;
			}
		</style>
	""", unsafe_allow_html=True)

	# st.sidebar.title("KGSD title")
	st.sidebar.markdown("### --📂-- 메뉴")

	# 메뉴 항목 리스트
	menu_items = ["소개", "걸어온 길", "같이하는 동료"]

	# 밑줄 텍스트 버튼 생성
	for item in menu_items:
		if st.sidebar.button(item, key=item, help=f"{item} 페이지로 이동", type="primary"):
			st.session_state.selected_page = item
		st.sidebar.markdown("---")

	# # 버튼 스타일로 마크다운 텍스트 클릭 구현
	# for item in menu_items:
	# 	if st.sidebar.button(item):
	# 		st.session_state.selected_page = item
	# 	st.sidebar.markdown("---")  # 항목 사이 구분선




	if st.session_state.selected_page == "Home":
		Info_KGSD()
	elif st.session_state.selected_page == "login":
		Login()
		ExecuteCount += 1
		st.text("ExecuteCount:{}".format(ExecuteCount))

		if(seluser.IsLogin):
			st.markdown("Login Info : OK login")
		else:
			st.markdown("Login Info : NG login")
	
	elif st.session_state.selected_page == "소개":
		Info_KGSD()

	elif st.session_state.selected_page == "걸어온 길":
		KGSD_History()

	elif st.session_state.selected_page == "같이하는 동료":
		st.text("Page 같이하는 동료")

	elif st.session_state.selected_page == "SignUp":
		SignUp()
	elif st.session_state.selected_page == "SearchData":
		SearchData()

	elif st.session_state.selected_page == "Test":
		# intro()
		result1 = triangle_area(200, 20)
		result2 = rectangle_area(200, 20)
		st.write(result1)
		st.write(result2)
	elif st.session_state.selected_page == "InsertData":
		# InsertData_demo()
		
		blood_sugar = st.number_input("혈당 입력", format="%.2f")
		lactic_acid = st.number_input("락틱산 입력", format="%.2f")

		try:
			st.text("IsLogin:{}".format(st.session_state.IsLogin))
			st.text("username:{}".format(st.session_state.username))
			st.text("ssn:{}".format(st.session_state.ssn))
			# st.text("IsLogin:{}".format(seluser.IsLogin))

			# if(st.session_state.IsLogin):
			# 	if(st.button("Add Data")):
			# 		add_user_data(st.session_state.ssn, blood_sugar, lactic_acid)

			# 	digit = st.session_state.ssn.replace('-','')
			# 	st.text("Execute TableInfo({})".format(digit))
			# 	TableInfo(digit)

			# elif choice == "plotting_demo":
			# 	plotting_demo()
		
		except sqlite3.OperationalError as e:
			st.text(f"Error:{e}")

if __name__ == '__main__':
	main()
