import tkinter
import os
from cryptography.fernet import Fernet, InvalidToken
import json
from utils import encrypt_cfg
import shutil

APP_NAME = 'MiuzPaths'
APP_VER = '1.6.2'

KEY = 'bNv711lJcHurusZBkBNhfZIX0yNFNFJ-HzpE3g_ifUM='

CFG_DIR = os.path.join(
    os.path.expanduser('~'), 'Library/Application Support/MiuzPaths')

IP = '192.168.10.105'
NETWORK = '/Volumes/Shares/Marketing/'

ROOT = tkinter.Tk()
ROOT.withdraw()

BGFONT = "#E2E2E2"
BGCOLOR = "#1A1A1A"
BGBUTTON = "#2C2C2C"
BGPRESSED = '#395432'
BGSELECTED = '#4E4769'
BGDISPLAY = '#151515'


def defaults():
    return {
        'APP_VER': APP_VER,
        'GEOMETRY': [700, 500, 0, 0],
        }

def read_cfg(what_read: str):
    """
    Decrypts `cfg.json` from `cfg.CFG_DIR` and returns dict.
    """
    key = Fernet(KEY)
    with open(what_read, 'rb') as file:
        data = file.read()
    try:
        return json.loads(key.decrypt(data).decode("utf-8"))
    except InvalidToken:
        config = defaults()
        encrypt_cfg(config)
        return config


if not os.path.exists(CFG_DIR):
    os.mkdir(CFG_DIR)

if os.path.exists(os.path.join(CFG_DIR, 'cfg')):
    config = read_cfg(os.path.join(CFG_DIR, 'cfg'))
else:
    config = defaults()
    encrypt_cfg(config)

defs = defaults()
part1 = {k:v for k, v in config.items() if k in defs.keys()}
part2 = {k:v for k, v in defs.items() if k not in config.keys()}
new_config = {**part1, **part2}
encrypt_cfg(new_config) if new_config.keys() != config.keys() else False
config = new_config if new_config.keys() != config.keys() else config