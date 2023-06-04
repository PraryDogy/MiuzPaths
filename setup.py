# -*- coding: utf-8 -*-

"""
    python setup.py py2app
"""

import os
import shutil

from setuptools import setup
import cfg
import icnsutil


src = 'icon.png'
img = icnsutil.IcnsFile()
img.add_media(file=src)
img.write(f'icon.icns')

APP = ['start.py']

DATA_FILES = []

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

setup(
    app = APP,
    name = cfg.APP_NAME,
    data_files = DATA_FILES,
    options = {'py2app': OPTIONS},
    setup_requires = ['py2app'],
    install_requires = ['cryptography']
    )

shutil.copytree(
    "lib",
    f"dist/{cfg.APP_NAME}.app/Contents/lib"
    )

shutil.move(
    f"dist/{cfg.APP_NAME}.app",
    os.path.expanduser(f"~/Desktop/{cfg.APP_NAME}.app")
    )

shutil.rmtree('build')
shutil.rmtree('.eggs')
shutil.rmtree('dist')
