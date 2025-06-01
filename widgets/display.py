import os
import subprocess
import tkinter

import customtkinter

from utils import Err, MainItem


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
    def __init__(self, root: CustomRow):
        tkinter.Menu.__init__(self, master=root)
        self.root = root
        self.add_command(label=f"Удалить", command=lambda: self.clear())
        self.add_separator()
        self.add_command(label="Удалить все", command=lambda: self.clear_all())

    def clear(self):
        MainItem.path_list.remove(self.root.path)
        MainItem.string_var.set(MainItem.none_type)

    def clear_all(self):
        MainItem.path_list.clear()
        MainItem.string_var.set(MainItem.none_type)


class Rows(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame):
        super().__init__(master=master)
  
        for x, path in enumerate(MainItem.path_list):
            row = CustomRow(self, path)
            row.pack(fill="x", padx=4, pady=(0, 4))

            if x != len(MainItem.path_list) - 1:
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
    empty_history = "История пуста"

    def __init__(self, root: tkinter.Tk, main_item: MainItem):
        super().__init__(master=root)
        self.root = root

        self.main_item = main_item
        self.main_item.string_var.trace_add("write", self.shared_string_var_cmd)

        self.update_display()

    def moveup(self, e=None):
        try:
            self._parent_canvas.yview_moveto("0.0")
        except Exception as e:
            Err.print_error(e)

    def shared_string_var_cmd(self, *args):
        text = self.main_item.string_var.get()

        if text == self.main_item.error_text:
            self.show_message(text, auto_reload=True)
        elif text != self.main_item.none_type:
            if text not in self.main_item.path_list:
                self.main_item.path_list.insert(0, text)
            if len(self.main_item.path_list) > 20:
                self.main_item.path_list.pop(-1)
            self.update_display()
        else:
            self.update_display()

    def remove_widgets(self):
        if self.scrollable:
            self.scrollable.destroy()
        if self.rows:
            self.rows.destroy()

    def update_display(self):
        self.remove_widgets()

        self.scrollable = customtkinter.CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        if self.main_item.path_list:
            self.rows = Rows(self.scrollable)
            self.rows.pack(fill="both", expand=1)
        else:
            self.show_message(Display.empty_history)

    def show_message(self, text: str, auto_reload=False):
        self.remove_widgets()

        self.scrollable = customtkinter.CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        self.rows = customtkinter.CTkLabel(master=self.scrollable, text=text)
        self.rows.place(relx=0.5, rely=0.5, anchor="center")

        if auto_reload:
            self.root.after(2000, self.update_display)
