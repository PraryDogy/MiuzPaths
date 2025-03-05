import os
import re
import subprocess
import tkinter

from cfg import cnf
from utils import PathFinder, Shared

from .widgets import CButton
from .display import HistoryPaths, DisplayVar

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

            res = PathFinder(path=input_path)
            new_path = res.get_result()

            if new_path:

                if new_path == Shared.result_none:
                    self.press()
                    self.btn_message(text="Не могу найти путь")
                    return

                if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
                    subprocess.Popen(["open", "-R", new_path])
                    self.press()

                else:
                    subprocess.Popen(["open", new_path])
                    self.press()

                if new_path in HistoryPaths.lst:
                    HistoryPaths.lst.remove(new_path)

                HistoryPaths.lst.insert(0, new_path)

                if len(HistoryPaths.lst) > 20:
                    HistoryPaths.lst.pop(-1)

            DisplayVar.v.set(value=DisplayVar.v.get() + 1)

        else:
            # self.press()
            self.btn_message(text="Скопируйте путь\nв буфер обмена")

    def btn_message(self, text: str):
        self.configure(text=text, fg_color=cnf.blue_color)
        self.after(ms=500, func=lambda: self.configure(
            text="Открыть", fg_color=cnf.btn_color))