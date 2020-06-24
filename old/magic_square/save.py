'''
Created on Nov 1, 2018

@author: prashant
'''

import copy
from __builtin__ import True

class Ai():
    
    def propagate(self, state, csg):
        tot = 0
        for i in range(self.n):
            for j in csg[self.sumconst_row_seed+i]:
                tot += state[0][j]
            for j in csg[self.sumconst_row_seed+i]:
                if state[0][j] == 0:
                    for v in copy.deepcopy(state[1][j]):
                        if tot+v > self.sum:
                            state[1][j].remove(v)
            tot = 0
            for j in csg[self.sumconst_col_seed+i]:
                tot += state[0][j]
            for j in csg[self.sumconst_col_seed+i]:
                if state[0][j] == 0:
                    for v in copy.deepcopy(state[1][j]):
                        if tot+v > self.sum:
                            state[1][j].remove(v)
        tot = 0
        for i in csg[self.diag_seed+0]:
            tot += state[0][i]
        for i in csg[self.diag_seed+0]:
            if state[0][i] == 0:
                for v in copy.deepcopy(state[1][i]):
                    if tot+v > self.sum:
                        state[1][i].remove(v)
        tot = 0
        for i in csg[self.diag_seed+1]:
            tot += state[0][i]
        for i in csg[self.diag_seed+1]:
            if state[0][i] == 0:
                for v in copy.deepcopy(state[1][i]):
                    if tot+v > self.sum:
                        state[1][i].remove(v)
    # end of fn
    
    
    
    def sum_constraint(self, state, csg):
        for i in range(0, self.n):
            tot = 0
            for j in csg[self.sumconst_row_seed+i]:
                tot += state[j]
            if tot != self.sum:
                return False
              
            tot = 0
            for j in csg[self.sumconst_col_seed+i]:
                tot += state[j]
            if tot != self.sum:
                return False
        tot = 0
        for i in csg[self.diag_seed+0]:
            tot += state[i]
        if tot != self.sum:
            return False
        tot = 0
        for i in csg[self.diag_seed+1]:
            tot += state[i]
        if tot != self.sum:
            return False
        return True
    
    
    
    
    
    