### [별그림자 이야기] 스테이지 정보 파일입니다

# ------------ import 파일들, 상수들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import
import math               # 원주율, 삼각함수

UNSET = 999               # 아직 정해지지 않은 것

# ------------ 스테이지 관련 변수, 상수 ------------

nowgamestage = 11 # 현재 스테이지
nowcollectedstar = 0 # 현재 모은 별 (이 해당 스테이지의 요구 별 개수와 같다면 스테이지 클리어

nowlifelength = 0  # 전체 제력 대비 현재 체력 표시 길이
nowenergylength = 0  # 전체 기력 대비 현재 기력 표시 길이
lifeimageadjust = 0 # 왼쪽으로 정렬 이동값
energyimageadjust = 0 # 왼쪽으로 정렬 이동값

nowtimelength = 0 # 전체 시간 대비 현재 남은 시간 표시 길이
timeimageadjust = 0 # 왼쪽으로 정렬 이동값
TIMEMAX = 100 # 한 스테이지당 시간 (초 단위 아님)

# 각 스테이지별 시간 줄어드는 속도 // 수정중

timespd = \
    [[0.20, 0.21, 0.22, 0.23, 0.24],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET]]

# 각 스테이지별 시간 줄어드는 속도 (어려움 난이도) // 난이도 구분할 때 적용 예정
# 제작자 본인이 이 속도로 클리어 가능한 정도 안에서 적당히 적용합니다

timespd_promode = \
    [[0.75, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET]]

# 각 차원-지역 (스테이지)당 필요한 별 개수 (== 그려야 하는 목표지점)
needtocollectstar = \
    [[2, 3, 2, 3, 4],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET],
    [UNSET, UNSET, UNSET, UNSET, UNSET]]

starplaces = [None, None, None, None, None, None, None, None, None, None] # 별을 저장할 배열
planetobjs = [None, None, None, None, None, None, None, None, None, None] # 행성을 저장할 배열
moonobjs = [None, None, None, None, None, None, None, None, None, None] # 위성을 저장할 배열

stardrawed = [False, False, False, False, False, False, False, False, False, False] # 해당 위치에 별이 그려졌는지 확인

# ------------ 오브젝트 좌표들 ------------

# 스테이지 오브젝트 좌표 범위는 [10~670, 200~680]으로 지정합니다

starplacesset = [ # 별을 표시할 위치 [10~670, 200~680]
    [ [100, 500], [500, 240], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ], # 1-1
    [ [90, 450], [250, 220], [500, 680], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ], # 1-2
    [ [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ], # 1-3
    [ [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ], # 1-4
    [ [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET] ], # 1-5

    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],  # 2-1
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],  # 2-2
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],  # 2-3
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],  # 2-4
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],  # 2-5
]

planetplacesset = [ # 행성을 표시할 위치 (x, y) [10~670, 200~680]
    # 1-1
    [[300, 480], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]],
    # 1-2
    [[UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET], [UNSET, UNSET]]
]

moonplacesset = [ # 달을 표시할 위치 (x, y, 공전 반지름, 회전 각속도) [10~670, 200~680]
    # 1-1
    [[40, 240, 120, 0.01], [UNSET, UNSET, UNSET, UNSET], [UNSET, UNSET, UNSET, UNSET], [UNSET, UNSET, UNSET, UNSET]],
    # 1-2
    [[UNSET, UNSET, UNSET, UNSET], [UNSET, UNSET, UNSET, UNSET], [UNSET, UNSET, UNSET, UNSET], [UNSET, UNSET, UNSET, UNSET]]
]



