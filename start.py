try:
    from cfg import cnf
    from widgets.main import Main
    app = Main()
    cnf.root.mainloop()
except Exception as e:
    ...