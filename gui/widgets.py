import tkinter

import cfg
from utils import (CustomButton, copy, detectPath, existsPath, open_path,
                   paste, toMac, toWin)

vars = {
    'display': tkinter.Label,
    'last_path': False
    }


def alarm():
    old = vars['display']['text']
    vars['display']['text'] = 'Скопируйте путь в буфер обмена'
    cfg.ROOT.after(1000, lambda: vars['display'].configure(text=old))


class Display(tkinter.Label):
    def __init__(self, **kwargs):
        tkinter.Label.__init__(self, cfg.ROOT, bg=cfg.BGDISPLAY, **kwargs,
        height=15, fg=cfg.BGFONT, justify=tkinter.LEFT,
        anchor=tkinter.CENTER, padx=5, pady=5, wraplength=295)
        vars['display'] = self
        self['text'] = (
            'Скопируйте путь до сетевого диска МЮЗ'
            '\nи нажмите "Открыть" или "Преобразовать".'
            )


class ConvertButton(CustomButton):
    def __init__(self, master):
        CustomButton.__init__(
            self, master, height=3, width=16, text = 'Преобразовать',
            bg=cfg.BGBUTTON,fg=cfg.BGFONT)
        self.bind('<Button-1>', lambda e: self.convert())

    def convert(self):
        self.press()

        clipbrd = paste()
        detected = detectPath(clipbrd)
        
        if detected == 'isWin':
            converted = toMac(clipbrd)
            t1 = (
                'Обнаружен путь для Windows:'
                f'\n{clipbrd}'
                '\n\nПреобразую для Mac:'
                f'\n{converted}'
                '\n\nСкопировано в буфер обмена'
                )
            vars['display']['text'] = t1
            copy(converted)
            vars['last_path'] = converted

        elif detected == 'isMac':
            converted = toWin(clipbrd)
            t2 = (
                'Обнаружен путь для Mac:'
                f'\n{clipbrd}'
                '\n\nПреобразую для Windows:'
                f'\n{converted}'
                '\n\nСкопировано в буфер обмена'
                )
            vars['display']['text'] = t2
            copy(converted)
            vars['last_path'] = converted

        elif detected == 'isLocal':
            t3 = (
                'Обнаружен локальный путь для Mac:'
                f'\n{clipbrd}'
                '\nНажмите "Открыть"'
                )
            vars['display']['text'] = t3
            vars['last_path'] = clipbrd

        elif not detected:
            alarm()


class OpenButton(CustomButton):
    def __init__(self, master):
        CustomButton.__init__(
            self, master, height=3, width=16, 
            text = 'Открыть', bg=cfg.BGBUTTON, fg=cfg.BGFONT)
        self.bind('<Button-1>', lambda e: self.open_path())
        
    def open_path(self):
        self.press()
        pasted = paste()
        detectedPath = detectPath(pasted)

        if detectedPath == 'isMac':
            converted = toMac(toWin(pasted))
            if not converted:
                alarm()
                return
            self.OpenConverted(converted)
            vars['last_path'] = converted
            return
        
        elif detectedPath == 'isWin':
            converted = toMac(pasted)
            if not converted:
                alarm()
                return
            
            self.OpenConverted(converted)
            vars['last_path'] = converted

        elif detectedPath == 'isLocal':
            self.OpenConverted(pasted)
            vars['last_path'] = pasted

        elif not detectedPath:
            if vars['last_path']:
                self.OpenConverted(vars['last_path'])

                return
            else:
                alarm()

    def OpenConverted(self, converted):
        openPath = existsPath(converted)

        if not openPath:
            alarm()
            return
        
        elif openPath['fullPath'] == openPath['shortPath']:
            open_path(openPath['fullPath'])

            vars['display']['text'] = (
                f'Открываю путь:'
                f'\n{openPath["fullPath"]}'
                )
            return

        elif openPath['fullPath'] != openPath['shortPath']:
            error = openPath['fullPath'].replace(openPath['shortPath'], '')
            open_path(openPath['shortPath'])

            vars['display']['text'] = (
                f'Возможно где-то здесь в пути есть ошибка:'
                f'\n{error}'
                '\nОткрываю ближайший путь:'
                f'\n{openPath["shortPath"]}'
                )
            return
