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

from simublocks.element.block import *
from simublocks.element.connection import *
from simublocks.dialog import Dialog

class Workspace:

    blocks = []
    graphs = []
    connections = dict()
    id = 0
    importCode = ''
    canvas = None
    new = dict({'conn': None,'block': None,'n_arc': None, 'arc': None})

    def createBlock(name,type, coords = (50,50,150,150), code=None):
        if type == "system":               
            block = System(Workspace.canvas,type,name,coords,code)  
        elif type == "input":
            if code == None: code = 'def ' + str(name) + '(t,k):\n\tif t < 25:\n\t\treturn 1\n\telse:\n\t\treturn 3'
            block = Input(Workspace.canvas,type,name,coords,code)
        elif type == "sum":
            if coords == (50,50,150,150): coords = (50,50,100,100)
            if code == None: code = ['+','+']
            block = Sum(Workspace.canvas,type,name,coords,code)
        elif type == "corner":
            if code == None: code = ['top','right']
            if coords == (50,50,150,150): coords = (50,50,80,80)
            block = Corner(Workspace.canvas,type,name,coords,code)

        Workspace.id +=1 
        block.id = Workspace.id
        Workspace.blocks.append(block)

        Workspace.canvas.tag_bind(block.self, '<B1-Motion>',
            lambda event: block.move(event))

        Workspace.canvas.tag_bind(block.self, '<Double-Button-1>',
        lambda event: Workspace.editBlock(event,block))

        # Bind of input and output ( _out_ , _in_ , _in2_ )

        Workspace.canvas.tag_bind(block._out_, '<ButtonPress-1>',
            lambda event: Workspace.connect(block,block._out_,1))
        
        if block.type != "input": 
            Workspace.canvas.tag_bind(block._in_, '<ButtonPress-1>',
            lambda event: Workspace.connect(block,block._in_,0))

        if block.type == "sum": 
            Workspace.canvas.tag_bind(block._in2_, '<ButtonPress-1>',
            lambda event: Workspace.connect(block,block._in2_,2))    

        return block

    def createGraph(name, coords = (50,50,150,150), code=None):
        if code == None: code = []
        block = Graph(Workspace.canvas,type,name,coords,code)

        Workspace.id +=1 
        block.id = Workspace.id
        Workspace.graphs.append(block)

        Workspace.canvas.tag_bind(block.self, '<B1-Motion>',
            lambda event: block.move(event))
        Workspace.canvas.tag_bind(block.self, '<Double-Button-1>',
            lambda event: Workspace.editGraph(event,block))

    def editGraph(event, block, isSum = False):
        name = Workspace.canvas.itemcget(block.text, 'text')
        
        res = Dialog.editGraph({
            'name': name,
            'code': block.code,
            'blocks': Workspace.blocks
        })

        if res['status'] == 'delete':
            Workspace.graphs.remove(block)
            block.remove()
        elif res['status'] == 'save':
            block.code = res['code']

    def editBlock(event, block, isSum = False):
        name = Workspace.canvas.itemcget(block.text, 'text')
        res = Dialog.editBlock({
            'name': name,
            'code': block.code,
            'type': block.type
        })
        if res['status'] == 'delete':
            if block.conn[0]['n_line'] == None and  block.conn[1]['n_line'] == None:
                Workspace.blocks.remove(block)
                block.remove()
            else:
                Dialog.alert("Alert", ["Block cannot be removed because it has connections"])
        elif res['status'] == 'save':
            code = res['data']['code']
            block.name = res['data']['name']
            Workspace.canvas.itemconfig(block.text, text=res['data']['name'])
            if block.type == 'sum' and (
                not (code[0] == '+' or  code[0] == '-') or
                not (code[1] == '+' or  code[1] == '-')
            ): Dialog.alert("Alert", ["Enter just + or -"])
            block.code = code  
                

    def connect(block, arc, n_arc):
        if (block.conn[n_arc]['n_line'] == None):
            conn = Connection.init(Workspace.canvas, arc, n_arc)
            if conn['status'] == 'start_connection':
                Workspace.new['block'] = block
                Workspace.new['n_arc'] = n_arc
                Workspace.new['arc']   = arc
            elif conn['status'] == "ok":

                Workspace.new['block'].conn[Workspace.new['n_arc']] = {
                    **conn,'n_line':0, 'otherblock': block, 
                    'otherblock_n_arc': n_arc
                }  
                block.conn[n_arc] = {
                    **conn, 'n_line':1, 'otherblock': Workspace.new['block'],
                    'otherblock_n_arc': Workspace.new['n_arc']
                }
                Workspace.connections[conn['line']] = {
                    **conn,
                    'block_out': Workspace.new['block'],
                    'block_out_type': Workspace.new['block'].type,
                    'block_out_id': Workspace.new['block'].id,
                    'block_in': block,
                    'block_in_type': block.type,
                    'block_in_id': block.id
                }
            elif conn['status'] == 'input-output-error':
                Workspace.canvas.itemconfig(arc, fill="black")
                Workspace.canvas.itemconfig(Workspace.new['arc'], fill="black")
                Dialog.alert("Alert", ["Ligue somente Sáida -> Entrada!"])

            if conn['status'] != 'start_connection':
                Workspace.new['n_arc'] = dict({'conn': None,'block': None,'n_arc': None, 'arc': None})

            color = "blue" if conn['status'] != "same" else "black"
            Workspace.canvas.itemconfig(arc, fill=color)

        else:
            conn = block.conn[n_arc]
            del Workspace.connections[conn['line']]
            _out_ = conn['_out_']
            _in_ = conn['_in_']
            Workspace.canvas.itemconfig(_out_, fill="black")
            Workspace.canvas.itemconfig(_in_, fill="black")  
            Workspace.canvas.delete(conn['line'])
            conn['otherblock'].conn[conn['otherblock_n_arc']] = { 'n_line': None }
            block.conn[n_arc] = { 'n_line': None }

    def clean():
        Workspace.canvas.delete('all')
        Workspace.blocks = []
        Workspace.graphs = []
        Workspace.connections = dict()
        Workspace.id = 0
        Workspace.importCode = ''
        Workspace.new = dict({'conn': None,'block': None,'n_arc': None, 'arc': None})