#!/usr/bin/env python3.5

# file timer3.py (3.X only)

"""
same usage as timer2.py, but uses 3.X keyword-only default arguments instead of dict pops for simpler code, no
need to hoist range() out of test in 3.X: always a generator in 3.X, and this can't run on 2.X.
"""

import time, sys

try:
    timer = time.perf_counter
except:
    timer = time.clock if sys.platform[:3] == 'win' else time.time

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


def spam(a, b, c, d):
    return a + b + c + d


def total(func, *args, _reps=1000, **kwargs):
    start = timer()
    for i in range(_reps):
        ret = func(*args, **kwargs)
    elapsed = timer() - start
    return (elapsed, ret)


def bestof(func, *args, _reps=5, **kwargs):
    best = 2 ** 32
    for i in range(_reps):
        start = timer()
        ret = func(*args, **kwargs)
        elapsed = timer() - start
        if elapsed < best: best = elapsed
    return (best, ret)


def bestoftotal(func, *args, _reps1=5, **kwargs):
    return min(total(func, *args, **kwargs) for i in range(_reps1))


def F():
    return [x**2 for x in range(1000)]

def L():
    L = [1,2,3,4,5]
    i = 0
    while i < len(L):
        L[i] += 1
        i += 1

# jpcc@ubuntu:~$ python3 -m timeit -n 1000 "[x ** 2 for x in range(1000)]"
# 1000 loops, best of 5: 279 usec per loop
# jpcc@ubuntu:~$ python2.7 -m timeit -n 1000 "[x ** 2 for x in range(1000)]"
# 1000 loops, best of 3: 62 usec per loop
# jpcc@ubuntu:~$ python2.7 -m timeit -n 1000 -r 5 "[x ** 2 for x in range(1000)]"
# 1000 loops, best of 5: 57.6 usec per loop
# jpcc@ubuntu:~$ python3 -m timeit -n 1000 -r 3 "L = [1,2,3,4,5]" "i=0" "while i< len(L):" " L[i] += 1" " i += 1"
# 1000 loops, best of 3: 725 nsec per loop

import timeit

if __name__ == '__main__':
    for test in (forLoop, listComp, mapCall, genExpr, genFunc):
        (a, b) = bestoftotal(test,_reps1=5,_reps =1000)
        print('%-9s:%.5f => [%s...%s]' % (test.__name__, a, b[0], b[-1]))
    # print(total(pow,2,1000)[0])
    # print(total(listComp)[0])
    # print(bestoftotal(F,_reps1=10,_reps =10000)[0])
    # print(min(timeit.repeat(number = 1000, repeat = 3, stmt = "L = [1,2,3,4,5]\ni=0\nwhile i < len(L):\n\tL[i] += 1\n\t"
    #                                                           "i += 1")))
    # print(bestoftotal(L, _reps1=3, _reps=1000)[0])
    #
    # print(min(timeit.repeat(number = 1000, repeat= 3, setup= "from mins import min1,min2,min3\n")))