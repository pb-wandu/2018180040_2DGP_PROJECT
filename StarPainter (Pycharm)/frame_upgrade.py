### [별그림자 이야기] 별그림자 회랑 (강화 메뉴) 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import

import frame_main         # main의 변수들 import
import frame_game         # 게임 메뉴 전환시 호출
import object_player      # 플레이어 관련 변수 사용

import game_world         # 게임 월드 및 스테이지 관련 변수, 함수
import stageinfo          # 스테이지 관련 변수, 함수
import control            # 컨트롤 관련 변수, 함수

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

    # 다음 스테이지(또는 다음 차원)로 이동
    stageinfo.nowgamestage += 1  # 다음 스테이지로 이동
    if int(stageinfo.nowgamestage % 10) == 5:  # 현재 5지역일 경우
        stageinfo.nowgamestage += 10  # 다음 차원으로
        stageinfo.nowgamestage -= 4  # 1지역으로

    frame_game.nowcollectedstar = 0  # 모은 별 개수 초기화
    frame_game.ifstagedrawed = 0  # 스테이지 그려짐 여부 초기화

    # 최대 체력과 기력으로 스테이지 시작
    frame_game.eunbi.lifenow, frame_game.eunbi.energynow = frame_game.eunbi.lifemax, frame_game.eunbi.energymax

    # 키 입력 초기화
    frame_game.keypressedleft = 0
    frame_game.keypressedright = 0
    frame_game.keypressedz, frame_game.keypressedq, frame_game.keypressedw = 0, 0, 0

    # 대기시간 초기화
    frame_game.nowskillmovecooltime = 0
    frame_game.nowskillqcooltime = 0

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
    control.frame_upgrade_events()

# 직접 실행시켰을 경우

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()

