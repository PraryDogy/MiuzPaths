import os
import re
import subprocess
import cfg
import threading


def paste():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


def detect_path(input):
    macRegex = r'/(?:.+/).{,10}'
    if re.findall(macRegex, input):

        link_regex = r'http://|https://'
        if re.findall(link_regex, input):
            return False

        return input

    return False


def exists_path(input):
    while not os.path.exists(input):
        input = os.path.split(input)[0]
    return input


def reveal_dir(input):
    try:
        subprocess.check_output(["/usr/bin/open", input])
        return True
    except subprocess.CalledProcessError:
        return False


def reveal_file(input):
    path = f"\"{input}\" as POSIX file"

    args = (
        "-e", "tell application \"Finder\"",
        "-e", f"reveal {{{path}}}",
        "-e", "activate",
        "-e", "end tell",
        )

    subprocess.call(["osascript", *args])


def reveal(input):
    if os.path.isfile(input):
        reveal_file(input)
        return True

    elif os.path.isdir(input):
        reveal_dir(input)
        return True

    return False
