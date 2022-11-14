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
import stageinfo          # 스테이지 관련 변수, 함수
import control            # 컨트롤 관련 변수, 함수

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = 999         # 아직 정해지지 않은 것
DELAYTIME = 0.005   # 지연 시간

WORLDNUM = 6 # 차원 개수
PLACENUM = 5 # 각 차원당 장소 개수
STARSIZE = 30 # 별 크기
OBJSNUMMAX = 6 # 오브젝트 개수 상한

# ------------ 변수들 ------------

imagebg, imagestagebg, eunbi, ground = None, None, None, None # 배경 이미지, 스테이지 배경, 별그림자 은비(플레이어), 발판
drawnowstage = None # 스테이지 표시
pauseimage = None # 일시정지 이미지
skill1image, skill2image, skill3image = None, None, None # 기술 사용 가능여부 이미지

jumpeffect, wingimage, quickmove, draweffect = None, None, None, None # 은비(플레이어) 관련 이미지

skill2usingimg = None # q (순간이동) 사용중 이미지

stagerestart = 0 # 스테이지 재시작 여부

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

# ------------ 스테이지 관리 함수 ------------

# 스테이지 확인

def stagecheck(stage):

    global nowdrawing  # 현재 그림 그리고 있는지 여부

    global eunbi # 은비(플레이어)

    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소

    # 체력, 기력 정보 관리

    stageinfo.nowlifelength = 120 * eunbi.lifenow / eunbi.lifemax # 전체 제력 대비 현재 체력
    stageinfo.nowenergylength = 120 * eunbi.energynow / eunbi.energymax # 전체 기력 대비 현재 기력
    stageinfo.lifeimageadjust = (120 - stageinfo.nowlifelength) / 2 # 왼쪽으로 정렬 이동값
    stageinfo.energyimageadjust = (120 - stageinfo.nowenergylength) / 2 # 왼쪽으로 정렬 이동값

    # starplacesset에서 현재 스테이지 좌표가 있는 위치
    starplacessetplace = (worldnow - 1) * PLACENUM + (placenow - 1)

    nowstageneedstar = stageinfo.needtocollectstar[worldnow - 1][placenow - 1]  # 현재 스테이지에서 필요한 별
    stageinfo.starplaces = [gameobjects.Star() for i in range(nowstageneedstar)]  # 별들을 저장할 위치

    for i in range(nowstageneedstar):

        x, y = stageinfo.starplacesset[starplacessetplace][i][0], stageinfo.starplacesset[starplacessetplace][i][1]
        drawx, drawy = UNSET, UNSET

        if eunbi.nowstate == LEFTDRAWING:
            drawx, drawy = eunbi.x - 15, eunbi.y + 17
        elif eunbi.nowstate == RIGHTDRAWING:
            drawx, drawy = eunbi.x + 15, eunbi.y + 17

        # 만약 별이 그려지지 않은 경우
        if not stageinfo.stardrawed[i] and nowdrawing == 1:

            # 별을 그리는 좌표가 목표 지점의 안에 있을 때 (15px 별 범위 보정 적용)
            if x - (STARSIZE / 2 - 15) <= drawx <= (x + STARSIZE / 2 + 15)\
                    and (y - STARSIZE / 2 - 15) <= drawy <= (y + STARSIZE / 2 + 15):
                stageinfo.stardrawed[i] = True
                stageinfo.starplaces[i].ifdraw = True  # 별을 그렸음
                nowdrawing = 0
                stageinfo.nowcollectedstar += 1  # 별을 하나 그림

    for i in range(OBJSNUMMAX):
        if stageinfo.planetobjs[i] is not None:
            if collide(eunbi, stageinfo.planetobjs[i]):
                eunbi.handle_collision(stageinfo.planetobjs[i], 'eunbi_planet')
                stageinfo.planetobjs[i].handle_collision(eunbi, 'eunbi_planet')

    # 현재 모은 별 개수가 현재 차원에서 요구하는 별 개수와 같다면
    if stageinfo.nowcollectedstar == nowstageneedstar:
        return 'cleared'

    # 은비(플레이어) 충돌시 무적상태
    if eunbi.hittime > 0:
        eunbi.hittime -= 1
    else:
        eunbi.nowinvincible = 0

    # 체력이 0 이하이면 시작 메뉴로 이동
    if eunbi.lifenow <= 0:
        game_framework.change_state(frame_main)

    pass


# 스테이지 그리기

