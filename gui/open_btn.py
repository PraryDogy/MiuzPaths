import os
import subprocess
import tkinter

import customtkinter

from utils import PathFinder, Shared

from .display import DisplayVar, HistoryPaths

__all__ = ("OpenBtn", )


class OpenBtn(customtkinter.CTkButton):
    def __init__(self, master: tkinter):
        super().__init__(master=master, text="Открыть", width=200, height=60,
                         anchor="center", corner_radius=12)
        self.bind(sequence="<ButtonRelease-1>", command=self.open_btn_cmd)

    def read_clipboard(self):
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

    def open_btn_cmd(self, e: tkinter.Event):
        input_path = self.read_clipboard()

        path_finder = PathFinder(input_path)
        result = path_finder.get_result()

        if result != Shared.error_text:
            if os.path.isfile(result) or result.endswith((".APP", ".app")):
                subprocess.Popen(["open", "-R", result])

            else:
                subprocess.Popen(["open", result])

            if result in HistoryPaths.lst:
                HistoryPaths.lst.remove(result)

            HistoryPaths.lst.insert(0, result)

            if len(HistoryPaths.lst) > 20:
                HistoryPaths.lst.pop(-1)

        else:
            DisplayVar.v.set(Shared.error_text)



    def btn_message(self, text: str):
        self.configure(text=text)
        self.after(ms=500, func=lambda: self.configure(text="Открыть"))