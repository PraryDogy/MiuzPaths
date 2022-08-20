from tkinter import Text
from cfg import FontColor, BGColor


class Display:
    def __init__(self, f1, root):
        self.root = root
        lbl = Text(f1)
    
        txt = (
            'Скопируйте путь до сетевого диска МЮЗ, например:'
            '\nZ:\\Marketing\\Photo2022\\Brilliance'
            '\nили'
            '\n/Volumes/Shares/Marketing' 
            '\nи нажмите "Конвертировать" или "Открыть"'
            )
        lbl.insert('end',txt)
        lbl.configure(
            fg=FontColor,
            state='disabled',
            wrap='word',
            padx=15,
            pady=15,
            highlightthickness=0,
            width=42,
            height=10,
            bg="#1A1A1A",
            highlightbackground=BGColor,
            )
        
        lbl.pack()        