from pico2d import *

XSIZE = 1000
YSIZE = 700

open_canvas(XSIZE, YSIZE) # 화면 실행

gamerunning = True # 게임 실행중 여부

resource_bg = load_image('bgtmp.png') # 배경
ground = load_image('groundtmp.png') # 발판
resource_player = load_image('character.png') # 캐릭터

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

LEFT = 0 # x 이동방향 (이동중)
RIGHT = 1 # x 이동방향 (이동중)
LEFTSTOP = 2 # x 이동방향 (멈춤)
RIGHTSTOP = 3 # x 이동방향 (멈춤)

nowstageplaying = False # 현재 스테이지 진행중 여부

# 이벤트 핸들러
def handle_events():

    global gamerunning # 게임 실행중 여부
    global playerx, playery # 플레이어 좌표
    global keypressing  # 키보드 입력중 여부
    global nowstageplaying # 현재 스테이지 진행중 여부

    global keypressedleft # 키 입력된 여부
    global keypressedright  # 키 입력된 여부
    # global keypressedup  # 키 입력된 여부
    # global keypresseddown  # 키 입력된 여부

    # global characterdirx # 현재 x 이동방향
    # global characterdiry # 현재 y 이동방향
    # global frame # 애니메이션 프레임

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            gamerunning = False

        # 키보드 눌렀을 때
        elif event.type == SDL_KEYDOWN:

            keypressing = 1

            if event.key == SDLK_LEFT:
                keypressedleft = 1

            elif event.key == SDLK_RIGHT:
                keypressedright = 1

            # elif event.key == SDLK_UP:
            #      keypressedup = 1

            # elif event.key == SDLK_DOWN:
            #     keypresseddown = 1

            # esc키 눌러 게임 종료
            elif event.key == SDLK_ESCAPE:
                gamerunning = False

            # enter키 눌러 스테이지 시작
            elif event.key == SDLK_SPACE:
                # 스테이지 실행중이 아닌 경우
                if not nowstageplaying:
                    nowstageplaying = True

        # 키보드 뗐을 때
        elif event.type == SDL_KEYUP:

            keypressing = 0

            if event.key == SDLK_LEFT:
                keypressedleft = 0

            elif event.key == SDLK_RIGHT:
                keypressedright = 0

            # elif event.key == SDLK_UP:
            #    keypressedup = 0

            # elif event.key == SDLK_DOWN:
            #    keypresseddown = 0
    pass

# ------------- 메인 코드 -------------

playerx = PLAYERXSTART  # 플레이어 x위치 (가운데 기준)
playery = PLAYERYSTART + PLAYERYSIZE / 2  # 플레이어 y위치 (아래 기준)

while gamerunning: # 게임 실행중일 경우

    handle_events() # 이벤트 핸들러 삽입

    clear_canvas() # 화면 지우기

    resource_bg.draw(XSIZE/2, YSIZE/2)

    ground.draw(340, 140)

    # nowstageplaying = True

    # 스테이지가 진행중일 경우
    if nowstageplaying:

        resource_player.draw(playerx, playery)  # 플레이어 표시

        # 현재 눌린 방향에 따라 이동 및 방향 지정
        if keypressedleft == 1:
            characterdirx = LEFT  # 캐릭터 방향
            playerx -= 2
        elif keypressedright == 1:
            characterdirx = RIGHT  # 캐릭터 방향
            playerx += 2

        # 범위 내에 플레이어가 있게 하기 # 어째서인지 10px만큼 보정해줘야 한다
        if playerx < (0 + PLAYERXSIZE / 2 - 10):
            playerx = (0 + PLAYERXSIZE / 2 - 10)
        elif playerx > (680 - PLAYERXSIZE / 2 + 10):
            playerx = (680 - PLAYERXSIZE / 2 + 10)

    update_canvas() # 화면 그리기

# 종료시 화면 닫기
close_canvas()

'''
resource_ground = load_image('ground.png')
character = load_image('animation_sheet.png')



playerx = 400 # 플레이어 x좌표 위치
playery = 90 # 플레이어 y좌표 위치

frame = 0 # 애니메이션 프레임

LEFT = 0 # x 이동방향
RIGHT = 1 # x 이동방향
LEFTSTOP = 2 # x 이동방향
RIGHTSTOP = 3 # x 이동방향

YSTOP = 0 # y 이동방향
UP = 1 # y 이동방향
DOWN = 2 # y 이동방향


characterdirx = RIGHTSTOP # 현재 x 이동방향
characterdiry = YSTOP # 현재 y 이동방향




while running: # 실행중일 경우



    # 플레이어 그리기
    # character.clip_draw(frame * 100, characterdirx * 100, 100, 100, playerx, playery)

    frame = (frame + 1) % 8 # 프레임 표시
    delay(0.035) # 프레임간 지연

    # 현재 눌린 방향에 따라 이동 및 방향 지정
    if keypressedleft == 1:
        characterdirx = LEFT  # 캐릭터 방향
        playerx -= 10
    elif keypressedright == 1:
        characterdirx = RIGHT  # 캐릭터 방향
        playerx += 10
    if keypressedup == 1:
        characterdiry = UP  # 캐릭터 방향
        playery += 10
    elif keypresseddown == 1:
        characterdiry = DOWN  # 캐릭터 방향
        playery -= 10

    # 플레이어 위치 넘어가지 않게 하기
    if playerx < 25:
        playerx = 25
    elif playerx > XSIZE - 25:
        playerx = XSIZE - 25
    if playery < 25:
        playery = 25
    elif playery > YSIZE - 25:
        playery = YSIZE - 25

    # 키보드를 누르고 있지 않을 경우 정지동작으로 표시
    if keypressing == 0:

        # 현재 0프레임일 경우 플레이어 이동동작 -> 정지동작
        if frame == 0:
            if characterdirx == LEFT:
                characterdirx = LEFTSTOP
            elif characterdirx == RIGHT:
                characterdirx = RIGHTSTOP

        # Y축 이동중 -> 정지 상태
        if characterdiry == UP or characterdiry == DOWN:
            characterdiry = YSTOP


'''
