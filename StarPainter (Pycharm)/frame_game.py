### [별그림자 이야기] 게임 메뉴 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import
import gameobjects        # 게임 오브젝트 import
import object_player      # 플레이어 오브젝트 import

import frame_main         # 메인 메뉴 전환시 호출
import frame_upgrade      # 별그림자 회랑 (강화) 메뉴 전환시 호출
import frame_pause        # 대기 전환시 호출

import game_world         # 게임 월드 및 스테이지 관련 변수, 함수

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

jumpeffect, wingimage, quickmove, draweffect = None, None, None, None # 은비(플레이어) 관련 이미지

skill2usingimg = None # q (순간이동) 사용중 이미지

keypressing = 0  # 키보드 입력중 여부
mousepressed = 0 # 마우스 클릭한 여부

stagerestart = 0 # 스테이지 재시작 여부

nowcollectedstar, ifstagedrawed = 0, 0

# 키 각각 입력 여부
keypressedleft, keypressedright, keypressedup, keypresseddown = 0, 0, 0, 0
keypressedz, keypressedq, keypressedw = 0, 0, 0

mousex, mousey = UNSET, UNSET # 마우스 x좌표, y좌표
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

# 동작 잠그기, 잠금 해제
skillmovelocked = 0
skillqlocked = 0
skillwlocked = 0

# 도약 판정 변수
ifnowclickr = 0 # 지금 오른쪽 눌렀는가 변수
ifnowclickl = 0 # 지금 왼쪽 눌렀는가 변수
nowdashtime = 0 # 0이 되기 전에 같은 키를 다시 누르면 도약을 수행
nowdashl, nowdashr = 0, 0  # 해당 방향으로 도약 여부

nowskillmovecooltime = 0  # 도약 대기시간
nowskillqcooltime = 0  # 순간이동 대기시간

nowqstate = 0 # q (순간이동) 기술 사용중 여부

# 별그림자 회랑에서 강화 가능한 값들 (// 수시로 수정하며 확인합니다)

dashtime = 40 # 이 시간 안에 같은 키를 다시 누르면 도약을 수행
skillmovecooltime = 60 # 현재 도약 대기시간
dashamount = 50 # 도약 크기

skillqcooltime = 150  # 순간이동 대기시간

skillmoveneedenergy = 50 # 도약 사용시 기력 요구치
skillqneedenergypercent = 40 # 순간이동 사용시 기력 요구 퍼센트

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
        return 'cleared'

    pass


# 스테이지 그리기

ifstagedrawed = 0 # 스테이지 그려짐 여부

