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

import tkinter as tk
from simublocks.dialog.dialogTools import dialogTools

class newBlockDialog(object):

    def __init__(self,b1, b2,b3):

        root = self.root = tk.Tk()
        root.title('Add new Block')
        
        # button frame
        frm_2 = tk.Frame(root)
        frm_2.pack(padx=10, pady=10)

        # buttons
        btn_1 = tk.Button(frm_2, width=10, text=b1)
        btn_1['command'] = lambda: self.button_action(b1)
        btn_1.pack(side='left')
        btn_1.focus_set()
        
        btn_2 = tk.Button(frm_2, width=10, text=b2)
        btn_2['command'] = lambda: self.button_action(b2)
        btn_2.pack(side='left')

        btn_3 = tk.Button(frm_2, width=10, text=b3)
        btn_3['command'] = lambda: self.button_action(b3)
        btn_3.pack(side='left')

        dialogTools.center(root)

    def button_action(self, value):
        self.returning = value
        self.root.quit()