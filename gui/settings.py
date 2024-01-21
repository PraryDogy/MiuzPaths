import tkinter

from customtkinter import CTkFrame, CTkTextbox

from cfg import cnf
from utils import PrePaths

from .widgets import CButton

__all__ = ("Settings", )


class Storage:
    win: tkinter.Toplevel = None


class SettingsTitle(tkinter.Label):
    def __init__(self, master: tkinter):
        text = [
            "Не меняйте настройки без необходимости",
            "Не забудьте оставить последнюю строчку пустой",
            "Поддержка: tg @evlosh, email evlosh@gmail.com"
            ]

        tkinter.Label.__init__(self, master=master, bg=cnf.bg_color,
                               anchor="w", justify="left",
                               text="\n".join(text))


class SettingsTextBox(CTkTextbox):
    def __init__(self, master: tkinter):
        CTkTextbox.__init__(self, master=master, fg_color=cnf.dgray_color)
        self.t_pre_paths = PrePaths()
        self.insert(index="1.0", text="\n".join(self.t_pre_paths.pre_paths))

    def save_prepaths(self):
        pre_paths = self.get("1.0", "end").splitlines()
        self.t_pre_paths.save(pre_paths=pre_paths)


class SettingsBtns(CTkFrame):
    def __init__(self, master: tkinter):
        CTkFrame.__init__(self, master=master, corner_radius=cnf.corner,
                          fg_color=cnf.bg_color)

        self.ok_btn = CButton(master=self, text="Ок")
        self.ok_btn.pack(side="left")

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

        SettingsTitle(master=self).pack(fill="both", expand=1, pady=(0, 10))

        self.t_box = SettingsTextBox(master=self)
        self.t_box.pack(fill="both", expand=1)

        btns = SettingsBtns(master=self)
        btns.pack(pady=(10, 0))
        btns.ok_btn.cmd(self.save_sett)

        self.place_center()

    def close_sett(self, e: tkinter.Event=None):
        self.destroy()
        Storage.win = None

    def save_sett(self, e: tkinter.Event):
        self.t_box.save_prepaths()
        self.close_sett()

    def place_center(self):
        x, y = cnf.root.winfo_x(), cnf.root.winfo_y()
        xx = x + cnf.root.winfo_width() // 2 - self.side // 2
        yy = y + cnf.root.winfo_height() // 2 - self.side // 2
        self.geometry(f"+{xx}+{yy}")


class Settings(SettingsWin):
    def __init__(self):
        SettingsWin.__init__(self)