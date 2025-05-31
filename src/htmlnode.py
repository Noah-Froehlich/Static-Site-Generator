

#represent a HtmlNode can be inline or box 
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    #returns a String of the props for html
    def props_to_html(self):
        if self.props == None:
            return ""
        text = ""
        for i in self.props:
            temp = self.props[i]
            text += f' {i}="{temp}"'
        return text
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    #represent a inline node of text like bold or Italic
class LeafNode(HTMLNode):
    def __init__(self, tag,value,props=None):
        super().__init__(tag, value, None, props)
    
    #creates a html inline block with the tags
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParrentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No Tag")
        if self.children == None:
            raise ValueError("No Children")
        text = ""
        for child in self.children:
            text += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"