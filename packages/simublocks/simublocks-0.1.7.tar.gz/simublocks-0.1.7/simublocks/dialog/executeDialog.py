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

class executeDialog(object):

    def __init__(self):

        root = self.root = tk.Tk()
        root.resizable(0,0)
        root.title("Run Simulation")

        tk.Label(root, text="Sampling Time:").grid(row=0, column=0, pady=10, padx=10, sticky="E")
        self.T = tk.Entry(root,width=5)
        self.T.insert(tk.END, "0.01")
        self.T.grid(row=0,column=1,sticky="EW", padx=(0,10))
        tk.Label(root, text="Simulation Time:").grid(row=1, column=0, pady=(0,10), padx=10, sticky="E")
        self.tf = tk.Entry(root,width=5)
        self.tf.insert(tk.END, "50")
        self.tf.grid(row=1,column=1,sticky="EW", padx=(0,10))

        tk.Button(root, width=11, text="Run", command=self.execute_button).grid(row=2, column=0, pady=(0,10), padx=10)
        tk.Button(root, width=11, text="Cancel", command=self.cancel_button).grid(row=2, column=1, pady=(0,10), padx=(0,10))
        
        dialogTools.center(root)

    def execute_button(self):
        self.returning = {
            'data': {
                'T': self.T.get(),
                'tf': self.tf.get()
            },
            'status': 'ok'
        }
        self.root.quit()

    def cancel_button(self):
        self.returning = {
            'status': 'cancel'
        }
        self.root.quit()