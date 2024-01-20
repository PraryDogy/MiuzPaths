import os
import re
import subprocess
import tkinter

from cfg import cnf
from utils import PathFinder

from .widgets_new import CButton
from .display import RowsPath, RowsVar

__all__ = ("OpenBtn", )


class OpenUtils:
    def paste(self):
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

    def path_check(self, path: str):
        striped = path.strip()

        link_reg = r'http://|https://'
        if re.findall(link_reg, striped):
            return False

        striped = striped.replace("\\", "/")

        mac_reg = r'/?.{,100}/.{,100}/.{,100}'
        if not re.findall(mac_reg, striped):
            return False
        
        return True



class OpenBtn(CButton, OpenUtils):
    def __init__(self, master: tkinter):
        CButton.__init__(self, master=master, text="Открыть",
                         width=200, height=60)
        
        self.cmd(self.open_btn_cmd)

    def open_btn_cmd(self, e: tkinter.Event):
        self.press()

        input_path = self.paste()

        if self.path_check(path=input_path):
            new_path = str(PathFinder(path=input_path))

            if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
                subprocess.Popen(["open", "-R", new_path])
            else:
                subprocess.Popen(["open", new_path])

            if new_path not in RowsPath.paths:
                RowsPath.paths.append(new_path)
            RowsVar.v.set(value=RowsVar.v.get() + 1)