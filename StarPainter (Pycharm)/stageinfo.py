### [별그림자 이야기] 스테이지 정보 파일입니다

# ------------ import 파일들, 상수들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import

UNSET = 999               # 아직 정해지지 않은 것

# ------------ 스테이지 관련 변수들 ------------

# 각 차원-지역 (스테이지)당 필요한 별 개수 (== 그려야 하는 목표지점)
needtocollectstar = \
    [[2, 4, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET]]

starplaces = [None, None, None, None, None, None, None, None, None, None] # 별을 저장할 배열
planetobjs = [None, None, None, None, None, None, None, None, None, None] # 행성을 저장할 배열

# 스테이지 오브젝트 좌표 범위는 [10~670, 200~690]으로 지정합니다

starplacesset = [ # 별을 표시할 위치
    # 1-1
    [ [100, 500], [500, 240], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ],
    # 1-2
    [ [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ]
]

planetplacesset = [ # 행성을 표시할 위치
    # 1-1
    [[300, 480], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],
    # 1-2
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]]
]


