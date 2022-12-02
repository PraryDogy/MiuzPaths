import tkinter

import cfg
from utils import copy, detectPath, existsPath, open_path, paste, toMac, toWin

widgets = {
    'display': tkinter.Label
    }


class Display(tkinter.Label):
    def __init__(self, **kwargs):
        tkinter.Label.__init__(self, cfg.ROOT, bg=cfg.BGDISPLAY, **kwargs,
        height=10, fg=cfg.BGFONT, justify=tkinter.LEFT,
        anchor=tkinter.CENTER, padx=5, pady=5, wraplength=295)
        widgets['display'] = self

        self['text'] = (
            'Скопируйте путь до сетевого диска МЮЗ'
            '\nи нажмите "Открыть" или "Преобразовать".'
            )

class ConvertButton(tkinter.Label):
    def __init__(self, master):
        tkinter.Label.__init__(
            self, master, height=3, width=16, text = 'Преобразовать',
            bg=cfg.BGBUTTON,fg=cfg.BGFONT)
        self.bind('<Button-1>', lambda event: self.Run())
        self.bind('<Enter>', lambda e: self.enter())
        self.bind('<Leave>', lambda e: self.leave())

    def enter(self):
        self['bg'] = cfg.BGSELECTED

    def leave(self):
        self['bg'] = cfg.BGBUTTON

    def Run(self):
        self['bg'] = cfg.BGPRESSED
        cfg.ROOT.after(100, lambda: self.configure(bg=cfg.BGBUTTON))
        self.ConvertPath()
        
    def ConvertPath(self):
        clipbrd = paste()
        detected = detectPath(clipbrd)
        
        if detected == 'isWin':
            converted = toMac(clipbrd)
            widgets['display']['text'] = converted
            
            t1 = (
                'Обнаружен путь для Windows:'
                f'\n{clipbrd}'
                '\n\nПреобразую для Mac:'
                f'\n{converted}'
                '\n\nСкопировано в буфер обмена'
                )

            widgets['display']['text'] = t1
            copy(converted)

            return

        elif detected == 'isMac':
            converted = toWin(clipbrd)
            # widgets['display']['text'] = converted
            t2 = (
            'Обнаружен путь для Mac:'
            f'\n{clipbrd}'
            '\n\nПреобразую для Windows:'
            f'\n{converted}'
            '\n\nСкопировано в буфер обмена'
            )

            widgets['display']['text'] = t2
            copy(converted)
            return

        elif detected == 'isLocal':
            widgets['display']['text'] = clipbrd
            t3 = (
            'Обнаружен локальный путь для Mac:'
            f'\n{clipbrd}'
            '\nНажмите "Открыть"'
            )
            widgets['display']['text'] = t3

        elif not detected:
            old = widgets['display']['text']
            widgets['display']['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(1000, lambda: widgets['display'].configure(text=old))

class OpenButton(tkinter.Label):
    def __init__(self, master):
        tkinter.Label.__init__(
            self, master, height=3, width=16, 
            text = 'Открыть', bg=cfg.BGBUTTON, fg=cfg.BGFONT)
        self.bind('<Button-1>', lambda e: self.Run())
        self.bind('<Enter>', lambda e: self.enter())
        self.bind('<Leave>', lambda e: self.leave())

    def enter(self):
        self['bg'] = cfg.BGSELECTED

    def leave(self):
        self['bg'] = cfg.BGBUTTON

    def Run(self):
        self['bg'] = cfg.BGPRESSED
        cfg.ROOT.after(100, lambda: self.configure(bg=cfg.BGBUTTON))
        self.DetectPath()
        
    def DetectPath(self):
        pasted = paste()
        detectedPath = detectPath(pasted)

        if detectedPath == 'isMac':
            converted = toMac(toWin(pasted))
            if not converted:
                old = widgets['display']['text']
                widgets['display']['text'] = 'Скопируйте путь в буфер обмена'
                cfg.ROOT.after(1000, lambda: widgets['display'].configure(text=old))
                return
            
            widgets['display']['text'] = converted
            self.OpenConverted(converted)
            return
        
        elif detectedPath == 'isWin':
            converted = toMac(pasted)
            if not converted:
                old = widgets['display']['text']
                widgets['display']['text'] = 'Скопируйте путь в буфер обмена'
                cfg.ROOT.after(1000, lambda: widgets['display'].configure(text=old))
                return
            
            widgets['display']['text'] = converted
            self.OpenConverted(converted)
            return
        
        elif detectedPath == 'isLocal':
            widgets['display']['text'] = pasted
            self.OpenConverted(pasted)
            return
        
        elif not detectedPath:
            lastPath = widgets['display']['text']
            
            if lastPath != 'Hello':
                self.OpenConverted(lastPath)
                return
            
            else:
                old = widgets['display']['text']
                widgets['display']['text'] = 'Скопируйте путь в буфер обмена'
                cfg.ROOT.after(1000, lambda: widgets['display'].configure(text=old))
                return

    def OpenConverted(self, converted):
        openPath = existsPath(converted)

        if not openPath:
            old = widgets['display']['text']
            widgets['display']['text'] = 'Скопируйте путь в буфер обмена'
            cfg.ROOT.after(2000, lambda: widgets['display'].configure(text=old))
            return
        
        elif openPath['fullPath'] == openPath['shortPath']:
            open_path(openPath['fullPath'])

            widgets['display']['text'] = (
                f'Открываю путь:'
                f'\n{openPath["fullPath"]}'
                )
            return

        elif openPath['fullPath'] != openPath['shortPath']:
            error = openPath['fullPath'].replace(openPath['shortPath'], '')
            open_path(openPath['shortPath'])

            widgets['display']['text'] = (
                f'Возможно где-то здесь в пути есть ошибка:'
                f'\n{error}'
                '\nОткрываю ближайший путь:'
                f'\n{openPath["shortPath"]}'
                )
            return
