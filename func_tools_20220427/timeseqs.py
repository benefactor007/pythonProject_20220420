#!/usr/bin/env python3.5

"""
Test the relative speed of iteration tool alternatives
"""

import sys, timer  # import timer functions

reps = 10000
reps_list = list(range(reps))  # Hoist(hang) out, list in both 2.X/3.X


def forLoop():
    res = []
    for x in reps_list:
        res.append(abs(x))
    return res


def listComp():
    return [abs(x) for x in reps_list]


def mapCall():
    return list(map(abs, reps_list))  # use list() here in 3.X only


def genExpr():
    return list(abs(x) for x in reps_list)  # list() required to force results


def genFunc():
    def gen():
        for x in reps_list:
            yield abs(x)
    return list(gen())  # list() required to force results


if __name__ == '__main__':
    print(sys.version)
    # for test in (forLoop, listComp, mapCall, genExpr, genFunc):
    #     (bestof, (total, result)) = timer.bestoftotal(5, 1000, test)
    #     print('%-9s: %.5f => [%s...%s]' % (test.__name__, bestof, result[0], result[-1]))
    print(timer.total(10000,mapCall)[0])
    print(timer.bestof(10000,mapCall)[0])
    print(timer.bestoftotal(5,10000,mapCall)[0])
