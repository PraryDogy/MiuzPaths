import os
import subprocess
import tkinter

from customtkinter import CTkFrame, CTkLabel

from cfg import cnf

from .widgets import CScroll
from utils import PrePaths

class RowsPath:
    p = []


class RowsDict:
    d = {}


class RowsVar:
    v = tkinter.Variable(value=0)


class Rows(tkinter.Frame):
    def __init__(self, master=tkinter):
        tkinter.Frame.__init__(self, master=master, bg=cnf.dgray_color)
        RowsDict.d.clear()
        max_len = 110
        pre_paths = PrePaths().pre_paths

        for x, input_path in enumerate(RowsPath.p):

            src_input_path = input_path

            for prepath in pre_paths[:-1]:
                if prepath in input_path:
                    input_path = input_path.replace(prepath, "")

            short_txt = f"...{input_path[-max_len:]}"
            RowsDict.d[short_txt] = src_input_path

            btn = CTkLabel(master=self, text=short_txt, corner_radius=cnf.corner,
                           anchor="w", justify="left", pady=5,
                           height=40,
                           font=("San Francisco Pro", 14, "normal")
                           )
            btn.pack(fill="x")

            btn.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, btn=btn: self.row_cmd(e=e, btn=btn)
                     )

            btn.bind(sequence='<Configure>',
                     command=lambda e, btn=btn: self.row_cmd_wrap(e=e, btn=btn)
                     )

            if x % 2 == 0:
                btn.configure(fg_color=cnf.bg_color,
                              text_color=cnf.text_color_dark)
            else:
                btn.configure(fg_color=cnf.dgray_color,
                              text_color=cnf.text_color_dark)

    def row_cmd_wrap(self, e: tkinter.Event, btn: CTkLabel):
        btn.configure(wraplength=self.winfo_width())

    def row_cmd(self, e: tkinter.Event, btn: CTkLabel):
        old_bg = btn.cget("fg_color")
        btn.configure(fg_color=cnf.blue_color)
        btn.after(100, lambda: btn.configure(fg_color=old_bg))

        new_path = RowsDict.d[btn.cget("text")]
        if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
            subprocess.Popen(["open", "-R", new_path])
        else:
            subprocess.Popen(["open", new_path])


class Display(CScroll):
    def __init__(self, master=tkinter):
        CScroll.__init__(self, master=master, corner_radius=cnf.corner,
                         fg_color=cnf.dgray_color, scroll_color=cnf.bg_color,
                         bg_color=cnf.bg_color)

        self.load_scroll()
        self.load_rows()

        RowsVar.v.trace_add(mode="read", callback=self.rows_var_callback)

    def rows_var_callback(self, *args):
        self.reload_display()

    def load_scroll(self):
        self.scrollable = CTkFrame(master=self, fg_color=cnf.dgray_color, 
                                   corner_radius=cnf.corner)
        self.scrollable.pack(expand=1, fill="both")

    def load_rows(self):
        self.rows = Rows(master=self.scrollable)
        self.rows.pack(fill="both", expand=1)

    def reload_display(self):
        self.scrollable.destroy()
        self.rows.destroy()

        self.load_scroll()
        self.load_rows()
    