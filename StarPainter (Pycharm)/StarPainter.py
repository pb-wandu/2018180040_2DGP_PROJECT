### [별그림자 이야기] 시작시 실행하는 파일입니다

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 임포트

import frame_main         # 메인메뉴

# ------------ [게임 실행] ------------

open_canvas(frame_main.WINDOWXSIZE, frame_main.WINDOWYSIZE) # 화면 열기

game_framework.run(frame_main) # 메인메뉴 실행

close_canvas() # 화면 닫기

