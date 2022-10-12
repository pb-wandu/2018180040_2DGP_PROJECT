### [별그림자 이야기] Main 파일입니다

from pico2d import *    # pico2d 라이브러리 import
import game_framework   # 게임 프레임워크 임포트
import random           # 랜덤 라이브러리 import

import mainmenu         # 메인메뉴
import gamemenu         # 게임중 메뉴
# import upgrademenu      # 별그림자 회랑 (강화) 메뉴

# ------------ 변수들 ------------

# ------------ 상수들 ------------

WINDOWXSIZE = 1000  # 화면 x 크기
WINDOWYSIZE = 700   # 화면 y 크기

# ------------ [게임 실행] ------------

open_canvas(WINDOWXSIZE, WINDOWYSIZE) # 화면 열기

game_framework.run(mainmenu) # 메인메뉴 실행

close_canvas() # 화면 닫기

