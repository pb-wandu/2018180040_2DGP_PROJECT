### [별그림자 이야기] 플레이어 오브젝트 파일입니다

# 프레임워크가 아닌 플레이어 오브젝트 파일입니다
# 은비(플레이어)와 관련된 오브젝트를 포함합니다

# ------------ import 파일들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_game         # 게임 메뉴 변수들 사용

# ------------ 은비(플레이어) 관련 변수들 ------------

YMINSPD = -14.0 # y속도 하한
YMAXSPD = +14.0 # y속도 상한

PLAYERXSIZE, PLAYERYSIZE = 30, 40  # 별그림자 은비 크기
PLAYERXSTART, PLAYERYSTART = 340, 150  # 별그림자 은비 시작좌표

# ------------ 플레이어 동작 클래스들 ------------

# 플레이어 오브젝트 동작들

class IDLE: # 플레이어 정지 동작

    # 상태를 실행할 때 수행하는 동작
    @staticmethod
    def enter(self, event):
        print("### nowplayerstate : IDLE") # IDLE 상태 진입 (테스트용)
        self.nowstate = frame_game.STOP # 현재 멈춤 상태

        # 왼쪽 키 눌렀을 때
        if event == EV_LD:
            frame_game.keypressedleft = 1  # 왼쪽 키 눌림

            if frame_game.ifnowclickl == 0:
                frame_game.ifnowclickl = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 왼쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickl == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickl = 0
                    frame_game.nowdashl = 1  # 왼쪽 도약 시작

        # 오른쪽 키 눌렀을 때
        if event == EV_RD:
            frame_game.keypressedright = 1  # 오른쪽 키 눌림

            if frame_game.ifnowclickr == 0:
                frame_game.ifnowclickr = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 오른쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickr == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickr = 0
                    frame_game.nowdashr = 1  # 오른쪽 도약 시작

        # 왼쪽 키 뗐을 때
        if event == EV_LU:
            frame_game.keypressedleft = 0  # 왼쪽 키 뗌

        # 오른쪽 키 뗐을 때
        if event == EV_RU:
            frame_game.keypressedright = 0  # 오른쪽 키 뗌

        # 스페이스바 뗐을 때
        if event == EV_SPU:
            # 날기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.yjumpneedenergy:
                self.energynow -= self.yjumpneedenergy
                self.yspd += self.yjumpamount # 날기(점프)
            else:
                self.energynow = 0

                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

        # z키 눌렀을 때
        if event == EV_ZD:
            # 별 그리기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.drawneedenergy:
                self.energynow -= self.drawneedenergy
                frame_game.keypressedz = 1 # z키 누름

        # z키 뗐을 때
        if event == EV_ZU:
            frame_game.keypressedz = 0  # z키 뗌

        pass

    # 상태를 종료할 때 수행하는 동작
    @staticmethod
    def exit(self):
        pass

    # 실행중에 지속적으로 수행하는 동작
    @staticmethod
    def do(self):

        # 눌린 키에 따라 동작 수행

        if frame_game.keypressedleft == 1:
            self.movexy(-self.xspd, 0)  # 왼쪽 이동
            self.frame = 0

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.LEFT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.LEFTDRAWING

        if frame_game.keypressedright == 1:
            self.movexy(+self.xspd, 0)  # 오른쪽 이동
            self.frame = 1

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.RIGHT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.RIGHTDRAWING

        # 플레이어는 yspd만큼 y축 방향으로 이동한다
        self.yspd -= 0.9
        self.y += self.yspd

        # y 이동속도 상한, 하한 제한
        if self.yspd < YMINSPD: self.yspd = YMINSPD
        if self.yspd > YMAXSPD: self.yspd = YMAXSPD

        # 땅 위에 있을 경우
        if self.y < 130:
            self.y = 130
            self.yspd = 0

            # 날기 상태인 경우
            if self.cur_state == FLY:
                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE  # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

            # 기력을 점차 회복한다
            if self.energynow < self.energymax:
                self.energynow += self.groundaddenergy
                if self.energynow > self.energymax:
                    self.energynow = self.energymax

        # 은비(플레이어) 이동 범위 제한

        if self.x < 0 + PLAYERXSIZE / 2:
            self.x = 0 + PLAYERXSIZE / 2
        if self.x > 680 - PLAYERXSIZE / 2:
            self.x = 680 - PLAYERXSIZE / 2
        if self.y < 120:
            self.y = 120
        if self.y > 700 - PLAYERYSIZE:
            self.y = 700 - PLAYERYSIZE
            self.yspd = 0

        pass

    # 그리기
    @staticmethod
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, abs(self.nowstate) * 50, 33, 43, self.x, self.y + 20)

        animationshow(self)  # 애니메이션 보여주기
        effectsdraw(self)  # 효과 그리기
        self.frame = 0  # 애니메이션 프레임 표시

        pass

    pass

