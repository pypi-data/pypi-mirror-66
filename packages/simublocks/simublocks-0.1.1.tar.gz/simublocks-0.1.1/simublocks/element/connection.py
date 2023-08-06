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

class Connection:
    el1 = None
    el2 = None
    n1 = None
    n2 = None
    
    def init(canvas, element,n_arc):
        
        if Connection.el1 == None:
            Connection.el1 = element
            Connection.n1 = n_arc
            return { 'status': 'start_connection' }
        else:
            Connection.el2 = element
            Connection.n2 = n_arc
            if Connection.el1 == Connection.el2:
                Connection.empty()
                return { 'status': "same" }
            if Connection.n1 != 1 or Connection.n2 == 1:
                Connection.empty()
                return { 'status': "input-output-error" }
            pos1 = canvas.coords(Connection.el1)
            pos2 = canvas.coords(Connection.el2)
            conn = {
                'status': 'ok',
                '_out_': Connection.el1,
                '_in_': Connection.el2,
                'n1': Connection.n1,
                'n2': Connection.n2,
                'line': canvas.create_line([
                    (pos1[0] + pos1[2])/2,
                    (pos1[1] + pos1[3])/2,
                    (pos2[0] + pos2[2])/2,
                    (pos2[1] + pos2[3])/2
                ],width=2)
            }
            Connection.empty()

        return conn

    def empty():
        Connection.el1 = None
        Connection.el2 = None

    def getDict(conns):
        connsDict = []
        for i in conns:
            if i['n_line'] == None: connsDict.append({})
            else: connsDict.append({
                "otherblock": i["otherblock"].name,
                "otherblock_n_arc": i["otherblock_n_arc"],
                "otherblock_id": i["otherblock"].id
            })
        return connsDict