# -*- coding: utf-8 -*-

"""
    python setup.py py2app
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

from setuptools import setup

from cfg import cnf
from copy_tcl_to_app import copy_tcl_to_app

def remove_trash():
    trash = ("build", ".eggs", "dist")
    for i in trash:
        try:
            shutil.rmtree(i)
        except Exception as e:
            print(e)
            continue


def move_app_to_desktop(appname: str):
    desktop = os.path.expanduser("~/Desktop")

    dest = os.path.join(desktop, f"{appname}.app")
    src = os.path.join("dist", f"{appname}.app")

    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
    except Exception as e:
        print(e)

    try:
        shutil.move(src, dest)
    except Exception as e:
        print(e)

    try:
        subprocess.Popen(["open", "-R", dest])
    except Exception as e:
        print(e)

    return dest

YEAR = datetime.now().year # CURRENT YEAR
AUTHOR = "Evgeny Loshkarev"  # "Evgeny Loshkarev"
SHORT_AUTHOR_NAME = "Evlosh" # "Evlosh"
COMPANY = "MIUZ Diamonds" # "MIUZ Diamonds" or ""
APP_NAME = cnf.app_name
APP_VER = cnf.app_ver # "1.0.0"
ICON_PATH = "icon.icns" # "icon/icon.icns" or "icon.icns"
MAIN_FILES = ["start.py"] # SINGLE OR MULTIPLE PYTHON FILES

BUNDLE_ID = f"com.{SHORT_AUTHOR_NAME}.{APP_NAME}" # DON'T CHANGE IT
PY_2APP = "py2app" # DON'T CHANGE IT

# IF YOU DON'T HAVE ADVANCED FILES
DATA_FILES = []



# DON'T CHANGE IT

OPTIONS = {"iconfile": ICON_PATH,
           "plist": {"CFBundleName": APP_NAME,
                     "CFBundleShortVersionString": APP_VER,
                     "CFBundleVersion": APP_VER,
                     "CFBundleIdentifier": BUNDLE_ID,
                     "NSHumanReadableCopyright": (
                         f"Created by {AUTHOR}"
                         f"\nCopyright © {YEAR} {COMPANY}."
                         f"\nAll rights reserved.")}}


if __name__ == "__main__":

    sys.argv.append(PY_2APP)

    try:
        remove_trash()

        setup(
            app=MAIN_FILES,
            name=APP_NAME,
            data_files=DATA_FILES,
            options={PY_2APP: OPTIONS},
            setup_requires=[PY_2APP],
            )

        dest = move_app_to_desktop(APP_NAME)
        remove_trash()
        copy_tcl_to_app(app_dest=dest)
        

    except Exception as e:
        print(e)
        remove_trash()