class WALK: # 플레이어 이동 동작

    # 상태를 실행할 때 수행하는 동작
    @staticmethod
    def enter(self, event):
        print("### nowplayerstate : WALK")  # WALK 상태 진입 (테스트용)

        # 눌린 키에 따라 동작 수행

        # 왼쪽 키 눌렀을 때
        if event == EV_LD:
            frame_game.keypressedleft = 1  # 왼쪽 키 눌림

            if frame_game.ifnowclickl == 0:
                frame_game.ifnowclickl = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 왼쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickl == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickl = 0
                    frame_game.nowdashl = 1  # 왼쪽 도약 시작

        # 오른쪽 키 눌렀을 때
        if event == EV_RD:
            frame_game.keypressedright = 1  # 오른쪽 키 눌림

            if frame_game.ifnowclickr == 0:
                frame_game.ifnowclickr = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 오른쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickr == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickr = 0
                    frame_game.nowdashr = 1  # 오른쪽 도약 시작

        # 왼쪽 키 뗐을 때
        if event == EV_LU:
            frame_game.keypressedleft = 0 # 왼쪽 키 뗌

        # 오른쪽 키 뗐을 때
        if event == EV_RU:
            frame_game.keypressedright = 0  # 오른쪽 키 뗌

        # 스페이스바 뗐을 때
        if event == EV_SPU:
            # 날기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.yjumpneedenergy:
                self.energynow -= self.yjumpneedenergy
                self.yspd += self.yjumpamount # 날기(점프)
            else:
                self.energynow = 0

                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

        # z키 눌렀을 때
        if event == EV_ZD:
            # 별 그리기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.drawneedenergy:
                self.energynow -= self.drawneedenergy
                frame_game.keypressedz = 1 # z키 누름

        # z키 뗐을 때
        if event == EV_ZU:
            frame_game.keypressedz = 0  # z키 뗌

        # 은비(플레이어) 이동 범위 제한

        if self.x < 0 + PLAYERXSIZE / 2:
            self.x = 0 + PLAYERXSIZE / 2
        if self.x > 680 - PLAYERXSIZE / 2:
            self.x = 680 - PLAYERXSIZE / 2
        if self.y < 120:
            self.y = 120
        if self.y > 700 - PLAYERYSIZE:
            self.y = 700 - PLAYERYSIZE
            self.yspd = 0

        pass

    # 상태를 종료할 때 수행하는 동작
    @staticmethod
    def exit(self):
        pass

    # 실행중에 지속적으로 수행하는 동작
    @staticmethod
    def do(self):

        # 눌린 키에 따라 동작 수행

        if frame_game.keypressedleft == 1:
            self.movexy(-self.xspd, 0)  # 왼쪽 이동
            self.frame = 0

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.LEFT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.LEFTDRAWING

        if frame_game.keypressedright == 1:
            self.movexy(+self.xspd, 0)  # 오른쪽 이동
            self.frame = 1

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.RIGHT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.RIGHTDRAWING

        # 플레이어는 yspd만큼 y축 방향으로 이동한다
        self.yspd -= 0.9
        self.y += self.yspd

        # y 이동속도 상한, 하한 제한
        if self.yspd < YMINSPD: self.yspd = YMINSPD
        if self.yspd > YMAXSPD: self.yspd = YMAXSPD

        # 땅 위에 있을 경우
        if self.y < 130:
            self.y = 130
            self.yspd = 0

            # 날기 상태인 경우
            if self.cur_state == FLY:
                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE  # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

            # 기력을 점차 회복한다
            if self.energynow < self.energymax:
                self.energynow += self.groundaddenergy
                if self.energynow > self.energymax:
                    self.energynow = self.energymax
        # 은비(플레이어) 이동 범위 제한

        if self.x < 0 + PLAYERXSIZE / 2:
            self.x = 0 + PLAYERXSIZE / 2
        if self.x > 680 - PLAYERXSIZE / 2:
            self.x = 680 - PLAYERXSIZE / 2
        if self.y < 120:
            self.y = 120
        if self.y > 700 - PLAYERYSIZE:
            self.y = 700 - PLAYERYSIZE
            self.yspd = 0

        pass

    # 그리기
    @staticmethod
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, abs(self.nowstate) * 50, 33, 43, self.x, self.y + 20)

        animationshow(self)  # 애니메이션 보여주기
        effectsdraw(self)  # 효과 그리기
        self.frame = 0  # 애니메이션 프레임 표시

        pass

    pass


