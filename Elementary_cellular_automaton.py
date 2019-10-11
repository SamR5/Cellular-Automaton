#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Elementary cellular automatons


import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import itertools as it
import copy


cs = 2 # cell size
RULES = list(it.product(['1', '0'], repeat=8))[::-1]
neighbor = ['111', '110', '101', '100', '011', '010', '001', '000']

interesting = [13, 18, 22, 26, 28, 30, 45, 50, 54, 57, 58, 60, 62, 73, 75,
               77, 82, 86, 89, 90, 92, 94, 99, 101, 102, 105, 109, 110, 114,
               118, 122, 124, 126, 129, 131, 133, 135, 137, 141, 144, 145,
               146, 147, 149, 150, 153, 154, 156, 158, 161, 163, 165, 167,
               169, 177, 178, 181, 182, 186, 188, 190, 193, 195, 210, 214,
               218, 220, 222, 225, 230, 242, 246, 250, 252, 254]


class Automaton():
    """"""
    def __init__(self, master, size=731):
        self.size = size
        self.line = '0' * (self.size // 2) + '1' + '0' * (self.size // 2)
        self.lines = []
        self.rule = RULES[182]
        
        self.master = master
        self.create_buttons()
        self.generate_lines()
        self.draw()
        
    def create_buttons(self):
        """Create and place all widget on the window"""
        self.canvas = tk.Canvas(self.master, width=self.size//2*cs+2,
                                             height=self.size//4*cs,
                                             bg='white')
        var = tk.StringVar()
        self.ruleEnt = tk.Entry(self.master, textvariable=var,
                                width=3)
        self.ruleEnt.bind("<Return>", func=lambda x:self.change_rule(None))
        self.ruleB = tk.Button(self.master, text='GO',
                                 command=self.change_rule)
        self.blankLab = tk.Label(self.master, text='', width=8)\
                        .grid(row=1, column=1)
        
        
        self.canvas.grid(row=0, columnspan=17)
        self.ruleEnt.grid(row=1, rowspan=2)
        self.ruleB.grid(row=3, rowspan=2, sticky='n')
        self.ruleEnt.insert(0, "182")
        
        count = 0
        for i in range(5):
            for j in range(15):
                lab = tk.Label(self.master, text=interesting[count],
                               anchor='w', height=1)
                lab.grid(row=i+1, column=j+2)
                lab.bind("<Button-1>",
                         lambda event, x=count :self.change_rule(interesting[x]))
                count += 1
        
    
    def next_line(self, oldLine):
        """Create the next line according to the rule"""
        nextLine = ''
        #nextLine += self.rule[neighbor.index('0' + oldLine[:2])]
        for i in range(len(oldLine) - 2):
            nextLine += self.rule[neighbor.index(oldLine[i:i+3])]
        if len(self.lines) == 1: # if we work on the second line
            nextLine = self.rule[neighbor.index(oldLine[-2:] + '0')] +\
                       nextLine +\
                       self.rule[neighbor.index(oldLine[-2:] + '0')]
        else:
            nextLine = oldLine[0] + nextLine + oldLine[-1]
        #nextLine += self.rule[neighbor.index(oldLine[-2:] + '0')]
        return nextLine
    
    def generate_lines(self):
        """Run the automaton n times with rule"""
        self.lines.append(self.line) # the first
        newL = copy.copy(self.line)
        for _ in range(self.size // 4):
            newL = copy.copy(self.next_line(newL))
            self.lines.append(newL)
        self.lines.append(newL)
    
    def change_rule(self, number=None):
        """"""
        if number != None:
            self.ruleEnt.delete(0, len(self.ruleEnt.get())) #from zero to end
            self.ruleEnt.insert(-1, number)
        self.rule = RULES[int(self.ruleEnt.get())]
        self.lines = []
        self.generate_lines()
        self.draw()
    
    def draw(self):
        """Draw"""
        self.canvas.delete(tk.ALL)
        for indL, line in enumerate(self.lines):
            # only display the second and third quarter to avoid
            # side effects not avoidable
            for indC, pix in enumerate(line[self.size//4:3*self.size//4+1]):
                if pix == '1':
                    self.canvas.create_rectangle(indC*cs, indL*cs+1,
                                                 indC*cs + cs, indL*cs + cs+1,
                                                 fill="blue", width=0)
    
if __name__ == "__main__":
    root = tk.Tk()
    auto = Automaton(root)
    root.mainloop()
