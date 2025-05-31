from textnode import TextNode,TextType
from copy import copy_static
from website import generate_page,generate_page_recursive
import os
import sys

path_public = "./docs"
path_static = "./static"
path_content = "./content"
path_template = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static(path_public,path_static)

    generate_page_recursive(path_content,path_template,path_public,basepath)

main()