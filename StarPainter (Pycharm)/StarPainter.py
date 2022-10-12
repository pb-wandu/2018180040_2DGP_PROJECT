### [별그림자 이야기] Main 파일입니다

from pico2d import *    # pico2d 라이브러리 import
import game_framework   # 게임 프레임워크 임포트
import random           # 랜덤 라이브러리 import

import mainmenu         # 메인메뉴
import gamemenu         # 게임중 메뉴
# import upgrademenu      # 별그림자 회랑 (강화) 메뉴

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기

# ------------ [게임 실행] ------------

open_canvas(WINDOWXSIZE, WINDOWYSIZE) # 화면 열기

game_framework.run(mainmenu) # 메인메뉴 실행

close_canvas() # 화면 닫기

'''


# ------------- 이벤트 핸들러 -------------

def handle_events():

    global gamerunning # 실행중 여부
    global frame # 애니메이션 프레임
    global mousepressed # 마우스 클릭한 여부
    global keypressing # 키보드 입력중 여부
    global keypressedleft, keypressedright # 왼쪽, 오른쪽 키 입력 여부
    global keypressedspace, keypressedz, keypresseda # 스페이스바, z키, a키 입력여부
    global nowplace # 현재 메뉴 위치
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표

    events = get_events() # 이벤트 입력받기

    # 이벤트 종류에 따라
    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            gamerunning = False # 게임 실행중을 False로 한다

        # 키보드 눌렀을 때
        elif event.type == SDL_KEYDOWN:

            keypressing = 1 # 키 눌림

            if event.key == SDLK_SPACE:
                keypressedspace = 1 # 스페이스바 눌림

            elif event.key == SDLK_LEFT:
                keypressedleft = 1 # 왼쪽 키 눌림

            elif event.key == SDLK_RIGHT:
                keypressedright = 1 # 오른쪽 키 눌림

            # z키 눌렀을 때
            elif event.key == SDLK_z: # z키 눌림
                keypressedz = 1

            # a키 눌렀을 때
            # elif event.key == SDLK_q: # a키 눌림
            #    keypressedq = 1

            # esc키 눌렸을 때
            elif event.key == SDLK_ESCAPE:

                # 메인메뉴가 아닌 곳에서는 메인메뉴로 이동하며, 메인메뉴에서는 게임을 종료
                if nowplace != 'mainmenu':
                    nowplace = 'mainmenu'
                else:
                    gamerunning = False

        # 키보드 뗐을 때
        elif event.type == SDL_KEYUP:

            keypressing = 0

            if event.key == SDLK_SPACE:
                keypressedspace = 0

            elif event.key == SDLK_z:
                keypressedz = 0

            # elif event.key == SDLK_a:
                # keypresseda = 0


            if event.key == SDLK_LEFT:
                keypressedleft = 0

            elif event.key == SDLK_RIGHT:
                keypressedright = 0

        # 마우스 눌렀을 때
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # x, y 좌표 지정
            mouseclickedx, mouseclickedy = event.x, WINDOWXSIZE - 1 - event.y

        # 마우스 떼었을 때
        elif event.type == SDL_MOUSEBUTTONUP:
            mousepressed = 1
    pass

# ------------- 메인 코드 -------------


       



        
        
        # '그림 그리고 있지 않을시에만' 이동
        if nowdrawing == 0:

            # 현재 눌린 방향에 따라 동작 지정

            if keypressedleft == 1:
                if keypressedz == 0:
                    player.nowstate = LEFT  # 캐릭터 방향
                    player.movexy(-10, 0)  # 플레이어 이동

                elif keypressedz == 1:  # z키 눌렀을 경우
                    player.nowstate = LEFTDRAWING
                    player.frame = 0  # 프레임 지정
                    nowdrawing = 1  # 현재 그리고 있음

            elif keypressedright == 1:
                if keypressedz == 0:
                    player.nowstate = RIGHT  # 캐릭터 방향
                    player.movexy(+10, 0)  # 플레이어 이동

                elif keypressedz == 1:  # z키 눌렀을 경우
                    player.nowstate = RIGHTDRAWING
                    player.frame = 1 # 프레임 지정
                    nowdrawing = 1  # 현재 그리고 있음

            else:
                player.frame = 0

            # 스페이스바 눌렀을 경우 날기(점프)
            if keypressedspace == 1:
                # 위로 날기
                player.yspd = player.yjumpamount
                player.y += 0.2
                keypressedspace = 0

            # y 이동속도 하한 제한
            if player.yspd < -16:
                player.yspd = -16

            # 플레이어는 yspd만큼 y축 방향으로 이동한다
            player.yspd -= 0.9
            player.y += player.yspd

            if player.y < 150:
                player.y = 150
                player.yspd = 0

        # 그림 그리고 있을 경우 약간 그림 그리는 지연시간 뒤 풀림
        elif nowdrawing == 1:

            # 별 그리기 효과 표시

            draweffect.frame = (draweffect.frame + 1) % 5

            draweffect.frame = 0
            if player.nowstate == LEFTDRAWING:
                draweffect.draw(player.x - 15, player.y + 20)
            elif player.nowstate == RIGHTDRAWING:
                draweffect.draw(player.x + 15, player.y + 20)

            delay(0.1)  # 프레임간 지연
            player.yspd = 0
            nowdrawing = 0

        # 범위 내에 플레이어가 있게 하기 # 어째서인지 10px만큼 보정해줘야 한다

        if player.x < (0 + PLAYERXSIZE / 2 - 10):
            player.x = (0 + PLAYERXSIZE / 2 - 10)
        elif player.x > (680 - PLAYERXSIZE / 2 + 10):
            player.x = (680 - PLAYERXSIZE / 2 + 10)

        if player.y > (WINDOWYSIZE - PLAYERYSIZE - 10):
            player.y = (WINDOWYSIZE - PLAYERYSIZE - 10)
            player.yspd = -1

        # 키보드를 누르고 있지 않으며 그림 그리고 있지 않을 경우 정지동작으로 표시
        if keypressing == 0 and nowdrawing == 0:
            player.nowstate = STOP

        # 캔버스 다시 그리기
        update_canvas()
'''


