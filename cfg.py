import tkinter
import os
import cffi
from cryptography.fernet import Fernet
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
BGCOLOR = "#1A1A1A"
BGBUTTON = "#2C2C2C"
BGPRESSED = '#395432'
BGSELECTED = '#4E4769'
BGDISPLAY = '#151515'


def defaults():
    return {
        'APP_VER': APP_VER,
        'GEOMETRY': [700, 500, 0, 0],
        'LAST_PATH': '',
        }


def encrypt_cfg(data: dict):
    """
    Converts dict with json dumps and enctypt converted with fernet module.
    Writes enctypted data to `cfg.json` in `cfg.CFG_DIR`
    *param `data`: python dict
    """
    key = Fernet(KEY)
    encrypted = key.encrypt(json.dumps(data).encode("utf-8"))
    with open(os.path.join(CFG_DIR, 'cfg'), 'wb') as file:
        file.write(encrypted)


def read_cfg(what_read: str):
    """
    Decrypts `cfg.json` from `cfg.CFG_DIR` and returns dict.
    """
    key = Fernet(KEY)
    with open(what_read, 'rb') as file:
        data = file.read()
        return json.loads(key.decrypt(data).decode("utf-8"))

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