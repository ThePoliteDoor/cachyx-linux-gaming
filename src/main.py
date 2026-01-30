import sys

from src.build.generate_sidebar import (
    build_sidebar_from_pages,
)
from src.build.generate_static import copy_directory_recursive
from src.build.recursive_generate import generate_pages_recursive
from src.data.site_path import collect_pages


def main():
    # Basepath from CLI
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    CONTENT = "content"
    OUTPUT = "docs"
    TEMPLATE = "template.html"

    # 1. Copy static assets
    copy_directory_recursive("static", OUTPUT)

    # 2. Collect ALL pages (single source of truth)
    pages = collect_pages(CONTENT, OUTPUT, basepath)

    # 3. Build sidebar from pages
    sidebar_html = build_sidebar_from_pages(pages)

    # 4. Generate pages (render only)
    generate_pages_recursive(pages, TEMPLATE, sidebar_html)


if __name__ == "__main__":
    main()
