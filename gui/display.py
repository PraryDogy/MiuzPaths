import tkinter
from cfg import cnf
from .widgets_new import CScroll, CButton
from customtkinter import CTkFrame, CTkLabel
import os

class RowsPath:
    paths = ["aaaaa" for i in range(20)]


class RowsText:
    d = {}


class DisplayRows(tkinter.Frame):
    def __init__(self, master=tkinter):
        tkinter.Frame.__init__(self, master=master, bg=cnf.dgray_color)
        count = 3

        for x, txt in enumerate(RowsPath.paths):
            short_txt = f".../{os.sep.join(txt.split(os.sep)[-count:])}"
            RowsText.d[short_txt] = txt

            btn = CTkLabel(master=self, text=short_txt, corner_radius=cnf.corner,
                           anchor="w", justify="left", height=40)
            btn.pack(fill="x")
            btn.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, btn=btn: self.row_cmd(e=e, btn=btn))

            if x % 2 == 0:
                btn.configure(fg_color=cnf.dgray_color)
            else:
                btn.configure(fg_color=cnf.bg_color)

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

    def load_scroll(self):
        self.scrollable = CTkFrame(master=self, fg_color=cnf.dgray_color, 
                                   corner_radius=cnf.corner)
        self.scrollable.pack(expand=1, fill="both")

    def load_rows(self):
        self.rows = DisplayRows(master=self.scrollable)
        self.rows.pack(fill="both", expand=1)

    def reload_display(self):
        self.scrollable.destroy()
        self.rows.destroy()

        self.load_scroll()
        self.load_rows()
    