################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Sep 7, 2018

@author: prashant
'''

from collections import deque
from itertools import product
import sys
import time
import random
from timeit import default_timer as timer
import math


class Ai(object):
    
    def __init__(self, n, p, m, status_bar):
        self.n = n
        self.p = p
        self.m = m
        self.status_bar = status_bar
    
    def initial_state_generator(self, init=False):
        if init:
            try:
                self.h
                return self.h, self.v
            except:
                pass
        self.status_bar['text'] = 'Computing initial state using initial state generator.'
        target = int((self.n * self.n * self.p)/100)
        max_sq_size = int(math.sqrt(self.n * self.n - target+1))
        h = [[0]*self.n for _ in range(self.n+1)]
        v = [[0]*(self.n+1) for _ in range(self.n)]
        check = [[False]*self.n for _ in range(self.n)]
        
        def possible_sq(r, c, l):
            for i, j in product(range(r, r+l), range(c, c+l)):
                if check[i][j]:
                    return False
            return True
        
        def create_sq(r, c, l):
            for pi in range(c, c+l):
                h[r][pi] = 1
                h[r+l][pi] = 1
            for pi in range(r, r+l):
                v[pi][c] = 1
                v[pi][c+l] = 1
            for i, j in product(range(r, r+l), range(c, c+l)):
                check[i][j] = True
        
        total_area_used = 0
        while target>0:
            size = random.randint(1, max_sq_size)
            r = random.randint(0, self.n-size)
            c = random.randint(0, self.n-size)
            rem_grid_size = self.n - size+1
            for sz in range(-1, rem_grid_size**2):
                if sz>=0:
                    r = int(sz / rem_grid_size)
                    c = sz % rem_grid_size
                if possible_sq(r, c, size):
                    create_sq(r, c, size)
                    target -= 1
                    total_area_used += size*size
                    max_sq_size = int(math.sqrt(self.n * self.n - total_area_used - (target-1)))
                    break
            else:
                max_sq_size = size - 1
        self.h, self.v = h, v
        self.status_bar['text'] = 'Initial state created.'
        return h, v
    
    
    def get_next_state(self):
        for i in range(self.n+1):
            for j in range(self.n+1):
                if i<len(self.h) and j<len(self.h[0]) and self.h[i][j] == 1:
                    self.h[i][j] = 0
                    return self.h, self.v
                if i<len(self.v) and j<len(self.v[0]) and self.v[i][j] == 1:
                    self.v[i][j] = 0
                    return self.h, self.v
        return None, None
        
        
    def draw_stick(self, x, y, w, h, color):
        self.t.pencolor(color)
        self.t.penup()
        self.t.setposition(x, y)
        self.t.pendown()
        self.t.setposition(x+w, y+h)
    
    
    def draw_grid(self, h, v):
        w = 20
        o = [-40, 50]
#         for i in range(len(h)):
#             for j in range(len(h[0])):
#                 self.draw_stick(o[0]+j*w, o[1]-i*w, w, 0, 'white')
#         for i in range(len(v)):
#             for j in range(len(v[0])):
#                 self.draw_stick(o[0]+j*w, o[1]-i*w, 0, -w, 'white')
        self.t.clear()
        for i in range(len(h)):
            for j in range(len(h[0])):
                if h[i][j]==1:
                    self.draw_stick(o[0]+j*w, o[1]-i*w, w, 0, 'red')
        for i in range(len(v)):
            for j in range(len(v[0])):
                if v[i][j]==1:
                    self.draw_stick(o[0]+j*w, o[1]-i*w, 0, -w, 'red')
    
    def bfs(self, t, init_state=True):
        self.status_bar['text'] = 'Starting bfs.'
        start_time = timer()
        meta = {}
        self.t = t
        states = {}
        h, v = self.initial_state_generator(init_state)
        init_state = self.compress(h, v)
        meta['node_mem'] = sys.getsizeof(init_state)
        meta['queue_max_len'] = 1
        meta['total_node_count'] = 1
        queue = deque()
        states[init_state] = None
        queue.append(init_state)
        self.draw_grid(*self.decompress(init_state))
        if self.goal_test(init_state):
            self.status_bar['text'] = 'BFS is complete.'
            end_time = timer()
            meta['cost'] = 0
            meta['time'] = (end_time-start_time)
            meta['path'] = self.create_path(states, init_state)
            return meta
        lvl = 1
        while len(queue) > 0:
            q2 = deque()
            self.status_bar['text'] = 'Searching in level '+str(lvl)+' of bfs tree.'
            while len(queue) > 0:
                curr_state = queue.popleft()
                child_states = self.get_child_states(curr_state)
                for child in child_states:
                    if child in states:
                        continue
                    meta['total_node_count'] += 1
                    states[child] = curr_state
                    q2.append(child)
#                     sq = self.validity_test(child)
#                     self.draw_grid(*self.decompress(child))
#                     if sq!=-1: print("sq", sq)
#                     time.sleep(1)
                    if self.goal_test(child):
#                         print("cost:", lvl)
                        self.status_bar['text'] = 'BFS is complete.'
                        end_time = timer()
                        meta['cost'] = lvl
                        meta['time'] = (end_time-start_time)
                        meta['path'] = self.create_path(states, child)
                        return meta
                meta['queue_max_len'] = max(meta['queue_max_len'], len(queue)+len(q2))
#             print("lvl end:", lvl)
            lvl+=1
            queue = q2
        print("Couldn't find required state through bfs.")
        self.status_bar['text'] = "Couldn't find required state through bfs."
        # function ends here
    
    
    def dfs(self, t, init_state=True):
        self.status_bar['text'] = 'Starting dfs.'
        self.t = t
        start_time = timer()
        h, v = self.initial_state_generator(init_state)
        init_state = self.compress(h, v)
        self.draw_grid(*self.decompress(init_state))
        meta = {}
        meta['node_mem'] = sys.getsizeof(init_state)
        meta['stack_max_len'] = 1
        meta['total_node_count'] = 1
        meta['cost'] = -1
        meta['path'] = []
        vis = set()
        parents = self.d(init_state, vis, meta, 1)
        if parents is None:
            self.status_bar['text'] = "Couldn't find required state using dfs."
            print("Couldn't find required state using dfs.")
            return meta
        self.status_bar['text'] = 'Dfs is complete.'
        path = []
        cur_state = parents[None]
        while cur_state is not None:
            path.append(cur_state)
            meta['cost'] += 1
            cur_state = parents[cur_state]
        end_time = timer()
        meta['time'] = (end_time-start_time)
        meta['path'] = path
        return meta
    
    def d(self, state, vis, meta, depth):
        self.status_bar['text'] = 'Dfs in on depth '+str(depth)+'.'
        meta['stack_max_len'] = max(meta['stack_max_len'], depth)
        if state in vis:
            return None
        vis.add(state)
        if self.goal_test(state):
            return {None:state, state:None}
        child_states = self.get_child_states(state)
        for child in child_states:
            if child in vis:
                continue
            meta['total_node_count'] += 1
#             self.draw_grid(*self.decompress(child))
#             sq = self.validity_test(child)
#             if sq!=-1: print("sq", sq)
#             time.sleep(1)
            parents = self.d(child, vis, meta, depth+1)
            if parents is not None:
                parents[state] = child
                parents[None] = state
                return parents
        return None
    
    def create_next_state(self, mat, action):
        mat[action[0]][action[1]] ^= 1
    
    def get_child_states(self, state):
        h, v = self.decompress(state)
        for i in range(self.n+1):
            for j in range(self.n+1):
                if i<len(h) and j<len(h[0]) and h[i][j]==1:
                    self.create_next_state(h, (i, j))
                    yield self.compress(h, v)
                    self.create_next_state(h, (i, j))
                if i<len(v) and j<len(v[0]) and v[i][j]==1:
                    self.create_next_state(v, (i, j))
                    yield self.compress(h, v)
                    self.create_next_state(v, (i, j))
        # end of get_child_state function
    
    def goal_test(self, state):
        val_score = self.validity_test(state)
        if val_score == self.m:
            return True
        return False
    
    def validity_test(self, state):
        h, v = self.decompress(state)
        check_h = [[False]*len(row) for row in h]
        check_v = [[False]*len(row) for row in v]
        sq = 0
        for i in range(len(h)-1):
            for j in range(len(h[0])):
                if h[i][j]==0: continue
                x, y = i, j
                while y >= 0:
                    if h[x][y]==0:
                        y = -1
                        break
                    if v[x][y]==1:
                        break
                    y -= 1
                if y < 0:
                    continue
                l = y+1
                while l < len(v[0]):
                    if h[x][l-1]==0:
                        l = len(v[0])
                        break
                    if v[x][l]==1:
                        break
                    l += 1
                if l >= len(v[0]):
                    continue
                
                l = l - y
                
                c = False
                for pi in range(y, y+l):
                    if x>=len(h) or x+l>=len(h) or pi>=len(h[0]):
                        c = True
                        break
                    if h[x][pi]==0 or h[x+l][pi]==0:
                        c = True
                        break
                for pi in range(x, x+l):
                    if y>=len(v[0]) or y+l>=len(v[0]) or pi>=len(v):
                        c = True
                        break
                    if v[pi][y]==0 or v[pi][y+l]==0:
                        c = True
                        break
                for xx, yy in product(range(x, x+l), range(y, y+l)):
                    if xx!=x and xx!=x+l and xx<len(h) and yy<len(h[0]) and h[xx][yy]==1:
                        c = True
                        break
                    if yy!=y and yy!=y+l and xx<len(v) and yy<len(v[0]) and v[xx][yy]==1:
                        c = True
                        break
                if c:
                    continue
                c = True
                for pi in range(y, y+l):
                    if check_h[x][pi]==False or check_h[x+l][pi]==False:
                        c = False
                for pi in range(x, x+l):
                    if check_v[pi][y]==False or check_v[pi][y+l]==False:
                        c = False
                if c:
                    continue
                for pi in range(y, y+l):
                    check_h[x][pi] = True
                    check_h[x+l][pi] = True
                for pi in range(x, x+l):
                    check_v[pi][y] = True
                    check_v[pi][y+l] = True
                sq += 1
        for i in range(self.n+1):
            for j in range(self.n+1):
                if i<len(h) and j<len(h[0]) and h[i][j]==1 and check_h[i][j]==False:
                    return -1
                if i<len(v) and j<len(v[0]) and v[i][j]==1 and check_v[i][j]==False:
                    return -1
        return sq
        # function ends here
    
    
    def create_path(self, states, final_state):
        path = []
        while final_state is not None:
            path.append(final_state)
            final_state = states[final_state]
        return path[::-1]
    
    
    def compress(self, h, v):
        h_str = ' '.join([''.join(map(str, row)) for row in h])
        v_str = ' '.join([''.join(map(str, row)) for row in v])
        return h_str+'+'+v_str
    
    def decompress(self, state):
        toks = state.split('+')
        h = [list(map(int, s)) for s in toks[0].split(' ')]
        v = [list(map(int, s)) for s in toks[1].split(' ')]
        return h, v
    
    
    
    