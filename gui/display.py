import os
import subprocess
import tkinter

import customtkinter

from cfg import cnf

from ._shared import _Shared


class ShortFullPaths:
    dct = {}


class DisplayVar:
    v = tkinter.StringVar(value="")


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
        _Shared.path_list.remove(ShortFullPaths.dct[e.widget.cget("text")])
        _Shared.string_var.set("")

    def clear_all(self, e: tkinter.Event = None):
        _Shared.path_list.clear()
        _Shared.string_var.set("")


class Rows(customtkinter.CTkFrame):
    def __init__(self, master=tkinter):
        super().__init__(master=master)
        ShortFullPaths.dct.clear()
  
        for x, input_path in enumerate(_Shared.path_list):

            ShortFullPaths.dct[input_path] = input_path

            btn = customtkinter.CTkLabel(
                master=self,
                text=input_path,
                anchor="w",
                justify="left",
                height=40,
                
                )
            btn.pack(fill="x", padx=4, pady=(0, 4))

            if x != len(_Shared.path_list) - 1:

                separator = customtkinter.CTkFrame(
                    master=self,
                    height=1,
                    fg_color="#444444"
                )
                separator.pack(fill="x", padx=10, pady=2)

            btn.bind(sequence="<ButtonRelease-1>",
                     command=lambda e, btn=btn: self.row_cmd(e=e, btn=btn)
                     )

            btn.bind(sequence='<Configure>',
                     command=lambda e, btn=btn: self.row_cmd_wrap(e=e, btn=btn)
                     )

            btn.bind(sequence="<ButtonRelease-2>",
                     command=self.pop_context_menu
                     )

    def row_cmd_wrap(self, e: tkinter.Event, btn: customtkinter.CTkLabel):
        btn.configure(wraplength=self.winfo_width() - 10)

    def row_cmd(self, e: tkinter.Event, btn: customtkinter.CTkLabel):
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

        _Shared.string_var.trace_add(
            mode="write",
            callback=self.shared_string_var_cmd
        )

    def get_parrent(self):
        return self._parent_canvas

    def moveup(self, e=None):
        try:
            self.get_parrent().yview_moveto("0.0")
        except Exception as e:
            self.print_err(parent=self, error=e)

    def shared_string_var_cmd(self, *args):
        text = _Shared.string_var.get()
        if text == _Shared.error_text:
            self.show_error_msg(DisplayVar.v.get())
        else:
            if text in _Shared.path_list:
                _Shared.path_list.remove(text)
            _Shared.path_list.insert(0, text)
            if len(_Shared.path_list) > 20:
                _Shared.path_list.pop(-1)
            self.reload_display()

    def load_scroll(self):
        self.scrollable = customtkinter.CTkFrame(master=self)
        self.scrollable.pack(expand=1, fill="both")

    def load_rows(self):
        if _Shared.path_list:
            self.rows = Rows(master=self.scrollable)
            self.rows.pack(fill="both", expand=1)
        else:
            text = "История пуста"
            self.rows = customtkinter.CTkLabel(master=self.scrollable, text=text)
            self.rows.place(relx=0.5, rely=0.5, anchor="center")

    def show_error_msg(self, text: str):
        self.scrollable.destroy()
        if self.rows:
            self.rows.destroy()
        self.load_scroll()
        self.rows = customtkinter.CTkLabel(master=self.scrollable, text=text)
        self.rows.place(relx=0.5, rely=0.5, anchor="center")

        cnf.root.after(1300, self.reload_display)

    def reload_display(self):
        self.scrollable.destroy()
        if self.rows:
            self.rows.destroy()
        self.load_scroll()
        self.load_rows()
    