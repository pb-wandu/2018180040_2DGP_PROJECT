### [별그림자 이야기] 게임 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트
import gameobjects        # 게임 오브젝트 임포트
import object_player      # 플레이어 오브젝트 임포트

import frame_main         # 메인 메뉴 전환시 호출
import frame_upgrade      # 별그림자 회랑 (강화) 메뉴 전환시 호출
import frame_pause        # 대기 전환시 호출

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = 999         # 아직 정해지지 않은 것
DELAYTIME = 0.005   # 지연 시간

# ------------ 변수들 ------------

imagebg, imagestagebg, eunbi, ground = None, None, None, None # 배경 이미지, 스테이지 배경, 별그림자 은비(플레이어), 발판
drawnowstage = None # 스테이지 표시
pauseimage = None # 일시정지 이미지
skill1image, skill2image, skill3image = None, None, None # 기술 사용 가능여부 이미지
quickmove = None # 도약 효과 이미지

lifeenergybar, lifeimage, energyimage = None, None, None # 바탕, 체력, 기력 이미지

jumpeffect = None # 점프 효과 오브젝트
wingimage = None  # 날개 오브젝트
quickmove = None  # 동작 효과 표시
draweffect = None  # 그리기 효과 오브젝트

keypressing = 0  # 키보드 입력중 여부
mousepressed = 0 # 마우스 클릭한 여부



# 키 각각 입력 여부
keypressedleft, keypressedright, keypressedup, keypresseddown = 0, 0, 0, 0
keypressedz, keypresseda = 0, 0

mouseclickedx, mouseclickedy = UNSET, UNSET # 마우스 클릭한 x좌표, y좌표

playersavex, playersavey = UNSET, UNSET # 플레이어 좌표 저장

# 난이도 설정 (// 추후 난이도에 따라 세부사항 적용 예정)

EASY, NORMAL, HARD = 11, 12, 13

diff_starpainter = EASY # 현재 별그림자 난이도
diff_planet = EASY # 현재 행성 난이도

# ------------ 플레이어 동작 관련 ------------

# 플레이어 동작들 (멈춤, 왼쪽, 오른쪽, 왼쪽 그리기, 오른쪽 그리기)
STOP, LEFT, RIGHT, LEFTDRAWING, RIGHTDRAWING = 0, 1, 2, -3, 3

nowdrawing = 0  # 현재 그림 그리고 있는지 여부

# 도약 판정 변수 (별그림자 회랑 강화 x)
ifnowclickr = 0 # 지금 오른쪽 눌렀는가 변수
ifnowclickl = 0 # 지금 왼쪽 눌렀는가 변수
nowdashtime = 0 # 0이 되기 전에 같은 키를 다시 누르면 도약을 수행
skillxcooltime = 0  # 도약 대기시간
nowdashl, nowdashr = 0, 0  # 해당 방향으로 도약 여부

# 도약 판정 변수 (별그림자 회랑 강화 o)
dashtime = 10 # 이 시간 안에 같은 키를 다시 누르면 도약을 수행
nowskillxcooltime = 60 # 현재 도약 대기시간
dashamount = 50 # 도약 크기

# ------------ 스테이지 관련 변수, 관리 함수 ------------

nowgamestage = 11 # 현재 스테이지
nowcollectedstar = 0 # 현재 모은 별 (이 해당 스테이지의 요구 별 개수와 같다면 스테이지 클리어

WORLDNUM = 6 # 차원 개수
PLACENUM = 5 # 각 차원당 장소 개수

STARSIZE = 30 # 별 크기

# 각 차원-지역 (스테이지)당 필요한 별 개수 (== 그려야 하는 목표지점)
needtocollectstar = \
    [[2, 4, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET]]

starplaces = [] # 별을 저장할 배열

