

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        string = ''
        if not self.props or len(self.props) == 0:
            return string

        for prop in self.props:
            string += f'{prop}="{self.props[prop]}" '
        return string[:-1]

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

