import os
import subprocess
import tkinter

import customtkinter

from cfg import cnf
from utils import Shared


class CustomRow(customtkinter.CTkLabel):
    def __init__(self, master: customtkinter.CTkFrame, path: str):
        super().__init__(
            master=master,
            text=path,
            anchor="w",
            justify="left",
            height=40,
        )
        self.path = path


class ContextMenu(tkinter.Menu):
    def __init__(self, wid: CustomRow):
        tkinter.Menu.__init__(self, master=cnf.root)

        self.widget = wid

        self.add_command(label=f"Удалить", command=lambda: self.clear())
        self.add_separator()
        self.add_command(label="Удалить все", command=lambda: self.clear_all())

    def clear(self):
        Shared.path_list.remove(self.widget.path)
        Shared.string_var.set(Shared.none_type)

    def clear_all(self):
        Shared.path_list.clear()
        Shared.string_var.set(Shared.none_type)


class Rows(customtkinter.CTkFrame):
    def __init__(self, master=tkinter):
        super().__init__(master=master)
  
        for x, path in enumerate(Shared.path_list):
            row = CustomRow(self, path)
            row.pack(fill="x", padx=4, pady=(0, 4))

            if x != len(Shared.path_list) - 1:
                separator = customtkinter.CTkFrame(
                    master=self,
                    height=1,
                    fg_color="#444444"
                )
                separator.pack(fill="x", padx=10, pady=2)

            row.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, row=row: self.row_cmd(e, row)
                     )

            row.bind(sequence='<Configure>',
                     command=lambda e, row=row: self.row_cmd_wrap(e, row)
                     )

            row.bind(sequence="<ButtonRelease-2>",
                     command=lambda e, row=row: self.pop_context_menu(e, row)
                     )

    def row_cmd_wrap(self, e: tkinter.Event, row: CustomRow):
        row.configure(wraplength=self.winfo_width() - 10)

    def row_cmd(self, e: tkinter.Event, row: CustomRow):
        if os.path.isfile(row.path) or row.path.endswith((".APP", ".app")):
            subprocess.Popen(["open", "-R", row.path])
        else:
            subprocess.Popen(["open", row.path])

    def pop_context_menu(self, e: tkinter.Event, row: CustomRow):
        menu = ContextMenu(row)
        menu.post(e.x_root, e.y_root)


class Display(customtkinter.CTkScrollableFrame):
    def __init__(self, master=tkinter):
        super().__init__(master=master)

        self.rows = None
        self.scrollable = None

        self.update_display()

        Shared.string_var.trace_add("write", self.shared_string_var_cmd)

    def get_parrent(self):
        return self._parent_canvas

    def moveup(self, e=None):
        try:
            self.get_parrent().yview_moveto("0.0")
        except Exception as e:
            self.print_err(parent=self, error=e)

    def shared_string_var_cmd(self, *args):
        text = Shared.string_var.get()

        if text == Shared.error_text:
            self.show_message(text, auto_reload=True)
        elif text != Shared.none_type:
            if text not in Shared.path_list:
                Shared.path_list.insert(0, text)
            if len(Shared.path_list) > 20:
                Shared.path_list.pop(-1)
            self.update_display()
        else:
            self.update_display()

    def update_display(self):
        if self.scrollable:
            self.scrollable.destroy()
        if self.rows:
            self.rows.destroy()

        self.scrollable = customtkinter.CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        if Shared.path_list:
            self.rows = Rows(master=self.scrollable)
            self.rows.pack(fill="both", expand=1)
        else:
            self.show_message("История пуста")

    def show_message(self, text: str, auto_reload=False):
        if self.scrollable:
            self.scrollable.destroy()
        if self.rows:
            self.rows.destroy()

        self.scrollable = customtkinter.CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        self.rows = customtkinter.CTkLabel(master=self.scrollable, text=text)
        self.rows.place(relx=0.5, rely=0.5, anchor="center")

        if auto_reload:
            cnf.root.after(2000, self.update_display)
