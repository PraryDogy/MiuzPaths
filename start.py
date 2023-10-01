import traceback
import os

try:
    import cfg
    from gui import InitGui

    cfg.ROOT.after(1, InitGui)
    cfg.ROOT.mainloop()


except Exception as ee:

    APP_NAME = 'MiuzPaths'
    CFG_DIR = os.path.join(
        os.path.expanduser('~'), f'Library/Application Support/{APP_NAME}')

    if not os.path.exists(CFG_DIR):
        os.mkdir(CFG_DIR)

    if not os.path.exists(os.path.join(CFG_DIR, 'err.txt')):
        with open(os.path.join(CFG_DIR, 'err.txt'), 'w') as err_file:
            pass

    with open(os.path.join(CFG_DIR, 'err.txt'), 'r') as err_file:
        data = err_file.read()

    data = f'{data}\n\n{traceback.format_exc()}'

    with open(os.path.join(CFG_DIR, 'err.txt'), 'w') as err_file:
        print(data, file=err_file)

    print(data)