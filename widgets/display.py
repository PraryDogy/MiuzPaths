import os
import subprocess
import tkinter

from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame

from cfg import Cfg
from utils import Err, MainItem


class CustomRow(CTkLabel):
    anchor = "w"
    justify = "left"
    h = 40
    def __init__(self, master: CTkFrame, path: str):
        super().__init__(
            master=master,
            text=path,
            anchor=CustomRow.anchor,
            justify=CustomRow.justify,
            height=CustomRow.h,
        )
        self.path = path


class RowsFrame(CTkFrame):
    remove_text = "Удалить"
    remove_all_text = "Удалить все"

    def __init__(self, master: CTkFrame, main_item: MainItem, cfg: Cfg):
        super().__init__(master=master)
        self.main_item = main_item
        self.cfg = cfg
  
        for x, path in enumerate(self.main_item.path_list):
            row = CustomRow(self, path)
            row.pack(fill="x", padx=4, pady=(0, 4))

            if x != len(self.main_item.path_list) - 1:
                separator = CTkFrame(
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
        if os.path.isfile(row.path) or row.path.endswith(self.cfg.app_exts):
            subprocess.Popen(["open", "-R", row.path])
        else:
            subprocess.Popen(["open", row.path])

    def remove_row(self, row: CustomRow):
        self.main_item.path_list.remove(row.path)
        self.main_item.string_var.set(self.main_item.none_type)

    def remove_all(self):
        self.main_item.path_list.clear()
        self.main_item.string_var.set(self.main_item.none_type)

    def pop_context_menu(self, e: tkinter.Event, row: CustomRow):
        menu = tkinter.Menu(master=row)
        menu.add_command(
            label=RowsFrame.remove_text,
            command=lambda: self.remove_row(row)
        )
        menu.add_separator()
        menu.add_command(
            label=RowsFrame.remove_all_text,
            command=self.remove_all
        )
        row.configure(fg_color="red")
        menu.post(e.x_root, e.y_root)
        row.configure(fg_color="transparent")


class Display(CTkScrollableFrame):
    empty_history = "История пуста"

    def __init__(self, root: tkinter.Tk, main_item: MainItem, cfg: Cfg):
        super().__init__(master=root)
        self.root = root
        self.cfg = cfg

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
        try:
            self.scrollable.destroy()
            self.rows.destroy()
        except AttributeError as e:
            print("display> no widgets on first load, ok", e)

    def update_display(self):
        self.remove_widgets()

        self.scrollable = CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        if self.main_item.path_list:
            self.rows = RowsFrame(self.scrollable, self.main_item, self.cfg)
            self.rows.pack(fill="both", expand=1)
        else:
            self.show_message(Display.empty_history)

    def show_message(self, text: str, auto_reload=False):
        self.remove_widgets()

        self.scrollable = CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

        self.rows = CTkLabel(master=self.scrollable, text=text)
        self.rows.place(relx=0.5, rely=0.5, anchor="center")

        if auto_reload:
            self.root.after(2000, self.update_display)
