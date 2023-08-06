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

from simublocks.element.block.tools import blockTools

class Block(blockTools):
    def __init__(self, canvas, text, coords, code):
        self.canvas= canvas
        self.conn = [{ 'n_line': None },{ 'n_line': None },{ 'n_line': None }]
        self.name = text
        self.code = code
        self.ss = None # Matrizes de Espaço de Estados
        self.x = None # Vetor de Estados
        self.u = None # Entrada do Bloco

        self.coords = coords
        self.self = canvas.create_rectangle(self.coords,fill="white")
        self.text = canvas.create_text((
            (self.coords[2] - self.coords[0])/2 + self.coords[0],
            (self.coords[3] - self.coords[1])/2 + self.coords[1],
        ), text=text)