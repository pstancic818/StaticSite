class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        newstr = ''
        for i in self.props:
            newstr += f' {i}="{self.props[i]}"'
        return newstr
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        #print(f'DEBUG: tag: {self.tag}, value: {self.value}, props: {self.props}')
        if not self.tag:
            return self.value
        if self.tag in ('img', 'br', 'hr', 'input', 'meta', 'link'):
            return f'<{self.tag} {self.props_to_html()} />'
        if not self.value:
            raise ValueError("invalid HTML: no value")
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("no children detected")
        rstring = ''
        for i in self.children:
            rstring += i.to_html()
        return f'<{self.tag}>{rstring}</{self.tag}>'
    
    def __repr__(self):
        return super().__repr__()