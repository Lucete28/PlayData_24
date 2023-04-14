#파일에 버전을 0.0 에서 0으로 수정(파일 import할때 문제발생)
#메인페이지 재구성
#재호님이 마켓리스트 테이블 데이터 재구성
from mysql import connector
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta,date
import plotly.express as px
import matplotlib.pyplot as plt
# from sqlalchemy import create_engine


HOST = '3.35.138.95'
USER = 'myname'
PW = '1234'
DATABASE='mydb'
PORT = '54199'

#페이지 전환 부분
def main():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "p_main"
    if st.session_state["current_page"] == "p_main":
        p_main()
    elif st.session_state["current_page"] =='get_marketlist':
        get_marketlist()
    elif st.session_state["current_page"]== 'category_info':
        category_info()
    elif st.session_state["current_page"] == 'registration':
        registration()
    elif st.session_state["current_page"] == 'Customer_dashboard':
        Customer_dashboard()
    elif st.session_state["current_page"] == 'manage':
        manage_count()
    elif st.session_state["current_page"] == 'sales_over_time':
        sales_over_time()
    elif st.session_state["current_page"] == 'age_group_sales':
        age_group_sales()
    elif st.session_state["current_page"] == 'yeary_sales_by_month':
        yeary_sales_by_month()
    elif st.session_state["current_page"] == 'Time_dashboard':
        Time_dashboard()

def conn_db(host, port, user, pw, database):
  conn = connector.connect(host=host, user=user, password=pw, port=port, database=database)
  return conn

def p_main():
    col1, col2, col3= st.columns(3)
    with col1:
        st.title("고객관련")
        if st.button('회원가입'):
            st.session_state["current_page"] = "registration"

    with col2:
        st.title("상품 관리")
        if st.button('제품 카테고리'):
            st.session_state["current_page"] = "category_info"
        if st.button('재고관리'):
            st.session_state["current_page"] = "manage"
        if st.button('신상품 등록'):
            st.session_state["current_page"] = "get_marketlist"

    with col3:
        st.title("관리")
        # if st.button('주문'):
        #     st.session_state["current_page"] = "order"
        if st.button('시간 기준 분석 -2'):
            st.session_state["current_page"] = "Time_dashboard"
        if st.button('고객 정보 기준 분석-1'):
            st.session_state["current_page"] = "Customer_dashboard"
        
def Time_dashboard():
    st.title("시간을 기준으로 분석")
    if st.button("1 : 선택한 기간동안의 제품별 판매 실적"):
        st.session_state["current_page"] = "sales_over_time"
    if st.button("2 : 2022년 월매출 분석"):
        st.session_state["current_page"] = "yeary_sales_by_month"
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"

def Customer_dashboard():
    st.title("고객 정보를 기준으로 분석")
    if st.button("1 : 연령대별 선호하는 품목"):
        st.session_state["current_page"] = "age_group_sales"
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"

def yeary_sales_by_month(): ##조재호님
    st.title("22년 월별 매출 분석")
    conn = connector.connect(host=HOST, user=USER, password=PW, port=PORT, database=DATABASE)
    df = pd.DataFrame(pd.read_sql("SELECT * FROM order_his", conn))
    df.to_csv('order_his.csv', index=False)
    # 애매한 order_his보다 order_history라는 이름으로 변수저장
    order_history = pd.read_csv('order_his.csv')
    #order_history.isnull().sum() 없는거 알지면 혹시모르는 결측치 처리를 위한 엑스트라 스텝
    # order_history.csv 만드는과정으로 똑같이 market_list.csv만듬
    df = pd.read_sql("SELECT * FROM market_list", conn)
    df.to_csv('market_list.csv', index=False)
    market_list = pd.read_csv('market_list.csv')
    # market_list랑 order_history 데이터프레임을 합치고 싶었으나 서로 id랑 product_id가 달라서 마켓리스트 칼럼하나 손봄
    market_list = market_list.rename(columns={'id': 'product_id'})
    # product_id를 바탕으로 두 데이터프레임 결합. 이렇게 하면 product_id를 이용해 product_name을 참조할수 있음
    merged_df = pd.merge(order_history, market_list, on='product_id')
    # 합쳐진 df에 order_date을 판다스가 이해할수있는 to_datetime으로 변환하는 과정
    merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])
    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Convert month column to Categorical data type with the specified order
    merged_df['month'] = pd.Categorical(merged_df['order_date'].dt.strftime('%B'), categories=month_order, ordered=True)
    # Filter for 2022 sales
    sales_2022 = merged_df[merged_df['order_date'].dt.year == 2022]
    # Group by month and sum total amount
    monthly_sales = sales_2022.groupby('month')['total_amount'].sum()
    # Create bar chart with sorted month order
    fig = plt.figure(figsize=(15, 6))
    plt.bar(month_order, monthly_sales)
    plt.title('Monthly Sales')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    st.pyplot(fig)

    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"

