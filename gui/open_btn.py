import os
import subprocess
import tkinter

import customtkinter

from utils import PathFinder, Shared

from ._shared import _Shared

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

        if result != _Shared.error_text:
            if os.path.isfile(result) or result.endswith((".APP", ".app")):
                subprocess.Popen(["open", "-R", result])
            else:
                subprocess.Popen(["open", result])
            _Shared.string_var.set(result)
        else:
            _Shared.string_var.set(_Shared.error_text)
