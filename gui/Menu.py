from tkinter import Label, Menu, Toplevel
from cfg import version, BGBUTTON, FONTCOLOR, BGCOLOR


class MenuGui:
    def __init__(self, root):
        self.root = root

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Меню", menu=filemenu)

        filemenu.add_command(label="О программе", command=self.AboutApp)
        filemenu.add_command(label="Инструкция", command=self.Descr)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.root.destroy)

        self.root.config(menu=menubar)

    def AboutApp(self):
        newWin = Toplevel(self.root, pady=10, padx=10, bg=BGCOLOR, )
        newWin.title('О программе')

        name = (
            'MiuzPaths {}'
            '\n\n'
            ).format(version)
        
        made = (
            'Created by Evgeny Loshkarev'
            '\nCopyright © 2022 MIUZ Diamonds.'
            '\nAll rights reserved.'
            '\n'
            )
        
        l1 = Label(newWin, text=name+made,fg='white', bg=BGCOLOR,)
        l1.pack()

        CloseButton = Label(
            newWin,
            height=3, 
            width=16,
            text = 'Закрыть', 
            bg=BGBUTTON,
            fg=FONTCOLOR,
            )
        CloseButton.bind('<Button-1>', lambda event: newWin.destroy())
        CloseButton.pack()
        
        self.root.eval('tk::PlaceWindow {} center'.format(newWin))

    
    def Descr(self):
        newWin = Toplevel(self.root, pady=10, padx=10, bg=BGCOLOR, )
        newWin.title('Инструкция')


        descrip1 = (
            'Программа преобазует путь для Mac в путь для Windows и наоборот,'
            '\nи автоматически копирует преобразованный путь в буфер обмена.'
            '\nТак же программа умеет открывать путь, который был скопирован в буфер обмена.'
        )
        warning = (
            '\nВнимание!'
        )
        descrip2 = (
            'Программа работает только с путями до сетевого диска MIUZ с папкой Marketing'
            '\nТ.е. если в пути нет папки Marketing, ничего не произойдет'
            '\n'
        )

        l1 = Label(newWin, text=descrip1,fg='white', bg=BGCOLOR, justify='left')
        l1.pack()

        l2 = Label(newWin, text=warning,fg='white', bg=BGCOLOR,)
        l2.pack()

        l3 = Label(newWin, text=descrip2,fg='white', bg=BGCOLOR, justify='left')
        l3.pack()

        CloseButton = Label(
            newWin,
            height=3, 
            width=16,
            text = 'Закрыть', 
            bg=BGBUTTON,
            fg=FONTCOLOR,
            )
        CloseButton.bind('<Button-1>', lambda event: newWin.destroy())
        CloseButton.pack()
        
        self.root.eval('tk::PlaceWindow {} center'.format(newWin))