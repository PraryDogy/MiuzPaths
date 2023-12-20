# -*- coding: utf-8 -*-

"""
    python setup.py py2app
"""

import sys

import icnsutil
from setuptools import setup

import cfg
from setup_ext import SetupExt

src = 'icon.png'
img = icnsutil.IcnsFile()
img.add_media(file=src)
img.write(f'icon.icns')


OPTIONS = {
    'iconfile': 'icon.icns',
    'plist': {
    'CFBundleName': cfg.APP_NAME,
    'CFBundleShortVersionString':cfg.APP_VER,
    'CFBundleVersion': cfg.APP_VER,
    'CFBundleIdentifier':f'com.evlosh.{cfg.APP_NAME}',
    'NSHumanReadableCopyright': (
        'Created by Evgeny Loshkarev'
        '\nCopyright © 2023 MIUZ Diamonds. All rights reserved.')
    }
    }


if __name__ == "__main__":
    sys.argv.append("py2app")

    setup(
        app = ['start.py'],
        name = cfg.APP_NAME,
        data_files = [],
        options = {'py2app': OPTIONS},
        setup_requires = ['py2app'],
        )

    SetupExt(py_ver="3.11", appname=cfg.APP_NAME)
