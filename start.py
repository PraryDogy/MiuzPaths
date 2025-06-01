import tkinter

import customtkinter

from cfg import Cfg
from utils import MainItem
from widgets.main_win import MainWin

root = tkinter.Tk()
root.withdraw()

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("themes/metal.json")

main_item = MainItem()
cfg = Cfg()
app = MainWin(root, main_item, cfg)

root.mainloop()
