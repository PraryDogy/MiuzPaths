import os
import re
import subprocess
import tkinter

import cfg


def copy(output: str):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def paste():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


def detectPath(from_clipboard: str):
    '''
    return 'isMac' if mac path to Miuz network (with 'Shares' or 'Marketing') folders\n
    return 'isLocal' if local mac path\n
    retutn 'isWin' if windows path\n
    '''
    winRegex = r'\\(?:.+\\).{,10}'
    if re.findall(winRegex, from_clipboard):
        return 'isWin'
    
    macRegex = r'/(?:.+/).{,10}'
    if re.findall(macRegex, from_clipboard):
    
        for word in ['shares', 'Shares', 'marketing', 'Marketing']:
            if word in from_clipboard:
                return 'isMac'
        return 'isLocal'

    return False


def toWin(from_clipboard: str):
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


def toMac(from_clipboard: str):
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


def existsPath(path_mac: str):
    '''
    {fullPath}, {shortPath}
    '''
    isFile = os.path.isfile(path_mac)
    
    if isFile:
        listPath = path_mac.split('/')[:-1]
    else:
        listPath = path_mac.split('/')
        
    allPaths = list()
    for i in reversed(range(1, len(listPath)+1)):

        shortPath = listPath[:i]
        strPath = os.path.join('/', *shortPath)
        allPaths.append(strPath)
        

    for i in allPaths:
        if os.path.exists(i):
            return {'fullPath': allPaths[0], 'shortPath': i}
        
    return False


# def openPath(path_mac: str):
#     try:
#         subprocess.check_output(["/usr/bin/open", path_mac])
#     except Exception:
#         print(traceback.format_exc())


def open_path(path_mac: str):
    # OpenPath return dict ([dir], [is_full], [error]) and open path (mac os subprocess command)
    # if path is right, dict[is_full] = True
    # if path is right partially. dict[is_full] = False, dict[dir]=only right part of path, dict[eror] = part of path with error
    # call this function on ConvertPath return dict only

    try:
        subprocess.check_output(["/usr/bin/open", path_mac])
        return {'dir': path_mac, 'is_full': True}

    except subprocess.CalledProcessError:
        splited = path_mac.split('/')
        dirlen = len(splited)
        
        while dirlen != 0:
            # searching directory, which function can open
            # sample: 
            # user/mister/desktop/1/ (1 folder not found)
            # try open user/mister/desktop (if desktop folder not found )
            # try open user/mister (found)
            new_path = '/'.join(splited[:dirlen])
            dirlen -= 1

            try:
                subprocess.check_output(["/usr/bin/open", new_path])
                return {'dir': new_path, 'is_full': False, 'error': path_mac.replace(new_path, '')}

            except subprocess.CalledProcessError:
                pass


def display(root: tkinter.Tk, text: str):
    '''
    Insert text in text widget
    '''
    # root > frame with text widget for showing text(top pack), frame with buttons: open, convert(bottom pack)
    # get label with text from root
    f1 = root.winfo_children()[0]
    textbox = f1.winfo_children()[0]

    # unlock textwidget
    textbox.configure(state='normal')
    
    # remove prev and paste new text
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', text)

    # lock textwidget
    textbox.configure(state='disabled')
    