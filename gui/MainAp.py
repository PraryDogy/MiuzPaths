import tkinter

from cfg import BGCOLOR

from .Menu import MenuGui
import cfg
from .widgets import OpenButton, ConvertButton, Display

class MainApp():
    def __init__(self):
        '''
        methods: Run
        '''
        cfg.ROOT.createcommand(
            'tk::mac::ReopenApplication', cfg.ROOT.deiconify)
        cfg.ROOT.protocol("WM_DELETE_WINDOW", lambda: cfg.ROOT.withdraw())
        cfg.ROOT.bind('<Command-w>', lambda e: cfg.ROOT.withdraw())
        cfg.ROOT.title('MiuzPaths')
        cfg.ROOT.config(pady=10, padx=10, bg=BGCOLOR,)
        cfg.ROOT.resizable(0,0)

        Display().pack(fill=tkinter.X)

        buttons_frame = tkinter.Frame(cfg.ROOT, bg=BGCOLOR)
        buttons_frame.pack(pady=(15, 0))
        
        OpenButton(buttons_frame).pack(side=tkinter.LEFT)
        ConvertButton(buttons_frame).pack(side=tkinter.RIGHT, padx=(15, 0))
        
        MenuGui()

        # place main window center screen
        cfg.ROOT.eval('tk::PlaceWindow {} center'.format(cfg.ROOT))
        cfg.ROOT.mainloop()
        

