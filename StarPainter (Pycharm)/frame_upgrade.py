### [별그림자 이야기] 별그림자 회랑 (강화 메뉴) 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 전환시 호출
import frame_main         # 프로그램 전체에 해당되는 값 사용
import object_player      # 플레이어 관련 변수 사용

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

                # 다음 스테이지(또는 다음 차원)로 이동
                frame_game.nowgamestage += 1 # 다음 스테이지로 이동
                if int(frame_game.nowgamestage % 10) == 5:  # 현재 5지역일 경우
                    frame_game.nowgamestage += 10  # 다음 차원으로
                    frame_game.nowgamestage -= 4  # 1지역으로

                frame_game.nowcollectedstar = 0 # 모은 별 개수 초기화
                frame_game.ifstagedrawed = 0 # 스테이지 그려짐 여부 초기화

                # 최대 체력과 기력으로 스테이지 시작
                object_player.lifenow, object_player.energynow = object_player.lifemax, object_player.energymax

                # 키 입력 초기화
                frame_game.keypressedleft = 0
                frame_game.keypressedright = 0
                frame_game.keypressedz = 0

                game_framework.change_state(frame_game) # 게임 메뉴로 이동
                delay(frame_main.DELAYTIME)

# 직접 실행시켰을 경우

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()