class FLY: # 플레이어 날기(점프) 동작

    # 상태를 실행할 때 수행하는 동작
    @staticmethod
    def enter(self, event):

        print("### nowplayerstate : FLY")  # FLY 상태 진입 (테스트용)

        # 왼쪽 키 눌렀을 때
        if event == EV_LD:
            self.movexy(-self.xspd, 0)  # 왼쪽 이동

            if frame_game.ifnowclickl == 0:
                frame_game.ifnowclickl = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 왼쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickl == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickl = 0
                    frame_game.nowdashl = 1  # 왼쪽 도약 시작

        # 오른쪽 키 눌렀을 때
        if event == EV_RD:
            self.movexy(+self.xspd, 0)  # 오른쪽 이동

            if frame_game.ifnowclickr == 0:
                frame_game.ifnowclickr = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 오른쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickr == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickr = 0
                    frame_game.nowdashr = 1  # 오른쪽 도약 시작

        # 왼쪽 키 뗐을 때
        if event == EV_LU:
            frame_game.keypressedleft = 0 # 왼쪽 키 뗌

        # 오른쪽 키 뗐을 때
        if event == EV_RU:
            frame_game.keypressedright = 0  # 오른쪽 키 뗌

        # 스페이스바 뗐을 때
        if event == EV_SPU:
            # 날기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.yjumpneedenergy:
                self.energynow -= self.yjumpneedenergy
                self.yspd += self.yjumpamount # 날기(점프)
            else:
                self.energynow = 0

                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

        # z키 눌렀을 때
        if event == EV_ZD:
            # 별 그리기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.drawneedenergy:
                self.energynow -= self.drawneedenergy
                frame_game.keypressedz = 1 # z키 누름

        # z키 뗐을 때
        if event == EV_ZU:
            frame_game.keypressedz = 0  # z키 뗌

        pass

    # 상태를 종료할 때 수행하는 동작
    @staticmethod
    def exit(self):
        pass

    # 실행중에 지속적으로 수행하는 동작
    @staticmethod
    def do(self):

        # 눌린 키에 따라 동작 수행

        if frame_game.keypressedleft == 1:
            self.movexy(-self.xspd, 0)  # 왼쪽 이동
            self.frame = 0

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.LEFT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.LEFTDRAWING

        if frame_game.keypressedright == 1:
            self.movexy(+self.xspd, 0)  # 오른쪽 이동
            self.frame = 1

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.RIGHT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.RIGHTDRAWING

        # 플레이어는 yspd만큼 y축 방향으로 이동한다
        self.yspd -= 0.9
        self.y += self.yspd

        # y 이동속도 상한, 하한 제한
        if self.yspd < YMINSPD: self.yspd = YMINSPD
        if self.yspd > YMAXSPD: self.yspd = YMAXSPD

        # 땅 위에 있을 경우
        if self.y < 130:
            self.y = 130
            self.yspd = 0

            # 날기 상태인 경우
            if self.cur_state == FLY:
                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE  # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

            # 기력을 점차 회복한다
            if self.energynow < self.energymax:
                self.energynow += self.groundaddenergy
                if self.energynow > self.energymax:
                    self.energynow = self.energymax

        # 은비(플레이어) 이동 범위 제한

        if self.x < 0 + PLAYERXSIZE / 2:
            self.x = 0 + PLAYERXSIZE / 2
        if self.x > 680 - PLAYERXSIZE / 2:
            self.x = 680 - PLAYERXSIZE / 2
        if self.y < 120:
            self.y = 120
        if self.y > 700 - PLAYERYSIZE:
            self.y = 700 - PLAYERYSIZE
            self.yspd = 0

        pass

    # 그리기
    @staticmethod
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, abs(self.nowstate) * 50, 33, 43, self.x, self.y + 20)

        animationshow(self)  # 애니메이션 보여주기
        effectsdraw(self)  # 효과 그리기
        self.frame = 0  # 애니메이션 프레임 표시

        pass

    pass

