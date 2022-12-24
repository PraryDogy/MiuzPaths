import tkinter

import cfg
from utils import (exists_path, is_mac, is_win, open_path, paste, remove_file,
                   to_mac)

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

        if is_mac(input):
            input = remove_file(input)
            exist_path = exists_path(input)
            self.path_operations(exist_path, input)

        elif is_win(input):
            input = to_mac(input)
            input = remove_file(input)
            exist_path = exists_path(input)
            self.path_operations(exist_path, input)

        else:
            old = display['text']
            display['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(1500, lambda: display.configure(text=old))

    def path_operations(self, exist_path: str, input: str):
        if exist_path == input:
            display['text'] = f'Открываю:\n{input}'
            [display.configure(text='Неизвестная ошибка') if not open_path(input) else False]

        else:
            bad_path = input.replace(exist_path, '')
            good_path = exist_path.replace(bad_path, '')
            display['text'] = (
                f'Где-то здесь есть ошибка:\n{bad_path}'
                f'\n\nОткрываю:\n{good_path}')
            [display.configure(text='Неизвестная ошибка') if not open_path(good_path) else False]
            

class ConvertBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master, text='Преобразовать')
        self['text'] = 'Преобр.'
        self['state'] = tkinter.DISABLED


class Display(tkinter.Label):
    def __init__(self, master: tkinter):
        tkinter.Label.__init__(self, master, bg='black', fg=cfg.BGFONT, padx=5)
        self['text'] = 'Miuz paths'
        global display
        display = self