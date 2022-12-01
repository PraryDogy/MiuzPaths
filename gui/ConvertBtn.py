import tkinter

import cfg
from utils import copy, detectPath, display, paste, toMac, toWin


class ConvertButton:
    def __init__(self, BotFrame, root):
        self.root = root

        convertButton = tkinter.Label(
            BotFrame,
            height=3, 
            width=16,
            text = 'Преобразовать', 
            bg=cfg.BGBUTTON,
            fg=cfg.FONTCOLOR,
            )
        convertButton.bind('<Button-1>', lambda event, button=convertButton: self.Run(button))
        convertButton.pack(side='right')
        convertButton.bind('<Enter>', lambda e: self.enter(convertButton))
        convertButton.bind('<Leave>', lambda e: self.leave(convertButton))

    def enter(self, btn: tkinter.Label):
        btn['bg'] = cfg.BGSELECTED

    def leave(self, btn: tkinter.Label):
        btn['bg'] = cfg.BGBUTTON

    def Run(self, button: tkinter.Label):
        button.configure(bg=cfg.BGPRESSED)
        self.root.after(100, lambda: button.configure(bg=cfg.BGBUTTON))
        self.ConvertPath()
        
        
    def ConvertPath(self):
        clipbrd = paste()
        detected = detectPath(clipbrd)
        
        if detected == 'isWin':
            converted = toMac(clipbrd)
            self.root.winfo_children()[-1].configure(text=converted)
            
            t1 = (
                'Обнаружен путь для Windows:'
                f'\n{clipbrd}'
                '\n\nПреобразую для Mac:'
                f'\n{converted}'
                '\n\nСкопировано в буфер обмена'
                )

            display(self.root, t1)
            copy(converted)

            return

        if detected == 'isMac':
            converted = toWin(clipbrd)
            self.root.winfo_children()[-1].configure(text=converted)
            t2 = (
            'Обнаружен путь для Mac:'
            f'\n{clipbrd}'
            '\n\nПреобразую для Windows:'
            f'\n{converted}'
            '\n\nСкопировано в буфер обмена'
            )

            display(self.root, t2)
            copy(converted)
            return

        if detected == 'isLocal':
            self.root.winfo_children()[-1].configure(text=clipbrd)
            t3 = (
            'Обнаружен локальный путь для Mac:'
            f'\n{clipbrd}'
            '\nНажмите "Открыть"'
            )
            display(self.root, t3)

        if not detected:
            display(self.root, 'Скопируйте путь в буфер обмена')
