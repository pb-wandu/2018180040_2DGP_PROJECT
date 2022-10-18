### [별그림자 이야기] 메인 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *    # pico2d 라이브러리 import
import game_framework   # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 전환시 호출

# from StarPainter import * # 게임 프레임워크 Main 파일 임포트

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = -999        # 아직 정해지지 않은 것
DELAYTIME = 0.01    # 지연 시간

# ------------ 변수들 ------------

imagebg = None # 배경 이미지

# ------------ 메뉴 함수들 ------------

# 메뉴 진입
def enter():
    global imagebg
    imagebg = load_image('mainmenuimg.png') # 시작 메뉴 이미지
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

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # 키를 눌렀을 때
        elif event.type == SDL_KEYUP:

            # enter키를 누를 경우 게임 메뉴로 이동
            if event.key == SDLK_RETURN:
                game_framework.change_state(frame_game)
                delay(DELAYTIME)

            # esc키를 누를 경우 게임 종료
            if event.key == SDLK_ESCAPE:
                game_framework.quit()