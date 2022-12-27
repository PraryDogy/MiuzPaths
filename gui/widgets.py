import tkinter

import cfg
from utils import (exists_path, is_mac, is_win, open_path, paste, remove_file,
                   to_mac, to_win)
import threading
import textwrap


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
        t1 = threading.Thread(target=self.task)
        t1.start()
        while t1.is_alive():
            cfg.ROOT.update()

    def task(self):
        try:
            self.command()
        except Exception:
            display['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(1500, lambda: display.configure(text='MiuzPaths'))

    def command(self):
        self.press()
        orig_path = remove_file(paste())

        if is_mac(orig_path):
            orig_path = to_win(orig_path)
            orig_path = to_mac(orig_path)

            self.path_operations(orig_path)
            return

        elif is_win(orig_path):
            orig_path = to_mac(orig_path)
            self.path_operations(orig_path)
            return

        elif cfg.config['LAST_PATH'] != '':
            self.path_operations(cfg.config['LAST_PATH'])
            return

        else:
            old = display['text']
            display['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(1500, lambda: display.configure(text=old))


    def path_operations(self, orig_path: str):
        orig_path = remove_file(orig_path)
        exist_path = exists_path(orig_path)

        if exist_path == cfg.config['LAST_PATH']:
            display['text'] = f'Открываю последний путь:\n{exist_path}'

            [display.configure(text='Неизвестная ошибка') if not open_path(exist_path) else False]
            return

        elif exist_path == orig_path:
            cfg.config['LAST_PATH'] = exist_path
            display['text'] = f'Открываю:\n{orig_path}'
            [display.configure(text='Неизвестная ошибка') if not open_path(exist_path) else False]
            return

        else:
            bad_path = orig_path.replace(exist_path, '')
            cfg.config['LAST_PATH'] = exist_path
            display['text'] = (
                f'Где-то здесь есть ошибка:\n{bad_path}'
                f'\n\nОткрываю:\n{exist_path}')
            [display.configure(text='Неизвестная ошибка') if not open_path(exist_path) else False]
            

class ConvertBtn(CBtn):
    def __init__(self, master: tkinter):
        CBtn.__init__(self, master, text='Преобразовать')
        self['text'] = 'Преобр.'
        self['state'] = tkinter.DISABLED


class Display(tkinter.Label):
    def __init__(self, master: tkinter):
        tkinter.Label.__init__(self, master, bg='black', fg=cfg.BGFONT, padx=5, justify=tkinter.LEFT)
        self['text'] = 'Miuz paths'
        global display
        display = self

        cfg.ROOT.bind('<ButtonRelease-1>', self.resize)

    def set_wraplength(self):
        cfg.ROOT.update_idletasks()
        w = cfg.config['GEOMETRY'][0]
        self['wraplength'] = w-20
    
    def resize(self, e: tkinter.Event):
        w = cfg.ROOT.winfo_width()
        
        if w != cfg.config['GEOMETRY'][0]:
            cfg.config['GEOMETRY'][0] = w
            self.set_wraplength()