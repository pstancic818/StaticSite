import os
import shutil

base = '/mnt/d/code/StaticSite'
shutil.rmtree(base + '/public')
os.mkdir(base + '/public')
os.mkdir(base + '/public/images')
for i in os.listdir(base + '/static'):
    if i.endswith('png'):
        shutil.copy(i, base + '/public/images')
    else:
        shutil.copy(i, base + '/public')