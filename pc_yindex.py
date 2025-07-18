# encoding: utf-8
from math import ceil

sourceList = [2.27, 1.87, 3.68, 2.35, 15.7]

candidateList = [0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.5,1,2,3,5]

def calculateStep(range1, candidateList):
    # 定义候选步长（按优先级排序）
    best_step = None
    min_intervals = 4
    max_intervals = 10
    best_intervals = 10

    for step in candidateList:
        intervals = range1 / step
        if min_intervals < intervals < max_intervals:
            if intervals-6 < best_intervals-6:
                best_step, best_intervals = step, intervals

    # 若无匹配，取最接近的候选步长
    if not best_step:
        return None

    return best_step, best_intervals

if __name__ == '__main__':
    for range1 in sourceList:
        caculatedStep = calculateStep(range1, candidateList)
        print(caculatedStep)