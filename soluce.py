#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from streetview import *
from choice import bfs, blf, update
from collections import defaultdict
import random
import operator

def create_answer(V):

    f = open('answer.txt', 'w')
    f.write('%s\n' % len(V))
    for v in V:
        f.write('%s\n' % len(v)) # nb intersections visitees par ci
        for edge in v:
            f.write('%s\n' % edge)

def choix(s, cost, length, score, covered):
    #max_score = 0
    #J = 0
    #ratios = []
    #for j in cost[s].keys():
    #    ratio = float(length[s][j]) / cost[s][j]
    #    ratios.append(ratio)
    #    if ratio >= max_ratio: # and boucle(path):
    #        J = j
    #        max_ratio = ratio
    
    J = max(score[s].keys(), key=score[s].get)
    max_score = score[s][J]

    # print ('min ratio:', min(ratios))
    # print ('max ratio:', max(ratios))
    ratio = length[s][J] / cost[s][J]
    pen = penalty(cost[s][J], covered[s][J], ratio)

    score[s][J] /= pen
    # if length[s][J] < 0:
    #     length[s][J] = 0
    if J in length and s in length[J]:
        score[J][s] /= pen

    return (J, cost[s][J], score, max_score)

# from http://stackoverflow.com/questions/4997851/python-dijkstra-algorithm
def dijkstra(net, s, t):
    # sanity check
    if s == t:
        return "The start and terminal nodes are the same. Minimum distance is 0."
    if net.has_key(s)==False:
        return "There is no start node called " + str(s) + "."
    if net.has_key(t)==False:
        return "There is no terminal node called " + str(t) + "."
    # create a labels dictionary
    labels={}
    # record whether a label was updated
    order={}
    # populate an initial labels dictionary
    for i in net.keys():
        if i == s: labels[i] = 0 # shortest distance form s to s is 0
        else: labels[i] = float("inf") # initial labels are infinity
    from copy import copy
    drop1 = copy(labels) # used for looping
    ## begin algorithm
    while len(drop1) > 0:
        # find the key with the lowest label
        minNode = min(drop1, key = drop1.get) #minNode is the node with the smallest label
        # update labels for nodes that are connected to minNode
        for i in net[minNode]:
            if labels[i] > (labels[minNode] + net[minNode][i]):
                labels[i] = labels[minNode] + net[minNode][i]
                drop1[i] = labels[minNode] + net[minNode][i]
                order[i] = minNode
        del drop1[minNode] # once a node has been visited, it's excluded from drop1
    ## end algorithm
    # print shortest path
    temp = copy(t)
    rpath = []
    path = []
    while 1:
        rpath.append(temp)
        if order.has_key(temp): temp = order[temp]
        else: return "There is no path from " + str(s) + " to " + str(t) + "."
        if temp == s:
            rpath.append(temp)
            break
    for j in range(len(rpath)-2,-1,-1):
        path.append(rpath[j])

    return path, labels[t]
    # return "The shortest path from " + s + " to " + t + " is " + str(path) + ". Minimum distance is " + str(labels[t]) + "."

# Given a large random network find the shortest path from '0' to '5'
# print dijkstra(net=randNet(), s='0', t='5')

# deplace une voiture
def deplace1V(cost, length, score, S, T, first, visited, covered):

    path = [S]
    c = 0
    s = S

    steps = 0

    #limit = 0.5
    #looplength = 6
    #loop = [False] * looplength
    #counter = 0
    loopcost = 0
    threshold = 1800

    dpath, t = dijkstra(cost, S, first)
    c += t
    for p in dpath:
        path.append(p)
    s = p

    while c < T:
        #if all(loop):
        if loopcost > threshold:
            print 'jump...'
            notvisited = list(set(range(N)) - visited)
            nextfirst = random.choice(notvisited)
            dpath, t = dijkstra(cost, s, nextfirst)
            print 'done'
            for i in range(len(dpath)-1):
                path.append(dpath[i])
                visited.add(dpath[i])
                covered[dpath[i]][dpath[i+1]] += 1
                try:
                    covered[dpath[i+1]][dpath[i]] += 1
                except KeyError:
                    pass
            path.append(dpath[-1])
            visited.add(dpath[-1])
            s = dpath[-1]
            #loop = [False] * looplength
            loopcost = 0
        else:
            #r, t, score, max_score = choix(s, cost, length, score, covered)
            #if (c + t) <= T:
            #    path.append(r)
            #    visited.add(r)
            #    covered[s][r] += 1
            #    try:
            #        covered[r][s] += 1
            #    except KeyError:
            #        pass
            #    s = r
            #counter += 1
            #loop[counter % looplength] = (max_score < limit)
            bp, ms = blf(s, 8, score, [])
            update(bp, visited, covered, score, cost, ratio)
            path.extend(bp[1:])
            s = bp[-1]
            t = sum(cost[bp[i]][bp[i+1]] for i in range(len(bp)-1))
            loopcost = 0 if covered[path[-2]][path[-1]] < 2 else loopcost + t
        c += t

    print 'c', c
    return (path, length)

if __name__ == '__main__':

    print 'reading map'
    #N, M, T, C, S, coord, edges, cost, length, ratio = readfile('paris_54000.txt')
    N, M, T, C, S, coord, edges, cost, length, ratio = readfile('paris_432000.txt')

    print 'N, M, T, C, S'
    print N, M, T, C, S

    visited = set() # for nodes
    covered = defaultdict(defaultdict) # for edges
    score = defaultdict(defaultdict)
    for (s, t) in edges:
        score[s][t] = ratio[s][t]
        covered[s][t] = 0

    print 'choosing path'

    start = [1000, 250, 140, 4000, 5000, 152, 79, 8000]
    #start = random.sample(range(N), 8)
    print 'starting destinations: %s' % start
    V = []
    
    for i in range(C):
        print 'car %s' % str(i+1)
        (path, length) = deplace1V(cost, length, score, S, T, start[i], visited, covered)
        path = trim(path, T, cost)
        V.append(path)

    print sorted([(i,j,covered[i][j]) for (i,j) in edges], key=operator.itemgetter(2))[-20:]
    print 'writing answer'
    create_answer(V)
