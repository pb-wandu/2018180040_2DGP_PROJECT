### [별그림자 이야기] 메인 메뉴 파일입니다

# main 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트
import frame_game         # 게임 메뉴 전환시 호출
import frame_info         # 정보 메뉴 전환시 호출

import control            # 컨트롤 관련 변수, 함수

import bgmplay            # 배경음 재생 관련

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기
UNSET = 999         # 아직 정해지지 않은 것
DELAYTIME = 0.005   # 지연 시간

# ------------ 변수들, 사용자 지정 함수 ------------

imagebg = None # 배경 이미지

mousepressed = 0 # 마우스 클릭한 여부

PL_MAIN, PL_INFO, PL_STAGE, PL_PAUSE, PL_UPGRADE = 10, 11, 20, 21, 30

nowplace = UNSET # 현재 위치

class BGM:
    bgm = None

    def __init__(self):
        self.bgm = load_music('BGM1 - Starlight in My Heart.wav')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

# ------------ 게임 프레임워크 동작들 ------------

bgmplay.nowbgm = None


# 메뉴 진입
def enter():
    global imagebg
    global nowplace
    show_cursor() # 마우스 커서 보이기

    imagebg = load_image('mainmenuimg.png') # 시작 메뉴 이미지

    # 배경음악
    if bgmplay.nowbgm != bgmplay.BGMNORMAL:
        bgmplay.nowbgm = bgmplay.BGMNORMAL
        bgmplay.bgm = BGM()  # 배경음악 클래스 실행

    # 현위치 지정
    nowplace = PL_MAIN

    pass

# 메뉴 종료
def exit():
    global imagebg
    del imagebg
    pass

# 화면 그리기
def draw():
    clear_canvas()

    imagebg.draw(WINDOWXSIZE / 2, WINDOWYSIZE / 2)  # 시작 메뉴 이미지 그리기



    update_canvas()

# 정보 갱신
def update():
    #
    pass

# 이벤트 핸들러
def handle_events():
    control.frame_main_events()

# 중단되었을 경우
def pause():

    pass

# 다시 실행된 경우
def resume():

    pass

# 직접 실행시켰을 경우

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()