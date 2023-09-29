import tkinter

import cfg

from .widgets import OpenBtn
import subprocess


class InitGui():
    def __init__(self):
        # cfg.ROOT.createcommand(
            # 'tk::mac::ReopenApplication', cfg.ROOT.deiconify)

        cfg.ROOT.createcommand("tk::mac::Quit" , self.on_exit)

        cfg.ROOT.protocol("WM_DELETE_WINDOW", self.minim)
        cfg.ROOT.bind('<Command-w>', lambda e: self.minim)

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
        
        cfg.ROOT.eval('tk::PlaceWindow . center')
        cfg.ROOT.deiconify()

    def on_exit(self, e=None):
        quit()

    def minim(self, e=None):

        args = (
            "-e", f"set tApp to \"{cfg.APP_NAME}\"",
            "-e", "tell application tApp to activate",
            "-e", "tell application \"System Events\" to "
            "tell process tApp to keystroke \"h\" using command down"
            )
            # "set visible of process tApp to false",
        subprocess.call(["osascript", *args])