import streamlit as st
import os
import pandas as pd

main_folder_PATH = 'C:/PlayData/day_38/stramlit_Test'
main_folder = os.listdir(main_folder_PATH)

category = ['','linux', 'python']


        
def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main_page"
    if st.session_state.current_page == "main_page":
        main_page()
    elif st.session_state.current_page == 'input':
        input()
    elif st.session_state.current_page == 'serch':
        serch()        
        
def main_page():
    st.title("안녕")
    if st.button('입력'):
        st.session_state.current_page = "input"
    if st.button('검색'):
        st.session_state.current_page = "serch"
        
def input():
    cat = st.radio("카테고리를 선택", category)
    target = st.text_input("타겟")  

    tag = st.text_area("설명")  

    if st.button('commit'):
        data = [[cat, target, tag]]
        df = pd.DataFrame(data=data, columns=["카테고리","타겟", "태그"])
        try:
            # 파일 불러오기
            existing_df = pd.read_excel('test1.xlsx')
            # 이어쓰기 데이터 추가
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            # 파일 저장
            updated_df.to_excel('test1.xlsx', index=False)
            st.write('완료')    
        except:
            df.to_excel('test1.xlsx', index=False)
            st.write('완료') 
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "main_page"

def serch():
    st.title('검색')
    cat = st.radio("카테고리를 선택", category) 
    target = st.text_input("타겟")  
    tag = st.text_area("설명")  
    if st.button('commit'):
        df = pd.read_excel('C:/PlayData/test1.xlsx')
        if cat:
            df = df[df['카테고리']==cat]
        if target:
            df = df[df['타겟'].str.contains(target)]

        if tag:
            df = df[df['태그'].str.contains(tag)]

        st.write(df)
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "main_page"
        
    


        
        
    
if __name__ == "__main__":
    main()
