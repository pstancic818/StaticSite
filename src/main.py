import os
import shutil
import sys
from copycontent import copy_content
from generate import generate_pages_recursive

def main():
    if not sys.argv[1]:
        basepath = '/'
    else:
        basepath = sys.argv[1]
    source = '/mnt/d/code/StaticSite/static'
    dest = '/mnt/d/code/StaticSite/docs'
    print("Deleting public directory...")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print("Copying static files to public directory...")
    copy_content(source, dest)

    content = '/mnt/d/code/StaticSite/content'
    temppath = '/mnt/d/code/StaticSite/template.html'
    generate_pages_recursive(content, temppath, dest, basepath)

main()
