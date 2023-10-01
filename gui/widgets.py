import threading
import tkinter

import tkmacosx

import cfg
from utils import exists_path, paste, reveal, detect_path

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
            text="Последние 20:",
            )
        hist.pack(anchor=tkinter.W)

        self.disp = tkmacosx.SFrame(
            master,
            background=cfg.BGDISP,
            scrollbarwidth=3,
            )
        self.disp.pack(pady=(10, 0), fill=tkinter.BOTH, expand=True)

        lbl = tkinter.Label(
            self.disp,
            text="Скопируйте путь в буфер обмена",
            bg=cfg.BGDISP,
            fg=cfg.BGFONT,
            anchor=tkinter.W,
            justify=tkinter.LEFT,
            pady=10,
            padx=5
            )
        lbl.pack(anchor=tkinter.W)

        self.btn = CBtn(master)
        self.btn.configure(height=4, text="Открыть")
        self.btn.cmd(lambda e: self.btn_cmd())
        self.btn.pack(fill=tkinter.X, pady=(10, 0))

        self.first_load = True

    def btn_cmd(self):
        self.btn.press()
        self.run_task(paste().lstrip().strip("\n"))

    def history_cmd(self, e: tkinter.Event):
        e.widget.configure(bg=cfg.BGPRESSED)
        cfg.ROOT.after(100, lambda: e.widget.configure(bg=cfg.BGDISP))
        self.run_task(e.widget.path)

    def run_task(self, path):
        t1 = threading.Thread(target=lambda: self.open_path(path), daemon=True)
        t1.start()
        while t1.is_alive():
            cfg.ROOT.update()

    def open_path(self, path: str):
        path = "/" + path.strip().strip("/")
        path = detect_path(path)

        if path:
            path = exists_path(path)
       
            if path == "/":
                return

            if reveal(path) and path not in paths:
                paths.insert(0, path)
                self.add_label(path)

    def add_label(self, path):
        if self.first_load:
            self.disp.winfo_children()[0].destroy()
            self.first_load = False

        if len(paths) > 20:
            paths.pop(-1)
            self.disp.winfo_children()[0].destroy()

        lbl = tkinter.Label(
            self.disp,
            text=path,
            bg=cfg.BGDISP,
            fg=cfg.BGFONT,
            anchor=tkinter.W,
            justify=tkinter.LEFT,
            pady=10,
            padx=5
            )

        lbl.path = path
        lbl.bind('<ButtonRelease-1>', self.history_cmd)

        lbl.bind(
            '<Configure>',
            lambda e: lbl.config(wraplength=self.disp.winfo_width())
            )

        widgets = self.disp.winfo_children()[::-1]

        for i in widgets:
            i.pack_forget()
            i.pack(anchor=tkinter.W, fill=tkinter.X, padx=(0, 5))
