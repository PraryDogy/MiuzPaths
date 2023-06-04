import tkinter

import cfg

from .macosx_menu import Menu
from .widgets import OpenBtn


class InitGui():
    def __init__(self):
        cfg.ROOT.createcommand(
            'tk::mac::ReopenApplication', cfg.ROOT.deiconify)
        cfg.ROOT.createcommand("tk::mac::Quit" , self.on_exit)
        cfg.ROOT.protocol("WM_DELETE_WINDOW", self.on_exit)
        cfg.ROOT.bind('<Command-w>', lambda e: cfg.ROOT.iconify())

        cfg.ROOT.title('MiuzPaths')
        cfg.ROOT.configure(bg=cfg.BGCOLOR)
        cfg.ROOT.geometry("300x200")

        cfg.ROOT.resizable(0, 0)

        t = (
            "Скопируйте путь в буфер обмена."
            )
        l = tkinter.Label(cfg.ROOT, bg=cfg.BGCOLOR, text=t, fg=cfg.BGFONT)
        l.pack(fill="x", expand=True)

        OpenBtn(cfg.ROOT).pack(padx=15, pady=15, fill="x")
        
        Menu()
        cfg.ROOT.eval('tk::PlaceWindow . center')
        cfg.ROOT.deiconify()

    def on_exit(self, e=None):
        quit()