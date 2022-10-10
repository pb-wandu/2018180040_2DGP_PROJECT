import random # 랜덤 기능 사용

from pico2d import *

WINDOWXSIZE = 1000 # 화면 x 크기
WINDOWYSIZE = 700 # 화면 y 크기

open_canvas(WINDOWXSIZE, WINDOWYSIZE) # 화면 실행

gamerunning = True # 게임 실행중 여부

UNSET = -999 # 아직 정해지지 않은 것

# 플레이어 크기
PLAYERXSIZE = 40
PLAYERYSIZE = 30

# 플레이어 좌표는 아래 가운데 기준으로 지정

PLAYERXSTART, PLAYERYSTART = 340, 150 # 플레이어 시작좌표

playerx = UNSET # 플레이어 x위치 (가운데 기준)
playery = UNSET + PLAYERYSIZE / 2 # 플레이어 y위치 (아래 기준)

keypressing = 0  # 키보드 입력중 여부
mousepressed = 0 # 마우스 클릭한 여부

keypressedleft = 0  # 왼쪽 키 입력된 여부
keypressedright = 0  # 오른쪽 키 입력된 여부
# keypressedup = 0  # 위쪽 키 입력된 여부
# keypresseddown = 0  # 아래쪽 키 입력된 여부

playeryspd = 0 # 플레이어 y속도

keypressedspace = 0 # 스페이스바 입력여부
keypressedz = 0 # z키 입력여부
keypresseda = 0 # a키 입력여부

mouseclickedx, mouseclickedy = UNSET, UNSET # 마우스 클릭한 x좌표, y좌표

STOP, LEFT, RIGHT = 0, 1, 2 # x방향 이동방향 (멈춤, 왼쪽, 오른쪽)

nowplace = 'mainmenu' # 현재 있는 위치
nowstageplaying = False # 현재 스테이지 진행중 여부

nowplayerframe = 0 # 플레이어 애니메이션 프레임

# ------------- 오브젝트 객체들 -------------

# 발판 오브젝트
class Ground:

    def __init__(self):
        self.image = load_image('groundtmp.png') # 발판 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y) # 발판 이미지 그리기

    pass

# 플레이어 오브젝트
class Player:

    # 초기화
    def __init__(self):
        self.image = load_image('characterimages.png') # 캐릭터 이미지 (작업중)

        self.x, self.y = PLAYERXSTART, PLAYERYSTART # 플레이어 좌표
        self.yspd = 0 # y축 이동속도
        self.frame = 0 # 애니메이션 프레임
        self.dirx = STOP  # 현재 x방향 이동방향

        # [별그림자 회랑]에서 강화할 수 있는 것
        self.LPamount = 100 # 체력
        self.EPamount = 100 # 기력
        self.yjumpamount = 11 # 날기(점프)시 이동하는 정도
        # self.cooltime_quickmove = UNSET # 도약 쿨타임
        # self.cooltime_warp = UNSET # 순간이동 쿨타임

    # x, y 각각 좌표만큼 이동
    def movexy(self, x, y):
        self.x += x
        self.y += y

    # 프레임 지정
    def setframe(self, f):
        self.frame = f

    # 정보 갱신
    def update(self):
        self.frame = (self.frame + 1) % 8

    # 그리기
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, self.dirx * 50, 33, 43, self.x, self.y + 20)

    pass

# 점프 효과 오브젝트
class Jumpeffect:

    def __init__(self):
        self.image = load_image('jumpeffect.png') # 날기(점프) 효과 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y) # 날기(점프) 효과 이미지 그리기

    pass

# 시작화면 오브젝트
class Startmenu:

    def __init__(self):
        self.image = load_image('startmenuimg.png') # 시작 메뉴 이미지 (임시)

    def draw(self):
        self.image.draw(WINDOWXSIZE/2, WINDOWYSIZE/2) # 시작 메뉴 이미지 그리기

    pass

# 게임화면 오브젝트
class Gamemenu:

    def __init__(self):
        self.image = load_image('bgtmp.png') # 배경 이미지 (임시)

    def draw(self):
        self.image.draw(WINDOWXSIZE/2, WINDOWYSIZE/2) # 배경 이미지 그리기

    pass

# 오브젝트 생성 및 초기화

ground = Ground() # 발판 오브젝트
ground.__init__()
player = Player() # 플레이어 오브젝트
player.__init__()
jumpeffect = Jumpeffect() # 점프 효과 오브젝트
jumpeffect.__init__()
startmenu = Startmenu() # 시작 메뉴 오브젝트
startmenu.__init__()
gamemenu = Gamemenu() # 게임 메뉴 오브젝트
gamemenu.__init__()

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
            # elif event.key == SDLK_z: # z키 눌림

            # a키 눌렀을 때
            # elif event.key == SDLK_q: # a키 눌림

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

            # elif event.key == SDLK_z:
                # keypressedz = 0

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

while gamerunning: # 실행중일 경우

    clear_canvas() # 화면 초기화

    handle_events()  # 이벤트 핸들러

    # 현위치가 [시작 메뉴]일 경우

    if nowplace == 'mainmenu':

        startmenu.draw()  # 시작 메뉴 배경 그리기

        update_canvas()

        # 마우스 클릭시 - 게임 메뉴로 이동 (임시)
        if mousepressed == 1:
            nowplace = 'gamemenu'
            mousepressed = 0

    # 현위치가 [게임 메뉴]일 경우

    elif nowplace == 'gamemenu':

        gamemenu.draw()  # 게임 메뉴 배경 그리기
        ground.draw(340, 140)  # 땅 그리기

        player.draw() # 플레이어 그리기

        if player.dirx == STOP:
            nowplayerframe = (nowplayerframe + 1) % 2  # 프레임 표시
        else:
            nowplayerframe = (nowplayerframe + 1) % 2  # 프레임 표시
        player.setframe(nowplayerframe) # 플레이어에게 현재 프레임 전달
        delay(0.045)  # 프레임간 지연

        # 점프중일 경우 점프 이펙트 그리기
        if player.yspd > 0:
            jumpeffect.draw(player.x, player.y - 5)

        update_canvas()

        # 현재 눌린 방향에 따라 이동 및 방향 지정

        if keypressedleft == 1:
            player.dirx = LEFT  # 캐릭터 방향
            player.movexy(-10, 0) # 플레이어 이동
        elif keypressedright == 1:
            player.dirx = RIGHT  # 캐릭터 방향
            player.movexy(+10, 0) # 플레이어 이동
        else:
            frame = 0

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

        # 범위 내에 플레이어가 있게 하기 # 어째서인지 10px만큼 보정해줘야 한다

        if player.x < (0 + PLAYERXSIZE / 2 - 10):
            player.x = (0 + PLAYERXSIZE / 2 - 10)
        elif player.x > (680 - PLAYERXSIZE / 2 + 10):
            player.x = (680 - PLAYERXSIZE / 2 + 10)

        if player.y > (WINDOWYSIZE - PLAYERYSIZE - 10):
            player.y = (WINDOWYSIZE - PLAYERYSIZE - 10)
            player.yspd = -1

        # 키보드를 누르고 있지 않을 경우 정지동작으로 표시
        if keypressing == 0:

            if player.dirx == LEFT:
                player.dirx = STOP
            elif player.dirx == RIGHT:
                player.dirx = STOP

close_canvas()
