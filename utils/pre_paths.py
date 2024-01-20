import json
import os

from cfg import cnf
from .system import SysUtils


__all__ = ("PrePaths", )

class Storage:
    def __init__(self):
        self.json_dir = os.path.join(cnf.cfg_dir, "prepaths.json")


class PrePathsBase:
    def __init__(self):
        self.default_prepaths = [
            "/Volumes/Shares/Marketing",
            "",
            ]


class PrePaths(Storage, PrePathsBase, SysUtils):
    def __init__(self):
        Storage.__init__(self)
        PrePathsBase.__init__(self)

        try:
            with open(file=self.json_dir, encoding="utf8", mode="r") as file:
                self.prepaths = json.loads(s=file.read())

        except FileNotFoundError:
            with open(file=self.json_dir, encoding="utf8", mode="w") as file:

                json.dump(obj=self.default_prepaths, fp=file,
                          indent=4, ensure_ascii=False)

            self.prepaths = self.default_prepaths