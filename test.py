import shutil
import os

ver = "3.11"
lib_src = f"/Library/Frameworks/Python.framework/Versions/{ver}/lib"
folders = "tcl8", "tcl8.6", "tk8.6"

for i in folders:
    shutil.copytree(
        os.path.join(lib_src, i),
        os.path.join("/Users/evlosh/Desktop", i)
        )