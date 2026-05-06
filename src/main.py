import os
import shutil
import sys
from pathlib import Path

from functions import *

def main():
    if not sys.argv[0]:
        basepath = '/'
    else:
        basepath = sys.argv[0]

    copy_content_to_public()
    generate_pages_recursive('./content', './template.html', './docs', basepath)

def copy_content_to_public():
    if os.path.exists('./docs'):
        shutil.rmtree('./docs')
        
    shutil.copytree('./static', './docs')


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(template_path) as template_file:
        template = template_file.read()
    with open(from_path) as from_file:
        content = from_file.read()

    html_string = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_root = Path(dir_path_content)
    dest_root = Path(dest_dir_path)

    for path in content_root.rglob("*.md"):
        rel_path = path.relative_to(content_root)
        dest_path = (dest_root / rel_path).with_suffix(".html")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        generate_page(str(path), template_path, str(dest_path), basepath)

main()

