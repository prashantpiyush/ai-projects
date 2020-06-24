################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Oct 26, 2018

@author: prashant
'''


import copy
import random
import time
from itertools import combinations

class Ai():
    
    def __init__(self, n=3, o=1, h=2):
        self.n = n
        self.sum = self.n*(self.n*self.n+1)//2
        self.algo = self.dfs_bt
        if o == 2:
            self.algo = self.dfs_bt_constraint_propagation
        if h==2:
            self.select_next_variable = self.mrv_heuristic
        elif h==3:
            self.select_next_variable = self.degree_heuristic
        
    def magic(self):
        self.create_csg()
        state = [[0]*self.n*self.n, [list(range(1, self.n*self.n+1)) for _ in range(self.n*self.n)]]
        rs = self.algo(state, self.g)
        
        if rs is None:
            print("No magic square found.")
            return
        
        # print result
        print("Magic square grid:")
        for i in range(0, self.n*self.n, self.n):
            for j in range(0, self.n):
                print(rs[0][i+j]," ", end='')
            print()
    
    def create_csg(self):
        self.N = self.n*self.n + 2*self.n + 3
        self.g = [[] for _ in range(self.N)]
        
        self.alldiff_node = self.n*self.n
        self.sumconst_row_seed = self.alldiff_node+1
        self.sumconst_col_seed = self.alldiff_node+self.n+1
        self.diag_seed = self.N-2
        
        for i in range(self.n*self.n):
            self.g[self.alldiff_node].append(i)
        
        for i in range(0, self.n*self.n, self.n):
            for j in range(self.n):
                self.g[self.sumconst_row_seed+i//self.n].append(i+j)
        
        for i in range(0, self.n):
            for j in range(self.n):
                self.g[self.sumconst_col_seed+i].append(i+self.n*j)
        
        for i in range(0, self.n):
            self.g[self.diag_seed+0].append(self.n*i + i)
            self.g[self.diag_seed+1].append((self.n-1)*(i+1))
    # end of create_csg
    
    def alldiff(self, state, csg):
        vis = set()
        
        for i in csg[self.alldiff_node]:
            if state[i]==0: continue
            if state[i] in vis: return False
            vis.add(state[i])
        return True
    
    def sum_constraint(self, state, csg):
        def check(idx):
            tot = 0
            for j in csg[idx]:
                tot += state[j]
            return tot
        
        for i in range(0, self.n):
            if check(self.sumconst_row_seed+i) != self.sum: return False
            if check(self.sumconst_col_seed+i) != self.sum: return False
        if check(self.diag_seed+0) != self.sum: return False
        if check(self.diag_seed+1) != self.sum: return False
        return True
    
    def mrv_heuristic(self, state, csg):
        var, min = -1, 10000
        for idx in range(len(state[1])):
            if len(state[1][idx]) < min and state[0][idx]==0:
                var, min = idx, len(state[1][idx])
        return var
    
    def degree_heuristic(self, state, csg):
        deg = [0]*self.n*self.n
        
        def count(idx):
            rs = 0
            for i in csg[idx]:
                if state[0][i] == 0:
                    rs += 1
            return rs
        
        def inc_deg(idx):
            cnt = count(idx)
            for i in csg[idx]:
                if state[0][i] == 0:
                    deg[i] += cnt
        
        for i in range(0, self.n):
            inc_deg(self.sumconst_row_seed+i)
            inc_deg(self.sumconst_col_seed+i)
        inc_deg(self.diag_seed+0)
        inc_deg(self.diag_seed+1)
        
        idx, min = -1, 10000
        for i in range(len(deg)):
            if state[0][i]==0 and deg[i]<min:
                min = deg[i]
                idx = i
        return idx
    
    def select_next_variable(self, state, csg):
        # default: choose the next unassigned variable
        for i in range(self.n*self.n):
            if state[0][i] == 0:
                return i
        return -1
    
    def dfs_bt(self, variable_list, constraint_graph):
        return self.dfs(variable_list, constraint_graph)
    
    def dfs(self, state, csg):
        idx = self.select_next_variable(state, csg)
        if idx == -1:
            if self.alldiff(state[0], csg) and self.sum_constraint(state[0], csg):
                return state
            return None
        
        for i in range(1, self.n*self.n+1):
            state[0][idx] = i
            
            if self.alldiff(state[0], csg):
                ret = self.dfs(state, csg)
                
                if ret is not None:
                    return state
        state[0][idx] = 0
    # end of dfs
    
    def propagate(self, state, csg, idx):
        # all-diff constraint
        v = state[0][idx]
        for dom in state[1]:
            if v in dom:
                dom.remove(v)
        
        def trim_domain(index):
            tot = 0
            for j in csg[index]:
                tot += state[0][j]
            for j in csg[index]:
                if state[0][j] == 0:
                    for v in copy.deepcopy(state[1][j]):
                        if tot+v > self.sum:
                            state[1][j].remove(v)
        # sum constraint
        for i in range(0, self.n):
            trim_domain(self.sumconst_row_seed+i)
            trim_domain(self.sumconst_col_seed+i)
        trim_domain(self.diag_seed+0)
        trim_domain(self.diag_seed+1)
        
    def dfs_bt_constraint_propagation(self, state, contraint_graph):
        return self.dfs_cp(state, contraint_graph)
    
    def dfs_cp(self, state, csg):
        idx = self.select_next_variable(state, csg)
        if idx == -1:
            if self.alldiff(state[0], csg) and self.sum_constraint(state[0], csg):
                return state
            return None
        
        init_domain = state[1]
        
        for v in state[1][idx]:
            state[0][idx] = v
            state[1] = copy.deepcopy(init_domain)
            self.propagate(state, csg, idx)
            
            ret = self.dfs_cp(state, csg)
            
            if ret is not None:
                return state
        state[0][idx] = 0
        state[1] = init_domain

def show_analysis():
    print("\n")
    print("The following values are computed for grid size 3.")
    print("\n")
    print("(a) DFS + BT")
    print("R1. Nodes generated: 187769")
    print("R2. Mem. allocated to one node: 2160 bytes")
    print("R3. Max stack size: 9")
    print("R4. Time to compute values: 2.744sec")
    print("R5. Node generated (MRV): 187769")
    print("\n")
    print("(b) DFS + BT + Constraint Propagation")
    print("R6. Nodes generated: 11473")
    print("R7. Computer ratio: 0.938")
    print("R8. Time to compute values: 0.98sec")
    print("\n")
    
if __name__ == '__main__':
    while True:
        n = int(input("Enter grid size (Enter 0 to show analysis): "))
        if n == 0:
            show_analysis()
            print("Do you want to Continue?")
            c = input("Enter [y/n]: ").strip()
            if c != 'y' and c != '':
                break
            else: continue
        while n<=2:
            n = int(input("Please enter a grid size greater than 2: "))
        
        print("Choose executing algorithm:")
        print("1. DFS + BT")
        print("2. DFS + BT + Constraint Propagation")
        
        o = int(input("Enter [1/2]: "))
        while o!=1 and o!=2:
            o = int(input("Please enter a valid choice [1/2]: "))
        
        print("Choose heuristic of variable ordering: ")
        print("1. No heuristic (default order)")
        print("2. Minimum remaining value (MRV)")
        print("3. Degree heuristic")
        
        h = int(input("Enter [1/2/3]: "))
        while h!=1 and h!=2 and h!=3:
            h = int(input("Please enter a valid choice [1/2/3]: "))
        
        ai = Ai(n, o, h)
        ai.magic()
        
        print("Do you want to Continue?")
        c = input("Enter [y/n]: ").strip()
        if c != 'y' and c != '':
            break
        print()
    # end of loop



