### [별그림자 이야기] 게임 정보 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_main         # 프로그램 전체에 해당되는 값 사용

infoimage = None

# ------------ 게임 프레임워크 동작들 ------------

# 메뉴 진입
def enter():
    global infoimage
    infoimage = load_image('infoimg.png')  # 일시정지 이미지
    pass

# 메뉴 종료
def exit():
    global infoimage
    del infoimage
    pass

# 화면 그리기
def draw():
    clear_canvas()

    # 게임 정보 메뉴 이미지 그리기
    infoimage.draw(frame_main.WINDOWXSIZE / 2, frame_main.WINDOWYSIZE / 2)

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

        # 키를 눌렀다 뗀 경우
        elif event.type == SDL_KEYUP:

            # esc키를 누를 경우 메인 메뉴로 이동
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(frame_main)
                delay(frame_main.DELAYTIME)

