import requests
from mysql import connector
import streamlit as st

HOST = '52.78.193.207'
USER = 'myname'
PW = '1234'
DATABASE='mydb'
PORT = '54890'

## streamlit으로 페이지 구현
def p_main():
    st.title("접수 / 수납")
    st.sidebar.title("메뉴")        
    if st.sidebar.button('환자'):
        st.session_state.current_page = "p_main"      
    if st.sidebar.button('진료'):
        st.session_state.current_page = "p_treat"

    if st.button("접수"):
        st.session_state.current_page = "p_registration"
    if st.button("수납"):
        st.session_state.current_page = "p_receipt"
    if st.button("조회"):
        st.session_state.current_page = "p_search"
    if st.button("정보삭제"):
        st.session_state.current_page = "p_delete"

def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "p_main"
    if st.session_state.current_page == "p_main":
        p_main()
    elif st.session_state.current_page == "p_registration":
        p_registration()
    elif st.session_state.current_page == "p_firstvisit":
        p_firstvisit()
    elif st.session_state.current_page == "p_revisit":
        p_revisit()
    elif st.session_state.current_page == "p_search":
        p_search()
    elif st.session_state.current_page == "p_delete":
        delete_patient_info()
    elif st.session_state.current_page == "p_treat":
        treat()
    elif st.session_state.current_page == "p_receipt":
        receipt()
    


def receipt():
    st.title("수납을 위한 페이지")
    p_name = st.text_input("환자이름을 입력하세요 :")
    phone_num = st.text_input("환자 휴대폰번호를 입력해 주세요")
    select_price = f"select price from patient_info where phone_num = '{phone_num}'"
    pay = f"UPDATE patient_info SET price = 0 WHERE phone_num = '{phone_num}'"
    # if select_price:
    #     st.write(f"결재가 필요한 금액은 {(select_price)}입니다.")
    if st.button("검색"):
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(select_price)
        result = cursor.fetchall()
        st.write(f"결재가 필요한 금액은 {result[0][0]}입니다.")

        if st.button("결재하기"):
            print(pay)
            cursor.execute(pay)
            connection_result.commit()
            connection_result.close()
            st.session_state.current_page = "p_main"
            st.experimental_rerun()
    if st.button("메인페이지로..."):
        st.session_state.current_page = "p_main"
    

def treat():
    st.title("진료를 위한 페이지")
    p_name = st.text_input("환자이름을 입력하세요 :")
    phone_num = st.text_input("환자 휴대폰번호를 입력해 주세요")
    patient_id_select = f"SELECT id FROM patient_info WHERE phone_num = '{phone_num}'"
    clinic_content = st.text_input("진료내용을 적어주세요")
    clinic_price = st.number_input("금액을 적어주세요",step=1)
    creat_clinic_data = f"INSERT into clinic_data (p_id, phone_num, clinic_content, clinic_price) values (({patient_id_select}), '{phone_num}', '{clinic_content}', {clinic_price})"
    add_price = f"UPDATE patient_info SET price = price + {clinic_price} WHERE phone_num = '{phone_num}'"
    if st.button("완료."):   
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(creat_clinic_data)
        cursor.execute(add_price)
        connection_result.commit()
        connection_result.close()
        print("진료가 끝났습니다.")
        st.session_state.current_page = "p_main"
    if st.button("메인페이지로..."):
        st.session_state.current_page = "p_main"



# db 연결하기
def conn_db(host, port, user, pw, database):
  conn = connector.connect(host=host, user=user, password=pw, port=port, database=database)
  return conn


def p_search():
    st.title("회원 조회를 위한 페이지입니다.")
    info_search()


def p_registration():
    st.title("접수")
    st.write("처음 오셨습니까?")
    if st.button("처음입니다."):
        st.session_state.current_page = "p_firstvisit"
    if st.button("와본적이 있습니다."):
        st.session_state.current_page = "p_revisit"



def p_firstvisit():
    st.title("처음오셨군요")
    insert_patient_info()

def p_revisit():
    st.title("또오셨군요")
    update_patient_info()





# connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
# cursor = connection_result.cursor()

# 처음 환자등록
def insert_patient_info():
    p_name = st.text_input("이름을 입력하세요 :")
    age = st.number_input("나이를 알려주세요 :",step=1)
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
        st.session_state.current_page = "p_main"
    

def update_patient_info():
    p_name = st.text_input("이름을 입력하세요 :")
    phone_num = st.text_input("등록하신 휴대폰번호를 입력해 주세요")

    medical_field = st.radio('어느과에 진료를 희망하십니까?', ('정형외과','외과','이비인후과', '안과'))
    sql = f"UPDATE patient_info SET visit_count = visit_count + 1,medical_field ='{medical_field}' WHERE phone_num = '{phone_num}'"
    if st.button("완료."):   
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(sql)
        connection_result.commit()
        connection_result.close()
        print("잘 저장되었습니다")
        st.session_state.current_page = "p_main"

def info_search():
    st.title("정보 조회")
    p_name = st.text_input("이름을 입력하세요 :")
    phone_num = st.text_input("등록하신 휴대폰번호를 입력해 주세요")
    sql = f"SELECT * FROM patient_info WHERE phone_num='{phone_num}' and p_name = '{p_name}'"
    if st.button("완료."):    
        try:
            # db연결
            connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
            cursor = connection_result.cursor()
            # query문 실행
            cursor.execute(sql)
            result = cursor.fetchall()
            connection_result.close()
            st.write(f"회원 ID : {result[0][0]}")
            st.write(f"회원 성명 : {result[0][1]}")
            st.write(f"최근진료과 : {result[0][2]}")
            st.write(f"회원 나이 : {result[0][3]}")
            st.write(f"성별 : {result[0][4]}")
            st.write(f"전화번호 : {result[0][5]}")
            st.write(f"병원 방문횟수 : {result[0][6]}")
            print(result)
            # st.write(result)
            print("조회되었습니다.")
            st.session_state.current_page = "p_main"
        except:
            st.write("회원정보가 조회되지 않습니다.")
    if st.button("메인페이지로..."):
        st.session_state.current_page = "p_main"

def delete_patient_info():
    p_name = st.text_input("삭제하고자 하는 회원의 이름을 입력해 주세요")
    phone_num = st.text_input("등록하신 휴대폰번호를 입력해 주세요")
    sql_1 = f"DELETE FROM clinic_data WHERE phone_num='{phone_num}'"
    sql = f"DELETE FROM patient_info WHERE phone_num='{phone_num}' and p_name = '{p_name}'"
    if st.button("완료."):   
        # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(sql_1)
        cursor.execute(sql)
        connection_result.commit()
        connection_result.close()
        print("회원정보가 삭제되었습니다.")
        st.session_state.current_page = "p_main"
    if st.button("메인페이지로..."):
        st.session_state.current_page = "p_main"


    

if __name__ == "__main__":
    main()