import os

from src.core.block_node import markdown_to_html_node
from src.data.extract_title import strip_frontmatter


def generate_page(page, template_path, sidebar_html, base_path):
    print(f"Generating page: {page['dest_path']}")

    with open(page["source_path"], "r") as f:
        markdown = f.read()

    clean_markdown = strip_frontmatter(markdown)
    content_html = markdown_to_html_node(clean_markdown).to_html()

    with open(template_path, "r") as f:
        template = f.read()

    html = (
        template.replace("{{ Title }}", page["title"])
        .replace("{{ Content }}", content_html)
        .replace("{{ Sidebar }}", sidebar_html)
        .replace("{{ BasePath }}", base_path)
    )

    os.makedirs(os.path.dirname(page["dest_path"]), exist_ok=True)

    with open(page["dest_path"], "w") as f:
        f.write(html)
