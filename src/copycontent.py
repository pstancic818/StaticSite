import os
import shutil

def copy_content(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    print(f'copying contents of {source} to {destination}')
    for i in os.listdir(source):
        frompath = os.path.join(source, i)
        topath = os.path.join(destination, i)
        print(f'Copying {frompath} -> {topath}')
        if os.path.isfile(frompath):
            shutil.copy(frompath, topath)
        else:
            copy_content(frompath, topath)