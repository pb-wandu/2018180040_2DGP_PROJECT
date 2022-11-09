### [별그림자 이야기] 메인 메뉴 파일입니다

# main 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트
import frame_game         # 게임 메뉴 전환시 호출
import frame_info         # 정보 메뉴 전환시 호출

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = 999         # 아직 정해지지 않은 것
DELAYTIME = 0.005   # 지연 시간

# ------------ 변수들 ------------

imagebg = None # 배경 이미지

mouseclickedx, mouseclickedy = UNSET, UNSET # 마우스 클릭한 x좌표, y좌표
mousepressed = 0 # 마우스 클릭한 여부

PL_MAIN, PL_INFO, PL_STAGE, PL_PAUSE, PL_UPGRADE = 10, 11, 20, 21, 30

nowplace = UNSET

# ------------ 게임 프레임워크 동작들 ------------

# 메뉴 진입
def enter():
    global imagebg
    global nowplace
    
    imagebg = load_image('mainmenuimg.png') # 시작 메뉴 이미지

    # 현위치 지정
    nowplace = PL_MAIN

    pass

# 메뉴 종료
def exit():
    global imagebg
    del imagebg
    pass

# 화면 그리기
def draw():
    clear_canvas()
    imagebg.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 시작 메뉴 이미지 그리기
    update_canvas()

# 정보 갱신
def update():
    #
    pass

# 이벤트 핸들러
def handle_events():
    events = get_events()

    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표
    global mousepressed  # 마우스 클릭한 여부

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # 키를 눌렀을 때
        elif event.type == SDL_KEYUP:

            # F1키를 누를 경우 정보 메뉴 열기
            if event.key == SDLK_F1:
                game_framework.push_state(frame_info)
                delay(DELAYTIME)

            # enter키를 누를 경우 게임 메뉴로 이동
            if event.key == SDLK_RETURN:
                game_framework.change_state(frame_game)
                delay(DELAYTIME)

            # esc키를 누를 경우 게임 종료
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

        # 마우스 눌렀을 때
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # x, y 좌표 지정
            mouseclickedx, mouseclickedy = event.x, WINDOWXSIZE - 1 - event.y

        # 마우스 떼었을 때
        elif event.type == SDL_MOUSEBUTTONUP:
            mousepressed = 1

# 중단되었을 경우
def pause():

    pass

# 다시 실행된 경우
def resume():

    pass

# 직접 실행시켰을 경우

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()