class DRAW: # 플레이어 별 그리기 동작

    # 상태를 실행할 때 수행하는 동작
    @staticmethod
    def enter(self, event):
        print("### nowplayerstate : DRAW")  # DRAW 상태 진입 (테스트용)
        frame_game.nowdrawing = 1 # 현재 그리는 상태

        # 왼쪽 키 눌렀을 때
        if event == EV_LD:
            self.movexy(-self.xspd)

            if frame_game.ifnowclickl == 0:
                frame_game.ifnowclickl = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 왼쪽 키를 누르고 있을 때
            elif ifnowclickl == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickl = 0
                    frame_game.nowdashl = 1  # 왼쪽 도약 시작

        # 오른쪽 키 눌렀을 때
        if event == EV_RD:
            self.movexy(+self.xspd)

            if frame_game.ifnowclickr == 0:
                frame_game.ifnowclickr = 1  # 왼쪽 눌렸음
                frame_game.nowdashtime = frame_game.dashtime  # 이 시간 안에 같은 키를 다시 누르면 도약을 수행

            # 왼쪽 키를 누르고 있을 때
            elif frame_game.ifnowclickr == 1:
                # 시간 안에 다시 같은 키를 누르고 그림 그리는 중이 아니고 대기 시간이 아니라면
                if frame_game.keypressedz == 0 and frame_game.nowdashtime > 0 and frame_game.skillxcooltime == 0:
                    frame_game.nowdashtime = 0
                    frame_game.ifnowclickr = 0
                    frame_game.nowdashr = 1  # 오른쪽 도약 시작

        # 왼쪽 키 뗐을 때
        if event == EV_LU:
            frame_game.keypressedleft = 0 # 왼쪽 키 뗌

        # 오른쪽 키 뗐을 때
        if event == EV_RU:
            frame_game.keypressedright = 0  # 오른쪽 키 뗌

        # 스페이스바 뗐을 때
        if event == EV_SPU:
            # 날기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.yjumpneedenergy:
                self.energynow -= self.yjumpneedenergy
                self.yspd += self.yjumpamount # 날기(점프)
            else:
                self.energynow = 0

                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

        # z키 눌렀을 때
        if event == EV_ZD:
            # 별 그리기에 필요한 기력보다 현재 기력이 많을 경우
            if self.energynow >= self.drawneedenergy:
                self.energynow -= self.drawneedenergy
                frame_game.keypressedz = 1 # z키 누름

        # z키 뗐을 때
        if event == EV_ZU:
            frame_game.keypressedz = 0  # z키 뗌

        pass

    # 상태를 종료할 때 수행하는 동작
    @staticmethod
    def exit(self):
        frame_game.nowdrawing = 0  # 현재 그리는 상태 해제
        pass

    # 실행중에 지속적으로 수행하는 동작
    @staticmethod
    def do(self):

        # 눌린 키에 따라 동작 수행

        if frame_game.keypressedleft == 1:
            self.frame = 0

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.LEFT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.LEFTDRAWING

        if frame_game.keypressedright == 1:
            self.frame = 1

            if frame_game.keypressedz == 0:
                self.nowstate = frame_game.RIGHT
            elif frame_game.keypressedz == 1:
                self.nowstate = frame_game.RIGHTDRAWING

        # 그림 그리고 있을 경우 그 자리에서 정지
        if frame_game.nowdrawing == 1:
            # 별 그리기 효과 표시
            frame_game.draweffect.update()
            self.yspd = 0

            # [별 그리기]에 필요한 기력보다 많이 있으면 [별 그리기]를 수행하고 아니라면 중단한다.
            if self.energynow >= self.drawneedenergy:
                self.energynow -= self.drawneedenergy
            else:
                frame_game.nowdrawing = 0
                self.energynow = 0

                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행


        # y 이동속도 상한, 하한 제한
        if self.yspd < YMINSPD: self.yspd = YMINSPD
        if self.yspd > YMAXSPD: self.yspd = YMAXSPD

        # 땅 위에 있을 경우
        if self.y < 130:
            self.y = 130
            self.yspd = 0

            # 날기 상태인 경우
            if self.cur_state == FLY:
                self.cur_state.exit(self)  # 현재 상태의 exit 동작을 수행한다.
                self.cur_state = IDLE  # IDLE 상태로 강제 이동
                self.cur_state.enter(self, None)  # 다음 상태 enter 동작 수행

            # 기력을 점차 회복한다
            if self.energynow < self.energymax:
                self.energynow += self.groundaddenergy
                if self.energynow > self.energymax:
                    self.energynow = self.energymax

        # 은비(플레이어) 이동 범위 제한

        if self.x < 0 + PLAYERXSIZE / 2:
            self.x = 0 + PLAYERXSIZE / 2
        if self.x > 680 - PLAYERXSIZE / 2:
            self.x = 680 - PLAYERXSIZE / 2
        if self.y < 120:
            self.y = 120
        if self.y > 700 - PLAYERYSIZE:
            self.y = 700 - PLAYERYSIZE
            self.yspd = 0

        pass

    # 그리기
    @staticmethod
    def draw(self):
        # 플레이어 그리기 (3픽셀은 임시 보정)
        self.image.clip_draw(self.frame * 40, abs(self.nowstate) * 50, 33, 43, self.x, self.y + 20)

        animationshow(self)  # 애니메이션 보여주기
        effectsdraw(self)  # 효과 그리기
        self.frame = 0  # 애니메이션 프레임 표시

        pass

    pass

