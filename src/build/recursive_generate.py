from src.build.generate_page import generate_page


def generate_pages_recursive(pages, template_path, sidebar_html, index=0):
    if index >= len(pages):
        return

    generate_page(pages[index], template_path, sidebar_html)
    generate_pages_recursive(pages, template_path, sidebar_html, index + 1)
