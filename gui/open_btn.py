import os
import re
import subprocess
import tkinter

from cfg import cnf
from utils import PathFinder

from .widgets import CButton
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
        input_path = self.paste()

        if self.path_check(path=input_path):
            self.press()
            new_path = str(PathFinder(path=input_path))

            if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
                subprocess.Popen(["open", "-R", new_path])
            else:
                subprocess.Popen(["open", new_path])

            if new_path in RowsPath.p:
                RowsPath.p.remove(new_path)
            RowsPath.p.insert(0, new_path)

            if len(RowsPath.p) > 20:
                RowsPath.p.pop(-1)

            RowsVar.v.set(value=RowsVar.v.get() + 1)
        else:
            self.configure(text="Скопируйте путь\nв буфер обмена",
                          fg_color=cnf.blue_color)
            self.after(ms=1500, func=lambda: self.configure(
                text="Открыть", fg_color=cnf.btn_color))
