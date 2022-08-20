import os
import re


def detectPath(fromClipboard):
    '''
    return 'isMac' if mac path to Miuz network (with 'Shares' or 'Marketing') folders\n
    return 'isLocal' if local mac path\n
    retutn 'isWin' if windows path\n
    '''

    winRegex = r'\\(?:.+\\).{,10}'
    if re.findall(winRegex, fromClipboard):
        return 'isWin'
    
    macRegex = r'/(?:.+/).{,10}'
    if re.findall(macRegex, fromClipboard):
    
        for word in ['shares', 'Shares', 'marketing', 'Marketing']:
            if word in fromClipboard:
                return 'isMac'
        return 'isLocal'

    return False


def toWin(fromClipboard):
    tmp = fromClipboard.casefold().split('/')

    if 'shares' in tmp:
        sharesIndex = tmp.index('shares')
        splited = fromClipboard.split('/')[sharesIndex:]
        networkMiuz = '192.168.10.105'
        return '\\'.join(['smb:']+[networkMiuz]+splited)

    if 'marketing' in tmp:
        marketingIndex = tmp.index('marketing')
        splited = fromClipboard.split('/')[marketingIndex:]
        networkMiuz = '192.168.10.105'
        return '\\'.join(['smb:']+[networkMiuz]+['Shares']+splited)

    return False

def toMac(fromClipboard):
    tmp = fromClipboard.casefold().split('\\')

    if 'shares' in tmp:
        sharesIndex = tmp.index('shares')
        pathList = fromClipboard.split('\\')[sharesIndex:]
        return os.path.join(os.path.sep, 'Volumes', *pathList)
        
    if 'marketing' in tmp:
        marketingIndex = tmp.index('marketing')
        pathList = fromClipboard.split('\\')[marketingIndex:]
        return os.path.join(os.path.sep, 'Volumes', 'Shares', *pathList)
    
    return False
