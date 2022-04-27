#!/usr/bin/env python3.5

import timer,sys
def F(x):
    return x

reps = 10000
repslist = list(range(reps))

def listComp():
    return  [F(x) for x in repslist]

def mapCall():
    return list(map(F, repslist))


if __name__ == '__main__':
    print(sys.version)
    print(list(map(F, repslist)))
    # for test in (listComp, mapCall):
    #     (bestof, (total, result)) = timer.bestoftotal(5, 1000, test)
    #     print('%-9s: %.5f => [%s...%s]' % (test.__name__, bestof, result[0], result[-1]))