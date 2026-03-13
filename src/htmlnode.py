class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list['HTMLNode'] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ""
        if self.props:
            for key, value in self.props.items():
                html += f"{key}=\"{value}\" "
        return html.strip()

    def __repr__(self):
        html = f""

        if self.tag:
            html += f"<{self.tag} {self.props_to_html()}>"
        else:
            return "HTMLNode('')"

        if self.value:
            html += f"{self.value} "

        if self.children:
            for child in self.children:
                html += f"{child.to_html()} "

        html += f" </{self.tag}>"

        return f"HTMLNode({html})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.tag:
            return self.value
        
        html = f"<{self.tag}"
        if self.props:
            for key, value in self.props.items():
                html += f" {key}=\"{value}\""
        html += f">{self.value}</{self.tag}>"
        return html

    def __repr__(self):
        return f"LeafNode({self.to_html()})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")

        if not self.children:
            raise ValueError("Children are required")

        html = f"<{self.tag}"
        if self.props:
            for key, value in self.props.items():
                html += f" {key}=\"{value}\""
        html += f">"
        for child in self.children:
            html += f"{child.to_html()}"

        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return f"ParentNode({self.to_html()})"
