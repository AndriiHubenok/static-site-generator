from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('Child node must have a tag')
        if not self.children:
            raise ValueError('Child node must have children')

        return f'<{self.tag}>' + ''.join([child.to_html() for child in self.children]) + f'</{self.tag}>'