def stagedraw(stage):

    global nowdrawing  # 현재 그림 그리고 있는지 여부


    worldnow = int(stage / 10)  # 현재 차원
    placenow = stage % 10  # 현재 장소

    # 글자 표시
    stagefont = load_font('WLR-1_Yeongyeon_v1_3.TTF', 16)
    stagetext = '현재 위치 : 차원 ' + str(worldnow) + ' - 구역 ' + str(placenow)

    stagefont.draw(5, frame_main.WINDOWYSIZE - 21, stagetext, (0, 0, 80))

    # 현재 스테이지 좌표가 있는 위치
    placessetplace = (worldnow - 1) * PLACENUM + (placenow - 1)

    nowstageneedstar = stageinfo.needtocollectstar[worldnow - 1][placenow - 1] # 현재 스테이지에서 필요한 별
    starplaces = [gameobjects.Star() for i in range(nowstageneedstar)] # 별들을 저장할 위치

    for i in range(nowstageneedstar):

        if stageinfo.stardrawed[i]:
            starplaces[i].ifdraw = True
        else:
            starplaces[i].ifdraw = False

        x = stageinfo.starplacesset[placessetplace][i][0]
        y = stageinfo.starplacesset[placessetplace][i][1]
        starplaces[i].draw(x, y)

    stageinfo.planetobjs = [gameobjects.Planet() for i in range(OBJSNUMMAX)]  # 행성들을 저장할 위치

    for i in range(OBJSNUMMAX):
        if stageinfo.planetobjs[i] is not None:
            stageinfo.planetobjs[i].x = stageinfo.planetplacesset[placessetplace][i][0]
            stageinfo.planetobjs[i].y = stageinfo.planetplacesset[placessetplace][i][1]
            stageinfo.planetobjs[i].draw(stageinfo.planetobjs[i].x, stageinfo.planetobjs[i].y)

    # 은비(플레이어) 충돌시 무적상태
    if eunbi.hittime > 0:
        invincibleimg = load_image('invincibleimg.png')  # 무적 상태 이미지
        invincibleimg.draw(eunbi.x, eunbi.y + 20)

    pass

# ------------ 메뉴 진입 ------------

def enter():
    global imagebg, imagestagebg
    global eunbi
    global ground
    global drawnowstage
    global pauseimage

    global skill1image, skill2image, skill3image

    global jumpeffect, wingimage, quickmove, draweffect

    global skill2usingimg

    # 별 그린 것 초기화
    for i in range(10):
        stageinfo.stardrawed[i] = False
    stageinfo.nowcollectedstar = 0

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

    # 충돌 대상 정보 등록
    # ### 게임 월드를 이용한 처리가 안 되어 임시방편으로 코드 짠 상태 - 수정 예정
    # game_world.add_collision_pairs(eunbi, planetobjs, "eunbi_planetobjs") # 은비(플레이어)와 행성

    pass

# 충돌 확인

def collide(a, b):

    # None이 아닌 값들에 한하여 확인한다
    if a is not None and b is not None:

        aleft, atop, aright, abottom = a.gethitarea()
        bleft, btop, bright, bbottom = b.gethitarea()

        if aleft > bright: return False
        if aright < bleft: return False
        if abottom > btop: return False
        if atop < bbottom: return False

        return True

    return False

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
            game_object.draw(stageinfo.nowgamestage)  # 스테이지 표시 그리기

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
            game_object.draw(150 - stageinfo.lifeimageadjust, 82, int(stageinfo.nowlifelength))
        elif game_object == game_world.energyimage:
            game_object.draw(150 - stageinfo.energyimageadjust, 38, int(stageinfo.nowenergylength))

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
        skill2usingimg.draw(control.mousex, control.mousey)
    else:
        show_cursor()

    stagedraw(stageinfo.nowgamestage) # 스테이지 그리기

    update_canvas() # 화면 업데이트

    pass

# 업데이트

def update():

    # for game_object in game_world.all_objects():
    #    game_object.update()

    # 충돌 확인 및 처리
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print("Collision ", group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)


    global skill1image, skill2image, skill3image # 기술 이미지

    global eunbi # 은비(플레이어)

    global stagerestart # 스테이지 재시작 여부

    global nowdashr, nowdashl

    global nowdrawing # z키 (별 그리기) 사용중 여부
    global nowqstate # q키 (순간이동) 사용중 여부

    global skillmovecooltime, nowskillmovecooltime
    global skillqcooltime, nowskillqcooltime

    global skillmoveneedenergy # 도약 사용시 기력 요구치
    global skillqneedenergypercent # 순간이동 사용시 기력 요구 퍼센트

    # 동작 잠그기, 잠금 해제
    global skillmovelocked, skillqlocked, skillwlocked

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

    if control.keypressedz == 1:
        nowdrawing = 1
        draweffect.update()

    # 날기 동작 대기 시간 (쿨타임) 감소
    if nowskillmovecooltime > 0:
        nowskillmovecooltime -= 1
        # 대기 시간이 일정 비율 이하로 줄어들면 잔상표시 지우기
        if nowskillmovecooltime <= skillmovecooltime * (3 / 4):
            nowdashr, nowdashl = 0, 0

    # 순간이동

    if control.keypressedq == 1:
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
    if control.keypressedw == 1:
        # // 추가 예정
        pass

    # 스테이지 정보 확인
    stagecheckresult = stagecheck(stageinfo.nowgamestage)
    if stagecheckresult == 'cleared':
        # [별그림자 회랑] 강화 메뉴로 이동
        game_framework.change_state(frame_upgrade)

    # 현위치가 STAGE일 경우
    if frame_main.nowplace == frame_main.PL_STAGE:
        eunbi.update()

    update_canvas() # 캔버스 다시 그리기

    pass

# 이벤트 핸들러

def handle_events():
    control.frame_game_events()

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

# 종료

def exit():
    control.keypressedleft, control.keypressedright = 0, 0
    control.keypressedz, control.keypressedq, control.keypressedw = 0, 0, 0
    eunbi.nowstate = STOP

    # 게임 월드에 있는 모든 오브젝트 지우기
    game_world.clear_all_objects()

# ------------ 직접 실행시켰을 경우 ------------

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()
