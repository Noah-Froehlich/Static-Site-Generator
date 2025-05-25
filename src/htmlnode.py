
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_text = ""
        for i in self.props:
            temp = self.props[i]
            text = f' {i}="{temp}"'
            html_text += text
        return html_text
    
    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildern: {self.children}\nprops: {self.props}"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParrentNode(HTMLNode):
    def __init__(self, tag, children,props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Missing Tag")
        if not self.children:
            raise ValueError("Missing Children")
        html_text =""
        for node in self.children:
            html_text += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_text}</{self.tag}>"