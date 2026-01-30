import os
import re

from src.core.block_node import markdown_to_html_node
from src.data.extract_title import strip_frontmatter


def apply_base_path(html, base_path):
    if base_path == "/":
        return html

    # Fix:
    # href="/..."  → href="{base_path}..."
    # src="/..."   → src="{base_path}..."
    return re.sub(
        r'(href|src)="/(?!/)',
        rf'\1="{base_path}',
        html,
    )


def generate_page(page, template_path, sidebar_html, base_path):
    print(f"Generating page: {page['dest_path']}")

    with open(page["source_path"], "r") as f:
        markdown = f.read()

    clean_markdown = strip_frontmatter(markdown)
    content_html = markdown_to_html_node(clean_markdown).to_html()
    content_html = apply_base_path(content_html, base_path)

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
