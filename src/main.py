import os
import shutil
from copycontent import copy_content
from generate import generate_pages_recursive

def main():
    source = '/mnt/d/code/StaticSite/static'
    dest = '/mnt/d/code/StaticSite/public'
    print("Deleting public directory...")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print("Copying static files to public directory...")
    copy_content(source, dest)

    content = '/mnt/d/code/StaticSite/content'
    temppath = '/mnt/d/code/StaticSite/template.html'
    generate_pages_recursive(content, temppath, dest)

main()
