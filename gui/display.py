import os
import subprocess
import tkinter

import customtkinter
from customtkinter import CTkFrame, CTkLabel

from cfg import cnf


class HistoryPaths:
    lst = []


class ShortFullPaths:
    dct = {}


class DisplayVar:
    v = tkinter.Variable(value=0)


class ContextMenu(tkinter.Menu):
    def __init__(self, e: tkinter.Event):
        tkinter.Menu.__init__(self, master=cnf.root)

        widget: tkinter.Label = e.widget
        widget_text = widget.cget("text")

        if len(widget_text) > 100:
            widget_text = widget_text[:100]

        self.add_command(label=f"Удалить",
                         command=lambda: self.clear(e=e))
        self.add_separator()
        self.add_command(label="Удалить все",
                         command=lambda: self.clear_all(e=e))

    def clear(self, e: tkinter.Event = None):
        HistoryPaths.lst.remove(ShortFullPaths.dct[e.widget.cget("text")])
        DisplayVar.v.set(value=DisplayVar.v.get() + 1)

    def clear_all(self, e: tkinter.Event = None):
        HistoryPaths.lst.clear()
        DisplayVar.v.set(value=DisplayVar.v.get() + 1)



class Rows(tkinter.Frame):
    def __init__(self, master=tkinter):
        tkinter.Frame.__init__(self, master=master)
        ShortFullPaths.dct.clear()
  
        for x, input_path in enumerate(HistoryPaths.lst):

            ShortFullPaths.dct[input_path] = input_path

            btn = CTkLabel(master=self, text=input_path,
                           anchor="w", justify="left", pady=5,
                           height=40
                           )
            btn.pack(fill="x")

            btn.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, btn=btn: self.row_cmd(e=e, btn=btn)
                     )

            btn.bind(sequence='<Configure>',
                     command=lambda e, btn=btn: self.row_cmd_wrap(e=e, btn=btn)
                     )

            btn.bind(sequence="<ButtonRelease-2>",
                     command=self.pop_context_menu
                     )

    def row_cmd_wrap(self, e: tkinter.Event, btn: CTkLabel):
        btn.configure(wraplength=self.winfo_width() - 10)

    def row_cmd(self, e: tkinter.Event, btn: CTkLabel):
        new_path = ShortFullPaths.dct[btn.cget("text")]
        if os.path.isfile(new_path) or new_path.endswith((".APP", ".app")):
            subprocess.Popen(["open", "-R", new_path])
        else:
            subprocess.Popen(["open", new_path])

    def pop_context_menu(self, event):
        ContextMenu(e=event).post(event.x_root, event.y_root)


class Display(customtkinter.CTkScrollableFrame):
    def __init__(self, master=tkinter):
        super().__init__(master=master)

        self.load_scroll()
        self.load_rows()

        DisplayVar.v.trace_add(mode="read", callback=self.rows_var_callback)

    def get_parrent(self):
        return self._parent_canvas

    def moveup(self, e=None):
        try:
            self.get_parrent().yview_moveto("0.0")
        except Exception as e:
            self.print_err(parent=self, error=e)

    def rows_var_callback(self, *args):
        self.reload_display()

    def load_scroll(self):
        self.scrollable = CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

    def load_rows(self):
        self.rows = Rows(master=self.scrollable)
        self.rows.pack(fill="both", expand=1)

    def reload_display(self):
        self.scrollable.destroy()
        self.rows.destroy()

        self.load_scroll()
        self.load_rows()
    