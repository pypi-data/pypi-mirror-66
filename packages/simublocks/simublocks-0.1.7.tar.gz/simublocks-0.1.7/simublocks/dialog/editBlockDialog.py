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
from tkinter import ttk
from simublocks.dialog.dialogTools import dialogTools

class editBlockDialog(object):

    def __init__(self, data):

        root = self.root = tk.Tk()
        root.resizable(0,0)
        root.title(str("Edit Block: ") + str(data['name']))
        self.data = data 
        self.root = root

        if data['type'] != 'corner':
            tk.Label(root, text="Name:").grid(row=0, column=0, pady=10)
            self.inputName = tk.Entry(root)
            self.inputName.insert(tk.END, self.data['name'])
            self.inputName.grid(row=0,column=1,columnspan=2,sticky="EW", pady=10, padx=(0,10))

        if data['type'] == 'input':
            self.editInput(root)
        elif data['type'] == 'sum':
            self.editSum(root)
        elif data['type'] == "system":
            if data['code']['type'] == "TF":
                self.editSystemTF(root)
            else:
                self.editSystemSS(root)
        
        if data['type'] != 'corner':
            tk.Button(root, width=11, text="Save", command=self.save_button).grid(row=4, column=0, pady=(5,10), padx=(10,0))
        tk.Button(root, width=11, text="Cancel", command=self.cancel_button).grid(row=4, column=1, pady=(5,10), padx=(10,10))
        tk.Button(root, width=11, text="Remove Block", command=self.remove_button).grid(row=4, column=2, pady=(5,10), padx=(0,10))
        
        dialogTools.center(root)

    def save_button(self):
        self.data['name'] = self.inputName.get()

        if self.data['type'] == 'input':
            self.data['code'] = self.inputCode.get(1.0, tk.END)
        elif self.data['type'] == 'sum':
            self.data['code'] = [
                self.input1.get(),
                self.input2.get()
            ]
        else:
            if self.data['code']['type'] == "TF":
                self.data['code']['self'] = [
                    self.input1.get(),
                    self.input2.get()
                ]
            else:
                self.data['code']['self'] = [
                    self.input1.get(),
                    self.input2.get(),
                    self.input3.get(),
                    self.input4.get()
                ]
            self.data['code']['sub_type'] = self.dropdown.get()

        self.returning = {
            'data': self.data,
            'status': 'save'
        }
        self.root.quit()

    def cancel_button(self):
        self.returning = {
            'status': 'cancel'
        }
        self.root.quit()

    def remove_button(self):
        self.returning = {
            'status': 'delete'
        }
        self.root.quit()

    def twoEntries(self, root, code):
        self.input1 = tk.Entry(root, width=11)
        self.input1.insert(tk.END, code[0])
        self.input1.grid(row=2, column=1, pady=5)
        self.input2 = tk.Entry(root, width=11)
        self.input2.insert(tk.END, code[1])
        self.input2.grid(row=2, column=2, pady=5)
    
    def moreTwoEntries(self, root, code):
        self.input3 = tk.Entry(root, width=11)
        self.input3.insert(tk.END, code[0])
        self.input3.grid(row=3, column=1, pady=5)
        self.input4 = tk.Entry(root, width=11)
        self.input4.insert(tk.END, code[1])
        self.input4.grid(row=3, column=2, pady=5)

    def editSum(self, root):
        tk.Label(root, text="Type:").grid(row=2, column=0)
        code = self.data['code']
        self.dropdownButton1(code)
        self.dropdownButton2(code)

    def dropdownButton(self,root):
        tk.Label(root, text="Type:").grid(row=1, column=0)
        self.dropdown = ttk.Combobox(root,state="readonly", values=[ "continuous",  "discrete"])
        self.dropdown.grid(row=1, column=1, columnspan=2)
        if self.data['code']['sub_type'] == "continuous":
            self.dropdown.current(0)
        else:
            self.dropdown.current(1)

    def editSystemTF(self, root):
        self.dropdownButton(root)
        tk.Label(root, text="Num and Den:").grid(row=2, column=0)
        code = self.data['code']['self']
        self.twoEntries(root, code)

    def editSystemSS(self, root):
        self.dropdownButton(root)
        code = self.data['code']['self']
        tk.Label(root, text="A and B:").grid(row=2, column=0)
        self.twoEntries(root, code)
        tk.Label(root, text="C and D:").grid(row=3, column=0)
        self.moreTwoEntries(root, code[2:])

    def editInput(self, root):
        tk.Label(root, text="Code:").grid(row=1, column=0)
        self.inputCode = ScrolledText(root, height=7,width=50)
        self.inputCode.insert(tk.END, self.data['code'])
        self.inputCode.grid(row=1, column=1,columnspan=2)

    def dropdownButton1(self, code):
        self.input1 = ttk.Combobox(self.root, width=8, state="readonly", values=["+","-"])
        self.input1.grid(row=2, column=1, pady=(5,10))
        if code[0] == "+": self.input1.current(0)
        else: self.input1.current(1)

    def dropdownButton2(self, code):
        self.input2 = ttk.Combobox(self.root,  width=8, state="readonly", values=["+", "-"])
        self.input2.grid(row=2, column=2)
        if code[1] == "+": self.input2.current(0)
        else: self.input2.current(1)