def age_group_sales():  #손준성님 1
    conn = connector.connect(host=HOST, user=USER, password=PW, port=PORT, database=DATABASE)
    data_df = pd.DataFrame(pd.read_sql("SELECT * FROM order_his", conn))
    customer_df = pd.DataFrame(pd.read_sql("SELECT * FROM customers", conn))
    merge_df = pd.merge(data_df, customer_df, on='customer_id')
    merge_df1 = merge_df.copy()

    # 연령대 구하기
    today = date.today().year
    merge_df1['date_birth'] = pd.to_datetime(merge_df1['date_birth'])
    merge_df1['Age'] = today - merge_df1['date_birth'].dt.year

    def age(age):
        if age<14:
            return 'child'
        if age<20 and age>=14:
            return 'teenagers'
        if age<30 and age>=20:
            return '20th'
        if age<40 and age>=30:
            return '30th'
        if age<50 and age>=40:
            return '40th'
        if age<60 and age>=50:
            return '50th'
        if age<70 and age>=60:
            return '60th'
        if age<80 and age>=70:
            return '70th'
        if age<90 and age>=80:
            return '80th'
        else:
            return 'elder'

    merge_df1['group']=merge_df1['Age'].apply(age)

    # 그래프 그리기
    group_cat = merge_df1.groupby(['group','category_id'])['quantity'].sum()
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    group_cat.unstack().plot(kind='bar', stacked=True, ax=ax1)
    ax1.set_xlabel('group')
    ax1.set_ylabel('Quantity')
    ax1.set_title('Quantity by Group and Category ID')
    st.pyplot(fig1)

    product_id = st.number_input("분석하실 product_id를 적어주세요",step=1)
    filtered_data= merge_df1[(merge_df1['product_id']==product_id)]
    sales_by_age = filtered_data.groupby(['group'])['quantity'].sum().reset_index()
    fig = px.bar(sales_by_age, x='group', y='quantity', color='quantity', title='선택한물품별 연령별판매갯수')
    st.pyplot(fig)
    # MySQL 연결 종료
    conn.close()

    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"


def manage_count():
    
    col1,col2 = st.columns(2)
    with col1: 
        # 마켓리스트 테이블에서 재고량 num 미만일경우 알림띄어줌#조재호님 코드부분
        num = st.number_input("몇개미만 남아있는 제품을 알고 싶으세요?",step=1)
        query = f"SELECT id, product_name, product_count FROM market_list WHERE product_count < {num}"
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        # 재고량 num미만일 제품이 있을경우 메세지출력
        if len(results) > 0:
            for row in results:
                st.write(f"제품명 : {row[1]} (ID {row[0]}) 이(가) {row[2]}개 남았습니다.")

    with col2:
        #제품 아이디로 검색해서 재고 확인
        num_2 = st.number_input("어떤 제품의 재고가 알고 싶으신가요", step= 1)
        query_2 = f"select product_name,product_count FROM market_list where id = {num_2}"
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(query_2)
        results_2 = cursor.fetchall()
        if len(results_2) == 0:
            st.write("해당 제품이 없습니다.")
        else:
            st.write(f"ID: {num_2}, 제품명: {results_2[0][0]}은(는) {results_2[0][1]}개 남았습니다.")
    st.title('재고 추가하기')
    p_id = st.number_input('주문하고자 하는 제품 아이디를 입력해주세요',step=1)
    add_num = st.number_input("원하는 수량을 입력해주세요",step=1)
    if st.button("완료"):
        category_query = f"SELECT category_id FROM market_list WHERE id = {p_id}"
        price_query = f"SELECT product_price FROM market_list WHERE id={p_id}"
        cursor.execute(category_query)
        category_id = cursor.fetchone()[0]
        cursor.execute(price_query)
        price = int(cursor.fetchone()[0])   
        current_time = datetime.now()
        order_date = current_time.strftime("%Y-%m-%d")
        total_price = add_num * price
        st.write("재고가 추가되었습니다.")
        
        sql = f"UPDATE market_list SET product_count = product_count + {add_num} WHERE id = {p_id}"
        sql_2 = f"INSERT INTO market_order (category_id, product_id, order_date, quantity, total_price) VALUES ({category_id}, {p_id}, '{order_date}', {add_num}, {total_price})"
        cursor.execute(sql)
        cursor.execute(sql_2)
        connection_result.commit()
    if st.button("메인페이지로..."):
        connection_result.commit()
        connection_result.close()
        st.session_state["current_page"] = "p_main"

