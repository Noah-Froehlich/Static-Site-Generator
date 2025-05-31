from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_page(from_path,template_path,dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path,"r")
    md = file.read()
    file.close()
    template_file =  open(template_path,"r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(md)
    html = node.to_html()

    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}",html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    path  = os.path.dirname(dest_path)
    if path != "":
        os.makedirs(path,exist_ok=True)
    dest_file = open(dest_path,"w")
    dest_file.write(template)

def generate_page_recursive(dir_path_content, template_path,dest_dir_path,basepath):
    for file in os.listdir(dir_path_content):
        path_from = os.path.join(dir_path_content,file)
        path_dest = os.path.join(dest_dir_path,file)
        if os.path.isfile(path_from):
            path_dest = Path(path_dest).with_suffix(".html")
            generate_page(path_from, template_path, path_dest,basepath)
        else:
            generate_page_recursive(path_from,template_path,path_dest,basepath)