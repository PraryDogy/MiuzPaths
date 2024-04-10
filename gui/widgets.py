import abc
import sys
import tkinter

try:
    from typing_extensions import Callable, Literal
except ImportError:
    from typing import Literal, Callable

import customtkinter

from cfg import cnf
from utils import SysUtils

__all__ = (
    "CScroll",
    "CButton",
    "MacMenu",
    )


class BaseCWid(abc.ABC):
    @abc.abstractmethod
    def get_parrent(self):
        pass


class CScroll(customtkinter.CTkScrollableFrame, BaseCWid, SysUtils):
    def __init__(self, master: tkinter, width: int = 200,
                 corner_radius: int = 0, fg_color: str = cnf.bg_color,
                 scroll_width: int = cnf.scroll_width,
                 scroll_color: str = None,
                 **kw):

        customtkinter.CTkScrollableFrame.__init__(
            self, master=master, width=width, corner_radius=corner_radius,
            fg_color=fg_color, **kw)

        self._scrollbar.configure(width=scroll_width)
        if scroll_color:
            self._scrollbar.configure(button_color=scroll_color)

    def get_parrent(self):
        return self._parent_canvas

    def moveup(self, e=None):
        try:
            self.get_parrent().yview_moveto("0.0")
        except Exception:
            self.print_err()


class CButton(customtkinter.CTkButton, BaseCWid):
    def __init__(self, master: tkinter, text_color: str = cnf.text_color,
                 fg_color: str = cnf.btn_color, corner_radius: int = cnf.corner,
                 width: int = 75, hover: bool = 0, border_spacing: int = 2,
                 anchor="center",
                 font: tuple[str, int, str] = ("San Francisco Pro", 13, "normal"),
                 **kw):

        customtkinter.CTkButton.__init__(
            self, master=master, text_color=text_color, fg_color=fg_color,
            corner_radius=corner_radius, width=width, hover=hover,
            border_spacing=border_spacing, font=font, anchor=anchor, **kw)

    def get_parrent(self):
        return self._canvas

    def cmd(self, cmd: Callable):
        self.bind(sequence="<ButtonRelease-1>", command=cmd)

    def uncmd(self):
        self.unbind(sequence="<ButtonRelease-1>")

    def press(self):
        self.configure(fg_color=cnf.blue_color)
        cnf.root.after(100, lambda: self.configure(fg_color=cnf.btn_color))


class MacMenu(tkinter.Menu, SysUtils):
    def __init__(self):
        main_menu = tkinter.Menu(cnf.root)
        cnf.root.configure(menu=main_menu)

        if sys.version_info.minor < 10:
            cnf.root.createcommand("tkAboutDialog", self.about_dialog)

        # sett_menu = tkinter.Menu(master=main_menu, tearoff=0)
        # sett_menu.add_command(label="Настройки", command=self.settings_cmd)
        # main_menu.add_cascade(label="Настройки", menu=sett_menu)

    def about_dialog(self):
        try:
            cnf.root.tk.call("tk::mac::standardAboutPanel")
        except Exception:
            self.print_err()

    def settings_cmd(self):
        from .settings import Settings
        Settings()