import tkinter

import cfg

from .widgets import OpenBtn
import subprocess


class InitGui():
    def __init__(self):
        cfg.ROOT.bind('<Command-w>', lambda e: self.minim)
        cfg.ROOT.protocol("WM_DELETE_WINDOW", self.minim)
        cfg.ROOT.createcommand('tk::mac::ReopenApplication', cfg.ROOT.deiconify)
        cfg.ROOT.createcommand("tk::mac::Quit" , exit)


        cfg.ROOT.title(cfg.APP_NAME)
        cfg.ROOT.configure(bg=cfg.BGCOLOR, padx=10, pady=10)
        cfg.ROOT.minsize(360, 400)

        OpenBtn(cfg.ROOT)
        
        cfg.ROOT.eval('tk::PlaceWindow . center')
        cfg.ROOT.wm_deiconify()

    def minim(self, e=None):
        applescript = f"""
            set appName to "{cfg.APP_NAME}"
            tell application "System Events"
                if visible of application process appName is true then
                    set visible of application process appName to false
                else
                    set visible of application process appName to true
                end if
            end tell
            """

        args = [
            item
            for x in [("-e",l.strip())
            for l in applescript.split('\n')
            if l.strip() != ''] for item in x]
        subprocess.call(["osascript"] + args)