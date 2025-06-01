try:
    import tkinter

    from utils import MainItem
    from widgets.main_win import MainWin

    root = tkinter.Tk()
    root.withdraw()
    main_item = MainItem()
    app = MainWin(root, main_item)

    root.mainloop()

except Exception as e:
    from utils import Err
    Err.print_error(e)