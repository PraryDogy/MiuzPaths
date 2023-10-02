path = "/Users/Loshkarev/Downloads/2022_MIUZ_Premium11576_1 1x1.jpg"
path = "smb://192.168.10.105/Shares/Marketing/Photo/2023/MUIZ paper bg.psd"



# script = f"""
#         set thePath to POSIX file "{path}"
#         tell application "Finder" to reveal thePath
#         tell application "Finder" to activate
#         """


# from utils import run_applescript

# run_applescript(script)

import re

reg = r"smb://.{,100}/.{,100}"
a = re.findall(reg, path)

print(a)