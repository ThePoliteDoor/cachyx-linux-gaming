class HTMLNode:
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
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props}"
            f")"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf nodes must not have children
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        # No tag → raw text
        if self.tag is None:
            return self.value

        # Normal HTML tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # tag and children are required, value is not used
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        html = ""
        for child in self.children:
            html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )
