import os
import subprocess
import tkinter
import traceback

from cfg import cnf

__all__ = ("SysUtils", )


class SysUtils:
    @staticmethod
    def run_applescript(self, script: str):
        args = [
            arg for row in script.split("\n")
            for arg in ("-e", row.strip())
            if row.strip()
            ]
        subprocess.call(args=["osascript"] + args)

    @staticmethod
    def print_err(parent: object, error: Exception):
        tb = traceback.extract_tb(error.__traceback__)
        last_call = tb[-1]
        filepath = last_call.filename
        filename = os.path.basename(filepath)
        class_name = parent.__class__.__name__
        line_number = last_call.lineno
        error_message = str(error)
        
        print()
        print(f"{filename} > {class_name} > row {line_number}: {error_message}")
        print(f"{filepath}:{line_number}")
        print()

    def on_exit(self, e: tkinter.Event = None):
        ...
        quit()
