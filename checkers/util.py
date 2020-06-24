################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Oct 14, 2018

@author: prashant
'''

import copy
import random
import time
from itertools import combinations

class Ai():
    
    def __init__(self):
        self.o = (-100, 50)
        self.hor = 50
        self.ver = 100
        self.radius = 15
        self.pos_value = {}
        for i in range(1, 6):
            x = self.o[0]+abs(i-3)*self.hor
            y = self.o[1]-(i-1)*self.ver
            n = 6 - abs(i-3)
            for j in range(n):
                if i==0 or i==5 or j==0 or j==n-1:
                    self.pos_value[(x+2*j*self.hor, y+self.radius)] = 3
                elif j==1 or j==n-2:
                    self.pos_value[(x+2*j*self.hor, y+self.radius)] = 2
                else:
                    self.pos_value[(x+2*j*self.hor, y+self.radius)] = 1
        # end of init
        
    def initial_state_generator(self):
        centers = {}
        pos = []
        for i in range(1, 6):
            x = self.o[0]+abs(i-3)*self.hor
            y = self.o[1]-(i-1)*self.ver
            n = 6 - abs(i-3)
            p = []
            for j in range(n):
                centers[(x+2*j*self.hor, y+self.radius)] = 0
                p.append((x+2*j*self.hor, y+self.radius))
            pos.append(p)
        p1_pos = [(0, 0),
                  (1, 0), (1, 1), (1, 2), (1, 4),
                  (2, 0), (2, 3), (2, 5),
                  (3, 2),
                  (4, 0)]
        p2_pos = [(0, 2), (0, 3),
                  (1, 3),
                  (2, 1), (2, 2), (2, 4),
                  (3, 4),
                  (4, 1), (4, 2), (4, 3)]
        for x, y in p1_pos:
            centers[pos[x][y]] = 1
        for x, y in p2_pos:
            centers[pos[x][y]] = 2
        self.centers = centers
        self.pos = pos
        return centers
    
    def successor_function(self, state, player):
        try:
            centers = copy.deepcopy(state)
            steps = [(-2*self.hor, 0), (2*self.hor, 0), (-self.hor, self.ver),
                     (-self.hor, -self.ver), (self.hor, self.ver), (self.hor, -self.ver)]
            random.shuffle(steps)
            for pos in centers.keys():
                if centers[pos] != player:
                    continue
                for dx, dy in steps:
                    try:
                        mid = (pos[0]+dx, pos[1]+dy)
                        nxt = (pos[0]+2*dx, pos[1]+2*dy)
                        if centers[nxt]==0 and centers[mid]!=player and centers[mid]!=0:
                            centers[pos], centers[nxt] = 0, player
                            centers[mid] = 0
                            yield centers
                            centers[mid] = 1 if player==2 else 2
                            centers[pos], centers[nxt] = player, 0
                    except GeneratorExit:
                        return
                    except:
                        pass
            for pos in centers.keys():
                if centers[pos] != player:
                    continue
                for dx, dy in steps:
                    try:
                        nxt = (pos[0]+dx, pos[1]+dy)
                        if centers[nxt] == 0:
                            centers[pos], centers[nxt] = 0, player
                            yield centers
                            centers[pos], centers[nxt] = player, 0
                    except GeneratorExit:
                        return
                    except:
                        pass
        except:
            return
        # end of function
    
    def terminal_states_generator(self):
        self.terminal_states = set()
        self.terminal_states.add(tuple([0]*24))
        idx = range(24)
        for i in range(1, 9):
            for c in combinations(idx, i):
                p1 = tuple(1 if j in c else 0 for j in range(24))
                p2 = tuple(2 if j in c else 0 for j in range(24))
                self.terminal_states.add(p1)
                self.terminal_states.add(p2)
        # end of function
    
    def terminal_test(self, state):
#         if type(state) != tuple:
#             state = self.compress(state)
#         try:
#             self.terminal_states
#         except:
#             self.terminal_states_generator()
#         if state in self.terminal_states:
#             return True
#         return False
        steps = [(-2*self.hor, 0), (2*self.hor, 0), (-self.hor, self.ver),
                 (-self.hor, -self.ver), (self.hor, self.ver), (self.hor, -self.ver)]
        cnt = [0, 0, 0]
        move_possible = False
        for pos in state.keys():
            cnt[state[pos]] += 1
            for dx, dy in steps:
                try:
                    nxt = (pos[0]+dx, pos[1]+dy)
                    if state[nxt] == 0:
                        move_possible = True
                    mid = nxt
                    nxt = (mid[0]+dx, mid[1]+dy)
                    if state[nxt]==0 and state[mid]!=state[pos]:
                        move_possible = True
                except: pass
        if cnt[1]==0 or cnt[2]==0:
            return True
        if not move_possible:
            return True
        return False
        
    def utility_value(self, state):
        cnt = [0, 0, 0]
        for pos in state.keys():
            cnt[state[pos]] += 1#self.pos_value[pos]
        return cnt[1]-cnt[2]
    
    def min_value(self, state, depth):
        self.iter += 1
        if self.terminal_test(state) or depth<=0:
            return self.utility_value(state)
        value = 1000
        for child in self.successor_function(state, 2):
            if self.compress(child) in self.vis:
                continue     
            value = min(value, self.max_value(child, depth-1))
        return value
    
    def max_value(self, state, depth):
        self.iter += 1
        if self.terminal_test(state) or depth<=0:
            return self.utility_value(state)
        value = -1000
        for child in self.successor_function(state, 1):
            if self.compress(child) in self.vis:
                continue
            value = max(value, self.min_value(child, depth-1))
        return value
        
    def minmax(self, state, color, screen):
        print("Calculating next move using minmax algo...", end='')
        if self.terminal_test(state):
            return None, None # game over
        minv = 0
        cs = None
        self.color = color
        self.screen = screen
        self.iter = 0
        self.vis = {self.compress(state):True}
        depth = 3
        for child in self.successor_function(copy.deepcopy(state), 2):
            if cs is None:
                #minv = self.dfs(copy.deepcopy(child), True, depth)
                minv = self.min_value(copy.deepcopy(child), depth)
                cs = copy.deepcopy(child)
            else:
                if self.compress(child) in self.vis:
                    continue
                #value = self.dfs(copy.deepcopy(child), True, depth)
                value = self.min_value(copy.deepcopy(child), depth)
                if value < minv:
                    minv = value
                    cs = copy.deepcopy(child)
        print("done")
        p, n = None, None
        for pos in state:
            if state[pos]==2 and cs[pos]==0:
                p = pos
            elif state[pos]==0 and cs[pos]==2:
                n = pos
        return p, n
    
    def alphabeta(self, state, color, screen):
        print("Calculating next move using alpha-beta algo...", end='')
        if self.terminal_test(state):
            return None, None # game over
        cs = None
        self.color = color
        self.screen = screen
        self.iter = 0
        self.vis = {self.compress(state):[False, False]}
        depth = 6
        v = self.ab_min_value(state, depth, -10000, 100000)
        for child in self.successor_function(copy.deepcopy(state), 2):
            if self.vis[self.compress(child)][0] == v:
                cs = copy.deepcopy(child)
                break
        print("done")
        p, n = None, None
        for pos in state:
            if state[pos]==2 and cs[pos]==0:
                p = pos
            elif state[pos]==0 and cs[pos]==2:
                n = pos
        return p, n
    
    def ab_max_value(self, state, depth, alpha, beta):
        self.iter += 1
        comp = self.compress(state)
        if comp in self.vis:
            if self.vis[comp][0]:
                return self.vis[comp][0]
        else:
            self.vis[comp] = [False, False]
        if self.terminal_test(state) or depth<=0:
            self.vis[comp][0] = self.utility_value(state)
            return self.vis[comp][0]
        v = -10000
        for child in self.successor_function(state, 1):
            v = max(v, self.ab_min_value(child, depth-1, alpha, beta))
            if v >= beta:
                self.vis[comp][0] = v
                return v
            alpha = max(alpha, v)
        self.vis[comp][0] = v
        return v
    
    def ab_min_value(self, state, depth, alpha, beta):
        self.iter += 1
        comp = self.compress(state)
        if comp in self.vis:
            if self.vis[comp][1]:
                return self.vis[comp][1]
        else:
            self.vis[comp] = [False, False]
        if self.terminal_test(state) or depth<=0:
            self.vis[comp][1] = self.utility_value(state)
            return self.vis[comp][1]
        v = 10000
        for child in self.successor_function(state, 2):
            v = min(v, self.ab_max_value(child, depth-1, alpha, beta))
            if v <= alpha:
                self.vis[comp][1] = v
                return v
            beta = min(beta, v)
        self.vis[comp][1] = v
        return v
    
    def compress(self, state):
        comp = tuple()
        for i in range(1, 6):
            x = self.o[0]+abs(i-3)*self.hor
            y = self.o[1]-(i-1)*self.ver
            n = 6 - abs(i-3)
            for j in range(n):
                comp = comp + (state[(x+2*j*self.hor, y+self.radius)],)
        return comp
    
    def decompress(self, comp):
        centers = {}
        cnt = 0
        for i in range(1, 6):
            x = self.o[0]+abs(i-3)*self.hor
            y = self.o[1]-(i-1)*self.ver
            n = 6 - abs(i-3)
            for j in range(n):
                centers[(x+2*j*self.hor, y+self.radius)] = comp[cnt]
                cnt += 1
        return centers
    