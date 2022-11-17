### [별그림자 이야기] 게임 오브젝트 파일입니다

# 프레임워크가 아닌 오브젝트 모음 파일입니다
# 플레이어와 관련 없는 오브젝트들을 표시합니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 변수들 사용
import frame_main         # 메인 메뉴 상수들 사용

import math               # 삼각함수

# ------------ 오브젝트 클래스들 ------------

# 발판 오브젝트
class Ground:
    image = None

    def __init__(self):
        if Ground.image is None:
            self.image = load_image('ground.png')  # 발판 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y)  # 발판 이미지 그리기

    pass

# 스테이지 표시 오브젝트

class Drawnowstage:

    def __init__(self):
        self.imageworld = load_image('level_world.png')  # 월드 이미지
        self.imagestage = load_image('level_stage.png')  # 스테이지 이미지

    def draw(self, n):
        self.imageworld.clip_draw((int(n / 10) - 1) * 56, 0, 48, 48, 737, 434)
        self.imagestage.clip_draw(0, (int(n % 10) - 1) * 56, 198, 48, 869.5, 434)
    pass

# 동작 표시 오브젝트

class Skill1image:
    image = None

    def __init__(self):
        self.frame = 0  # 애니메이션 프레임
        Skill1image.image = load_image('skill1show.png')  # 기술 이미지 그리기

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 82, 0, 75, 103, x, y) # 기술 이미지 그리기

    pass

class Skill2image:
    image = None

    def __init__(self):
        self.frame = 0  # 애니메이션 프레임
        Skill2image.image = load_image('skill2show.png')  # 기술 이미지 그리기

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 82, 0, 75, 103, x, y) # 기술 이미지 그리기

    pass

class Skill3image:
    image = None

    def __init__(self):
        self.frame = 0  # 애니메이션 프레임
        Skill3image.image = load_image('skill3show.png')  # 기술 이미지 그리기

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 82, 0, 75, 103, x, y)  # 기술 이미지 그리기

    pass

# 별

class Star:

    def __init__(self):
        self.x, self.y = frame_main.UNSET, frame_main.UNSET
        self.image = None # 아래 참고
        self.ifdraw = False # 그렸는지 판정 변수

    def draw(self, x, y):
        self.x, self.y = x, y
        if self.ifdraw:
            self.image = load_image('starpainted.png')  # 별 이미지 이미지 그리기
        else:
            self.image = load_image('starplace.png')  # 목표 지점 이미지 그리기

        self.image.draw(x, y) # 별 이미지 그리기
        draw_rectangle(*self.gethitarea())

    # 충돌 범위
    def gethitarea(self):
        return self.x-15, self.y+15, self.x+15, self.y-15

    # 충돌 처리
    def handle_collision(self, other, group):
        self.ifdraw = True
        pass

    pass

# 체력 기력 표시칸

class Lifeenergybar:
    image = None

    def __init__(self):
        if Lifeenergybar.image is None:
            Lifeenergybar.image = load_image('lifeenergybar.png')  # 도약 효과 이미지 그리기
            self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.draw(x, y)

    pass

# 체력 표시

class Lifeimage:
    image = None

    def __init__(self):
        if Lifeimage.image is None:
            Lifeimage.image = load_image('lifeimage.png')
            self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y, drawl):
        self.image.clip_draw(0, 0, drawl, 30, x, y)

    pass

# 기력 표시

class Energyimage:
    image = None

    def __init__(self):
        if Energyimage.image is None:
            Energyimage.image = load_image('energyimage.png')
            self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y, drawl):
        self.image.clip_draw(0, 0, drawl, 30, x, y)

    pass

# 시간 표시

class Timeimage:
    image = None

    def __init__(self):
        if Timeimage.image is None:
            Timeimage.image = load_image('Timeimage.png')
            self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y, drawl):
        self.image.clip_draw(0, 0, drawl, 30, x, y)

    pass

# ------------ 장애물, 적 오브젝트 클래스들 ------------

# 장애물 - 행성

class Planet:
    image = None

    def __init__(self):
        self.x, self.y = frame_main.UNSET, frame_main.UNSET
        if Planet.image is None:
            Planet.image = load_image('planetimage.png')


    def draw(self, x, y):
        self.image.draw(x, y)
        self.x, self.y = x, y
        draw_rectangle(*self.gethitarea())

    # 충돌 범위 (상하좌우 3px 보정)
    def gethitarea(self):
        return self.x-32, self.y+27, self.x+32,self.y-27

    # 충돌 처리
    def handle_collision(self, other, group):
        pass

    pass

# 장애물 -

class Planet:
    image = None

    def __init__(self):
        self.x, self.y = frame_main.UNSET, frame_main.UNSET
        if Planet.image is None:
            Planet.image = load_image('planetimage.png')


    def draw(self, x, y):
        self.image.draw(x, y)
        self.x, self.y = x, y
        draw_rectangle(*self.gethitarea())

    # 충돌 범위 (상하좌우 3px 보정)
    def gethitarea(self):
        return self.x-32, self.y+27, self.x+32,self.y-27

    # 충돌 처리
    def handle_collision(self, other, group):
        pass

    pass

# ------------ 직접 실행시켰을 경우 ------------

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()
