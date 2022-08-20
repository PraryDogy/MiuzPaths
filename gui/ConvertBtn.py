import tkinter

import cfg
from utils import Converter, ShowText, ClipBrd


class ConvertButton:
    def __init__(self, BotFrame, root) -> None:
        self.root = root

        convertButton = tkinter.Label(
            BotFrame,
            height=3, 
            width=16,
            text = 'Преобразовать', 
            bg=cfg.BGButton,
            fg=cfg.FontColor,
            )
        convertButton.bind('<Button-1>', lambda event, button=convertButton: self.Run(button))
        convertButton.pack(side='right')


    def Run(self, button):
        button.configure(bg=cfg.bgPressed)
        self.root.after(300, lambda: button.configure(bg=cfg.BGButton))
        self.ConvertPath()
        
        
    def ConvertPath(self):
        clipbrd = ClipBrd.paste()
        detected = Converter.detectPath(clipbrd)
        
        if detected == 'isWin':
            converted = Converter.toMac(clipbrd)
            self.root.winfo_children()[-1].configure(text=converted)
            
            t1 = (
                'Обнаружен путь для Windows:'
                f'\n{clipbrd}'
                '\n\nПреобразую для Mac:'
                f'\n{converted}'
                '\n\nСкопировано в буфер обмена'
                )

            ShowText.display(self.root, t1)
            ClipBrd.copy(converted)

            return

        if detected == 'isMac':
            converted = Converter.toWin(clipbrd)
            self.root.winfo_children()[-1].configure(text=converted)
            t2 = (
            'Обнаружен путь для Mac:'
            f'\n{clipbrd}'
            '\n\nПреобразую для Windows:'
            f'\n{converted}'
            '\n\nСкопировано в буфер обмена'
            )

            ShowText.display(self.root, t2)
            ClipBrd.copy(converted)
            return

        if detected == 'isLocal':
            self.root.winfo_children()[-1].configure(text=clipbrd)
            t3 = (
            'Обнаружен локальный путь для Mac:'
            f'\n{clipbrd}'
            '\nНажмите "Открыть"'
            )
            ShowText.display(self.root, t3)

        if not detected:
            ShowText.display(self.root, 'Скопируйте путь в буфер обмена')
