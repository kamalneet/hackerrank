#!/bin/python3

# "RBG Queries"
# https://www.hackerrank.com/contests/hackerrank-hackfest-2020/challenges/rbg

import math
import os
import random
import re
import sys

#
# Complete the 'mixColors' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY colors
#  2. 2D_INTEGER_ARRAY queries
#

def mixColors(colors, queries):
    # One dict for each color. In each dict, key is the component value of that
    # color, value is a list of pairs of other two color components. The value
    # is later replaced by a list of only the important colors.
    d = [{}, {}, {}]
    for i,c in enumerate(colors):
        for ci, cval in enumerate(c):
            otherComponents = (c[(ci+1)%3], c[(ci+2)%3])
            if cval in d[ci]:
                d[ci][cval].add(otherComponents)
            else:
                s = set()
                s.add(otherComponents)
                d[ci][cval] = s

    # keep only the colors that matter. Sort by othercomponents[0], and keep
    # only the colors where we see a drop in othercomponents[1]. This forms the
    # frontier below which there exists no color.
    for dcol in d:
        for compVal, lst in dcol.items():
            lst = sorted(lst)
            # form the min frontier
            frontierLst = []
            mn = 100001 # little more than the max color component
            for oc in lst:
                if oc[1] < mn:
                    frontierLst.append(oc)
                    mn = oc[1]
            dcol[compVal] = frontierLst

    ret = []
    for q in queries:
        if reachable(q, d, colors):
            ret.append("YES")
        else:
            ret.append("NO")
    return ret

# ec: end/desired color
def reachable(ec, d, colors):
# we need to find three colors.
    for ci in range(3):
        if not colorReachable(ci, ec, d, colors):
            return False
    return True

# ci: color component index, 0-2
# ec: end/desired color
# returns true if there exists a color with ci component equal to ec[ci] and
# other components less than or equal to ec[other-two-components].
def colorReachable(ci, ec, d, colors):
    dcol = d[ci]
    if not ec[ci] in dcol:
        # none of the given colors has this value
        return False
    options = dcol[ec[ci]]
    endColorOtherComponents = (ec[(ci+1)%3], ec[(ci+2)%3])
    for otherComponents in options:
        compatible=True
        for i in range(2):
            if otherComponents[i] > endColorOtherComponents[i]:
                compatible = False
                break
        if compatible:
            return True
    return False

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    colors = []

    for _ in range(n):
        colors.append(list(map(int, input().rstrip().split())))

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = mixColors(colors, queries)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()

