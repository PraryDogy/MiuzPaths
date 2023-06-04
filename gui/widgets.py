import threading
import tkinter

import cfg
from utils import (exists_path, is_mac, is_win, paste,
                   reveal, to_mac, to_win)


class CBtn(tkinter.Label):
    def __init__(self, master: tkinter, **kwargs):
        tkinter.Label.__init__(
            self, master, bg=cfg.BGBUTTON, fg=cfg.BGFONT, height=3)

    def press(self):
        self['bg'] = cfg.BGPRESSED
        cfg.ROOT.after(100, lambda: self.configure(bg=cfg.BGBUTTON))

    def cmd(self, cmd):
        self.bind('<ButtonRelease-1>', cmd)


class OpenBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master)
        self['width'] = 10
        self['text'] = 'Открыть'
        self.cmd(lambda e: self.open_path())

    def open_path(self):
        t1 = threading.Thread(target=self.task)
        t1.start()
        while t1.is_alive():
            cfg.ROOT.update()
            
    def task(self):
        self.press()
        path = paste()

        if is_win(path):
            path = to_mac(path)

        elif is_mac(path):
            path = to_win(path)
            path = to_mac(path)
            
        exist = exists_path(path)
        reveal(exist)