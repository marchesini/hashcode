#!/usr/bin/env python
from __future__ import division
from streetview import penalty
from copy import deepcopy as dpc

def bfs(s, steps, score, covered, cost, ratio):
    print 'steps: %s' % steps
    if steps == 0:
        return [s], 0, score, covered
    max_path_score = -1
    ts = score[s].keys()
    for t in ts:
        print 'checking (%s, %s)' % (s, t)
        bp, mps, ups, upc = bfs(t, steps-1, dpc(score), dpc(covered), cost, ratio)
        if ups[s][t] + mps > max_path_score:
            T = t
            max_path_score = ups[s][t] + mps
            print 'ups + mps = %s + %s' % (ups[s][t], mps)
            best_path = [s] + bp
            pen = penalty(cost[s][t], upc[s][t], ratio[s][t])
            print 'cost, cov, ratio = %s, %s, %s' % (cost[s][t], upc[s][t], ratio[s][t])
            ups_bp = [(x, ups[x]) for x in best_path]
            upc_bp = [(x, upc[x]) for x in best_path]
    updated_score = score
    for (x, y) in ups_bp:
        updated_score[x] = y
    updated_score[s][T] /= pen
    print 'updated score (%s, %s) from %s to %s (pen = %s)' % (s, T, updated_score[s][T] * pen, updated_score[s][T], pen)
    updated_covered = covered
    for (x, y) in upc_bp:
        updated_covered[x] = y
    updated_covered[s][T] += 1
    try:
        updated_score[T][s] /= pen
        updated_covered[T][s] += 1
    except KeyError:
        pass
    print updated_score[s], updated_covered[s]
    return best_path, max_path_score, updated_score, updated_covered
    
    
def blf(s, steps, score, forbidden):
# Best Loop-Free path of length steps starting from s
    if steps == 0:
        return ([s], 0)
    best_path = None
    max_score = -1
    ts = score[s].keys()
    for t in ts:
        if (s, t) not in forbidden:
            bp, ms = blf(t, steps-1, score, forbidden + [(s, t)])
            if bp is not None and score[s][t] + ms > max_score:
                max_score = score[s][t] + ms
                best_path = [s] + bp
    return (best_path, max_score)
    

def update(path, visited, covered, score, cost, ratio):
    visited.union(path)
    for i in range(len(path)-1):
        s, t = path[i], path[i+1]
        covered[s][t] += 1
        #pen = penalty(cost[s][t], covered[s][t], ratio[s][t])
        #score[s][t] /= pen
        score[s][t] = 0
        try:
            covered[t][s] += 1
            #score[t][s] /= pen
            score[t][s] = 0
        except KeyError:
            pass

