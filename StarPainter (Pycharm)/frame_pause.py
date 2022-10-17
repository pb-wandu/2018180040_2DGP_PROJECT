### [별그림자 이야기] 일시정지 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 전환시 호출
import frame_main         # 프로그램 전체에 해당되는 값 사용

pauseimage = None

# 메뉴 진입
def enter():
    global pauseimage
    pauseimage = load_image('pauseimg.png')  # 일시정지 이미지
    pass

# 메뉴 종료
def exit():
    global pauseimage
    del pauseimage
    pass

# 화면 그리기
def draw():
    clear_canvas()

    # 일시정지 메뉴 이미지 그리기
    pauseimage.draw(frame_main.WINDOWXSIZE / 2, frame_main.WINDOWYSIZE / 2)

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

        # F1키를 누를 경우 게임 메뉴로 이동
        elif event.type == SDL_KEYUP :
            if event.key == SDLK_F1:
                game_framework.change_state(frame_game)
                delay(frame_main.DELAYTIME)

            # esc키를 누를 경우 게임 메뉴로 이동
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(frame_game)
                delay(frame_main.DELAYTIME)

