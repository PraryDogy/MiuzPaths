import os
import re
import subprocess
import tkinter

import customtkinter

from cfg import cnf
from utils import PathFinder, Shared

from .display import DisplayVar, HistoryPaths

__all__ = ("OpenBtn", )


class OpenUtils:
    @classmethod
    def paste(cls):
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

    @classmethod
    def path_check(cls, path: str):
        striped = path.strip()

        link_reg = r'http://|https://'
        if re.findall(link_reg, striped):
            return False

        striped = striped.replace("\\", "/")

        mac_reg = r'/?.{,100}/.{,100}/.{,100}'
        if not re.findall(mac_reg, striped):
            return False
        
        return True


class OpenBtn(customtkinter.CTkButton):
    def __init__(self, master: tkinter):
        super().__init__(
            master=master,
            text="Открыть",
            width=200,
            height=60,
            anchor="center",
            corner_radius=12
        )
        self.cmd(self.open_btn_cmd)

    def cmd(self, cmd: callable):
        self.bind(sequence="<ButtonRelease-1>", command=cmd)

    def uncmd(self):
        self.unbind(sequence="<ButtonRelease-1>")

    def open_btn_cmd(self, e: tkinter.Event):
        input_path = OpenUtils.paste()

        if OpenUtils.path_check(input_path):

            res = PathFinder(input_path)
            new_path = res.get_result()

            if new_path:

                if new_path == Shared.result_none:
                    self.btn_message("Не могу найти путь")
                    return

                if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
                    subprocess.Popen(["open", "-R", new_path])

                else:
                    subprocess.Popen(["open", new_path])

                if new_path in HistoryPaths.lst:
                    HistoryPaths.lst.remove(new_path)

                HistoryPaths.lst.insert(0, new_path)

                if len(HistoryPaths.lst) > 20:
                    HistoryPaths.lst.pop(-1)

            else:
                self.btn_message("Не могу найти путь")
                return

            DisplayVar.v.set(value=DisplayVar.v.get() + 1)

        else:
            self.btn_message("Скопируйте путь\nв буфер обмена")

    def btn_message(self, text: str):
        self.configure(text=text)
        self.after(ms=500, func=lambda: self.configure(text="Открыть"))