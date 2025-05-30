import tkinter


class Config:
    def __init__(self):
        super().__init__()
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.app_name = 'Paths'
        self.app_ver = '2.1.0'


cnf = Config()
cnf.check_dir()