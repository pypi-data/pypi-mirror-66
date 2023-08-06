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

from simublocks.dialog.newBlockDialog import newBlockDialog
from simublocks.dialog.editBlockDialog import editBlockDialog
from simublocks.dialog.editGraphDialog import editGraphDialog
from simublocks.dialog.alertDialog import alertDialog
from simublocks.dialog.executeDialog import executeDialog
from simublocks.dialog.importCodeDialog import importCodeDialog
from simublocks.dialog.newCornerDialog import newCornerDialog

class Dialog:

    def newBlock(op1,op2,op3):
        msgbox = newBlockDialog(op1,op2,op3)
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning

    def editBlock(data):
        msgbox = editBlockDialog(data)
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning

    def editGraph(data):
        msgbox = editGraphDialog(data)
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning

    def alert(title, msg):
        msgbox = alertDialog(title,msg)
        msgbox.root.mainloop()
        msgbox.root.destroy()

    def execute():
        msgbox = executeDialog()
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning

    def importCode(code):
        msgbox = importCodeDialog(code)
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning

    def newCorner():
        msgbox = newCornerDialog()
        msgbox.root.mainloop()
        msgbox.root.destroy()
        return msgbox.returning
        
