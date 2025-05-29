import abc
import sys
import tkinter
from typing import Callable

import customtkinter

from cfg import cnf
from utils import SysUtils
import subprocess

__all__ = (
    "CScroll",
    "MacMenu",
    )


class CScroll(customtkinter.CTkScrollableFrame):
    def __init__(self, master: tkinter, corner_radius: int = 0, **kw):
        super().__init__(master=master, corner_radius=corner_radius, **kw)

    def get_parrent(self):
        return self._parent_canvas

    def moveup(self, e=None):
        try:
            self.get_parrent().yview_moveto("0.0")
        except Exception as e:
            self.print_err(parent=self, error=e)


class MacMenu(tkinter.Menu, SysUtils):
    def __init__(self):
        main_menu = tkinter.Menu(cnf.root)
        cnf.root.configure(menu=main_menu)

        if sys.version_info.minor < 10:
            cnf.root.createcommand("tkAboutDialog", self.about_dialog)

        self.file_menu = tkinter.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Настройки", menu=self.file_menu)
        self.file_menu.add_command(label="Открыть настройки", command=self.open_settings)

        if sys.version_info.minor < 10:
            self.root.createcommand("tkAboutDialog", self.about_dialog)


    def about_dialog(self):
        try:
            cnf.root.tk.call("tk::mac::standardAboutPanel")
        except Exception as e:
            self.print_err(parent=self, error=e)

    def open_settings(self):
        subprocess.Popen(["open", cnf.json_dir])