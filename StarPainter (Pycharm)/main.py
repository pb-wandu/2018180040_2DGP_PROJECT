from pico2d import *

WINDOWXSIZE = 1000
WINDOWYSIZE = 700

open_canvas(WINDOWXSIZE, WINDOWYSIZE) # 화면 실행

gamerunning = True # 게임 실행중 여부

# 이미지 가져오기
img_bg = load_image('bgtmp.png') # 배경 (임시)
img_ground = load_image('groundtmp.png') # 발판 (임시)
img_player = load_image('characterimages.png') # 캐릭터 (임시)
img_jumpeffect = load_image('jumpeffect.png') # 날기(점프) 효과 (임시)
img_startmenu = load_image('startmenuimg.png') # 시작 메뉴 (임시)

UNSET = -999 # 아직 정해지지 않은 것

# 플레이어 크기
PLAYERXSIZE = 80
PLAYERYSIZE = 60

# 플레이어 좌표는 아래 가운데 기준으로 지정

PLAYERXSTART = 340
PLAYERYSTART = 150

playerx = UNSET # 플레이어 x위치 (가운데 기준)
playery = UNSET + PLAYERYSIZE / 2 # 플레이어 y위치 (아래 기준)

keypressing = 0  # 키보드 입력중 여부

keypressedleft = 0  # 왼쪽 키 입력된 여부
keypressedright = 0  # 오른쪽 키 입력된 여부
# keypressedup = 0  # 위쪽 키 입력된 여부
# keypresseddown = 0  # 아래쪽 키 입력된 여부

keypressedz = 0 # z키 입력여부


STOP = 0 # x 이동방향 (멈춤)
LEFT = 1 # x 이동방향 (이동중)
RIGHT = 2 # x 이동방향 (이동중)

nowplace = 'mainmenu' # 현재 있는 위치
nowstageplaying = False # 현재 스테이지 진행중 여부

playerdirx = STOP

frame = 0

playeryspd = 0 # 플레이어 y속도

def handle_events():

    ### global을 빼면 함수 내의 지역변수로 선언된다

    global gamerunning # 실행중 여부
    global playerx, playery # 플레이어 좌표

    global playerdirx # 현재 x 이동방향

    global frame # 애니메이션 프레임

    global keypressing # 키보드 입력중 여부

    global keypressedleft # 키 입력 여부
    global keypressedright  # 키 입력 여부

    global keypressedz # z키 입력여부

    global nowplace # 현재 위치

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            gamerunning = False

        # 키보드 눌렀을 때
        elif event.type == SDL_KEYDOWN:

            keypressing = 1

            if event.key == SDLK_SPACE and nowplace == 'mainmenu':
                nowplace = 'gamemenu'

            if event.key == SDLK_LEFT:
                keypressedleft = 1

            elif event.key == SDLK_RIGHT:
                keypressedright = 1

            # z키 눌렀을 때
            elif event.key == SDLK_z:
                keypressedz = 1

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

            if event.key == SDLK_z:
                keypressedz = 0

            if event.key == SDLK_LEFT:
                keypressedleft = 0

            elif event.key == SDLK_RIGHT:
                keypressedright = 0
    pass

# ------------- 메인 코드 -------------

playerx = PLAYERXSTART  # 플레이어 x위치 (가운데 기준)
playery = PLAYERYSTART + PLAYERYSIZE / 2  # 플레이어 y위치 (아래 기준)

while gamerunning: # 실행중일 경우

    clear_canvas() # 화면 초기화

    handle_events()  # 이벤트 핸들러

    # 현위치가 [시작 메뉴]일 경우

    if nowplace == 'mainmenu':

        img_startmenu.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 시작 메뉴 배경 그리기
        update_canvas()

    # 현위치가 [게임 메뉴]일 경우

    elif nowplace == 'gamemenu':

        img_bg.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 게임 메뉴 배경 그리기

        img_ground.draw(340, 140)  # 땅 그리기

        # 플레이어 그리기 (3픽셀은 임시 보정)
        img_player.clip_draw(frame * 80, playerdirx * 100, 63, 83, playerx, playery)

        # 점프중일 경우 점프 이펙트 그리기
        if playeryspd > 0:
            img_jumpeffect.draw(playerx, playery - 50)

        update_canvas()

        frame = (frame + 1) % 2  # 프레임 표시
        delay(0.045)  # 프레임간 지연

        # 현재 눌린 방향에 따라 이동 및 방향 지정

        if keypressedleft == 1:
            playerdirx = LEFT  # 캐릭터 방향
            playerx -= 10
        elif keypressedright == 1:
            playerdirx = RIGHT  # 캐릭터 방향
            playerx += 10
        else:
            frame = 0

        if keypressedz == 1:  # z키 입력시
            # 위로 날기
            playery += 0.0 # 땅에 닿아있다고 점프가 안 되는 걸 막기 위한 보정
            playeryspd = 12
            keypressedz = 0

        # y 이동속도 하한 제한
        if playeryspd < -16:
            playeryspd = -16

        # 플레이어는 yspd만큼 y축 방향으로 이동한다

        if playery < 180:
            playery = 180
            playeryspd = 0
        else:
            playery += playeryspd
            playeryspd -= 0.9

        # 범위 내에 플레이어가 있게 하기 # 어째서인지 10px만큼 보정해줘야 한다

        if playerx < (0 + PLAYERXSIZE / 2 - 10):
            playerx = (0 + PLAYERXSIZE / 2 - 10)
        elif playerx > (680 - PLAYERXSIZE / 2 + 10):
            playerx = (680 - PLAYERXSIZE / 2 + 10)

        if playery > (WINDOWYSIZE - PLAYERYSIZE / 2 - 10):
            playery = (WINDOWYSIZE - PLAYERYSIZE / 2 - 10)
            playeryspd = -1

        # 키보드를 누르고 있지 않을 경우 정지동작으로 표시
        if keypressing == 0:

            if playerdirx == LEFT:
                playerdirx = STOP
            elif playerdirx == RIGHT:
                playerdirx = STOP

close_canvas()
