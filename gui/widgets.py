import tkinter

import cfg
from utils import paste, is_mac, is_win, exists_path, file_path
display = tkinter.Label


class CBtn(tkinter.Label):
    def __init__(self, master: tkinter, **kwargs):
        tkinter.Label.__init__(
            self, master, bg=cfg.BGBUTTON, fg=cfg.BGFONT, height=3)

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
        input = paste()
        print(input)

        if is_mac(input):
            without_file = file_path(input)
            exist_path = exists_path(without_file)

            if exist_path == input:
                print('open')

            else:
                print(input.replace(exist_path, ''))

        elif is_win(input):
            print('is win')
        
        else:
            old = display['text']
            display['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(1500, lambda: display.configure(text=old))


class ConvertBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master, text='Преобразовать')
        self['text'] = 'Преобр.'


class Display(tkinter.Label):
    def __init__(self, master: tkinter):
        tkinter.Label.__init__(self, master, bg='black', fg=cfg.BGFONT)
        self['text'] = 'Miuz paths'
        global display
        display = self