import subprocess
import sys
import tkinter

from cfg import cnf
from utils import Err


class MacMenu(tkinter.Menu):
    def __init__(self):
        main_menu = tkinter.Menu(cnf.root)
        cnf.root.configure(menu=main_menu)

        if sys.version_info.minor < 10:
            cnf.root.createcommand("tkAboutDialog", self.about_dialog)

        if sys.version_info.minor < 10:
            self.root.createcommand("tkAboutDialog", self.about_dialog)

    def about_dialog(self):
        try:
            cnf.root.tk.call("tk::mac::standardAboutPanel")
        except Exception as e:
            Err.print_error(e)
