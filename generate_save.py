#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Elementary cellular automaton save generator

import pickle as pk
import itertools as it
import time as t


def generate_save(size):
    """Generate a save"""
    data = {}
    for rule in range(0, 64):
        auto = Automaton2D(size, rule)
        data[rule] = auto.generate_all_steps()
    with open("save.sv", 'wb') as save:
        myPick = pk.Pickler(save)
        myPick.dump(data)


def del_bottom(lol):
    """Delete the bottom half of the list"""
    return lol[:len(lol)//2 + 1]

def del_right(lol):
    """Delete the right part of the list"""
    l = len(lol[0])
    return [li[:l//2 + 1] for li in lol]

RULES = list(it.product([1, 0], repeat=6))
neighbors = ((-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1),  (1, 0),  (1, 1))

class Automaton2D():
    """"""
    def __init__(self, size, ruleNum):
        
        # size must be odd to have a cell in center
        self.size = size if size%2 else size-1
        # from 111111 to 000000 (two first and two last not counted)
        self.rule = RULES[ruleNum]
        self.grid = [[1 for _ in range(self.size)] for _ in range(self.size)]
        # first filled cell at the center
        self.grid[self.size-1][self.size-1] = 0
    
    def count_neighbors(self, grid, cell):
        """Return the number of filled neighbor"""
        c = 0
        for n in neighbors:
            newR = cell[0] + n[0]
            newC = cell[1] + n[1]
            #if negative indexes, search will be in the end of the list
            if newR < 0 or newC < 0:
                c += 1
            if newR == self.size:
                newR -= 2
            if newC == self.size:
                newC -= 2
            if grid[newR][newC] == 0:
                c += 1
        return c
    
    def next_step(self, step, grid):
        """Change the color for the next step"""
        tmpDict = {} # changes {cell:newcolor}
        halfLen = len(grid) // 2
        # since the propagation is only one cell from the center each step
        # checking cells around is not necessary
        for row in range(self.size - step - 1, self.size):
            for col in range(self.size - step - 1, self.size):
                c = self.count_neighbors(grid, (row, col))
                if c in (0, 8):
                    tmpDict[(row, col)] = 1
                elif c == 1:
                    tmpDict[(row, col)] = 0
                elif c in (2, 3, 4, 5, 6, 7):
                    # the cell is changed according to the rule
                    tmpDict[(row, col)] = self.rule[c-2]
        for coord, val in tmpDict.items():
            grid[coord[0]][coord[1]] = val
        return grid
    
    def generate_all_steps(self):
        liste = []
        nxtgrid = self.grid
        liste.append([i[:] for i in nxtgrid])
        for stp in range(1, self.size-1):
            nxtgrid = self.next_step(stp, nxtgrid)
            liste.append([i[:] for i in nxtgrid])
        return liste

if __name__ == "__main__":
    t0 = t.time()
    generate_save(50);
    t1 = t.time()
    print(t1-t0)
