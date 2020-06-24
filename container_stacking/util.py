################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Sep 24, 2018

@author: prashant
'''

from collections import deque
from itertools import product
import sys
import copy
import time
try: 
    import queue
except ImportError:
    import Queue as queue
import random
from timeit import default_timer as timer
import math

# import logging
# logfile = 'log.txt'
# logging.basicConfig(filename=logfile,level=logging.DEBUG)
# LOG_ENABLED = False
# def log(*args):
#     if not LOG_ENABLED: return
#     for arg in args:
#         logging.debug(arg)


class Ai():
    
    def __init__(self, n, m):
        self.n = n
        self.m = m
        
    def initial_state_generator(self, init=False):
        if init:
            try:
                self.init_stacks
                return self.init_stacks
            except:
                pass
        randints = [random.randint(0, self.m) for _ in range(self.n)]
        self.init_stacks = [[-1]*randint for randint in randints]
        self.total_blocks = sum(randints)
        self.init_pos = [0]*self.total_blocks
        block_ids = list(range(self.total_blocks))
        random.shuffle(block_ids)
        ptr = 0
        for row in range(len(self.init_stacks)):
            for col in range(len(self.init_stacks[row])):
                self.init_stacks[row][col] = block_ids[ptr]
                self.init_pos[self.init_stacks[row][col]] = (row, col)
                ptr += 1
        self.init_pos = tuple(self.init_pos)
        return self.init_stacks
    
    def goal_state_generator(self, init=False):
        if init:
            try:
                self.goal_stacks
                return self.goal_stacks
            except:
                pass
        self.initial_state_generator(init=True)
        randints = [0]*self.n
        total = self.total_blocks
        for i in range(self.n):
            randint = random.randint(0, min(self.m, total))
            if total - randint < 0:
                continue
            randints[i] = randint
            total -= randint
        while total > 0:
            for i in range(self.n):
                if randints[i]+1<=self.m:
                    randints[i] += 1
                    total -= 1
                    if total <= 0:
                        break
        self.goal_stacks = [[-1]*randint for randint in randints]
        self.goal_pos = [0]*self.total_blocks
        block_ids = list(range(self.total_blocks))
        random.shuffle(block_ids)
        ptr = 0
        for row in range(len(self.goal_stacks)):
            for col in range(len(self.goal_stacks[row])):
                self.goal_stacks[row][col] = block_ids[ptr]
                self.goal_pos[self.goal_stacks[row][col]] = (row, col)
                ptr += 1
        self.goal_pos = tuple(self.goal_pos)
        return self.goal_stacks
    
    def get_block_pos(self, state_name):
        return getattr(self, state_name, [])
    
    def get_block_count(self):
        return getattr(self, 'total_blocks', 0)
    
    def h1(self, curr_pos):
        goal_pos = self.get_block_pos('goal_pos')
        h = 0
        for curr, goal in zip(curr_pos, goal_pos):
            if curr[0] != goal[0]:
                h += 1
            elif curr[1] <= goal[1]:
                h += goal[1] - curr[1]
        return h
    
    def h2(self, curr_pos):
        """
        How many moves will it approx take to correct
        if the box is not in its place
        +1 if its not in its stacks
        +(diff in height)
        """
        goal_pos = self.get_block_pos('goal_pos')
        h = 0
        for curr, goal in zip(curr_pos, goal_pos):
            if curr[0] != goal[0]:
                h += 1
            else:
                h += abs(goal[1] - curr[1])
        return h
    
    def h3(self, curr_pos):
        """
        How much of stack is already created
        """
        goal_pos = self.get_block_pos('goal_pos')
        curr = self.decompress(curr_pos)
        goal = self.decompress(goal_pos)
        h = 0
        for i in range(len(goal)):
            j = 0
            while j<len(goal[i]) and j<len(curr[i]) and curr[i][j]==goal[i][j]:
                j += 1
            while j<len(curr[i]):
                h += 1
                j += 1
        return h
    
    def h4(self, curr_pos):
        """
        Out of place heuristic value
        """
        goal_pos = self.get_block_pos('goal_pos')
        h = 0
        for curr, goal in zip(curr_pos, goal_pos):
            if curr[0] != goal[0] or curr[1] != goal[1]:
                h += 1
        return h
    
    def hc(self, start, goal, heuristic):
        parent = {start:None}
        current = start
        while True:
            try:
                h_current = heuristic(current)
            except:
                print(current)
            child_states = self.get_child_states(current, rand=True)
            next_state = None
            for child in child_states:
                h_child = heuristic(child)
                if h_child < h_current:
                    next_state = child
                    break
            if next_state is None:
                return self.reconstruct_path(parent, current)
            parent[next_state] = current
            current = next_state
        # end of function
    
    def gbfs(self, start, goal, heuristic):
        closed_set = set()
        open_set = set()
        q = queue.PriorityQueue()
        
        parent = {start:None}
        f_score = {start:heuristic(start)}
        
        q.put((f_score[start], start))
        open_set.add(start)
        
        while len(open_set) > 0:
            # print("len", len(open_set))
            _, current = q.get()
            open_set.remove(current)
            
            if self.compare(current, goal):
                return self.reconstruct_path(parent, current)
            
            closed_set.add(current)
            
            child_states = self.get_child_states(current)
            
            for child in child_states:
                if child in closed_set:
                    continue
                parent[child] = current
                f_score[child] = heuristic(child)
                                
                if child not in open_set:
                    open_set.add(child)
                    q.put((f_score[child], child))
        # end of function
    
    def astar(self, start, goal, heuristic):
        closed_set = set()
        open_set = set()
        q = queue.PriorityQueue()
        
        parent = {start:None}
        g_score = {start:0}
        f_score = {start:heuristic(start)}
        
        q.put((f_score[start], start))
        open_set.add(start)
        
        while len(open_set) > 0:
            # print("len", len(open_set))
            _, current = q.get()
            open_set.remove(current)
            
            if self.compare(current, goal):
                return self.reconstruct_path(parent, current)
            
            closed_set.add(current)
            
            child_states = self.get_child_states(current)
            
            for child in child_states:
                if child in closed_set:
                    continue
                
                tentative_g_score = g_score.get(current, 100000) + 1
                
                if (child in open_set) and tentative_g_score >= g_score.get(child, 10000):
                    continue
                
                parent[child] = current
                g_score[child] = tentative_g_score
                f_score[child] = g_score[child] + heuristic(child)
                
                if child not in open_set:
                    open_set.add(child)
                    q.put((f_score[child], child))
        # end of function
    
    def next_state(self):
        pass
    
    def get_child_states(self, state, rand=False):
        state = list(state)
        stacks = self.decompress(state)
        rowids = range(len(stacks))
        if rand:
            random.shuffle(rowids)
        for i in rowids:
            if len(stacks[i]) <= 0:
                continue
            bid = stacks[i][-1]
            stacks[i] = stacks[i][:-1]
            for j in rowids:
                if i == j:
                    continue
                stacks[j] += [bid]
                yield self.compress(stacks)
                stacks[j] = stacks[j][:-1]
            stacks[i] += [bid]
        # end of func
    
    def reconstruct_path(self, parent, final_state):
        path = []
        while final_state is not None:
            path.append(final_state)
            final_state = parent[final_state]
        return path[::-1]
    
    def compare(self, curr_state, goal_state):
        for curr, goal in zip(curr_state, goal_state):
            if curr[0] != goal[0] or curr[1] != goal[1]:
                return False
        return True
    
    def compress(self, stacks):
        count = 0
        for row in stacks:
            count += len(row)
        pos = [0]*count
        for r in range(len(stacks)):
            for c in range(len(stacks[r])):
                pos[stacks[r][c]] = (r, c)
        pos = tuple(pos)
        return pos
    
    def decompress(self, state):
        heights = [0]*self.n
        for r, c in state:
            heights[r] += 1
        stacks = [[-1]*h for h in heights]
        for i in range(len(state)):
            r, c = state[i]
            stacks[r][c] = i
        return stacks
    
    
    
    
    
    
    
    