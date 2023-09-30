import threading
import tkinter

import tkmacosx

import cfg
from utils import exists_path, is_mac, is_win, paste, reveal, to_mac, to_win

paths = []


class CBtn(tkinter.Label):
    def __init__(self, master: tkinter, **kwargs):
        tkinter.Label.__init__(
            self, master, bg=cfg.BGBUTTON, fg=cfg.BGFONT, height=3)

    def press(self):
        self['bg'] = cfg.BGPRESSED
        cfg.ROOT.after(100, lambda: self.configure(bg=cfg.BGBUTTON))

    def cmd(self, cmd):
        self.bind('<ButtonRelease-1>', cmd)


class OpenBtn:
    def __init__(self, master: tkinter):
        hist = tkinter.Label(
            master,
            bg=cfg.BGCOLOR,
            fg=cfg.BGFONT,
            text="Последние 20",
            )
        hist.pack(anchor=tkinter.W)

        self.disp = tkmacosx.SFrame(
            master,
            background=cfg.BGDISP,
            scrollbarwidth=1,
            
            )
        self.disp.pack(pady=(10, 0), fill=tkinter.BOTH, expand=True)

        lbl = tkinter.Label(
            self.disp,
            text="Скопируйте путь в буфер обмена",
            anchor=tkinter.W,
            bg=cfg.BGDISP,
            fg=cfg.BGFONT,
            )
        lbl.pack(pady=5, padx=5)

        self.btn = CBtn(master)
        self.btn.configure(height=4, text="Открыть")
        self.btn.cmd(lambda e: self.open_path())
        self.btn.pack(fill=tkinter.X, pady=(10, 0))

        self.first_load = True

    def open_path(self):
        self.btn.press()
        path = paste().lstrip().strip("\n")

        t1 = threading.Thread(target=lambda: self.task(path))
        t1.start()
        while t1.is_alive():
            cfg.ROOT.update()
            
    def task(self, path, e=None):
        if e:
            path = e.widget["text"]
            e.widget.configure(bg=cfg.BGDISP)

        if is_win(path):
            path = to_mac(path)

        elif is_mac(path):
            path = to_win(path)
            path = to_mac(path)

        exist = exists_path(path)
        reveal(exist)

        if exist not in paths:
            paths.append(exist)
            self.add_label(exist)

    def ent(self, e=tkinter.Event):
        e.widget.configure(bg=cfg.BGSELECTED)

    def out(self, e=tkinter.Event):
        e.widget.configure(bg=cfg.BGDISP)


    def add_label(self, path):
        if self.first_load:
            self.disp.winfo_children()[0].destroy()
            self.first_load = False

        if len(paths) > 20:
            paths.pop(0)
            self.disp.winfo_children()[0].destroy()

        lbl = tkinter.Label(
            self.disp,
            text=path,
            anchor=tkinter.W,
            justify=tkinter.LEFT,
            bg=cfg.BGDISP,
            fg=cfg.BGFONT,
            wraplength=500,
            pady=10,
            padx=5
            )
        lbl.pack(anchor=tkinter.W, fill=tkinter.X, side="top")
        lbl.bind('<ButtonRelease-1>', lambda e: self.task(None, e))
        lbl.bind("<Enter>", self.ent)
        lbl.bind("<Leave>", self.out)