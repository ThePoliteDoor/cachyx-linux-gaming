from src.build.config import get_base_path
from src.build.generate_sidebar import build_sidebar_from_pages
from src.build.generate_static import copy_directory_recursive
from src.build.recursive_generate import generate_pages_recursive
from src.data.site_path import collect_pages

base_path = get_base_path()


def main():
    CONTENT = "content"
    OUTPUT = "docs"
    TEMPLATE = "template.html"

    # 1. Copy static assets
    copy_directory_recursive("static", OUTPUT)

    # 2. Collect ALL pages (single source of truth)
    pages = collect_pages(CONTENT, base_path)

    # 3. Build sidebar from pages
    sidebar_html = build_sidebar_from_pages(pages, base_path)

    # 4. Generate pages (render only)
    generate_pages_recursive(pages, TEMPLATE, sidebar_html, base_path)


if __name__ == "__main__":
    main()
