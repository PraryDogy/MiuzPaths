import os
import re
import subprocess


def paste():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


def run_applescript(applescript: str):
    args = [
        item
        for x in [("-e",l.strip())
        for l in applescript.split('\n')
        if l.strip() != ''] for item in x]
    subprocess.call(["osascript"] + args)


def normalize_path(input):
    striped = input.strip()

    link_reg = r'http://|https://'
    if re.findall(link_reg, input):
        return False

    striped = striped.replace("\\", "/")

    mac_reg = r'/?.{,100}/.{,100}/.{,100}'
    if not re.findall(mac_reg, striped):
        return False

    smb_reg = r"[sS]?[mM]?[bB]?:?/?/?\d{,10}\.\d{,10}\.\d{,10}\.\d{,10}/"
    res = re.findall(smb_reg, striped)
    if res:
        striped = striped.replace(res[0], "Volumes/")

    sbc_reg = r"[sS][bB][cC][^/]{,10}/"
    res = re.findall(sbc_reg, striped)
    if res:
        striped = striped.replace(res[0], "Volumes/")

    win_reg = r"\w:/[mM][aA][rR][kK][eE][tT][iI][nN][gG]/"
    res = re.findall(win_reg, striped)
    if res:
        striped = striped.replace(res[0], "/Volumes/Shares/Marketing/")

    return "/" + striped.strip("/")


def exists_path(input):
    while not os.path.exists(input):
        input = os.path.split(input)[0]
    return input


def create_applescript(input):
    return f"""
            set thePath to POSIX file "{input}"
            tell application "Finder" to reveal thePath
            tell application "Finder" to activate
            """