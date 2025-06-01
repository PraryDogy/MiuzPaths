import tkinter

from cfg import Cfg
from utils import MainItem
from widgets.main_win import MainWin

root = tkinter.Tk()
root.withdraw()
main_item = MainItem()
cfg = Cfg()
app = MainWin(root, main_item, cfg)

root.mainloop()
