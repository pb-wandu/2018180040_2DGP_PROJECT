### [별그림자 이야기] 게임 오브젝트 파일입니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 변수들 사용
import frame_main         # 메인 메뉴 변수들 사용

# 플레이어 오브젝트
class Player:

    # 초기화
    def __init__(self):
        self.image = load_image('characterimages.png')  # 캐릭터 이미지 (작업중)

        self.x, self.y = frame_game.PLAYERXSTART, frame_game.PLAYERYSTART  # 플레이어 좌표
        self.xspd = 8 # x축 이동속도
        self.yspd = 0  # y축 이동속도
        self.frame = 0  # 애니메이션 프레임
        self.nowstate = frame_game.STOP  # 현재 플레이어 상태

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
        self.frame = (self.frame + 1) % 2

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
        self.image.clip_draw(self.frame * 20, 0, 10, 10, x, y - self.frame * 5)

    def update(self):
        if self.frame < 5:
            self.frame += 1

    pass

# 스테이지 표시 오브젝트

class Drawstage:

    def __init__(self):
        self.imageworld = load_image('level_world.png')  # 날기(점프) 효과 이미지 (임시)
        self.imagestage = load_image('level_stage.png')  # 날기(점프) 효과 이미지 (임시)

    def draw(self, n):
        self.imageworld.clip_draw( (int(n / 10) - 1) * 56, 0, 48, 48, 737, 434)
        self.imagestage.clip_draw(0, (int(n % 10) - 1) * 56, 198, 48, 869.5, 434)
    pass

# 날개 오브젝트

class Wingimage:

    def __init__(self):
        self.image = load_image('wingimg.png')  # 날개 이미지
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(0, self.frame * 24, 55, 14, x, y - self.frame * 4)  # 날기(점프) 효과 이미지 그리기

    def update(self):
        if self.frame < 2:
            self.frame += 1

    pass

# 동작 표시 오브젝트

class Skill1image:

    def __init__(self):
        self.image = load_image('skill1show.png')  # 기술 이미지 그리기
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 82, 0, 75, 103, x, y) # 기술 이미지 그리기

    pass

class Skill2image:

    def __init__(self):
        self.image = load_image('skill2show.png')  # 기술 이미지 그리기
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(0, self.frame * 82, 75, 103, x, y) # 기술 이미지 그리기

    pass

class Skill3image:

    def __init__(self):
        self.image = load_image('skill3show.png')  # 기술 이미지 그리기
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(0, self.frame * 82, 75, 103, x, y)  # 기술 이미지 그리기

    pass

# 도약 효과

class Quickmove:

    def __init__(self):
        self.image = load_image('quickmove.png')  # 도약 효과 이미지 그리기
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 50, 0, 43, 43, x, y) # 도약 효과 그리기

    pass

# 도약 효과

class Star:

    def __init__(self):
        self.image = None # 아래 참고
        self.ifdraw = False # 그렸는지 판정 변수
        self.num = None # 현위치 번째

    def draw(self, x, y):
        if self.ifdraw:
            self.image = load_image('starpainted.png')  # 별 이미지 이미지 그리기
        else:
            self.image = load_image('starplace.png')  # 목표 지점 이미지 그리기

        self.image.draw(x, y) # 별 이미지 그리기

    pass