try:
    import tkinter

    from utils import Shared
    from widgets.main import Main

    root = tkinter.Tk()
    Shared.setup_string_var()

    root.withdraw()
    app = Main(root)

    root.mainloop()

except Exception as e:
    from utils import Err
    Err.print_error(e)