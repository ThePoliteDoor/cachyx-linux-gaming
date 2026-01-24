import os

from src.block_node import markdown_to_html_node
from src.extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown
    with open(from_path, "r") as f:
        markdown = f.read()

    # Read template
    with open(template_path, "r") as f:
        template = f.read()

    # Convert markdown → HTML
    content_html = markdown_to_html_node(markdown).to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content_html)

    # Apply basepath
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write output
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(content_path):
            if entry.endswith(".md"):
                dest_html = dest_path.replace(".md", ".html")
                generate_page(
                    content_path,
                    template_path,
                    dest_html,
                    basepath,
                )
        else:
            generate_pages_recursive(
                content_path,
                template_path,
                dest_path,
                basepath,
            )
