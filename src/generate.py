from markdownblocks import markdown_to_html_node
from extract import extract_title
import os

def generate_page(frompath, temppath, topath):
    print(f'Generating page from {frompath} to {topath} using {temppath}')
    fromfile = ''
    with open(frompath, 'r') as file:
        fromfile += file.read()
    tempfile = ''
    with open(temppath, 'r') as file:
        tempfile += file.read()
    node = markdown_to_html_node(fromfile)
    html = node.to_html()
    extract = extract_title(fromfile)
    tempfile = tempfile.replace('{{ Title }}', extract)
    tempfile = tempfile.replace('{{ Content }}', html)
    if not os.path.exists(topath):
        os.makedirs(topath)
    with open(topath + '/index.html', 'w') as w:
        print(tempfile, file=w)
    
def generate_pages_recursive(content_path, temppath, topath):
    for i in os.listdir(content_path):
        if os.path.isdir(os.path.join(content_path, i)):
            generate_pages_recursive(os.path.join(content_path, i), temppath, os.path.join(topath, i))
        elif os.path.isfile(os.path.join(content_path, i)):
            generate_page(os.path.join(content_path, i), temppath, topath)
        else:
            raise ValueError(f'path {os.path.join(content_path, i)} does not exist')