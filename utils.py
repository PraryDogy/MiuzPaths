import os
import re
import subprocess
import cfg
import threading

def copy(output: str):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def paste():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


def is_win(clipboard: str):
    winRegex = r'\\(?:.+\\).{,10}'
    if re.findall(winRegex, clipboard):
        return True
    return False


def is_mac(clipboard: str):
    macRegex = r'/(?:.+/).{,10}'
    if re.findall(macRegex, clipboard):

        link_regex = r'http://|https://'
        if re.findall(link_regex, clipboard):
            return False

        return True
    return False


def to_win(from_clipboard: str):
    tmp = from_clipboard.casefold().split('/')

    if 'shares' in tmp:
        sharesIndex = tmp.index('shares')
        splited = from_clipboard.split('/')[sharesIndex:]
        return '\\'.join(['smb:']+[cfg.IP]+splited)

    if 'marketing' in tmp:
        marketingIndex = tmp.index('marketing')
        splited = from_clipboard.split('/')[marketingIndex:]
        return '\\'.join(['smb:']+[cfg.IP]+['Shares']+splited)

    return False


def to_mac(from_clipboard: str):
    tmp = from_clipboard.casefold().split('\\')

    if 'shares' in tmp:
        sharesIndex = tmp.index('shares')
        pathList = from_clipboard.split('\\')[sharesIndex:]
        return os.path.join(os.path.sep, 'Volumes', *pathList)
        
    if 'marketing' in tmp:
        marketingIndex = tmp.index('marketing')
        pathList = from_clipboard.split('\\')[marketingIndex:]
        return os.path.join(os.path.sep, 'Volumes', 'Shares', *pathList)
    
    return False


def remove_file(input):
    if os.path.isfile(input):
        return os.path.split(input)[0]
    return input


def exists_path(input):
    if input[0] is not os.sep:
        input = os.sep + input

    while not os.path.exists(input):
        input = os.path.split(input)[0]

    return input


def open_path(path_mac: str):
    try:
        subprocess.check_output(["/usr/bin/open", path_mac])
        return True
    except subprocess.CalledProcessError:
        return False
