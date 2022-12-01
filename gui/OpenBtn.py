from tkinter import Label

import cfg
from utils import detectPath, display, paste, toMac, toWin, existsPath, open_path
import tkinter

class OpenButton():
    def __init__(self, frameForButtons, root):
        self.root = root

        CloseButton = Label(frameForButtons, height=3, width=16, text = 'Открыть', bg=cfg.BGBUTTON, fg=cfg.FONTCOLOR,)
        CloseButton.bind('<Button-1>', lambda event, button=CloseButton: self.Run(button))
        CloseButton.pack(side='left')
        CloseButton.bind('<Enter>', lambda e: self.enter(CloseButton))
        CloseButton.bind('<Leave>', lambda e: self.leave(CloseButton))

    def enter(self, btn: tkinter.Label):
        btn['bg'] = cfg.BGSELECTED

    def leave(self, btn: tkinter.Label):
        btn['bg'] = cfg.BGBUTTON

    def Run(self, button):
        button.configure(bg=cfg.BGPRESSED)
        self.root.after(100, lambda: button.configure(bg=cfg.BGBUTTON))
        self.DetectPath()
        
        
    def DetectPath(self):
        pasted = paste()
        detectedPath = detectPath(pasted)

        if detectedPath == 'isMac':
            converted = toMac(toWin(pasted))
            if not converted:
                display(self.root, 'Скопируйте путь в буфер обмена')
                return
            
            lastPath = self.root.winfo_children()[-1].configure(text=converted)
            self.OpenConverted(converted)
            return
        
        if detectedPath == 'isWin':
            converted = toMac(pasted)
            if not converted:
                display(self.root, 'Скопируйте путь в буфер обмена')
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
                display(self.root, f'Скопируйте путь в буфер обмена')
                return

    
    def OpenConverted(self, converted):
        openPath = existsPath(converted)

        if not openPath:
            display(self.root, 'Скопируйте путь в буфер обмена')
            return
        
        if openPath['fullPath'] == openPath['shortPath']:
            open_path(openPath['fullPath'])

            display(self.root, (f'Открываю путь:\n\n{openPath["fullPath"]}'))
            return

        if openPath['fullPath'] != openPath['shortPath']:
            error = openPath['fullPath'].replace(openPath['shortPath'], '')
            open_path(openPath['shortPath'])

            display(
                self.root, 
                f'Возможно где-то здесь в пути есть ошибка:\n{error}\n\nОткрываю ближайший путь:\n{openPath["shortPath"]}'
                )
            return
