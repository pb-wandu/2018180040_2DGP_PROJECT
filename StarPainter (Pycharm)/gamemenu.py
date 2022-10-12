### [별그림자 이야기] 게임 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *    # pico2d 라이브러리 import
import game_framework   # 게임 프레임워크 임포트
import mainmenu         # 메인 메뉴 전환시 호출

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = -999        # 아직 정해지지 않은 것
DELAYTIME = 0.01    # 지연 시간

# ------------ 변수들 ------------

imagebg = None # 배경 이미지
eunbi = None # 별그림자 은비(플레이어)
ground = None # 발판
jumpeffect = None # 점프 효과
draweffect = None # 그리기 효과

keypressing = 0  # 키보드 입력중 여부
mousepressed = 0 # 마우스 클릭한 여부

keypressedleft = 0  # 왼쪽 키 입력된 여부
keypressedright = 0  # 오른쪽 키 입력된 여부
keypressedup = 0  # 위쪽 키 입력된 여부
keypresseddown = 0  # 아래쪽 키 입력된 여부

keypressedspace = 0 # 스페이스바 입력여부
keypressedz = 0 # z키 입력여부
keypresseda = 0 # a키 입력여부

mouseclickedx, mouseclickedy = UNSET, UNSET # 마우스 클릭한 x좌표, y좌표

# ------------ 플레이어 동작 관련 ------------

# 별그림자 은비 == 플레이어블 캐릭터 이름
PLAYERXSIZE, PLAYERYSIZE = 40, 30  # 별그림자 은비 크기
PLAYERXSTART, PLAYERYSTART = 340, 150  # 별그림자 은비 시작좌표

# 플레이어 동작들 (멈춤, 왼쪽, 오른쪽, 왼쪽 그리기, 오른쪽 그리기)
STOP, LEFT, RIGHT, LEFTDRAWING, RIGHTDRAWING = 0, 1, 2, -3, 3

nowdrawing = 0  # 현재 그림 그리고 있는지 여부

# ------------- 오브젝트 객체들 -------------

# 플레이어 오브젝트
class Player:

    # 초기화
    def __init__(self):
        self.image = load_image('characterimages.png')  # 캐릭터 이미지 (작업중)

        self.x, self.y = PLAYERXSTART, PLAYERYSTART  # 플레이어 좌표
        self.yspd = 0  # y축 이동속도
        self.frame = 0  # 애니메이션 프레임
        self.nowstate = STOP  # 현재 플레이어 상태

        # [별그림자 회랑]에서 강화할 수 있는 것
        self.LPamount = 100  # 체력
        self.EPamount = 100  # 기력
        self.yjumpamount = 11  # 날기(점프)시 이동하는 정도
        # self.cooltime_quickmove = UNSET # 도약 쿨타임
        # self.cooltime_warp = UNSET # 순간이동 쿨타임

    # x, y 각각 좌표만큼 이동
    def movexy(self, x, y):
        self.x += x
        self.y += y

    # 정보 갱신
    def update(self):
        self.frame = (self.frame + 1) % 8

    # 그리기
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, abs(self.nowstate) * 50, 33, 43, self.x, self.y + 20)

    pass


# 발판 오브젝트
class Ground:

    def __init__(self):
        self.image = load_image('groundtmp.png')  # 발판 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y)  # 발판 이미지 그리기

    pass


# 점프 효과 오브젝트
class Jumpeffect:

    def __init__(self):
        self.image = load_image('jumpeffect.png')  # 날기(점프) 효과 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y)  # 날기(점프) 효과 이미지 그리기

    pass


# 별 그리기 효과 오브젝트
class Draweffect:

    def __init__(self):
        self.image = load_image('starlight.png')  # 날기(점프) 효과 이미지 (임시)
        self.frame = 0

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 30, 0, 20, 20, x, y)

    pass

# ------------ 메뉴 함수들 ------------

# 메뉴 진입
def enter():
    global imagebg
    global eunbi
    global ground
    global jumpeffect
    global draweffect

    imagebg = load_image('gamemenuimg.png')  # 배경 이미지

    # 오브젝트 생성 및 초기화

    eunbi = Player()  # 별그림자 은비 (플레이어 오브젝트)
    eunbi.__init__()
    ground = Ground()  # 발판 오브젝트
    ground.__init__()
    jumpeffect = Jumpeffect()  # 점프 효과 오브젝트
    jumpeffect.__init__()
    draweffect = Draweffect()  # 그리기 효과 오브젝트
    draweffect.__init__()

    pass


# 메뉴 종료
def exit():
    global imagebg
    global eunbi
    global ground
    global jumpeffect
    global draweffect

    del imagebg
    del eunbi
    del ground
    del jumpeffect
    del draweffect
    pass

# 화면 그리기
def draw():
    clear_canvas() # 화면 초기화

    imagebg.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 배경 이미지 그리기
    ground.draw(340, 140)  # 땅 그리기
    eunbi.draw()  # 은비 (플레이어) 그리기

    # 점프중일 경우 점프 이펙트 그리기
    if eunbi.yspd > 0:
        jumpeffect.draw(eunbi.x, eunbi.y - 5)

    # 그리는 중인 경우별 그리기 효과 표시
    if nowdrawing == 1:
        draweffect.frame = (draweffect.frame + 1) % 5
        draweffect.frame = 0

        if eunbi.nowstate == LEFTDRAWING:
            draweffect.draw(eunbi.x - 15, eunbi.y + 20)
        elif eunbi.nowstate == RIGHTDRAWING:
            draweffect.draw(eunbi.x + 15, eunbi.y + 20)

    update_canvas()

