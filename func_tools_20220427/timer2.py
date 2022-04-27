#!/usr/bin/env python3.5
# File timer2.py (2.X and 3.X)
"""
total(spam,1,2,a=3,b=4,_reps=1000) calls and times spam(1,2,a =3, b=4)
_reps times, and returns total time for all rns, with final result

best of (spam,1,2,a=3,b-4,_reps=5) runs best-of-N timer to attempt to filter out system load variation,
and returns best time among _reps tests.

bestoftotal(spam, 1,2,a=3,b=4, _rep1=5, reps=1000) runs best-of-totals test, which takes the best among _reps1 runs
of (the total of _reps runs);

"""

import time,sys

try:
    timer = time.perf_counter
except:
    timer = time.clock if sys.platform[:3] == 'win' else time.time

def total(func, *args,**kwargs):
    _reps = kwargs.pop('_reps', 1000)           # passed-in or efault reps
    print(_reps)
    repslist = list(range(_reps))               # hoist(hang) range out for 2.X lists
    start = timer()
    for i in repslist:
        ret = func(*args,**kwargs)
    elapsed = timer() - start
    return (elapsed,ret)


if __name__ == '__main__':
    print(total(pow,2,1000,))