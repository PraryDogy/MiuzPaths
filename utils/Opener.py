import os
import subprocess
import traceback


def existsPath(pathMac):
    '''
    {fullPath}, {shortPath}
    '''
    isFile = os.path.isfile(pathMac)
    
    if isFile:
        listPath = pathMac.split('/')[:-1]
    else:
        listPath = pathMac.split('/')
        
    allPaths = list()
    for i in reversed(range(1, len(listPath)+1)):

        shortPath = listPath[:i]
        strPath = os.path.join('/', *shortPath)
        allPaths.append(strPath)
        

    for i in allPaths:
        if os.path.exists(i):
            return {'fullPath': allPaths[0], 'shortPath': i}
        
    return False


def openPath(pathMac):
    try:
        subprocess.check_output(["/usr/bin/open", pathMac])
    except Exception:
        print(traceback.format_exc())
