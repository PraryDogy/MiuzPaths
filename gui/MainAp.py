from tkinter import Frame, Tk

from cfg import BGColor

from .ConvertBtn import ConvertButton
from .Displ import Display
from .GlobalPath import GlobalPath
from .Menu import MenuGui
from .OpenBtn import OpenButton


class MainApp():
    def __init__(self) -> None:
        '''
        methods: Run
        '''
        self.root = Tk()

        # improve when deiconify not working by click to icon in Mac Os dock
        self.root.createcommand('tk::mac::ReopenApplication', self.root.deiconify)

        self.root.title('MiuzPaths')
        self.root.config(pady=10, padx=10, bg=BGColor,)

        self.root.resizable(0,0)


    def Run(self):
        # Structure: root > frame1(top): TextWidget for showing text & padding frame, frame2(bottom): Open path button, Convert Button
        f1 = Frame(
            self.root,
            bg = BGColor,
            )
        f1.pack()

        Display(f1, self.root)
        # this frame created for one side padding only (below Display text widget)
        Frame(
            f1,
            height=10,
            bg =BGColor,
            ).pack()

        f2 = Frame(
            self.root,
            bg=BGColor,
            )
        f2.pack()
        
        OpenButton(f2, self.root)
        # this frame created for one side padding only (between buttons)
        Frame(
            f2,
            bg=BGColor,
            width=20,
            ).pack(side='left')
        ConvertButton(f2, self.root)
        
        MenuGui(root=self.root)

        GlobalPath(self.root)

        # place main window center screen
        self.root.eval('tk::PlaceWindow {} center'.format(self.root))
        self.root.mainloop()
        