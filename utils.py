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

    win_reg = r"/?/?[a-zA-Z]://?marketing/"
    striped = re.sub(win_reg, "Shares/Marketing/", striped, flags=re.IGNORECASE)

    smb_reg = r"/?/?smb://?"
    striped = re.sub(smb_reg, "", striped, count=1, flags=re.IGNORECASE)

    sbc_reg = r"/?/?sbc\d\d/(.+/)"
    if re.match(sbc_reg, striped, flags=re.IGNORECASE):
        sbc_reg = r"(sbc\d\d/)"
        striped = re.sub(sbc_reg, "", striped, count=1, flags=re.IGNORECASE)

    ip_reg = r"/?/?\d{,4}\.\d{,4}\.\d{,4}\.\d{,4}/(.+)/"
    if re.match(ip_reg, striped, flags=re.IGNORECASE):
        ip_reg = r"\d{,4}\.\d{,4}\.\d{,4}\.\d{,4}/"
        striped = re.sub(ip_reg, "", striped, count=1, flags=re.IGNORECASE)

    sh_reg = r"/?/?Shares/(.+/)"
    if re.match(sh_reg, striped, flags=re.IGNORECASE):
        sh_reg = r"/?Shares/"
        striped = re.sub(sh_reg, "Volumes/Shares/", striped, count=1, flags=re.IGNORECASE)

    sh_reg = r"/?/?Marketing/(.+/)"
    if re.match(sh_reg, striped, flags=re.IGNORECASE):
        striped = "Volumes/Shares/" + striped

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

def reveal(input):
    if os.path.isfile(input):
        subprocess.Popen(["open", "-R", input])
    else:
        subprocess.Popen(["open", input])