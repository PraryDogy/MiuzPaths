import json
import os
import tkinter


class Colors:
    def __init__(self) -> None:
        self.fg_color = "#E2E2E2"
        self.bg_color = "#1e1e1e"
        self.btn_color = "#303030"
        self.blue_color = "#3d6a97"
        self.lgray_color = "#4B4B4B"
        self.dgray_color = "#141416"


class GuiDigits:
    def __init__(self):
        self.corner = 8
        self.scroll_width = 17


class Config(Colors, GuiDigits):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.withdraw()

        self.app_name = 'MiuzPaths'
        self.app_ver = '1.8.5'
        self.cfg_dir = os.path.join(os.path.expanduser("~"),
            f"Library", "Application Support", self.app_name)

        Colors.__init__(self)
        GuiDigits.__init__(self)

    def check_dir(self):
        if not os.path.exists(path=self.cfg_dir):
            os.makedirs(name=self.cfg_dir, exist_ok=True)


cnf = Config()
cnf.check_dir()