# 이벤트 정의

EV_RD, EV_RU, EV_LD, EV_LU, EV_SPU, EV_ZD, EV_ZU = range(7)

# 이벤트 테이블

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): EV_RD, # 오른쪽 화살표키 누르기
    (SDL_KEYUP, SDLK_RIGHT): EV_RU, # 오른쪽 화살표키 떼기
    (SDL_KEYDOWN, SDLK_LEFT): EV_LD, # 왼쪽 화살표키 누르기
    (SDL_KEYUP, SDLK_LEFT): EV_LU, # 왼쪽 화살표키 떼기
    (SDL_KEYUP, SDLK_SPACE): EV_SPU, # 스페이스바 떼기
    (SDL_KEYDOWN, SDLK_z) : EV_ZD, # z키 누르기
    (SDL_KEYUP, SDLK_z) : EV_ZU, # z키 떼기
}

# 다음 상태

next_state = {

    # EV_LD, EV_RD (왼쪽, 오른쪽 화살표키 누르기) : WALK (좌우이동)
    # EV_SPU (스페이스바 떼기) : FLY (날기(점프))
    # EV_ZD (z키 누르기) : DRAW (별 그리기)
    # EV_ZU (z키 떼기) : IDLE

    IDLE: {EV_LD: WALK, EV_LU: IDLE, EV_RD: WALK, EV_RU: IDLE, EV_SPU: FLY, EV_ZD: DRAW, EV_ZU: IDLE},
    WALK: {EV_LD: WALK, EV_LU: IDLE, EV_RD: WALK, EV_RU: IDLE, EV_SPU: FLY, EV_ZD: DRAW, EV_ZU: IDLE},
    FLY:  {EV_LD: WALK, EV_LU: IDLE, EV_RD: WALK, EV_RU: IDLE, EV_SPU: FLY, EV_ZD: DRAW, EV_ZU: IDLE},
    DRAW: {EV_LD: WALK, EV_LU: IDLE, EV_RD: WALK, EV_RU: IDLE, EV_SPU: FLY, EV_ZD: DRAW, EV_ZU: IDLE},
}

