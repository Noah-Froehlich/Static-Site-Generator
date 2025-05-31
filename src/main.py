from textnode import TextNode,TextType
from copy import copy_static
from website import generate_page,generate_page_recursive
import os

path_public = "./public"
path_static = "./static"
path_content = "./content"
path_template = "./template.html"

def main():

    copy_static(path_public,path_static)

    generate_page_recursive(path_content,path_template,path_public)

main()