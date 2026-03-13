import os
from pathlib import Path
import shutil
import re
from src.textnode import TextNode, TextType, markdown_to_html_node
import sys


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def clean_public_directory():
    os.makedirs("public", exist_ok=True)
    for file in os.listdir("public"):
        if os.path.isdir(os.path.join("public", file)):
            shutil.rmtree(os.path.join("public", file))
        else:  
            os.remove(os.path.join("public", file))


def copy_static_files(directory: str, to_directory: str):
    for file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, file)):
            os.makedirs(os.path.join(to_directory, file), exist_ok=True)
            copy_static_files(os.path.join(directory, file), os.path.join(to_directory, file))
        else:
            shutil.copy(os.path.join(directory, file), os.path.join(to_directory, file))

def extract_title(markdown):
    match = re.findall(r"^# (.*)", markdown.strip())
    if not match:
        raise ValueError("No title found")
    return match[0]


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__ == "__main__":
    main()