# ------------ 플레이어 오브젝트 클래스 ------------

# 플레이어 오브젝트

class Player:
    player_keypressed = 0

    # 캐릭터 컨트롤러
    def handle_event(self, event):

        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.q.insert(0, key_event)

    # 초기화
    def __init__(self):
        self.image = load_image('characterimages.png')  # 캐릭터 이미지

        self.x, self.y = PLAYERXSTART, PLAYERYSTART  # 플레이어 좌표

        self.xspd = 8  # x축 이동속도
        self.yspd = 0  # y축 이동속도
        self.frame = 0  # 애니메이션 프레임

        self.LPamount = 100  # 체력
        self.EPamount = 100  # 기력

        self.yjumpamount = 11  # 날기(점프)시 이동하는 정도
        self.cooltime_quickmove = frame_game.UNSET  # 도약 쿨타임
        self.cooltime_warp = frame_game.UNSET  # 순간이동 쿨타임

        self.nowstate = frame_game.STOP # 현재 상태

        self.lifemax, self.energymax = 100, 100  # 시작시엔 최대 체력 100으로 시작
        self.lifenow, self.energynow = 100, 100  # 시작시엔 최대 기력 100으로 시작

        # (// 기력 관련 변수는 테스트하면서 값을 조정합니다)
        self.groundaddenergy = 2.4  # 땅에서 점점 회복되는 기력
        self.drawneedenergy = 3  # 그리는데 필요한 기력
        self.yjumpneedenergy = 7.5  # 날기(점프)에 필요한 기력

        self.q = [] # 이벤트 큐 초기화
        self.cur_state = IDLE # 현재 상태를 정지 상태로 지정
        self.cur_state.enter(self, None) # 초기 상태(IDLE) enter 동작 수행


    # 정보 갱신
    def update(self):
        self.cur_state.do(self)

        if self.q: # 큐에 이벤트가 있으면
            event = self.q.pop()
            print("### New Event")
            self.cur_state.exit(self) # 현재 상태의 exit 동작을 수행한다.
            self.cur_state = next_state[self.cur_state][event] # 다음 상태를 구한다
            self.cur_state.enter(self, event) # 다음 상태 enter 동작 수행

        pass

    # 그리기
    def draw(self):
        self.cur_state.draw(self)
        pass

    # x, y 각각 좌표만큼 이동
    def movexy(self, x, y):
        self.x += x
        self.y += y
        pass

    pass

# ----- 효과 그리기, 애니메이션 -----

# 효과 그리기

