### [별그림자 이야기] 컨트롤 관련 파일입니다

# ------------ import 파일들, 상수들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import

import frame_main         # 메인 메뉴
import frame_game         # 게임 메뉴
import frame_info         # 정보 메뉴
import frame_upgrade      # 별그림자 회랑
import frame_pause        # 대기 전환

import stageinfo          # 스테이지 관련 변수, 함수

UNSET = 999                     # 아직 정해지지 않은 것
BTNSIZEX, BTNSIZEY = 260, 100   # 버튼 크기

# ------------ 컨트롤 관련 변수, 함수 ------------

# 키 각각 입력 여부
keypressedleft, keypressedright, keypressedup, keypresseddown = 0, 0, 0, 0
keypressedz, keypressedq, keypressedw = 0, 0, 0

mousex, mousey = UNSET, UNSET               # 마우스 x좌표, y좌표
mouseclickedx, mouseclickedy = UNSET, UNSET # 마우스 클릭한 x좌표, y좌표

keypressing = 0    # 키보드 입력중 여부
mousepressed = 0   # 마우스 클릭한 여부

# 내부에 있는지 확인하는 함수
def ifinsidesq(sql, sqr, sqd, squ, x, y):
    if sql <= x <= sqr and sqd <= y <= squ:
        return True
    else:
        return False

# ------------ 메뉴별 키 입력 이벤트 ------------

# ----- 메인 메뉴 -----

def frame_main_events():

    events = get_events()

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
                delay(frame_main.DELAYTIME)

            # enter키를 누를 경우 게임 메뉴로 이동
            if event.key == SDLK_RETURN:
                game_framework.change_state(frame_game)
                delay(frame_main.DELAYTIME)

            # esc키를 누를 경우 게임 종료
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

        # 마우스 눌렀을 때
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # x, y 좌표 지정
            x, y = event.x, frame_main.WINDOWYSIZE - 1 - event.y

            # 마우스 누른 위치와 버튼 위치 비교

            # 게임 시작 버튼
            if ifinsidesq(150 - BTNSIZEX / 2, 150 + BTNSIZEX / 2, 70 - BTNSIZEY / 2, 70 + BTNSIZEY / 2, x, y):
                game_framework.change_state(frame_game)
                delay(frame_main.DELAYTIME)
                pass

            # 게임 정보 버튼
            elif ifinsidesq(430 - BTNSIZEX / 2, 430 + BTNSIZEX / 2, 70 - BTNSIZEY / 2, 70 + BTNSIZEY / 2, x, y):
                game_framework.push_state(frame_info)
                delay(frame_main.DELAYTIME)
                pass

            # 게임 종료 버튼
            elif ifinsidesq(710 - BTNSIZEX / 2, 710 + BTNSIZEX / 2, 70 - BTNSIZEY / 2, 70 + BTNSIZEY / 2, x, y):
                game_framework.quit()
                pass


        # 마우스 떼었을 때
        elif event.type == SDL_MOUSEBUTTONUP:
            mousepressed = 1

# ----- 게임 메뉴 -----

def frame_game_events():
    global keypressedleft, keypressedright, keypressedup, keypresseddown
    global keypressedz, keypressedq, keypressedw
    global mousex, mousey, mouseclickedx, mouseclickedy

    events = get_events()

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # F1키를 눌렀다 뗄 경우 중단
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F1):
            game_framework.push_state(frame_pause)  # 일시정지 메뉴 열기

        # 숫자키로 기술 잠그기, 잠금 해제

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_1):
            frame_game.skillmovelocked = 1 - frame_game.skillmovelocked
            if frame_game.skillmovelocked == 1:
                frame_game.nowskillmovecooltime = 0

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_2):
            frame_game.skillqlocked = 1 - frame_game.skillqlocked
            if frame_game.skillqlocked == 1:
                frame_game.nowqstate = 0

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_3):
            frame_game.skillwlocked = 1 - frame_game.skillwlocked

        # F9, F10키는 테스트용으로, 각각 이전, 다음 스테이지 이동키입니다

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F9):
            stageinfo.nowcollectedstar = 0  # 모은 별 개수 초기화
            stageinfo.ifstagedrawed = 0  # 스테이지 그려짐 여부 초기화

            if stageinfo.nowgamestage > 11:  # 시작 스테이지가 아닐 경우
                if int(stageinfo.nowgamestage % 10) == 1:  # 현재 1지역일 경우
                    stageinfo.nowgamestage -= 10  # 이전 차원으로
                    stageinfo.nowgamestage += 4  # 5지역으로
                else:
                    stageinfo.nowgamestage -= 1  # 이전 지역으로

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F10):
            stageinfo.nowcollectedstar = 0  # 모은 별 개수 초기화
            stageinfo.ifstagedrawed = 0  # 스테이지 그려짐 여부 초기화

            if stageinfo.nowgamestage < 65:  # 6번째 차원의 5지역에 도달하지 않았을 경우
                if int(stageinfo.nowgamestage % 10) == 5:  # 현재 5지역일 경우
                    stageinfo.nowgamestage += 10  # 다음 차원으로
                    stageinfo.nowgamestage -= 4  # 1지역으로
                else:
                    stageinfo.nowgamestage += 1  # 다음 지역으로

        # 키보드 각각 누른 경우

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            keypressedz = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            keypressedz = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            keypressedq = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_q):
            keypressedq = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            keypressedw = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_w):
            keypressedw = 0

        # esc키를 누를 경우 메인 메뉴로 이동
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_ESCAPE):
            game_framework.change_state(frame_main)
            delay(frame_main.DELAYTIME)

        # 마우스 이동시
        elif event.type == SDL_MOUSEMOTION:
            mousex, mousey = event.x, frame_main.WINDOWYSIZE - 1 - event.y

            if frame_game.nowqstate == 1:
                if mousex < 0:
                    mousex = 0
                if mousex > 680:
                    mousex = 680
                if mousey < 120:
                    mousey = 120
                if mousey > 700:
                    mousey = 700

        # 마우스 떼었을 때
        elif event.type == SDL_MOUSEBUTTONUP:
            if frame_game.nowqstate == 1:
                if frame_game.eunbi.energynow >= frame_game.eunbi.energymax * (frame_game.skillqneedenergypercent / 100):
                    frame_game.eunbi.energynow -= frame_game.eunbi.energymax * (frame_game.skillqneedenergypercent / 100)
                    frame_game.nowqstate = 2
                    mouseclickedx, mouseclickedy = mousex, mousey
                    frame_game.eunbi.x, frame_game.eunbi.y = mouseclickedx, mouseclickedy

                else:
                    frame_game.nowqstate = 0


        # 그 외의 경우 은비(플레이어) 캐릭터 컨트롤러 실행
        else:
            frame_game.eunbi.handle_event(event)

# ----- 별그림자 회랑 (강화 메뉴) -----

def frame_upgrade_events():

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