try:
    import tkinter

    from cfg import Cfg
    from utils import MainItem
    from widgets.main_win import MainWin

    root = tkinter.Tk()
    root.withdraw()
    main_item = MainItem()
    cfg = Cfg()
    app = MainWin(root, main_item, cfg)

    root.mainloop()

except Exception as e:
    from utils import Err
    Err.print_error(e)