def effectsdraw(self):

    # 도약중일 경우 도약 효과 그리기
    if frame_game.nowdashl == 2:
        frame_game.quickmove.frame = 0
        frame_game.quickmove.draw(self.x + 20, self.y + 20)

    elif frame_game.nowdashr == 2:
        frame_game.quickmove.frame = 1
        frame_game.quickmove.draw(self.x - 20, self.y + 20)

    # 점프중일 경우 점프 이펙트 그리기
    if self.yspd > 0:
        frame_game.jumpeffect.draw(self.x, self.y - 5)

    # 현재 FLY 상태인 경우 날개 그리기
    if self.cur_state == FLY:
        frame_game.wingimage.update()
        frame_game.wingimage.draw(self.x, self.y + 20)

    # 그리는 중인 경우별 그리기 효과 표시
    if frame_game.nowdrawing == 1:
        if self.nowstate == frame_game.LEFTDRAWING:
            frame_game.draweffect.draw(self.x - 15, self.y + 17)
        elif self.nowstate == frame_game.RIGHTDRAWING:
            frame_game.draweffect.draw(self.x + 15, self.y + 17)


def animationshow(self):

    if frame_game.nowdashr == 1:  # 오른쪽 도약 실행시
        frame_game.nowdashr = 2
        frame_game.skillxcooltime = frame_game.nowskillxcooltime  # 대기시간 켜기
        self.x += frame_game.dashamount  # 오른쪽으로 크게 이동

    elif frame_game.nowdashl == 1:  # 왼쪽 도약 실행시
        frame_game.nowdashl = 2
        frame_game.skillxcooltime = frame_game.nowskillxcooltime  # 대기시간 켜기
        self.x -= frame_game.dashamount  # 왼쪽으로 크게 이동

    # 대기 시간 (쿨타임) 감소
    if frame_game.skillxcooltime > 0:
        frame_game.skillxcooltime -= 1
        # 대기 시간이 일정 비율 이하로 줄어들면 잔상표시 지우기
        if frame_game.skillxcooltime <= frame_game.nowskillxcooltime * (3 / 4):
            frame_game.nowdashr, frame_game.nowdashl = 0, 0

    delay(0.030)  # 프레임간 지연

    pass

# ------------ 은비(플레이어)와 관련 있는 오브젝트 ------------

# 점프 효과

class Jumpeffect:

    def __init__(self):
        self.image = load_image('jumpeffect.png')  # 날기(점프) 효과 이미지 (임시)

    def draw(self, x, y):
        self.image.draw(x, y)  # 날기(점프) 효과 이미지 그리기

    pass

# 도약 효과

class Quickmove:

    def __init__(self):
        self.image = load_image('quickmove.png')  # 도약 효과 이미지 그리기
        self.frame = 0  # 애니메이션 프레임

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 50, 0, 43, 43, x, y) # 도약 효과 그리기

    pass

# 날개 오브젝트

class Wingimage:

    def __init__(self):
        self.image = load_image('wingimg.png')  # 날개 이미지
        self.frame = 0  # 애니메이션 프레임
        self.dir = 0 # 날개 이동 방향

    def draw(self, x, y):
        self.image.clip_draw(0, self.frame * 24, 55, 14, x, y - self.frame * 4)  # 날기(점프) 효과 이미지 그리기

    def update(self):

        if self.dir == 0:
            if self.frame < 2:
                self.frame += 1
            elif self.frame == 2:
                self.dir = 1

        elif self.dir == 1:
            if self.frame > 0:
                self.frame -= 1
            elif self.frame == 0:
                self.dir = 0



    pass

# 별 그리기 효과 오브젝트

class Draweffect:

    def __init__(self):
        self.image = load_image('starlight.png')  # 날기(점프) 효과 이미지 (임시)
        self.frame = 0
        self.dir = 1

    def draw(self, x, y):
        self.image.clip_draw(self.frame * 30, 0, 20, 20, x, y)

    def update(self):
        if self.dir == 1:
            self.frame += 1
            if self.frame == 4:
                self.dir = 2

        elif self.dir == 2:
            self.frame -= 1
            if self.frame == 1:
                self.dir = 1

    pass

# ------------ 직접 실행시켰을 경우 ------------

def test_self():
    inputany = input("StarPainter.py 파일로 접속해주세요. 아무 키 눌러 종료")

if __name__ == '__main__':
    test_self()