import tkinter
import cfg


class Menu(tkinter.Menu):
    """
    Mac osx bar menu.
    """
    def __init__(self):
        menubar = tkinter.Menu(cfg.ROOT)
        tkinter.Menu.__init__(self, menubar)
        menubar.add_cascade(label="Меню", menu=self)
        self.add_command(
            label='О программе', command=abs)
        self.add_command(label="О программе", command=self.about_widget)

        cfg.ROOT.createcommand(
            'tkAboutDialog',
            lambda: cfg.ROOT.tk.call('tk::mac::standardAboutPanel'))
        
        cfg.ROOT.configure(menu=menubar)

    def about_widget(self):
        win =tkinter.Toplevel(cfg.ROOT, pady=10, padx=10, bg=cfg.BGCOLOR)
        win.title('О программе')

        made = (
            f'{cfg.APP_NAME} {cfg.APP_VER}'
            '\n\nCreated by Evgeny Loshkarev'
            '\nCopyright © 2022 MIUZ Diamonds.'
            '\nAll rights reserved.'
            '\n'
            )
        
        l1 = tkinter.Label(win, text=made, fg=cfg.BGFONT, bg=cfg.BGCOLOR)
        l1.pack()

        CloseButton = tkinter.Label(
            win,
            height=3, 
            width=16,
            text = 'Закрыть',
            bg=cfg.BGBUTTON,
            fg=cfg.BGFONT,
            )
        CloseButton.bind('<Button-1>', lambda event: win.destroy())
        CloseButton.pack()
        
        cfg.ROOT.eval('tk::PlaceWindow {} center'.format(win))