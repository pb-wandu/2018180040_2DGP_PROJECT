### [게임 월드] 파일입니다

# ------------ import 파일들, 상수들 ------------

from pico2d import *      # pico2d 라이브러리 import
import game_framework     # 게임 프레임워크 import

import frame_game         # 은비(플레이어) 변수 등 import
import gameobjects        # 게임 오브젝트 import

UNSET = 999         # 아직 정해지지 않은 것

lifeenergybar, lifeimage, energyimage = None, None, None # 바탕, 체력, 기력 이미지

# ------------ 게임 월드 기본 설정 ------------

# [레이어] : 숫자가 클 수록 앞에 보입니다

# layer 2: 플레이어
# layer 1: 플레이어 이외 스테이지 오브젝트
# layer 0: 배경, 땅, 그 외 UI

gameobjectsarr = [[], [], []]

collision_group = dict()

# 오브젝트 1개 더하기
def add_object(obj, depth):
    gameobjectsarr[depth].append(obj)
    pass

# 오브젝트 여러개 더하기
def add_objects(objs, depth):
    gameobjectsarr[depth] += objs
    pass

# 오브젝트 제거하기
def remove_object(obj):
    for layer in gameobjectsarr:
        if obj in layer:
            layer.remove(obj)

            remove_collision_object(obj)

            del obj
            return
    raise ValueError('Trying destroy non existing object')

# 게임 월드의 모든 오브젝트 꺼내오기
def all_objects():
    for layer in gameobjectsarr:
        for o in layer:
            yield o

# 게임 월드의 모든 오브젝트 지우기
def clear_all_objects():
    for obj in all_objects():
        del obj
    for layer in gameobjectsarr:
        layer.clear()

# 충돌 대상 더하기
def add_collision_pairs(a, b, group):
    if group not in collision_group:
        print('add new group')
        collision_group[group] = [ [], [] ]

    if a:
        if type(a) == list:
            collision_group[group][0] += a # 리스트 추가
        else:
            collision_group[group][0].append(a) # 단일 오브젝트 추가

    if b:
        if type(b) == list:
            collision_group[group][1] += b # 리스트 추가
        else:
            collision_group[group][1].append(b) # 단일 오브젝트 추가

# 모든 충돌 쌍들
def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group

# 충돌 오브젝트 제거
def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]: pairs[0].remove(o)
        elif o in pairs[1]: pairs[1].remove(o)
