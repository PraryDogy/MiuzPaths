import tkinter

import cfg
from utils import run_applescript

from .widgets import Widgets


class InitGui():
    def __init__(self):
        # cfg.ROOT.bind('<Command-w>', lambda e: self.minim)
        # cfg.ROOT.protocol("WM_DELETE_WINDOW", self.minim)
        # cfg.ROOT.createcommand('tk::mac::ReopenApplication', self.maxim)
        cfg.ROOT.createcommand("tk::mac::Quit" , exit)

        self.root.bind(sequence="<Command-Key>", func=self.minimize)
        cfg.ROOT.protocol(name="WM_DELETE_WINDOW", func=cfg.ROOT.withdraw)
        cfg.ROOT.createcommand("tk::mac::ReopenApplication", cfg.ROOT.deiconify)

        cfg.ROOT.title(cfg.APP_NAME)
        cfg.ROOT.configure(bg=cfg.BGCOLOR, padx=10, pady=10)
        cfg.ROOT.minsize(360, 400)

        Widgets(cfg.ROOT)
        
        cfg.ROOT.eval('tk::PlaceWindow . center')
        cfg.ROOT.wm_deiconify()

    def minimize(self, e: tkinter.Event):
        if e.char == "w":
            cfg.ROOT.wm_withdraw()

    def minim(self, e=None):
        applescript = f"""
            set appName to "{cfg.APP_NAME}"
            tell application "System Events"
                set visible of application process appName to false
            end tell
            """

        run_applescript(applescript)

    def maxim(self, e=None):
        applescript = f"""
            set appName to "{cfg.APP_NAME}"
            tell application appName to activate 
            end tell
            """

        run_applescript(applescript)