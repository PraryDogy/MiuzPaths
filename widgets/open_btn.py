import os
import subprocess
import tkinter

import customtkinter

from cfg import Cfg
from utils import MainItem, PathFinder


class OpenBtn(customtkinter.CTkButton):
    text_ = "Открыть"
    w, h = 200, 60
    anchor = "center"
    radius = 12

    def __init__(self, root: tkinter.Tk, main_item: MainItem, cfg: Cfg):
        super().__init__(
            master=root,
            text=OpenBtn.text_,
            width=OpenBtn.w,
            height=OpenBtn.h,
            anchor=OpenBtn.anchor,
            corner_radius=OpenBtn.radius
        )
        self.bind(sequence="<ButtonRelease-1>", command=self.open_btn_cmd)
        self.root = root
        self.main_item = main_item
        self.cfg = cfg

    def read_clipboard(self):
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}
        ).decode('utf-8')

    def open_btn_cmd(self, e: tkinter.Event):
        input_path = self.read_clipboard()
        path_finder = PathFinder(input_path, self.root, self.main_item)
        result = path_finder.get_result()

        if result != self.main_item.error_text:
            if os.path.isfile(result) or result.endswith(self.cfg.app_exts):
                subprocess.Popen(["open", "-R", result])
            else:
                subprocess.Popen(["open", result])
            self.main_item.string_var.set(result)
        else:
            self.main_item.string_var.set(self.main_item.error_text)

"/Volumes/Shares/test/not exists path/1.jpg"