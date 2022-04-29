#!/usr/bin/env python3.5

def intersect(*args):
    res = []
    for x in args[0]:                                   # Scan first sequence
        if x in res: continue                          # Skip duplicate
        for other in args[1:]:                          # for all other args
            if x not in other: break                    # Item in each one?
        else:                                           # no: break out of loop
            res.append(x)                               # yes: add items to end
    return res


def union(*args):
    res = []
    for seq in args:                                    # for all args
        for x in seq:                                   # for all nodes
            if not x in res:
                res.append(x)                           # add new items to result
    return res


def tester(func, items, trace =True):
    for i in range(len(items)):
        items = items[1:] + items[:1]
        if trace:
            print(items)
        print(sorted(func(*items)))


s1,s2,s3 = "SPAM","SCAM","SLAM"

if __name__ == '__main__':
    print(intersect(s1,s2))
    print(union(s1,s2))
    # print(tester(intersect,('a','abcdefg','abdst','albmcnd')))
    print(tester(intersect, (s1,s2,s3)))
    print(tester(union,(s1,s2,s3)))