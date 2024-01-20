import tkinter
from cfg import cnf
from .widgets_new import CScroll, CButton
from customtkinter import CTkFrame, CTkLabel
import os

class RowsPath:
    # paths = ["aaaaa" for i in range(20)]
    paths = []


class RowsDict:
    d = {}


class RowsVar:
    v = tkinter.Variable(value=0)


class Rows(tkinter.Frame):
    def __init__(self, master=tkinter):
        tkinter.Frame.__init__(self, master=master, bg=cnf.dgray_color)
        max_len = 100
        max_chunks = -3

        for x, txt in enumerate(RowsPath.paths):
            short_path = txt.split(os.sep)[max_chunks:]
            short_txt = f"...{os.path.join(*short_path)[:max_len]}"

            RowsDict.d[short_txt] = txt

            btn = CTkLabel(master=self, text=short_txt, corner_radius=cnf.corner,
                           anchor="w", justify="left", height=40)
            btn.pack(fill="x")

            btn.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, btn=btn: self.row_cmd(e=e, btn=btn)
                     )

            btn.bind(sequence='<Configure>',
                     command=lambda e, btn=btn: self.row_cmd_wrap(e=e, btn=btn)
                     )

            if x % 2 == 0:
                btn.configure(fg_color=cnf.dgray_color)
            else:
                btn.configure(fg_color=cnf.bg_color)

    def row_cmd_wrap(self, e: tkinter.Event, btn: CTkLabel):
        btn.configure(wraplength=self.winfo_width())

    def row_cmd(self, e: tkinter.Event, btn: CTkLabel):
        oldbg = btn.cget("fg_color")
        btn.configure(fg_color=cnf.blue_color)
        btn.after(100, lambda: btn.configure(fg_color=oldbg))


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
    