def stagedraw(stage, arr):
    global nowcollectedstar # 현재 모은 별
    global starplaces # 별을 저장할 배열

    global nowdrawing  # 현재 그림 그리고 있는지 여부
    global ifstagedrawed  # 스테이지 그려짐 여부

    global nowlifelength, nowenergylength, lifeimageadjust, energyimageadjust

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소
    nowstageneedstar = arr[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별
    starplaces = [gameobjects.Star() for i in range(nowstageneedstar)]  # 별들을 저장할 위치

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소
    nowstageneedstar = arr[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별

    # 글자 표시
    stagefont = load_font('WLR-1_Yeongyeon_v1_3.TTF', 16)
    stagetext = '현재 위치 : 차원 ' + str(worldnow) + ' - 구역 ' + str(placenow)

    stagefont.draw(5, frame_main.WINDOWYSIZE - 21, stagetext, (0, 0, 80))

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

    global skill1image, skill2image, skill3image

    global jumpeffect, wingimage, quickmove, draweffect

    global skill2usingimg

    # 현위치 지정
    frame_main.nowplace = frame_main.PL_STAGE

    handle_events() # 이벤트 핸들러

    # 오브젝트 생성 및 초기화

    imagebg = load_image('gamemenuimg.png')  # 배경 이미지
    imagestagebg = load_image('stagebg.png')  # 스테이지 배경 이미지

    skill2usingimg = load_image('skill2usingimg.png') # q (순간이동) 사용중 이미지

    ground = gameobjects.Ground()  # 발판 오브젝트
    drawnowstage = gameobjects.Drawnowstage()  # 스테이지 표시 오브젝트

    eunbi = object_player.Player()  # 별그림자 은비 (플레이어 오브젝트)

    jumpeffect = object_player.Jumpeffect()  # 점프 효과 오브젝트
    wingimage = object_player.Wingimage()  # 날개 오브젝트
    quickmove = object_player.Quickmove()  # 동작 효과 표시
    draweffect = object_player.Draweffect()  # 그리기 효과 오브젝트

    skill1image = gameobjects.Skill1image() # 동작 실행 가능여부 표시
    skill2image = gameobjects.Skill2image()  # 동작 실행 가능여부 표시
    skill3image = gameobjects.Skill3image()  # 동작 실행 가능여부 표시

    game_world.lifeenergybar = gameobjects.Lifeenergybar() # 체력, 기력 바탕 이미지
    game_world.lifeimage = gameobjects.Lifeimage() # 체력 이미지
    game_world.energyimage = gameobjects.Energyimage() # 기력 이미지

    # [Layer 2] - 은비 (플레이어) 그리기

    game_world.add_object(eunbi, 2) # 은비(플레이어)

    # [Layer 1] - Stage 관련 이미지들

    game_world.add_object(ground, 1) # 발판 오브젝트


    # (// 별 그리기 여기 넣을예정)


    # [Layer 0] - 기타 이미지들

    game_world.add_object(imagebg, 0) # 배경 이미지
    game_world.add_object(imagestagebg, 0) # 스테이지 배경 이미지

    game_world.add_object(drawnowstage, 0) # 스테이지 표시 오브젝트

    game_world.add_object(skill1image, 0) # 동작 실행 가능여부 표시
    game_world.add_object(skill2image, 0) # 동작 실행 가능여부 표시
    game_world.add_object(skill3image, 0) # 동작 실행 가능여부 표시

    game_world.add_object(game_world.lifeenergybar, 0) # 체력, 기력 바탕 이미지
    game_world.add_object(game_world.lifeimage, 0) # 체력 이미지
    game_world.add_object(game_world.energyimage, 0) # 기력 이미지

    pass

# 화면 그리기
def draw():
    global skill2usingimg
    global skillmovelocked, skillqlocked, skillwlocked

    clear_canvas() # 화면 초기화

    # 게임 월드에 있는 오브젝트에 한하여
    for game_object in game_world.all_objects():

        # [Layer 2] - 은비 (플레이어) 그리기

        if game_object == eunbi:
            game_object.draw()

        # [Layer 1] - Stage 관련 이미지들

        if game_object == ground:
            game_object.draw(340, 136)  # 땅 그리기

        # [Layer 0] - 기타 이미지들

        # 배경 이미지 그리기
        elif game_object == imagebg:
            game_object.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 배경 이미지 그리기
        elif game_object == imagestagebg:
            game_object.draw(340, 410)  # 스테이지 배경 이미지 그리기

        # 스테이지 표시 그리기
        elif game_object == drawnowstage:
            game_object.draw(nowgamestage)  # 스테이지 표시 그리기

        elif game_object == skill1image:
            game_object.draw(472, 56)  # 기술 1 그리기
        elif game_object == skill2image:
            game_object.draw(558, 58)  # 기술 2 그리기
        elif game_object == skill3image:
            game_object.draw(644, 58)  # 기술 3 그리기

        elif game_object == game_world.lifeenergybar:
            game_object.draw(150, 82) # 체력 표시 자리
            game_object.draw(150, 38) # 기력 표시 자리

        elif game_object == game_world.lifeimage:
            game_object.draw(150 - lifeimageadjust, 82, int(nowlifelength))
        elif game_object == game_world.energyimage:
            game_object.draw(150 - energyimageadjust, 38, int(nowenergylength))

    # 잠근 기술 위에 잠김 이미지 표시하기

    lockimage = load_image('lockimage.png')  # 배경 이미지
    if skillmovelocked == 1:
        lockimage.draw(471, 72)  # 기술 1 그리기
    if skillqlocked == 1:
        lockimage.draw(557, 72)  # 기술 2 그리기
    if skillwlocked == 1:
        lockimage.draw(643, 72)  # 기술 3 그리기

    # q 기술(순간이동) 사용중일 때는 커서 숨기고 q 기술 이미지 표시하기

    if nowqstate == 1:
        hide_cursor()
        skill2usingimg.draw(mousex, mousey)
    else:
        show_cursor()

    # 스테이지 그리기

    stagedraw(nowgamestage, needtocollectstar)

    # 화면 업데이트

    update_canvas()

    pass

# 업데이트

def update():

    global mousepressed # 마우스 클릭한 여부
    global mouseclickedx, mouseclickedy  # 마우스 클릭한 x좌표, y좌표
    global skill1image, skill2image, skill3image # 기술 이미지

    global keypressedleft, keypressedright, keypressedz, keypressedq, keypressedw

    global eunbi # 은비(플레이어)

    global stagerestart # 스테이지 재시작 여부

    global nowcollectedstar, ifstagedrawed, nowgamestage
    global nowdashr, nowdashl

    global nowdrawing # z키 (별 그리기) 사용중 여부
    global nowqstate # q키 (순간이동) 사용중 여부

    global skillmovecooltime, nowskillmovecooltime
    global skillqcooltime, nowskillqcooltime

    global skillmoveneedenergy # 도약 사용시 기력 요구치
    global skillqneedenergypercent # 순간이동 사용시 기력 요구 퍼센트

    # 동작 잠그기, 잠금 해제
    global skillmovelocked, skillqlocked, skillwlocked

    # 스테이지 재시작시
    if stagerestart == 1:

        # 다음 스테이지(또는 다음 차원)로 이동
        nowgamestage += 1  # 다음 스테이지로 이동
        if int(nowgamestage % 10) == 5:  # 현재 5지역일 경우
            nowgamestage += 10  # 다음 차원으로
            nowgamestage -= 4  # 1지역으로

        nowcollectedstar = 0  # 모은 별 개수 초기화
        ifstagedrawed = 0  # 스테이지 그려짐 여부 초기화

        # 최대 체력과 기력으로 스테이지 시작
        eunbi.lifenow, eunbi.energynow = eunbi.lifemax, eunbi.energymax

        # 키 입력 초기화
        keypressedleft = 0
        keypressedright = 0
        keypressedz, keypressedq, keypressedw = 0, 0, 0

        # 재시작 재설정 완료
        stagerestart = 0
        pass

    # --- 기술 메뉴 표시 ---

    if nowskillmovecooltime == 0:
        skill1image.frame = 0  # 도약 실행 가능
    elif nowdashl == 2 or nowdashr == 2:
        skill1image.frame = 1  # 도약 실행중
    elif nowskillmovecooltime > 0:
        skill1image.frame = 2  # 도약 대기시간중

    if nowqstate == 0:
        skill2image.frame = 0  # 순간이동 실행 가능
    elif nowqstate == 1:
        skill2image.frame = 1  # 순간이동 실행중
    elif nowqstate == 2 or nowqstate == 3:
        skill2image.frame = 2  # 순간이동 대기시간중

    # 도약 동작
    if nowdashr == 1:  # 오른쪽 도약 실행시
        if skillmovelocked == 0:
            nowdashr = 2
            nowskillmovecooltime = skillmovecooltime  # 대기시간 켜기
            self.x += dashamount  # 오른쪽으로 크게 이동
        else:
            nowdashl = 0

    elif nowdashl == 1:  # 왼쪽 도약 실행시
        if skillmovelocked == 0:
            nowdashl = 2
            nowskillmovecooltime = skillmovecooltime  # 대기시간 켜기
            self.x -= dashamount  # 왼쪽으로 크게 이동
        else:
            nowdashl = 0

    if keypressedz == 1:
        nowdrawing = 1
        draweffect.update()

    # 날기 동작 대기 시간 (쿨타임) 감소
    if nowskillmovecooltime > 0:
        nowskillmovecooltime -= 1
        # 대기 시간이 일정 비율 이하로 줄어들면 잔상표시 지우기
        if nowskillmovecooltime <= skillmovecooltime * (3 / 4):
            nowdashr, nowdashl = 0, 0

    # 순간이동

    if keypressedq == 1:
        if nowqstate == 0 and skillqlocked == 0:
            nowqstate = 1

    # 순간이동 (쿨타임) 감소

    if nowqstate == 2:
        nowskillqcooltime = skillqcooltime
        nowqstate = 3

    elif nowqstate == 3:

        nowskillqcooltime -= 1

        if nowskillqcooltime <= 0:
            nowskillqcooltime = 0
            nowqstate = 0

    # 반짝임
    if keypressedw == 1:
        # // 추가 예정
        pass

    # 스테이지 정보 확인
    stagecheckresult = stagecheck(nowgamestage, needtocollectstar)
    if stagecheckresult == 'cleared':
        # [별그림자 회랑] 강화 메뉴로 이동
        game_framework.change_state(frame_upgrade)

    # 현위치가 STAGE일 경우
    if frame_main.nowplace == frame_main.PL_STAGE:
        eunbi.update()

    # 캔버스 다시 그리기
    update_canvas()

    pass

# 종료

def exit():
    # 게임 월드에 있는 모든 오브젝트 지우기
    game_world.clear_all_objects()

# 이벤트 핸들러

def handle_events():
    events = get_events()

    global eunbi # 은비(플레이어)

    global mousepressed # 마우스 클릭한 여부
    global keypressing # 키보드 입력중 여부
    global keypressedleft, keypressedright # 왼쪽, 오른쪽 키 입력 여부
    global keypressedz, keypressedq, keypressedw # 기술 키 입력여부
    global mousex, mousey, mouseclickedx, mouseclickedy  # 마우스 x좌표, y좌표

    global playersavex, playersavey # 플레이어 좌표 저장

    global ifnowclickl, ifnowclickr, nowdashtime, dashtime # 도약 판정 변수
    global skillmovecooltime # 도약 대기시간 (쿨타임)
    global nowdashl, nowdashr # 해당 방향으로 도약 여부

    global nowqstate # 현재 q (순간이동) 수행중 여부
    global skillqcooltime  # 도약 대기시간 (쿨타임)
    global nowskillqcooltime # 현재 도약 대기시간 (쿨타임)

    global nowgamestage

    global skillmovelocked, skillqlocked, skillwlocked

    for event in events:

        # 종료일 때
        if event.type == SDL_QUIT:
            game_framework.quit()

        # F1키를 눌렀다 뗄 경우 중단
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_F1):
            game_framework.push_state(frame_pause)  # 일시정지 메뉴 열기

        # 숫자키로 기술 잠그기, 잠금 해제
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_1):
            skillmovelocked = 1 - skillmovelocked
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_2):
            skillqlocked = 1 - skillqlocked
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_3):
            skillwlocked = 1 - skillwlocked

        # F2 F3키는 테스트용으로, 각각 이전, 다음 스테이지 이동키입니다
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
            delay(DELAYTIME)

        # 마우스 이동시
        elif event.type == SDL_MOUSEMOTION:
            mousex, mousey = event.x, frame_main.WINDOWYSIZE - 1 - event.y

            if nowqstate == 1:
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
            if nowqstate == 1:
                if eunbi.energynow >= eunbi.energymax * (skillqneedenergypercent / 100):
                    eunbi.energynow -= eunbi.energymax * (skillqneedenergypercent / 100)
                    nowqstate = 2
                    mouseclickedx, mouseclickedy = mousex, mousey
                    eunbi.x, eunbi.y = mouseclickedx, mouseclickedy

                else:
                    nowqstate = 0


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

# ------------ 직접 실행시켰을 경우 ------------

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()
