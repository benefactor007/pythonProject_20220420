#!/usr/bin/python3.5

def min1(*args):
    res = args[0]
    for arg in args[1:]:
        if arg < res:
            res = arg
    return res


def min2(first, *rest):
    for arg in rest:
        if arg < first:
            first = arg
    return  first


def min3(*args):
    tmp = list(args)                # or, in python 2.4+: return sorted(args)[0]
    tmp.sort()
    return tmp[0]


if __name__ == '__main__':
    print(min1(3,4,1,2))
    print(min2('bb','aa'))
    print(min3([2,2],[1,1],[3,3]))