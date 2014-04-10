#!/usr/bin/env python
import sys
from streetview import readfile
import copy

_, _, T, C, S, _, _, cost, truelength, _ = readfile('paris_54000.txt')
length = copy.deepcopy(truelength)

def checksol(filename):
    sol = open(filename)
    cars = int(sol.readline())
    if cars != C:
        sys.exit('Wrong number of cars.')
    grand_total = 0
    for i in range(cars):
        total_cost = 0
        total_length = 0
        total_true = 0
        path_len = int(sol.readline())
        s = S
        start = int(sol.readline())
        if start != s:
            sys.exit('Wrong starting point for car %s.' % str(i+1))
        for _ in range(1, path_len):
            try:
                t = int(sol.readline())
                total_cost += cost[s][t]
                total_length += length[s][t]
                total_true += truelength[s][t]
                length[s][t] = 0
                length[t][s] = 0
                s = t
            except KeyError:
                sys.exit('Error: attempting to go from %s to %s.' % (s,t))
        print('Car %s: %s meters (%s valid) in %s seconds.' % (str(i+1), total_true, total_length, total_cost))
        grand_total += total_length

    print 'Total: %s.' % grand_total
    
if __name__ == '__main__':
    checksol(sys.argv[1])
