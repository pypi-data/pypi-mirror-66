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
from tkinter.scrolledtext import ScrolledText
from simublocks.dialog.dialogTools import dialogTools

class importCodeDialog(object):

    def __init__(self, code):

        root = self.root = tk.Tk()
        root.resizable(0,0)
        root.title("Import Code and Packages")

        self.inputCode = ScrolledText(root, height=5,width=50)
        self.inputCode.insert(tk.END, code)
        self.inputCode.grid(row=0, column=0,columnspan=2)
        tk.Button(root, width=11, text="Save", command=self.save_button).grid(row=1, column=0)
        tk.Button(root, width=11, text="Cancel", command=self.cancel_button).grid(row=1, column=1)

        dialogTools.center(root)

    def save_button(self):
        self.returning = {
            'code': self.inputCode.get(1.0, tk.END),
            'status': 'ok'
        }
        self.root.quit()

    def cancel_button(self):
        self.returning = {
            'status': 'cancel'
        }
        self.root.quit()