import tkinter

from cfg import cnf

from .display import Display
from .mac_menu import MacMenu
from .open_btn import OpenBtn


class MainWin:
    def __init__(self, root: tkinter.Tk):
        self.root = root

        self.root.createcommand("tk::mac::Quit" , exit)

        self.root.bind(sequence="<Command-Key>", func=self.minimize)
        self.root.protocol(name="WM_DELETE_WINDOW", func=self.root.wm_withdraw)
        self.root.createcommand("tk::mac::ReopenApplication", self.demin)

        self.root.title(cnf.app_name)
        self.root.configure(padx=10, pady=10)
        self.root.minsize(360, 400)

        self.disp = Display(self.root)
        self.disp.pack(expand=1, fill="both")

        self.open_btn = OpenBtn(self.root)
        self.open_btn.pack(pady=(10, 0))

        MacMenu(master=self.root)
        
        self.root.eval('tk::PlaceWindow . center')
        self.root.wm_deiconify()

    def minimize(self, e: tkinter.Event):
        if e.char == "w":
            self.root.wm_withdraw()

    def demin(self, e: tkinter.Event = None):
        self.root.wm_deiconify()
