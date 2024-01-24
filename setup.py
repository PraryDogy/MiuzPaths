import sys
import icnsutil
from setuptools import setup
from datetime import datetime

from setup_ext import SetupExt
from cfg import cnf

src = 'icon.png'
img = icnsutil.IcnsFile()
img.add_media(file=src)
img.write(f'icon.icns')

current_year = datetime.now().year

OPTIONS = {
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': cnf.app_name,
        'CFBundleShortVersionString': cnf.app_ver,
        'CFBundleVersion': cnf.app_ver,
        'CFBundleIdentifier': f'com.evlosh.{cnf.app_name}',
        'NSHumanReadableCopyright': (
            f'Created by Evgeny Loshkarev'
            f'\nCopyright © {current_year} {cnf.app_name}. All rights reserved.')
    }
}

if __name__ == "__main__":
    sys.argv.append("py2app")

    setup(
        app=['start.py'],
        name=cnf.app_name,
        data_files=[],
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

    SetupExt(py_ver="3.12", appname=cnf.app_name)
