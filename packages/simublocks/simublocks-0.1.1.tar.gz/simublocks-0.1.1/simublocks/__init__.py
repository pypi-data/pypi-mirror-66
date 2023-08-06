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

from simublocks.menubar import *
from simublocks.element import *
from tkinter import Tk, Canvas, BOTH
import os

class Index(Canvas):

    def main():  
        root = Tk()
        app = Index(root)
        root.mainloop()

    def __init__(self, root=None):
        Canvas.__init__(self, root, bg="white",width=1000,height=500)              
        self.root = root
        self.init_window()

    def init_window(self):     
        self.root.title("SIMUBLOCKS\tPython Simulation Blocks for Dynamic Systems")
        self.pack(fill=BOTH, expand=1)
        Workspace.canvas = self
        MenuBar(self)
        