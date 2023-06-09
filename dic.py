import streamlit as st
import os
import time
import pandas as pd

col=["카테고리","타겟", "태그"]
category = [None,'linux', 'python']
folder_path = r'C:\streamlit'
file_name = 'test3.csv'
file_path = os.path.join(folder_path, file_name)



def concat_df(file_path, new_df):
    try:
        # 파일 열기
        old_df = pd.read_csv(file_path)

        # 데이터 프레임 수정
        # 여기서는 예시로 "column_name" 열의 값을 수정
        updated_df = pd.concat([old_df, new_df], ignore_index=True)

        # 수정된 데이터 프레임을 파일에 저장
        updated_df.to_csv(file_path, index=False)
        st.write("성공")
        return True  # 데이터 프레임 수정 성공
    except Exception as e:
        print(f"데이터 프레임 수정 중 오류 발생: {str(e)}")
        st.write('실패')
        return False  # 데이터 프레임 수정 실패
def search():
    st.title('검색')
    cat = st.radio("카테고리를 선택", category) 
    target = st.text_input("타겟")  
    tag = st.text_area("설명")  
    
    output = st.empty()  # 출력 컨테이너 초기화
    
    df = pd.read_csv(file_path)
    if cat:
        df = df[df['카테고리']==cat]
    if target:  
        df = df[df['타겟']==target]
    if tag:
        df = df[df['태그']==tag]
    
    output.write(df)  # 결과 출력





def input():
    st.title('입력')
    cat = st.radio("카테고리를 선택", category)
    target = st.text_input("타겟")  
    tag = st.text_area("설명")  

    if st.button('commit'):
        data = [[cat, target, tag]]
        df = pd.DataFrame(data=data, columns=col)
        concat_df(file_path,df)
        




        
def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main_page"
    if st.session_state.current_page == "main_page":
        main_page()
    elif st.session_state.current_page == 'input':
        input()
    elif st.session_state.current_page == 'search':
        search()   
    elif st.session_state.current_page == 'README':
        README()      
        
def main_page():
    st.sidebar.title("Sidebar")
    sidebar_options = ["README","입력", "검색"]
    selected_option = st.sidebar.radio("옵션 선택", sidebar_options)
    
    if selected_option == "입력":
        input()
    elif selected_option == "검색":
        search()
    elif selected_option == "README":
        README()

def README():
    st.title('Custom Dictionary')
    st.write('사용자가 직접 내용을 작성할 수 있는 사전입니다')
    st.write('개발중에 있으며 모바일환경에서는 작동하지 않을 수 있습니다.')
    st.write('앱 사용시 파일이 자동생성되며 삭제시 제대로 기능하지 않을 수 있습니다.')
    st.write('좌측 sidebar에서 입력 또는 검색을 눌러 사용해주세요')
    st.write('추가로 원하는 카테고리등은 직접 문의해주세요')
    st.write('Email : 2580jhy28@gmail.com')
    st.write('')
    if folder_state:
        if file_state:
            st.write('파일이 정상 생성되었습니다')
        else:
            st.write('파일을 생성하지 못했습니다.')

        
    


        
        
    
if __name__ == "__main__":
    # 폴더 경로 입력
    # 폴더 생성
    try:
        os.mkdir(folder_path)
        folder_state = True
    except FileExistsError:
        folder_state = True



# 파일이 이미 존재하는지 확인
if not os.path.isfile(file_path):
    try:
        # 빈 데이터프레임 생성
        df = pd.DataFrame(columns=col)
        # 데이터프레임을 파일에 저장
        df.to_csv(file_path, index=False)

        file_state = True
    except Exception as e:
        file_state = False
else:
        file_state = True

    
main()
