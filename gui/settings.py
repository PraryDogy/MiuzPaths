import tkinter

from customtkinter import CTkFrame, CTkTextbox

from cfg import cnf
from utils import PrePaths

from .widgets import CButton

__all__ = ("Settings", )


class Storage:
    win: tkinter.Toplevel = None


class SettingsTextBox(CTkTextbox):
    def __init__(self, master: tkinter):
        CTkTextbox.__init__(self, master=master, fg_color=cnf.dgray_color)
        pre_paths = PrePaths().pre_paths

        self.insert(index="1.0", text="\n".join(pre_paths))
        
        



class SettingsBtns(CTkFrame):
    def __init__(self, master: tkinter):
        CTkFrame.__init__(self, master=master, corner_radius=cnf.corner,
                          fg_color=cnf.bg_color)

        ok_btn = CButton(master=self, text="Ок")
        ok_btn.pack(side="left")

        can_btn = CButton(master=self, text="Отмена")
        can_btn.pack(side="left", padx=(10, 0))


class SettingsWin(tkinter.Toplevel):
    def __init__(self):
        if Storage.win:
            Storage.win.destroy()

        tkinter.Toplevel.__init__(self, bg=cnf.bg_color, padx=10, pady=10)
        Storage.win = self
        self.side = 300

        self.title("Настройки")
        self.minsize(width=self.side, height=self.side)
        self.protocol(name="WM_DELETE_WINDOW", func=self.close_sett)
        self.bind(sequence="<Escape>", func=self.close_sett)

        SettingsTextBox(master=self).pack(fill="both", expand=1)
        SettingsBtns(master=self).pack(pady=(10, 0))

        self.place_center()

    def close_sett(self, e: tkinter.Event=None):
        self.destroy()
        Storage.win = None

    def place_center(self):
        x, y = cnf.root.winfo_x(), cnf.root.winfo_y()
        xx = x + cnf.root.winfo_width() // 2 - self.side // 2
        yy = y + cnf.root.winfo_height() // 2 - self.side // 2
        self.geometry(f"+{xx}+{yy}")



class Settings(SettingsWin):
    def __init__(self):
        SettingsWin.__init__(self)