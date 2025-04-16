from textnode import TextNode, TextType
from block import markdown_to_html_node
import os
import shutil
import sys

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    os.mkdir(dest_dir)

    # Recrusive copy of all files and directories
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            os.mkdir(dest_path)
            copy_static(source_path, dest_path)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/index.css', f'href="{basepath}static/index.css')
    full_html = full_html.replace('src="/images/', f'src="{basepath}static/images/')
    full_html = full_html.replace('href="/blog/', f'href="{basepath}blog/')
    full_html = full_html.replace('href="/contact', f'href="{basepath}contact')
    full_html = full_html.replace('href="/"', f'href="{basepath}"')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):  # Handle the single file case
        if dir_path_content.endswith(".md"):
            file_name = os.path.basename(dir_path_content)
            dest_file_path = os.path.join(dest_dir_path, file_name.replace(".md", ".html"))

            os.makedirs(dest_dir_path, exist_ok=True)

            generate_page(dir_path_content, template_path, dest_file_path, basepath)
        return

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        if os.path.isfile(item_path):  # Process markdown files
            if item_path.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
                os.makedirs(dest_dir_path, exist_ok=True)
                generate_page(item_path, template_path, dest_path, basepath)

        elif os.path.isdir(item_path):  # Recurse into subdirectories
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_dir_path, basepath)

    


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    content_path = "content"
    template_path = "template.html"
    output_path = "docs"
    print(f"Basepath is set to: {basepath}")
    print(f"Generating static site...")
    generate_pages_recursive(content_path, template_path, output_path, basepath)
    print(f"Site generated successfully in the '{output_path}' directory!")


if __name__ == "__main__":
    main()
