#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Elementary cellular automatons

import itertools as it
import pickle as pk
import tkinter as tk
import time as t


def add_right(lol):
    """Mirror the list to the right"""
    for i in range(len(lol)):
        lol[i] += lol[i][:-1][::-1]
    return lol

def add_bottom(lol):
    """Mirror the list to the bottom"""
    l = len(lol)
    for i in range(l - 1):
        lol.insert(l, lol[i])
    return lol


cs = 5 # cell size
cc = 'blue' # cell color
bgc = 'green' # background color
delay = 300 # delay between steps

RULES = list(it.product([1, 0], repeat=6))


class Automaton2D():
    """"""
    def __init__(self, master, ruleNum):
        
        self.allDict = self.load()
        self.allSteps = self.allDict[ruleNum]
        # add the right and bottom part of the grid
        a = []
        for stp in self.allSteps:
            a.append(add_bottom(add_right(stp)))
        self.allSteps = a
        
        self.step = 0
        self.grid = self.allSteps[0]
        self.size = len(self.grid)
        
        self.master = master
        self.create_buttons()
        self.ruleVar.set('rule ' + str(ruleNum))
        self.draw_step(self.grid)
    
    def load(self):
        """Load the allSteps dict of each rule"""
        with open("save.sv", 'rb') as save:
            #myUnp = pk.Unpickler(save)
            #data = myUnp.load()
            data = pk.loads(save.read())
        return data
    
    def set_rule(self, event=None):
        """Change the level of the automaton"""
        self.grid = [[1 for _ in range(self.size)] for _ in range(self.size)]
        self.grid[self.size//2][self.size//2] = 0
        self.step = 0
        self.allSteps = self.allDict[int(self.ruleEnt.get())]
        # add the right and bottom part of the grid
        a = []
        for stp in self.allSteps:
            a.append(add_bottom(add_right(stp)))
        self.allSteps = a
        
        self.ruleVar.set('rule ' + self.ruleEnt.get())
        self.draw_step(self.grid)
        
    
    def create_buttons(self):
        """Create and place all widget on the window"""
        # -2 because the canvas is offset
        self.canvas = tk.Canvas(self.master, width=self.size*cs - 2,
                                             height=self.size*cs - 2,
                                             bg=bgc)
        self.nextB1 = tk.Button(self.master, text='x1',
                                command=self.plus_step)
        self.nextB10 = tk.Button(self.master, text='x10',
                                 command=self.plus_n)
        self.maxB = tk.Button(self.master, text='END',
                              command=self.go_max)
        self.previousB1 = tk.Button(self.master, text='-1',
                                    command=self.minus_step)
        self.previousB10 = tk.Button(self.master, text='-10',
                                     command=self.minus_n)
        self.minB = tk.Button(self.master, text='START',
                              command=self.go_start)
        self.movieB = tk.Button(self.master, text="MOVIE",
                                command=self.movie)
        var = tk.StringVar()
        self.ruleEnt = tk.Entry(self.master, textvariable=var,
                                width=6)
        self.ruleEnt.bind("<Return>", func=self.set_rule)
        self.ruleSet = tk.Button(self.master, text='Change',
                                 command=self.set_rule)
        self.stpVar = tk.StringVar()
        self.stpLab = tk.Label(self.master, textvariable=self.stpVar,
                               justify='left', width=8)
        self.ruleVar = tk.StringVar()
        self.ruleLab = tk.Label(self.master, textvariable=self.ruleVar,
                                justify='left', width=8)
        
        self.canvas.grid(columnspan=9)
        self.minB.grid(row=1, column=0, sticky='nswe')
        self.nextB1.grid(row=1, column=1, sticky='nswe')
        self.nextB10.grid(row=1, column=2, sticky='nswe')
        self.maxB.grid(row=2, column=0, sticky='nswe')
        self.previousB1.grid(row=2, column=1, sticky='nswe')
        self.previousB10.grid(row=2, column=2, sticky='nswe')
        self.movieB.grid(row=1, rowspan=2, column=3, sticky='nswe')
        self.ruleEnt.grid(row=1, column=6)
        self.ruleSet.grid(row=2, column=6, sticky='n')
        self.stpLab.grid(row=1, column=8, sticky='e')#, columnspan=2)
        self.ruleLab.grid(row=2, column=8, sticky='e')#, columnspan=2)
    
    def plus_step(self):
        """Go one step further"""
        self.step += 1
        try:
            self.grid = self.allSteps[self.step]
        except IndexError:
            self.step -= 1
        return self.draw_step(self.allSteps[self.step])
    
    def minus_step(self):
        """Go one step before"""
        self.step -= 1
        if self.step < 0:
            self.step = 0
        self.grid = self.allSteps[self.step]
        return self.draw_step(self.allSteps[self.step])
    
    def plus_n(self, n=10):
        """Go n steps further"""
        for i in range(n):
            if self.step == self.size//2 - 1:
                return
            self.master.after(delay, self.plus_step())
#            self.master.update_idletasks()
    
    def minus_n(self, n=10):
        """Go ten step before"""
        for i in range(n):
            if self.step == 0:
                return
            self.master.after(delay, self.minus_step())
#            self.master.update_idletasks()
    
    def go_max(self):
        """Got to the last step of the draw"""
        self.step = self.size // 2 - 1
        self.draw_step(self.allSteps[-1])
    
    def go_start(self):
        """Go to the first step of the draw"""
        self.step = 0
        self.draw_step(self.allSteps[0])
    
    def movie(self):
        """Travel through all steps"""
        while self.step < self.size // 2 - 1:
            self.master.after(delay, self.plus_step())
#            self.master.update_idletasks()
    
    def draw_step(self, grid):
        """Draw one step"""
        self.canvas.delete(tk.ALL)
        self.stpVar.set("step " + str(self.step))
        for indL, line in enumerate(grid):
            for indC, pix in enumerate(line):
                if pix == 0:
                    self.canvas.create_rectangle(indL*cs, indC*cs,
                                                 indL*cs + cs, indC*cs + cs,
                                                 fill=cc, width=0)
        self.master.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    auto = Automaton2D(root, ruleNum=0) #153
    #auto.movie()
    root.mainloop()
