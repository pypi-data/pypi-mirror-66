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

from simublocks.element.connection import Connection

class blockTools:
    def move(self, event):
        pos = self.canvas.coords(self.self)
        w = abs(pos[2] - pos[0])
        h = abs(pos[3] - pos[1])
        pos[0] = event.x - w/2
        pos[2] = event.x + w/2
        pos[1] = event.y - h/2
        pos[3] = event.y + h/2
        self.coords = pos
        self.canvas.coords(self.self, self.coords)
        self.canvas.coords(self.text, (
            (self.coords[2] - self.coords[0])/2 + self.coords[0],
            (self.coords[3] - self.coords[1])/2 + self.coords[1],
        ) )
        
        if self.type != "graph":
            self.moveArc()
            self.moveLines()

    def moveLines(self):
        for n_arc in [0,1,2]:
            conn = self.conn[n_arc]
            if conn['n_line'] != None:
                pos = self.canvas.coords(self.conn[n_arc]['line'])
                if self.type != 'corner':
                    pos = self.moveLineOfBlock(n_arc,pos)
                else:
                    pos = self.moveLineOfCorner(n_arc,pos)
                self.canvas.coords(self.conn[n_arc]['line'],pos)

    def moveLineOfBlock(self,n_arc, pos):
        conn = self.conn[n_arc]
        if n_arc != 2:
            pos[0 +conn['n_line']*2] = self.coords[0 + 2*n_arc]
            pos[1 +conn['n_line']*2] = (self.coords[1] + self.coords[3])/2
        else:
            pos[1 +conn['n_line']*2] = self.coords[1 + 2*(3 - n_arc)]
            pos[0 +conn['n_line']*2] = (self.coords[0] + self.coords[2])/2
        return pos

    def moveLineOfCorner(self,n_arc, pos):
        conn = self.conn[n_arc]

        if self.code[n_arc] == 'left':
            pos[1 +conn['n_line']*2] = (self.coords[1] + self.coords[3])/2
            pos[0 +conn['n_line']*2] = self.coords[0]
        elif self.code[n_arc] == 'right':
            pos[1 +conn['n_line']*2] = (self.coords[1] + self.coords[3])/2
            pos[0 +conn['n_line']*2] = self.coords[2]
        elif self.code[n_arc] == 'top':
            pos[1 +conn['n_line']*2] = self.coords[1]
            pos[0 +conn['n_line']*2] = (self.coords[0] + self.coords[2])/2
        else:
            pos[1 +conn['n_line']*2] = self.coords[3]
            pos[0 +conn['n_line']*2] = (self.coords[0] + self.coords[2])/2
        return pos

    def right_pos(self, c):
        return (
            c[2]-10, 
            (c[3] - c[1])/2 + c[1] - 10, 
            c[2]+10, 
            (c[3] - c[1])/2 + c[1] + 10
        )

    def left_pos(self, c):
        return (
            c[0]-10, 
            (c[3] - c[1])/2 + c[1] - 10, 
            c[0]+10, 
            (c[3] - c[1])/2 + c[1] + 10
        )

    def top_pos(self, c):
        return (
            (c[2] - c[0])/2 + c[0] - 10, 
            c[1]-10, 
            (c[2] - c[0])/2 + c[0] + 10, 
            c[1] + 10
        )
    
    def bottom_pos(self, c):
        return (
            (c[2] - c[0])/2 + c[0] - 10, 
            c[3]-10, 
            (c[2] - c[0])/2 + c[0] + 10, 
            c[3] + 10
        )
    
    def remove(self):
        self.canvas.delete(self.self)
        self.canvas.delete(self.text)

    def getBlocksDict(blocks):
        blocksDict = {}
        for i in blocks:
            blocksDict[i.id] = dict({
                'name':   i.name,
                'type':   i.type,
                'conn':   Connection.getDict(i.conn),
                'code':   i.code,
                'coords': i.coords
            })
        return blocksDict