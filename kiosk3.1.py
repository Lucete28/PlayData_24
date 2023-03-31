#### 패치노트
#클래스 menu를 만듬
#클래스 menu를 통해 매장별 메뉴 결정
####미완성####

#'메뉴': [0가격, 1타입(drink/food), 2온도, 3사이즈, 4개수, 5메뉴 주문 번호]
class Menu:
    menu = {
        # 음료 메뉴
        '아메리카노': [3000, 'drink', 'hot/ice', '중/대/특대', 0,0],
        '라떼': [4000, 'drink', 'hot/ice', '중/대/특대', 0,0],
        '밀크티': [4500, 'drink', 'hot/ice', '중/대/특대', 0,0],

        # 음식 메뉴
        '케이크' : [5000, 'food', '', '', 0,0],
        '샌드위치' : [4000, 'food', '', '', 0,0]
        }




class Cafe:
    menu = Menu.menu
    def __init__(self):
        self.total_price = 0
        self.total_menu = {}
        self.basket = {}
        self.menu_num = 0
       

    def add_cart_menu(self):
        ans = input("메뉴를 골라주세요 : ")
        if ans not in self.menu:
            print(f"{ans}은(는) 메뉴에 없습니다.")
            ans2 = input("종료하시겠습니까? : (Y/N)")
            if ans2 == 'Y' or ans2 == 'y':
                return
            else:
                self.add_cart_menu()
        
        #고른게 음료메뉴인 경우
        elif self.menu[ans][1] == 'drink':
            self.basket[ans] = self.menu[ans]
            self.menu_num +=1
            #음료 설정하는 함수
            self.set_drink(ans)
        
        #고른게 음식메뉴인 경우
        elif self.menu[ans][1] == 'food':
            self.basket[ans] = self.menu[ans]
            self.menu_num +=1
            #음식 설정하는 함수
            self.set_food(ans)

        else:
            print("뭔가 잘못되었습니다.")
            return
        

        #추가 주문
        print("현재까지 주문한 메뉴입니다.\n",self.total_menu)
        add_more = input("더 주문 하시겠습니까? : (Y/N)")
        if add_more == 'Y'or add_more == 'y':
            self.add_cart_menu()
        
        #메뉴 수정
        ans3 = input("메뉴를 수정하시겠습니까? : (Y/N)")
        if ans3 == 'Y'or ans3 == 'y':
            self.change_menu()

        #계산
        self.get_price()

    #'메뉴': [0가격, 1타입(drink/food), 2온도, 3사이즈, 4개수]
    def set_drink(self, ans):
        #온도 설정
        print("ice는 500원이 추가됩니다.")
        temp = input("온도를 선택해주세요 : (HOT/ICE)")
        if temp == 'HOT' or temp == 'hot' or temp == 'h':
            self.basket[ans][2] = 'HOT'
        elif temp == 'ICE' or temp == 'ice' or temp == 'i':
            self.basket[ans][2] = 'ICE'
            self.basket[ans][0] += 500
        else:
            print("잘못된 입력입니다.")
            ans2 = input("종료하시겠습니까? : (Y/N)")
            if ans2 == 'Y'or ans2 == 'y':
                return
            else:
                self.set_drink(ans)
                    
        #사이즈 설정
        print("대 사이즈는 500원\n특대 사이즈는 1000원이 추가됩니다")
        size = input("크기를 선택해주세요 : (중/대/특대)")
        if size == '중':
            self.basket[ans][3] = '중'
        elif size == '대':
            self.basket[ans][3] = '대'
            self.basket[ans][0] += 500
        elif size == '특대':
            self.basket[ans][3] = '특대'   
            self.basket[ans][0] += 1000

        else:
            print("잘못된 입력입니다.")
            ans2 = input("종료하시겠습니까? : (Y/N)")
            if ans2 == 'Y'or ans2 == 'y':
                return
            else:
                self.set_drink(ans)

        #개수 설정
        count = int(input("몇잔 주문하시겠습니까? :"))
        self.basket[ans][4] -= count
        #메뉴번호 설정
        self.basket[ans][5] = self.menu_num
        self.total_menu[ans] = self.basket[ans]

    ######## 같은메뉴 여러번 주문시 오류발생
        # if basket[ans] not in total_menu: #새로운 메뉴
        #     total_menu[1][ans] = basket[ans]
        # elif total_menu[ans] in total_menu:
        #     #새로 주문한 메뉴의 온도, size까지 확인하여 구분
        #     try:
        #         for i in total_menu[ans][:3]:
        #             if i in basket[ans]:
        #                 pass
        #             else: #같은 메뉴 다른 주문
        #                 total_menu[ans] = basket[ans]
        #     #같은메뉴 같은 주문
        #     except:
        
                
        #'메뉴': [0가격, 1타입(drink/food), 2온도, 3사이즈, 4-개수, 5메뉴번호]
    def set_food(self, ans):
        
        #개수 설정
        count = int(input(f"{ans}를 몇개 주문하시겠습니까? : "))
        self.basket[ans][4] -= count
        #메뉴번호 등록
        self.basket[ans][5] = self.menu_num
        self.total_menu[ans] = self.basket[ans]

    def change_menu(self):
        #제거할 거 특정
        delete_menu_num = int(input("몇번째 메뉴를 제거하시겠습니까? : "))

        # for key in total_menu:
        #     value_list = total_menu[key]
        #     second_value = value_list[1]
        #     print(f"The second value of {key} is {second_value}")

        #잘못된 번호
        if delete_menu_num > self.menu_num:
            print("다시 선택해주세요")
            self.change_menu()
        #올바른 번호
        else:
            del_menu =[]
            for key, value in self.total_menu.items():
                if delete_menu_num in value:
                    del_menu += key
            del_menu = ''.join(del_menu)
            print(del_menu)
            del self.total_menu[del_menu]
            print(f"현재 남은 메뉴 : {self.total_menu}")
            #[k for k, v in total_menu.items() if v == delete_menu_num]

    def get_price(self):
        price = 0
        for value in self.total_menu.values():
            price += -1*(value[0] * value[4])
        print(f"총 금액은{price}입니다.")


class Cafe_1(Cafe):
    def change_menu(self):
        super().change_menu()
        take_out = input("Take_Out 하시겠습니까? : (Y/N)")
        if take_out == 'N'or take_out == 'n':
            print("매장용기를 사용하겠습니다.")
        else:
            pack = input("개인 용기를 사용하시겠습니까?: (Y/N)")
            if pack == 'N'or pack == 'n':
                print("일회용기를 사용하여 환경이 파괴되었습니다.")
            else: 
                print("환경을 생각해주셔서 감사합니다.")

    def run(self):
        #메뉴출력
        for key, value in self.menu.items():
            print(key + ', ' + str(value[0]))
        #주문받기 시작
        self.add_cart_menu()

First_store = Cafe_1()
First_store.run()





