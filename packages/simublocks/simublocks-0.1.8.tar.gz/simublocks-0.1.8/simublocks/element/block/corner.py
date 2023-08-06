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

from simublocks.element.block.block import Block 

class Corner(Block):
    def __init__(self, canvas, type, text, coords, code):
        Block.__init__(self,canvas,'', coords, code)
        self.type = type
        c = self.coords

        # code[0] is the input
        if code[0] == 'left':
            self._in_ = canvas.create_arc(self.left_pos(self.coords), start=-90, extent=180, fill="black")
        elif code[0] == 'right':
            self._in_ = canvas.create_arc(self.right_pos(self.coords), start=90, extent=180, fill="black")
        elif code[0] == 'top':
            self._in_ = canvas.create_arc(self.top_pos(self.coords), start=180, extent=180, fill="black")
        else:
            self._in_ = canvas.create_arc(self.bottom_pos(self.coords), start=0, extent=180, fill="black")

        # code[1] is the output
        if code[1] == 'left':
            self._out_ = canvas.create_arc(self.left_pos(self.coords), start=90, extent=180, fill="black")
        elif code[1] == 'right':
            self._out_ = canvas.create_arc(self.right_pos(self.coords), start=-90, extent=180, fill="black")
        elif code[1] == 'top':
            self._out_ = canvas.create_arc(self.top_pos(self.coords), start=0, extent=180, fill="black")
        else:
            self._out_ = canvas.create_arc(self.bottom_pos(self.coords), start=180, extent=180, fill="black")
        
    
    def moveArc(self):

        # self.code[0] is the input
        if self.code[0] == 'left':
            self.canvas.coords(self._in_, self.left_pos(self.coords))
        elif self.code[0] == 'right':
            self.canvas.coords(self._in_, self.right_pos(self.coords))
        elif self.code[0] == 'top':
            self.canvas.coords(self._in_, self.top_pos(self.coords))
        else:
            self.canvas.coords(self._in_, self.bottom_pos(self.coords))

        # self.code[1] is the output
        if self.code[1] == 'left':
            self.canvas.coords(self._out_, self.left_pos(self.coords))
        elif self.code[1] == 'right':
            self.canvas.coords(self._out_, self.right_pos(self.coords))
        elif self.code[1] == 'top':
            self.canvas.coords(self._out_, self.top_pos(self.coords))
        else:
            self.canvas.coords(self._out_, self.bottom_pos(self.coords))

    def remove(self):
        Block.remove(self)
        self.canvas.delete(self._out_)
        self.canvas.delete(self._in_)