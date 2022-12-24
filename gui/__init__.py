import tkinter

import cfg

from .macosx_menu import Menu
from .widgets import ConvertBtn, Display, OpenBtn


class InitGui():
    def __init__(self):
        cfg.ROOT.createcommand(
            'tk::mac::ReopenApplication', cfg.ROOT.deiconify)
        cfg.ROOT.protocol("WM_DELETE_WINDOW", lambda: cfg.ROOT.withdraw())
        cfg.ROOT.bind('<Command-w>', lambda e: cfg.ROOT.withdraw())

        cfg.ROOT.title('MiuzPaths')
        cfg.ROOT.configure(bg=cfg.BGCOLOR)
        cfg.ROOT.geometry(f'{300}x{300}')
        cfg.ROOT.resizable(1,1)

        Display(cfg.ROOT).pack(fill=tkinter.BOTH, expand=1)

        btns_frame = tkinter.Frame(cfg.ROOT, bg=cfg.BGCOLOR)
        btns_frame.pack(fill=tkinter.X, pady=5, padx=5)

        OpenBtn(btns_frame).pack(side=tkinter.LEFT, fill=tkinter.X, expand=1)
        ConvertBtn(btns_frame).pack(
            side=tkinter.RIGHT, fill=tkinter.X, expand=1, padx=(5, 0))
        
        Menu()

        cfg.ROOT.eval('tk::PlaceWindow {} center'.format(cfg.ROOT))
        cfg.ROOT.mainloop()
        

