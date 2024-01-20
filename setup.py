# -*- coding: utf-8 -*-

"""
    python setup.py py2app
"""

import sys

import icnsutil
from setuptools import setup

from setup_ext import SetupExt
from cfg import cnf

src = 'icon.png'
img = icnsutil.IcnsFile()
img.add_media(file=src)
img.write(f'icon.icns')


OPTIONS = {
    'iconfile': 'icon.icns',
    'plist': {
    'CFBundleName': cnf.app_name,
    'CFBundleShortVersionString':cnf.app_ver,
    'CFBundleVersion': cnf.app_ver,
    'CFBundleIdentifier':f'com.evlosh.{cnf.app_name}',
    'NSHumanReadableCopyright': (
        'Created by Evgeny Loshkarev'
        '\nCopyright © 2023 MIUZ Diamonds. All rights reserved.')
    }
    }


if __name__ == "__main__":
    sys.argv.append("py2app")

    setup(
        app = ['start.py'],
        name = cnf.app_name,
        data_files = [],
        options = {'py2app': OPTIONS},
        setup_requires = ['py2app'],
        )

    SetupExt(py_ver="3.11", appname=cnf.app_name)
