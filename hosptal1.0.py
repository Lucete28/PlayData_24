import requests
from mysql import connector
import streamlit as st

HOST = '52.78.193.207'
USER = 'myname'
PW = '1234'
DATABASE='mydb'
PORT = '50598'


## streamlit으로 페이지 구현
def page1():
    st.title("접수 / 수납")
    if st.button("접수"):
        st.session_state.current_page = "page2"
    elif st.button("정보삭제"):
        st.session_state.current_page = "page5"


def page2():
    st.title("접수")
    st.write("처음 오셨습니까?")
    if st.button("처음입니다."):
        st.session_state.current_page = "page3"
    if st.button("와본적이 있습니다."):
        st.session_state.current_page = "page4"

def page3():
    st.title("처음오셨군요")
    insert_patient_info()

def page4():
    st.title("또오셨군요")
    update_patient_info()

def page5():
    st.title("정보삭제")
    delete_patient_info()


def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "page1"
    if st.session_state.current_page == "page1":
        page1()
    elif st.session_state.current_page == "page2":
        page2()
    elif st.session_state.current_page == "page3":
        page3()
    elif st.session_state.current_page == "page4":
        page4()
    elif st.session_state.current_page == "page5":
        page5()






# db 연결하기
def conn_db(host, port, user, pw, database):
  conn = connector.connect(host=host, user=user, password=pw, port=port, database=database)
  return conn

# connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
# cursor = connection_result.cursor()

# 처음 환자등록
def insert_patient_info():
    p_name = st.text_input("이름을 입력하세요 :")
    age = st.number_input("나이를 알려주세요 :",step=1, format="%d")
    gender = st.radio('성별을 알려주세요' ,('male','female'))
    phone_num = st.text_input('전화번호를 공백없이 입력해주세요 :')
    medical_field = st.radio('어느과에 진료를 희망하십니까?', ('정형외과','외과','이비인후과', '안과'))
    sql = f"INSERT into patient_info (p_name,medical_field,age,gender,phone_num,visit_count) values('{p_name}','{medical_field}',{age},'{gender}','{phone_num}',1);"
    
    if st.button("완료."):
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        # query문 실행
        cursor.execute(sql)
        connection_result.commit()
        # db연결해제
        connection_result.close()
        print("잘 저장되었습니다")
        st.session_state.current_page = "page1"
    elif st.button("메인페이지로..."):
        st.session_state.current_page = "page1"
    

def update_patient_info():
    p_name = st.text_input("이름을 입력하세요 :")
    medical_field = st.radio('어느과에 진료를 희망하십니까?', ('정형외과','외과','이비인후과', '안과'))
    sql = f"UPDATE patient_info SET visit_count = visit_count + 1,medical_field ='{medical_field}' WHERE p_name = '{p_name}'"
    if st.button("완료."):   
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(sql)
        connection_result.commit()
        connection_result.close()
        print("정보가 업데이트 되었습니다.")
        st.session_state.current_page = "page1"
    elif st.button("메인페이지로..."):
        st.session_state.current_page = "page1"

def delete_patient_info():
    p_name = st.text_input("삭제하고자 하는 회원의 이름을 입력해 주세요")
    phone_num = st.text_input("등록하신 휴대폰번호를 입력해 주세요")
    sql = f"DELETE FROM patient_info WHERE phone_num={phone_num} and p_name = {p_name}"
    if st.button("완료."):   
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(sql)
        connection_result.commit()
        connection_result.close()
        print("회원정보가 삭제되었습니다.")
        st.session_state.current_page = "page1"
    elif st.button("메인페이지로..."):
        st.session_state.current_page = "page1"


if __name__ == "__main__":
    main()