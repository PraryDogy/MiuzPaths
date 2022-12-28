import icnsutil
import os


src = '/Users/Loshkarev/Documents/Разное/Projects/files/miuzpaths_icon.png'
name = os.path.split(src)[-1].replace('.png', '.icns')
img = icnsutil.IcnsFile()
img.add_media(file=src)
img.write(f'/Users/Loshkarev/Desktop/{name}')