import tkinter

from .widgets_new import CButton
from cfg import cnf

__all__ = ("OpenBtn", )


class OpenBtn(CButton):
    def __init__(self, master: tkinter):
        CButton.__init__(self, master=master, text="Открыть",
                         width=200, height=60)
        
        self.cmd(self.test)

    def test(self, e: tkinter.Event):
        self.press()
        ...