import sys

from src.generate_page import generate_pages_recursive
from src.generate_static import copy_directory_recursive


def main():
    # Get basepath from CLI args
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    # Copy static → docs
    output_dir = "docs"
    copy_directory_recursive("static", output_dir)

    # Generate index page
    generate_pages_recursive(
        "content",
        "template.html",
        output_dir,
        basepath,
    )


if __name__ == "__main__":
    main()
