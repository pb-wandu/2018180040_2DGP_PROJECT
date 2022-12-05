### [별그림자 이야기] BGM, 효과음 실행 파일입니다

# ------------ import 파일들 ------------

import frame_main         # 메인 메뉴
import frame_game         # 게임 메뉴
import frame_info         # 정보 메뉴
import frame_upgrade      # 강화 메뉴 (별그림자 회랑)

# ------------ 변수, 상수 ------------

ON, OFF = 1, 0                    # 배경음악 켜기, 끄기
BGMNORMAL, BGMUPGRADE = 11, 12    # 일반 배경음, 별그림자 회랑 배경음

nowbgm = None                     # 현재 배경음 여부

bgm = None                        # 현재 실행중 배경음
nowwingeffectsound = None          # 현재 날기 효과음