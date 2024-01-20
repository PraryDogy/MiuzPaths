import json
import os

from cfg import cnf
from .system import SysUtils


__all__ = ("PrePaths", )

class Storage:
    json_dir = os.path.join(cnf.cfg_dir, "cfg.json")


class PrePathsDefault:
    default_prepaths = [
        "/Volumes/Shares/Marketing",
        "",
        ]


class PrePaths(Storage, SysUtils):
    def __init__(self):
        try:
            with open(file=Storage.json_dir, encoding="utf8", mode="r") as file:
                self.pre_paths = json.loads(s=file.read())

        except FileNotFoundError:
            with open(file=Storage.json_dir, encoding="utf8", mode="w") as file:

                json.dump(obj=PrePathsDefault.default_prepaths, fp=file,
                          indent=4, ensure_ascii=False)

            self.pre_paths = PrePathsDefault.default_prepaths