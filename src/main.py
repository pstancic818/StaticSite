from textnode import TextNode, TextType
from htmlnode import HTMLNode
from markdownblocks import markdown_to_blocks, markdown_to_html_node

def main():
    a = """
# Countries

- Slovenia
- Croatia
- Serbia
- Montenegro
- Bosnia

## Song

1. here comes the
2. to the
3. to the
4. something something floor
"""
    b = markdown_to_html_node(a)
    print(repr(b.to_html()))

main()

        #tmp = []
        #for i in range(len(tmp1)):
        #    if i == len(tmp1)-1:
        #        tmp.append(tmp1[i])
        #    else:
        #        tmp.append(tmp1[i] + '\n')

        #tmp = []
        #for i in range(len(tmp1)):
        #    if i == len(tmp1)-1:
        #        tmp.append(tmp1[i])
        #    else:
        #        tmp.append(tmp1[i] + '\n')
        