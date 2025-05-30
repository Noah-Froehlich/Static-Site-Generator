from enum import Enum
# represten inline Text Types
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "Italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
# represent Inline Text fields
class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"