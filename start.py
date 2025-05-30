try:
    from widgets.main import Main
    import tkinter
    root = tkinter.Tk()
    root.withdraw()
    app = Main(root)
    root.mainloop()
except Exception as e:
    from utils import Err
    Err.print_error(e)