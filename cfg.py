import os
import tkinter
import json

class Colors:
    def __init__(self) -> None:
        super().__init__()

        self.text_color = "#E2E2E2"
        self.text_color_dark = "#D3D3D3"
        self.bg_color = "#1e1e1e"
        self.btn_color = "#303030"
        self.blue_color = "#3d6a97"
        self.red_color = "#960000"
        self.lgray_color = "#4B4B4B"
        self.dgray_color = "#141416"


class GuiDigits:
    def __init__(self):
        super().__init__()

        self.corner = 8
        self.scroll_width = 17


class Config(Colors, GuiDigits):
    def __init__(self):
        super().__init__()
        self.root = tkinter.Tk()
        self.root.withdraw()

        self.app_name = 'MiuzPaths'
        self.app_ver = '2.1.0'
        self.cfg_dir = os.path.join(os.path.expanduser("~"),
            f"Library", "Application Support", self.app_name)
        
        self.json_dir = os.path.join(self.cfg_dir, "cfg.json")


        self.extra_paths = ["/Studio/PANACEA", "/Studio/MIUZ"]

        # length 30
        # 1: 1--DsK4{#4w}OH!(v)8_109ho{}@R0
        # 2: ...
        # 3: ...
        self.product_key = "1--DsK4{#4w}OH!(v)8_109ho{}@R0"

        self.data = {
            "extra_paths": self.extra_paths,
            "product_key": self.product_key
        }

        Colors.__init__(self)
        GuiDigits.__init__(self)

    def check_dir(self):
        if not os.path.exists(path=self.cfg_dir):
            os.makedirs(name=self.cfg_dir, exist_ok=True)

        if not os.path.exists(path=self.json_dir):
            self.write_data()

        with open(file=self.json_dir, mode="r", encoding="utf-8") as file:

            try:
                data = json.load(file)

            except json.JSONDecodeError:
                data = self.data

            if type(data) != dict:
                data = self.data

            if data.keys() != self.data.keys():
                data = self.data

            if data["product_key"] != self.product_key:
                data = self.data

            self.data = data
            self.write_data()

    def write_data(self):
        with open(file=self.json_dir, mode="w", encoding="utf-8") as file:
            json.dump(obj=self.data, fp=file, ensure_ascii=False, indent=4)


cnf = Config()
cnf.check_dir()