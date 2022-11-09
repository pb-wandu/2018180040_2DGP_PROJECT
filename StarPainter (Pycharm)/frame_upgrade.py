### [별그림자 이야기] 별그림자 회랑 (강화 메뉴) 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import

import frame_main         # main의 변수들 import
import frame_game         # 게임 메뉴 전환시 호출
import object_player      # 플레이어 관련 변수 사용

import game_world         # 게임 월드 및 스테이지 관련 변수, 함수

upgradeimage = None

# ------------ 게임 프레임워크 동작들 ------------

# 메뉴 진입
def enter():
    global upgradeimage
    upgradeimage = load_image('upgradeimg.png')  # 일시정지 이미지

    # 현위치 지정
    frame_main.nowplace = frame_main.PL_UPGRADE

    pass

# 메뉴 종료
def exit():
    global upgradeimage
    del upgradeimage
    pass

# 화면 그리기
def draw():
    clear_canvas()

    # [별그림자 회랑] 강화 메뉴 이미지 그리기
    upgradeimage.draw(frame_main.WINDOWXSIZE / 2, frame_main.WINDOWYSIZE / 2)

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

        # esc 또는 엔터키를 누를 경우 게임 메뉴(다음 스테이지)로 이동
        elif event.type == SDL_KEYUP:

            if event.key == SDLK_RETURN or event.key == SDLK_ESCAPE:

                # 스테이지 재시작
                frame_game.stagerestart = 1

                # 게임 메뉴로 이동
                game_framework.change_state(frame_game)
                delay(frame_main.DELAYTIME)

# 직접 실행시켰을 경우

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()

