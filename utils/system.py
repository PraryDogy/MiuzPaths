import os
import subprocess
import tkinter
import traceback
from typing import Literal

from cfg import cnf

__all__ = ("SysUtils", )


class SysUtils:
    def run_applescript(self, script: Literal["applescript"]):
        args = [
            arg for row in script.split("\n")
            for arg in ("-e", row.strip())
            if row.strip()
            ]
        subprocess.call(args=["osascript"] + args)

    def print_err(self, write=False):
        print(traceback.format_exc())

        if write:
            with open(os.path.join(cnf.cfg_dir, "err.txt"), "a") as f:
                f.write(traceback.format_exc())

    def on_exit(self, e: tkinter.Event = None):
        ...
        quit()