def sales_over_time():
    connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
    col1, col2 = st.columns(2)
    with col1:  
        p_id = st.number_input("제품아이디 검색",step=1)
        if p_id:
            try:
                sql_2 = f"select * from market_list where id = '{p_id}'"
                cursor = connection_result.cursor()
                cursor.execute(sql_2)
                result = cursor.fetchall()
                
                st.write('카테고리 :',result[0][1])
                st.write('제품이름 :',result[0][2])
                st.write('가격 :',result[0][3])
                st.write('설명 :',result[0][4])
                st.write('재고 :',result[0][5])
            except:
                st.write('제품아이디가 등록되어있지 않습니다.')
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 4, 10)
    with col2:
        st.write('가장 많이 팔리상품 TOP 3')
        # product_id, quantity합을 total_sales로 정의하여 상위 3개의 제일 잘팔린 아이템을 출력해주는 쿼리문
        query = f"SELECT product_id, SUM(quantity) AS total_sales FROM order_his WHERE order_date >= '{start_date}' AND order_date <= '{end_date}' GROUP BY product_id ORDER BY total_sales DESC LIMIT 3"

        # 판다를 이용하여 해당 쿼리문을 데이터프레임형식으로 저장
        df = pd.read_sql(query, connection_result)
        st.write(df)
    # 카테고리 선택
    selected_ca = st.checkbox("ALL")
    if selected_ca:
        selected_id = "category_id"
    else:
        selected_id_list = []
        if st.checkbox("1 : FOOD"):
            selected_id_list.append(1)
        if st.checkbox("2 : APPLIANCES"):
            selected_id_list.append(2)
        if st.checkbox("3 : PET"):
            selected_id_list.append(3)
        if st.checkbox("4 : ELECTRONIC"):
            selected_id_list.append(4)
        if st.checkbox("5 : FASHION"):
            selected_id_list.append(5)
        if st.checkbox("6 : HOME"):
            selected_id_list.append(6)
        if len(selected_id_list) == 0:
            st.warning("하나 이상의 카테고리를 선택하세요")
            return
        selected_id = ','.join(map(str, selected_id_list))
        
    # 데이터프레임 불러오기
    sql = f"SELECT * FROM order_his WHERE category_id in ({selected_id})"
    
    df = pd.read_sql(sql, connection_result)
    st.title("선택한 기간동안의 제품별 판매 실적")
    
    selected_range = st.slider(
        '분석 범위를 설정해 주세요',
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        step=timedelta(days=1)
    )
    start_date = selected_range[0].date()
    end_date = selected_range[1].date()
    # 선택한 기간의 데이터 필터링
    filtered_df = df[(df['order_date'] >= start_date) & (df['order_date'] <= end_date)]


    # 제품별 판매 실적을 막대 그래프로 시각화
    sales_by_product = filtered_df.groupby('product_id')['quantity'].sum().reset_index()
    fig = px.bar(sales_by_product, x='product_id', y='quantity', color='quantity')
    st.plotly_chart(fig)
    
    
    if st.button("메인페이지로..."):
        connection_result.commit()
        connection_result.close()
        st.session_state["current_page"] = "p_main"


def category_info():
    sql = "SELECT * FROM category"
    connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
    cursor = connection_result.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        st.write(f"카테고리 ID : {result[i][0]}")
        st.write(f"카테고리 명 : {result[i][1]}")
    
    connection_result.close()
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"

def get_marketlist():
    st.write('관리자만 사용해주세요')
    category_id = st.number_input('카테고리 id',step=1)
    product_name = st.text_input("제품이름")
    product_price = st.number_input('제품 가격',step=1)
    product_details = st.text_input('제품 설명')
    product_count = st.number_input('제품 수량',step=1)
    sql = f"insert into maket_list (category_id, product_name,product_price ,product_details, product_count) values({category_id},'{product_name}',{product_price},'{product_details}',{product_count})"
    if st.button("완료."):   
    # db연결
        connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
        cursor = connection_result.cursor()
        cursor.execute(sql)
        connection_result.commit()
        connection_result.close()
        st.session_state["current_page"] = "p_main"
    if st.button("메인페이지로..."):
        st.session_state["current_page"] = "p_main"

def registration():
    st.title('회원가입')
    st.write('관리자만 사용하시오')
    min_date = datetime(1800, 1, 1)
    max_date = datetime(2023, 12, 31)
    
    customer_id = st.text_input('id를 입력해주세요')
    customer_password = st.text_input('비밀번호를 등록해주세요')
    first_name = st.text_input('이름')
    last_name = st.text_input('성')
    e_mail = st.text_input("이메일")
    date_birth = st.date_input('생년월일', min_value=min_date, max_value=max_date)
    sex = st.radio('성별',('M','F'))
    address = st.text_input('주소')
    phone_num = st.text_input('전화번호')
    sql = f"insert into customers (customer_id, customer_password, first_name, last_name,email,date_birth, address,phone_num,sex) values ('{customer_id}','{customer_password}','{first_name}','{last_name}','{e_mail}','{date_birth}','{address}','{phone_num}','{sex}')"
    if st.button("완료."):   
        # db연결
            connection_result = conn_db(host=HOST, port=PORT, user=USER, pw=PW, database=DATABASE)
            cursor = connection_result.cursor()
            cursor.execute(sql)
            connection_result.commit()
            connection_result.close()
            st.session_state["current_page"] = "p_main"
    if st.button("메인페이지로..."):
            st.session_state["current_page"] = "p_main"


if __name__ == "__main__":
    main()