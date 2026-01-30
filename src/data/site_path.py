import os

from src.data.extract_title import extract_title
from src.data.helper import parse_ordered_name


def collect_pages(content_root, basepath):
    pages = []

    for root, _, files in os.walk(content_root):
        for file in files:
            if not file.endswith(".md"):
                continue

            source_path = os.path.join(root, file)

            rel_path = os.path.relpath(source_path, content_root)
            parts = rel_path.split(os.sep)

            clean_parts = []
            orders = []

            # folders
            for part in parts[:-1]:
                order, clean = parse_ordered_name(part)
                orders.append(order)
                clean_parts.append(clean)

            # filename
            file_order, clean_file = parse_ordered_name(parts[-1].replace(".md", ""))

            # URL parts
            if clean_file != "index":
                clean_parts.append(clean_file)

            # ---- OUTPUT PATH (derived, not passed in) ----
            dest_path = os.path.join(
                "docs",
                *clean_parts,
                "index.html",
            )

            # ---- URL ----
            url = basepath + "/".join(clean_parts) + "/"

            with open(source_path, "r") as f:
                title = extract_title(f.read())

            section = clean_parts[0] if clean_parts else "Home"

            pages.append(
                {
                    "source_path": source_path,
                    "dest_path": dest_path,
                    "url": url,
                    "title": title,
                    "section": section.replace("-", " ").title(),
                    "is_index": clean_file == "index",
                    "slug": clean_parts[-1] if clean_parts else "home",
                    "weight": min(orders) if orders else 999,
                    "parent": clean_parts[-2] if len(clean_parts) > 1 else None,
                    "depth": len(clean_parts),
                }
            )

    return pages