# 별의 좌표 범위는 [10~670, 200~690]으로 지정합니다
starplacesset = [ # 별을 표시할 위치
    [ [100, 500], [500, 240], [UNSET, UNSET], [UNSET, UNSET] ], # 1-1
    [ [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ] # 1-2
]

# 스테이지 확인

stardrawed = [False, False, False, False, False, False, False, False, False, False] # 해당 위치에 별이 그려졌는지 확인



nowlifelength = 0  # 전체 제력 대비 현재 체력
nowenergylength = 0  # 전체 기력 대비 현재 기력
lifeimageadjust = 0 # 왼쪽으로 정렬 이동값
energyimageadjust = 0 # 왼쪽으로 정렬 이동값



def stagecheck(stage, arr):
    global nowcollectedstar # 현재 모은 별
    global starplaces # 별을 저장할 배열

    global nowdrawing  # 현재 그림 그리고 있는지 여부

    global ifstagedrawed  # 스테이지 그려짐 여부

    global nowlifelength, nowenergylength, lifeimageadjust, energyimageadjust

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소
    nowstageneedstar = arr[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별
    starplaces = [gameobjects.Star() for i in range(nowstageneedstar)]  # 별들을 저장할 위치

    # 체력, 기력 정보 관리

    nowlifelength = 120 * eunbi.lifenow / eunbi.lifemax # 전체 제력 대비 현재 체력
    nowenergylength = 120 * eunbi.energynow / eunbi.energymax # 전체 기력 대비 현재 기력
    lifeimageadjust = (120 - nowlifelength) / 2 # 왼쪽으로 정렬 이동값
    energyimageadjust = (120 - nowenergylength) / 2 # 왼쪽으로 정렬 이동값

    # starplacesset에서 현재 스테이지 좌표가 있는 위치
    starplacessetplace = (worldnow - 1) * PLACENUM + (placenow - 1)

    for i in range(nowstageneedstar):

        x = starplacesset[starplacessetplace][i][0]
        y = starplacesset[starplacessetplace][i][1]

        # 충돌 판정

        drawx, drawy = UNSET, UNSET

        if eunbi.nowstate == LEFTDRAWING:
            drawx, drawy = eunbi.x - 15, eunbi.y + 17
        elif eunbi.nowstate == RIGHTDRAWING:
            drawx, drawy = eunbi.x + 15, eunbi.y + 17

        # 만약 별이 그려지지 않은 경우
        if not stardrawed[i] and nowdrawing == 1:
            # 별을 그리는 좌표가 목표 지점의 안에 있을 때 (15px 별 범위 보정 적용)
            if x - (STARSIZE / 2 - 15) <= drawx <= (x + STARSIZE / 2 + 15)\
                    and (y - STARSIZE / 2 - 15) <= drawy <= (y + STARSIZE / 2 + 15):
                stardrawed[i] = True
                starplaces[i].ifdraw = True  # 별을 그렸음
                nowdrawing = 0
                nowcollectedstar += 1  # 별을 하나 그림

    # 현재 모은 별 개수가 현재 차원에서 요구하는 별 개수와 같다면
    if nowcollectedstar == nowstageneedstar:
        # [별그림자 회랑] 강화 메뉴로 이동
        game_framework.change_state(frame_upgrade)

    pass


# 스테이지 그리기

ifstagedrawed = 0 # 스테이지 그려짐 여부

def stagedraw(stage, arr):
    global nowcollectedstar # 현재 모은 별
    global starplaces # 별을 저장할 배열

    global nowdrawing  # 현재 그림 그리고 있는지 여부
    global ifstagedrawed  # 스테이지 그려짐 여부

    global lifeenergybar, lifeimage, energyimage  # 바탕, 체력, 기력 이미지

    global nowlifelength, nowenergylength, lifeimageadjust, energyimageadjust

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소
    nowstageneedstar = arr[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별
    starplaces = [gameobjects.Star() for i in range(nowstageneedstar)]  # 별들을 저장할 위치

    # 체력, 기력 그리기

    lifeenergybar.draw(150, 82) # 체력 표시 자리
    lifeenergybar.draw(150, 38) # 기력 표시 자리

    lifeimage.draw(150 - lifeimageadjust, 82, int(nowlifelength))
    energyimage.draw(150 - energyimageadjust, 38, int(nowenergylength))

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소
    nowstageneedstar = arr[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별

    # starplacesset에서 현재 스테이지 좌표가 있는 위치
    starplacessetplace = (worldnow - 1) * PLACENUM + (placenow - 1)

    for i in range(nowstageneedstar):

        if stardrawed[i]:
            starplaces[i].ifdraw = True
        else:
            starplaces[i].ifdraw = False

        x = starplacesset[starplacessetplace][i][0]
        y = starplacesset[starplacessetplace][i][1]
        starplaces[i].draw(x, y)

    pass

# ----- 메뉴 진입 -----

def enter():
    global imagebg, imagestagebg
    global eunbi
    global ground
    global drawnowstage
    global pauseimage

    global jumpeffect, wingimage, quickmove, draweffect


    global skill1image, skill2image, skill3image
    global quickmove
    global ifstagedrawed

    global lifeenergybar, lifeimage, energyimage  # 바탕, 체력, 기력 이미지

    # 현위치 지정
    frame_main.nowplace = frame_main.PL_STAGE

    imagebg = load_image('gamemenuimg.png')  # 배경 이미지
    imagestagebg = load_image('stagebg.png')  # 스테이지 배경 이미지

    handle_events() # 이벤트 핸들러

    ifstagedrawed = 0  # 스테이지 그려짐 여부 초기화

    # 오브젝트 생성 및 초기화

    eunbi = object_player.Player()  # 별그림자 은비 (플레이어 오브젝트)
    eunbi.__init__()

    ground = gameobjects.Ground()  # 발판 오브젝트
    ground.__init__()
    drawnowstage = gameobjects.Drawnowstage()  # 스테이지 표시 오브젝트
    drawnowstage.__init__()

    jumpeffect = object_player.Jumpeffect()  # 점프 효과 오브젝트
    jumpeffect.__init__()
    wingimage = object_player.Wingimage()  # 날개 오브젝트
    wingimage.__init__()
    quickmove = object_player.Quickmove()  # 동작 효과 표시
    quickmove.__init__()
    draweffect = object_player.Draweffect()  # 그리기 효과 오브젝트
    draweffect.__init__()

    skill1image = gameobjects.Skill1image() # 동작 실행 가능여부 표시
    skill1image.__init__()
    skill2image = gameobjects.Skill2image()  # 동작 실행 가능여부 표시
    skill2image.__init__()
    skill3image = gameobjects.Skill3image()  # 동작 실행 가능여부 표시
    skill3image.__init__()

    lifeenergybar = gameobjects.Lifeenergybar() # 체력, 기력 바탕 이미지
    lifeenergybar.__init__()

    lifeimage = gameobjects.Lifeimage() # 체력 이미지
    lifeimage.__init__()

    energyimage = gameobjects.Energyimage() # 기력 이미지
    energyimage.__init__()

    pass


# ----- 메뉴 종료 -----

def exit():
    global imagebg, imagestagebg
    global eunbi
    global ground
    global drawnowstage
    global skill1image, skill2image, skill3image

    del imagebg, imagestagebg
    del eunbi
    del ground
    del drawnowstage
    del skill1image, skill2image, skill3image

    pass

# ----- 화면 그리기 -----

def draw():
    clear_canvas() # 화면 초기화

    imagebg.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 배경 이미지 그리기
    imagestagebg.draw(340, 410)  # 스테이지 배경 이미지 그리기
    ground.draw(340, 136)  # 땅 그리기

    drawnowstage.draw(nowgamestage)  # 스테이지 표시 그리기

    skill1image.draw(472, 56)  # 기술 1 그리기
    skill2image.draw(558, 56)  # 기술 2 그리기
    skill3image.draw(644, 56)  # 기술 3 그리기

    stagedraw(nowgamestage, needtocollectstar) # 스테이지 그리기
    eunbi.draw()  # 은비 (플레이어) 그리기

    update_canvas()

    pass

# ----- 정보 갱신 -----

def update():

    global mousepressed # 마우스 클릭한 여부
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표
    global skill1image, skill2image, skill3image # 기술 이미지



    global eunbi # 은비(플레이어)

    # --- 기술 메뉴 표시 ---

    if skillxcooltime == 0:
        skill1image.frame = 0  # 도약 실행 가능
    elif nowdashl == 2 or nowdashr == 2:
        skill1image.frame = 1  # 도약 실행중
    elif skillxcooltime > 0:
        skill1image.frame = 2  # 도약 대기시간중

    stagecheck(nowgamestage, needtocollectstar) # 스테이지 정보 확인

    # 현위치가 STAGE일 경우
    if frame_main.nowplace == frame_main.PL_STAGE:
        eunbi.update()

    # 캔버스 다시 그리기
    update_canvas()

    pass

# 이벤트 핸들러

def handle_events():
    events = get_events()

    global eunbi # 은비(플레이어)

    global mousepressed # 마우스 클릭한 여부
    global keypressing # 키보드 입력중 여부
    global keypressedleft, keypressedright # 왼쪽, 오른쪽 키 입력 여부
    global keypressedspace, keypressedz, keypresseda # 스페이스바, z키, a키 입력여부
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표

    global nowgamestage # 현재 스테이지

    global playersavex, playersavey # 플레이어 좌표 저장

    global ifnowclickl, ifnowclickr, nowdashtime, dashtime # 도약 판정 변수
    global skillxcooltime # 도약 대기시간 (쿨타임)
    global nowdashl, nowdashr # 해당 방향으로 도약 여부

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # F1키를 눌렀다 뗄 경우 중단
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F1):
            game_framework.push_state(frame_pause)  # 일시정지 메뉴 열기

        # F3 F4키는 테스트용으로, 각각 다음/이전 스테이지 이동키입니다
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F2):
            if nowgamestage > 11:  # 시작 스테이지가 아닐 경우
                if int(nowgamestage % 10) == 1:  # 현재 1지역일 경우
                    nowgamestage -= 10  # 이전 차원으로
                    nowgamestage += 4  # 5지역으로
                else:
                    nowgamestage -= 1  # 이전 지역으로

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F3):
            if nowgamestage < 65:  # 6번째 차원의 5지역에 도달하지 않았을 경우
                if int(nowgamestage % 10) == 5:  # 현재 5지역일 경우
                    nowgamestage += 10  # 다음 차원으로
                    nowgamestage -= 4  # 1지역으로
                else:
                    nowgamestage += 1  # 다음 지역으로

        # esc키를 누를 경우 메인 메뉴로 이동
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_ESCAPE):
            game_framework.change_state(frame_main)
            delay(DELAYTIME)

        # 그 외의 경우 은비(플레이어) 캐릭터 컨트롤러 실행
        else:
            eunbi.handle_event(event)

    pass

# 중단되었을 경우
def pause():
    global playersavex, playersavey

    # 은비 좌표 저장하기
    playersavex, playersavey = eunbi.x, eunbi.y

    pass

# 다시 실행된 경우
def resume():

    # 저장해둔 은비 좌표 불러오기
    eunbi.x, eunbi.y = playersavex, playersavey

    pass


    pass

# ------------ 직접 실행시켰을 경우 ------------

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()
