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

class editGraphDialog(object):

    def __init__(self, data):

        root = self.root = tk.Tk()
        root.resizable(0,0)
        root.title(str("Edit Block: ") + str(data['name']))
        self.root = root
        self.data = data 
        tk.Label(root, text="legend:").grid(row=1, column=1)
        tk.Label(root, text="color:").grid(row=1, column=2)
        count = 0
        self.code = []
        for block in data['blocks']:
            if block.type == "system":
                count += 1
                self.code.append({
                    'id': block.id,
                    'type': block.type,
                    'subtype': 'output',
                    **self.listLine(count,'output of "' + block.name + '"')
                })
                count += 1
                self.code.append({
                    'id': block.id,
                    'type': block.type,
                    'subtype': 'input',
                    **self.listLine(count,'input of "' + block.name + '"')
                })
            elif block.type == "input":
                count += 1
                self.code.append({
                    'id': block.id,
                    'type': block.type,
                    **self.listLine(count,block.name)
                })

        
        tk.Button(root, width=11, text="Save", command=self.save_button).grid(row=0, column=0,pady=(10,10))
        tk.Button(root, width=11, text="Cancel", command=self.cancel_button).grid(row=0, column=1,pady=(10,10))
        tk.Button(root, width=11, text="Remove Block", command=self.remove_button).grid(row=0, column=2,pady=(10,10))
        
        dialogTools.center(root)

    def save_button(self):
        self.data['code'] = []
        for i in self.code:
            self.data['code'].append({
                **i,
                'check': i['check'].get(),
                'legend': i['legend'].get(),
                'color': i['color'].get()
            })
        self.returning = {
            'status': 'save',
            'code': self.data['code']
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

    def listLine(self, count, label):
        s = dict()
        s['legend'] = tk.Entry(self.root)
        try: s['legend'].insert(tk.END, self.data['code'][count-1]['legend'])
        except: pass      
        s['legend'].grid(row=count+1, column=1,padx=(5,5),pady=(0,10))

        s['color'] = tk.Entry(self.root)
        try: s['color'].insert(tk.END, self.data['code'][count-1]['color'])
        except: pass      
        s['color'].grid(row=count+1, column=2,padx=(5,10),pady=(0,10))

        s['check'] = tk.BooleanVar() 

        c = tk.Checkbutton(self.root, text=label,
            command=lambda:self.setCheck(s['check']))
        c.grid(row=count+1, column=0,stick="w",padx=(10,5),pady=(0,10))
        
        try: 
            value = self.data['code'][count-1]['check']
            s['check'].set(value)
            if value: c.select()
        except: pass

        return s

    def setCheck(self,var):
        if var.get() == 0: var.set(1)
        else: var.set(0)