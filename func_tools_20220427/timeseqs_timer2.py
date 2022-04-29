#!/usr/bin/env python3.5

import sys, timer2

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


def spam(a,b,c,d):
    return a+b+c+d

if __name__ == '__main__':
    for test in (forLoop, listComp, mapCall,genExpr, genFunc):
        (total,result) = timer2.bestoftotal(test,_reps1=5,_reps=1000)
        print('%-9s:%.5f => [%s...%s]'% (test.__name__,total,result[0],result[-1]))
    # print(timer2.total(pow,2,1000,_reps=1000000)[0])
    # print(timer2.total(pow,2,1000,_reps=1000)[0])
    # print(timer2.bestof(pow,2,100000)[0])
    # print(timer2.bestof(pow,2,100000,_reps=30)[0])
    # print(timer2.total(spam,1,2,c=3,d=4,_reps=1000))
    # print(timer2.bestoftotal(spam,1,2,c=3,d=4,_reps1=100,_reps=1000))
    # print(timer2.bestoftotal(spam,*(1,2),_reps1=100,_reps=1000,**dict(c=3,d=4)))