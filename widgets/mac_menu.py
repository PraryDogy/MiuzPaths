import sys
import tkinter

from utils import Err


class MacMenu(tkinter.Menu):
    def __init__(self, master: tkinter.Tk):
        self.root = master
        main_menu = tkinter.Menu(self.root)
        self.root.configure(menu=main_menu)

        if sys.version_info.minor < 10:
            self.root.createcommand("tkAboutDialog", self.about_dialog)

        if sys.version_info.minor < 10:
            self.root.createcommand("tkAboutDialog", self.about_dialog)

    def about_dialog(self):
        try:
            self.root.tk.call("tk::mac::standardAboutPanel")
        except Exception as e:
            Err.print_error(e)
