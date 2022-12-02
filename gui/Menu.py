from tkinter import Label, Menu, Toplevel
import cfg

class MenuGui:
    def __init__(self):

        menubar = Menu(cfg.ROOT)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Меню", menu=filemenu)

        filemenu.add_command(label="О программе", command=self.AboutApp)
        filemenu.add_command(label="Инструкция", command=self.Descr)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=cfg.ROOT.destroy)
        cfg.ROOT.createcommand(
            'tkAboutDialog',
            lambda: cfg.ROOT.tk.call('tk::mac::standardAboutPanel'))

        cfg.ROOT.config(menu=menubar)

    def AboutApp(self):
        newWin = Toplevel(cfg.ROOT, pady=10, padx=10, bg=cfg.BGCOLOR, )
        newWin.title('О программе')

        made = (
            f'{cfg.APP_NAME} {cfg.APP_VER}'
            '\n\nCreated by Evgeny Loshkarev'
            '\nCopyright © 2022 MIUZ Diamonds.'
            '\nAll rights reserved.'
            '\n'
            )
        
        l1 = Label(newWin, text=made, fg=cfg.BGFONT, bg=cfg.BGCOLOR)
        l1.pack()

        CloseButton = Label(
            newWin,
            height=3, 
            width=16,
            text = 'Закрыть',
            bg=cfg.BGBUTTON,
            fg=cfg.BGFONT,
            )
        CloseButton.bind('<Button-1>', lambda event: newWin.destroy())
        CloseButton.pack()
        
        cfg.ROOT.eval('tk::PlaceWindow {} center'.format(newWin))

    
    def Descr(self):
        newWin = Toplevel(cfg.ROOT, pady=10, padx=10, bg=cfg.BGCOLOR)
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

        l1 = Label(newWin, text=descrip1,fg='white', bg=cfg.BGCOLOR, justify='left')
        l1.pack()

        l2 = Label(newWin, text=warning,fg='white', bg=cfg.BGCOLOR,)
        l2.pack()

        l3 = Label(newWin, text=descrip2,fg='white', bg=cfg.BGCOLOR, justify='left')
        l3.pack()

        CloseButton = Label(
            newWin,
            height=3, 
            width=16,
            text = 'Закрыть', 
            bg=cfg.BGBUTTON,
            fg=cfg.BGFONT,
            )
        CloseButton.bind('<Button-1>', lambda event: newWin.destroy())
        CloseButton.pack()
        
        cfg.ROOT.eval('tk::PlaceWindow {} center'.format(newWin))