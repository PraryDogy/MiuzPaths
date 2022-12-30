import tkinter

import cfg

from .macosx_menu import Menu
from .widgets import ConvertBtn, Display, OpenBtn


class InitGui():
    def __init__(self):
        cfg.ROOT.createcommand(
            'tk::mac::ReopenApplication', cfg.ROOT.deiconify)
        cfg.ROOT.createcommand("tk::mac::Quit" , self.on_exit)

        cfg.ROOT.protocol("WM_DELETE_WINDOW", lambda: cfg.ROOT.withdraw())
        cfg.ROOT.bind('<Command-w>', lambda e: cfg.ROOT.withdraw())

        cfg.ROOT.title('MiuzPaths')
        cfg.ROOT.configure(bg=cfg.BGCOLOR)

        w, h, x, y = cfg.config['GEOMETRY']
        cfg.ROOT.resizable(1,1)

        display_widget = Display(cfg.ROOT)
        display_widget.pack(fill=tkinter.BOTH, expand=1, padx=5)
        display_widget.set_wraplength()

        btns_frame = tkinter.Frame(cfg.ROOT, bg=cfg.BGCOLOR)
        btns_frame.pack(fill=tkinter.X, pady=5, padx=5)

        OpenBtn(btns_frame).pack(side=tkinter.LEFT, fill=tkinter.X, expand=1)
        # ConvertBtn(btns_frame).pack(
            # side=tkinter.RIGHT, fill=tkinter.X, expand=1, padx=(5, 0))
        
        Menu()
        cfg.ROOT.geometry(f'{w}x{h}+{x}+{y}')
        cfg.ROOT.deiconify()

    def on_exit(self):
        w, h = cfg.ROOT.winfo_width(), cfg.ROOT.winfo_height()
        x, y = cfg.ROOT.winfo_x(), cfg.ROOT.winfo_y()
        cfg.config['GEOMETRY'] = [w, h, x, y]

        cfg.encrypt_cfg(cfg.config)
        quit()