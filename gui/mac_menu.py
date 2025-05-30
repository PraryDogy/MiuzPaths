import subprocess
import sys
import tkinter

from cfg import cnf
from utils.utils import Err


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
            Err.print_error(e)

    def open_settings(self):
        subprocess.Popen(["open", cnf.json_dir])