from tkinter import Label

import cfg
from utils import Converter, Opener, ShowText, ClipBrd


class OpenButton():
    def __init__(self, frameForButtons, root) -> None:
        self.root = root

        CloseButton = Label(frameForButtons, height=3, width=16, text = 'Открыть', bg=cfg.BGButton, fg=cfg.FontColor,)
        CloseButton.bind('<Button-1>', lambda event, button=CloseButton: self.Run(button))
        CloseButton.pack(side='left')


    def Run(self, button):
        button.configure(bg=cfg.bgPressed)
        self.root.after(300, lambda: button.configure(bg=cfg.BGButton))
        self.DetectPath()
        
        
    def DetectPath(self):
        pasted = ClipBrd.paste()
        detectedPath = Converter.detectPath(pasted)

        if detectedPath == 'isMac':
            converted = Converter.toMac(Converter.toWin(pasted))
            if not converted:
                ShowText.display(self.root, 'Скопируйте путь в буфер обмена')
                return
            
            lastPath = self.root.winfo_children()[-1].configure(text=converted)
            self.OpenConverted(converted)
            return
        
        if detectedPath == 'isWin':
            converted = Converter.toMac(pasted)
            if not converted:
                ShowText.display(self.root, 'Скопируйте путь в буфер обмена')
                return
            
            lastPath = self.root.winfo_children()[-1].configure(text=converted)
            self.OpenConverted(converted)
            return
        
        if detectedPath == 'isLocal':
            lastPath = self.root.winfo_children()[-1].configure(text=pasted)
            self.OpenConverted(pasted)
            return
        
        if not detectedPath:
            lastPath = self.root.winfo_children()[-1].cget('text')
            
            if lastPath != 'Hello':
                self.OpenConverted(lastPath)
                return
            
            else:
                ShowText.display(self.root, f'Скопируйте путь в буфер обмена')
                return

    
    def OpenConverted(self, converted):
        openPath = Opener.existsPath(converted)

        if not openPath:
            ShowText.display(self.root, 'Скопируйте путь в буфер обмена')
            return
        
        if openPath['fullPath'] == openPath['shortPath']:
            Opener.openPath(openPath['fullPath'])

            ShowText.display(self.root, (f'Открываю путь:\n\n{openPath["fullPath"]}'))
            return

        if openPath['fullPath'] != openPath['shortPath']:
            error = openPath['fullPath'].replace(openPath['shortPath'], '')
            Opener.openPath(openPath['shortPath'])

            ShowText.display(
                self.root, 
                f'Возможно где-то здесь в пути есть ошибка:\n{error}\n\nОткрываю ближайший путь:\n{openPath["shortPath"]}'
                )
            return
