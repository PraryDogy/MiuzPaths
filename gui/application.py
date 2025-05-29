import tkinter

from cfg import cnf

from .display import Display
from .open_btn import OpenBtn
from .widgets import MacMenu


class Application:
    def __init__(self):
        cnf.root.createcommand("tk::mac::Quit" , exit)

        cnf.root.bind(sequence="<Command-Key>", func=self.minimize)
        cnf.root.protocol(name="WM_DELETE_WINDOW", func=cnf.root.wm_withdraw)
        cnf.root.createcommand("tk::mac::ReopenApplication", self.demin)

        cnf.root.title(cnf.app_name)
        cnf.root.configure(padx=10, pady=10)
        cnf.root.minsize(360, 400)

        self.disp = Display(master=cnf.root)
        self.disp.pack(expand=1, fill="both")

        self.open_btn = OpenBtn(master=cnf.root)
        self.open_btn.pack(pady=(10, 0))

        MacMenu()
        
        cnf.root.eval('tk::PlaceWindow . center')
        cnf.root.wm_deiconify()

    def minimize(self, e: tkinter.Event):
        if e.char == "w":
            cnf.root.wm_withdraw()

    def demin(self, e: tkinter.Event = None):
        cnf.root.wm_deiconify()
        self.disp.reload_display()


app = Application()