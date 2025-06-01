try:
    import tkinter

    from utils import MainItem
    from widgets.main import Main

    root = tkinter.Tk()
    MainItem.setup_string_var()

    root.withdraw()
    app = Main(root)

    root.mainloop()

except Exception as e:
    from utils import Err
    Err.print_error(e)