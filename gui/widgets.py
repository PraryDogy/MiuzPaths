import tkinter

import cfg

display = tkinter.Label


class CBtn(tkinter.Label):
    def __init__(self, master: tkinter, **kwargs):
        tkinter.Label.__init__(
            self, master, bg=cfg.BGBUTTON, fg=cfg.BGFONT, height=2)

        self.bind('<Enter>', lambda e: self.enter())
        self.bind('<Leave>', lambda e: self.out())

    def press(self):
        self['bg'] = cfg.BGPRESSED
        cfg.ROOT.after(100, lambda: self.configure(bg=cfg.BGBUTTON))

    def enter(self):
        self['bg'] = cfg.BGSELECTED

    def out(self):
        self['bg'] = cfg.BGBUTTON

    def cmd(self, cmd):
        self.bind('<ButtonRelease-1>', cmd)


class OpenBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master)
        self['text'] = 'Открыть'
        self.cmd(lambda e: self.open_path())

    def open_path(self):
        self.press()
        display['text'] = 'Открытие'


class ConvertBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master, text='Преобразовать')
        self['text'] = 'Преобр.'


class Display(tkinter.Label):
    def __init__(self, master: tkinter):
        tkinter.Label.__init__(self, master, bg='black', fg=cfg.BGFONT)
        self['text'] = 'hello'
        global display
        display = self