# 정보 갱신
def update():

    global mousepressed # 마우스 클릭한 여부
    global keypressing # 키보드 입력중 여부
    global keypressedleft, keypressedright # 왼쪽, 오른쪽 키 입력 여부
    global keypressedspace, keypressedz, keypresseda # 스페이스바, z키, a키 입력여부
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표
    global nowdrawing # 현재 그림 그리고 있는지 여부

    # 플레이어 애니메이션
    if eunbi.nowstate == STOP:  # 멈춰 있을 경우
        eunbi.frame = 0  # 프레임 표시
    elif eunbi.nowstate == LEFTDRAWING:  # 왼쪽 그리기중
        eunbi.frame = 0  # 프레임 표시
    elif eunbi.nowstate == RIGHTDRAWING:  # 오른쪽 그리기중
        eunbi.frame = 1  # 프레임 표시
    else:
        eunbi.frame = (eunbi.frame + 1) % 2  # 프레임 표시
    delay(0.045)  # 프레임간 지연

    # '그림 그리고 있지 않을시에만' 이동
    if nowdrawing == 0:

        # 현재 눌린 방향에 따라 동작 지정

        if keypressedleft == 1:
            if keypressedz == 0:
                eunbi.nowstate = LEFT  # 캐릭터 방향
                eunbi.movexy(-10, 0)  # 플레이어 이동

            elif keypressedz == 1:  # z키 눌렀을 경우
                eunbi.nowstate = LEFTDRAWING
                eunbi.frame = 0  # 프레임 지정
                nowdrawing = 1  # 현재 그리고 있음

        elif keypressedright == 1:
            if keypressedz == 0:
                eunbi.nowstate = RIGHT  # 캐릭터 방향
                eunbi.movexy(+10, 0)  # 플레이어 이동

            elif keypressedz == 1:  # z키 눌렀을 경우
                eunbi.nowstate = RIGHTDRAWING
                eunbi.frame = 1  # 프레임 지정
                nowdrawing = 1  # 현재 그리고 있음

        else:
            eunbi.frame = 0

        # 스페이스바 눌렀을 경우 날기(점프)
        if keypressedspace == 1:
            # 위로 날기
            eunbi.yspd = eunbi.yjumpamount
            eunbi.y += 0.2
            keypressedspace = 0

        # y 이동속도 하한 제한
        if eunbi.yspd < -16:
            eunbi.yspd = -16

        # 플레이어는 yspd만큼 y축 방향으로 이동한다
        eunbi.yspd -= 0.9
        eunbi.y += eunbi.yspd

        if eunbi.y < 150:
            eunbi.y = 150
            eunbi.yspd = 0

    # 그림 그리고 있을 경우 약간 그림 그리는 지연시간 뒤 풀림
    elif nowdrawing == 1:

        # 별 그리기 효과 표시

        draweffect.frame = (draweffect.frame + 1) % 5

        draweffect.frame = 0

        delay(0.1)  # 프레임간 지연
        eunbi.yspd = 0
        nowdrawing = 0

    # 범위 내에 플레이어가 있게 하기 # 어째서인지 10px만큼 보정해줘야 한다

    if eunbi.x < (0 + PLAYERXSIZE / 2 - 10):
        eunbi.x = (0 + PLAYERXSIZE / 2 - 10)
    elif eunbi.x > (680 - PLAYERXSIZE / 2 + 10):
        eunbi.x = (680 - PLAYERXSIZE / 2 + 10)

    if eunbi.y > (WINDOWYSIZE - PLAYERYSIZE - 10):
        eunbi.y = (WINDOWYSIZE - PLAYERYSIZE - 10)
        eunbi.yspd = -1

    # 키보드를 누르고 있지 않으며 그림 그리고 있지 않을 경우 정지동작으로 표시
    if keypressing == 0 and nowdrawing == 0:
        eunbi.nowstate = STOP

    # 캔버스 다시 그리기
    update_canvas()

# 이벤트 핸들러
def handle_events():
    events = get_events()

    global mousepressed # 마우스 클릭한 여부
    global keypressing # 키보드 입력중 여부
    global keypressedleft, keypressedright # 왼쪽, 오른쪽 키 입력 여부
    global keypressedspace, keypressedz, keypresseda # 스페이스바, z키, a키 입력여부
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # 키보드 눌렀을 때
        elif event.type == SDL_KEYDOWN:

            keypressing = 1  # 키 눌림

            if event.key == SDLK_SPACE:
                keypressedspace = 1  # 스페이스바 눌림

            elif event.key == SDLK_LEFT:
                keypressedleft = 1  # 왼쪽 키 눌림

            elif event.key == SDLK_RIGHT:
                keypressedright = 1  # 오른쪽 키 눌림

            # z키 눌렀을 때
            elif event.key == SDLK_z:  # z키 눌림
                keypressedz = 1

            # a키 눌렀을 때
            # elif event.key == SDLK_q: # a키 눌림
            #    keypressedq = 1

            # esc키를 누를 경우 메인 메뉴로 이동
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(mainmenu)
                delay(DELAYTIME)

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