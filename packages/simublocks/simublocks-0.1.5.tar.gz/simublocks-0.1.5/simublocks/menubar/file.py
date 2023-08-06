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

import json
import os
from tkinter import filedialog
from simublocks.element import Workspace, Block
from simublocks.dialog import Dialog

class FileApp:
    def save():
        # open file
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        # if no file is selected, cancel process
        if f is None: return
        # save project as JSON
        f.write(json.dumps({
            'name': os.path.basename(f.name),
            'importCode': Workspace.importCode,
            'blocks': Block.getBlocksDict(Workspace.blocks),
            'graphs': Block.getBlocksDict(Workspace.graphs)
        },indent=4))
        # close file
        f.close()

    def new():
        # clear workspace for start a new project
        Workspace.clean()

    def open():
        # open file
        f = filedialog.askopenfile()
        if f != None:
            try:
                # init a new workspace
                FileApp.new()
                # create project from JSON
                FileApp.createProject( json.loads( f.read() ) )
            except Exception as e:
                print(e)
                # Error if a not JSON file is selected
                Dialog.alert("Alerta", ["Selecione um arquivo válido!"])

    def createProject(project):
        blocks = {}
        # Create each block
        for i in project['blocks']:
            b = project['blocks'][i]
            blocks[i] = Workspace.createBlock(b['name'],b['type'],b['coords'], b['code'])

        for i in project['graphs']:
            b = project['graphs'][i]
            blocks[i] = Workspace.createGraph(b['name'],b['coords'], b['code'])
        
        Workspace.importCode = project['importCode']

        # Create connections
        for i in project['blocks']:
            b = project['blocks'][i]
            conn = b['conn'][1]
            b = blocks[i]
            if not not conn:
                id = str(conn['otherblock_id'])
                other = blocks[id]
                
                Workspace.connect(b, b._out_, 1)
                if conn['otherblock_n_arc'] == 0:
                    Workspace.connect(other, other._in_, conn['otherblock_n_arc'])
                else:
                    Workspace.connect(other, other._in2_, conn['otherblock_n_arc'])
                
            