import tkinter
import os
import json


APP_NAME = 'MiuzPaths'
APP_VER = '1.7.0'

KEY = 'bNv711lJcHurusZBkBNhfZIX0yNFNFJ-HzpE3g_ifUM='

CFG_DIR = os.path.join(
    os.path.expanduser('~'), f'Library/Application Support/{APP_NAME}')

IP = '192.168.10.105'
NETWORK = '/Volumes/Shares/Marketing/'

ROOT = tkinter.Tk()
ROOT.withdraw()

BGFONT = "#E2E2E2"
BGCOLOR = "#19191B"
BGBUTTON = "#2A2A2D"
BGPRESSED = "#4B4B4B"
BGSELECTED = '#3A3A3E'
