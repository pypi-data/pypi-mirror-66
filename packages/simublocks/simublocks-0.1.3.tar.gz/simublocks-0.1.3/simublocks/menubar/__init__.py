# MIT License
#
# Copyright (c) 2020 Anderson Vitor Bento
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from simublocks.menubar.file import FileApp
from simublocks.menubar.simulation import SimulationFunc

import tkinter as tk
from simublocks.element import Workspace
from simublocks.dialog import Dialog


class MenuBar():
    def __init__(self, canvas):
        self.canvas = canvas
        menu = tk.Menu(self.canvas.master)
        self.canvas.master.config(menu=menu)
        
        menu.add_cascade(label="File",menu=self.menuFile(menu))
        menu.add_cascade(label="Add Blocks",menu=self.menuBlocks(menu))
        menu.add_cascade(label="Other",menu=self.menuExecute(menu))
        menu.add_command(label="Run Simulation", command=SimulationFunc.execute)

    def menuFile(self,menu):
        new = tk.Menu(menu)
        new.add_command(label="New File",command=FileApp.new)
        new.add_command(label="Open File",command=FileApp.open)
        new.add_command(label="Save File",command=FileApp.save)
        new.add_command(label="Quit",command=self.exit)
        return new

    def menuBlocks(self,menu):
        new = tk.Menu(menu)
        new.add_command(label="Input",
            command=lambda: Workspace.createBlock("Input","input"))
        new.add_command(label="Transfer Function",
            command=lambda: self.createNewSystem("TF"))
        new.add_command(label="State Space",
            command=lambda: self.createNewSystem("SS"))
        new.add_command(label="Sum",
            command=lambda: Workspace.createBlock("Sum","sum"))
        new.add_command(label="Corner",
            command=lambda:self.createCorner())
        new.add_command(label="Plot Graph",
            command=lambda: Workspace.createGraph("Graph"))
        return new

    def menuExecute(self,menu):
        new = tk.Menu(menu)
        new.add_command(label="Import Code",
            command=lambda:SimulationFunc.importCode())
        return new

    def createNewSystem(self, type):
        code = dict()
        code['type'] = type
        code['sub_type'] = "continuous"
        if type == "TF": code['self'] = ['[1]','[1,2,3]']
        else: code['self'] = ['[ [-5, -5],[1, 0] ]','[[1],[0]]', '[0,1]', '[0]']
        
        Workspace.createBlock("Sys ("+type+")","system", code=code)

    def createCorner(self):
        res = Dialog.newCorner()
        if res['status'] == "save":
            if res['code'] == ['','']: res['code'] = None
            Workspace.createBlock("Corner","corner", code=res['code'])

    def exit(self):
        exit(0)