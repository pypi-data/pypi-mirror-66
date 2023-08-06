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

import numpy as np
import control as c
import json

from simublocks.element import Workspace
from simublocks.dialog import Dialog

class simulationTools:

    def loadBlocks(self, s):
        for i in Workspace.blocks:
            if i.type == 'input':
                i.input = np.zeros(len(s['t']))
                s['inputs'][i.id] = i
            elif i.type == 'system':
                if i.code['type'] == "TF":
                    if i.code['sub_type'] == "continuous":
                        i.ss =  c.ssdata(
                                    c.c2d(
                                        c.ss(
                                            c.tf(
                                                json.loads(i.code['self'][0]),
                                                json.loads(i.code['self'][1])
                                            )
                                        ),s['T']
                                    )
                                )
                    else:
                        i.ss =  c.ssdata(
                                    c.ss(
                                        c.tf(
                                            json.loads(i.code['self'][0]),
                                            json.loads(i.code['self'][1]), s['T']
                                        )
                                    )
                                )
                elif i.code['type'] == "SS":
                    if i.code['sub_type'] == "continuous":
                        i.ss =  c.ssdata(
                                    c.c2d(
                                        c.ss(
                                            json.loads(i.code['self'][0]),
                                            json.loads(i.code['self'][1]),
                                            json.loads(i.code['self'][2]),
                                            json.loads(i.code['self'][3])
                                        ),s['T']
                                    )
                                )
                    else:
                        i.ss =  c.ssdata(
                                    c.ss(
                                        json.loads(i.code['self'][0]),
                                        json.loads(i.code['self'][1]),
                                        json.loads(i.code['self'][2]),
                                        json.loads(i.code['self'][3])
                                        , s['T']
                                    )
                                )
                else:
                    Dialog.alert("Alerta", ["Um dos blocos não está configurado como TF ou SS"])
                lt = len(s['t'])
                lA = len(i.ss[0])
                i.x = np.zeros((lt,lA,1))  
                i.u = np.zeros((lt,1,1))   
                s['blocks'][i.id] = i
                
        return s

    def search(self, other, k):
        if other.type == "sum":
            soma = 0
            
            if 'otherblock' in other.conn[0]:
                next0 = other.conn[0]['otherblock']
                if other.code[0] == "+":  soma += self.search(next0, k)
                else:  soma-= self.search(next0, k)
            
            if 'otherblock' in other.conn[2]:
                next2 = other.conn[2]['otherblock']
                if other.code[1] == "+": soma += self.search(next2, k)
                else: soma-= self.search(next2, k)
            
            return  soma
        
        elif other.type == "corner":
            if 'otherblock' in other.conn[0]:
                next = other.conn[0]['otherblock']
                return self.search(next, k)
            else:
                return 0
        
        elif other.type == "input":
            return other.input[k]
        
        elif other.type == "system":
            if other.ss[3] == 0 or 'otherblock' not in other.conn[0]:
                return (other.ss[2]@other.x[k])[0][0]
            else:
                next = other.conn[0]['otherblock']
                _value = self.search(next,k)
                return (other.ss[2]@other.x[k] + other.ss[3]*_value)[0][0]
