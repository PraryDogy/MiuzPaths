import subprocess


def OpenPath(pathMac):
    # OpenPath return dict ([dir], [is_full], [error]) and open path (mac os subprocess command)
    # if path is right, dict[is_full] = True
    # if path is right partially. dict[is_full] = False, dict[dir]=only right part of path, dict[eror] = part of path with error
    # call this function on ConvertPath return dict only

    try:
        subprocess.check_output(["/usr/bin/open", pathMac])
        return {'dir': pathMac, 'is_full': True}

    except subprocess.CalledProcessError:
        splited = pathMac.split('/')
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
                return {'dir': new_path, 'is_full': False, 'error': pathMac.replace(new_path, '')}

            except subprocess.CalledProcessError:
                pass
