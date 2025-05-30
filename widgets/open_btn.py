import os
import subprocess
import tkinter

import customtkinter

from utils import PathFinder, Shared


class OpenBtn(customtkinter.CTkButton):
    def __init__(self, root: tkinter.Tk):
        super().__init__(master=root, text="Открыть", width=200, height=60,
                         anchor="center", corner_radius=12)
        self.bind(sequence="<ButtonRelease-1>", command=self.open_btn_cmd)
        self.root = root

    def read_clipboard(self):
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

    def open_btn_cmd(self, e: tkinter.Event):
        input_path = self.read_clipboard()
        path_finder = PathFinder(input_path, self.root)
        result = path_finder.get_result()

        if result != Shared.error_text:
            if os.path.isfile(result) or result.endswith((".APP", ".app")):
                subprocess.Popen(["open", "-R", result])
            else:
                subprocess.Popen(["open", result])
            Shared.string_var.set(result)
        else:
            Shared.string_var.set(Shared.error_text)
