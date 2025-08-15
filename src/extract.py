from markdownblocks import markdown_to_blocks

def extract_title(markdown):
    for i in markdown_to_blocks(markdown):
        if i.startswith('# '):
            return i.lstrip('# ').strip()
    raise Exception('no header!')