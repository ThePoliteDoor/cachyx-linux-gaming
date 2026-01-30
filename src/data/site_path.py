import os

from src.data.extract_title import extract_title
from src.data.helper import parse_ordered_name


def collect_pages(content_root, output_root, basepath):
    pages = []

    for root, _, files in os.walk(content_root):
        for file in files:
            if not file.endswith(".md"):
                continue

            source_path = os.path.join(root, file)

            rel_path = os.path.relpath(source_path, content_root)
            parts = rel_path.split(os.sep)

            # --- NEW: parse ordered folders ---
            clean_parts = []
            orders = []

            for part in parts[:-1]:  # folders only
                order, clean = parse_ordered_name(part)
                orders.append(order)
                clean_parts.append(clean)

            # file name (index.md)
            file_order, clean_file = parse_ordered_name(parts[-1].replace(".md", ""))

            # --- paths ---
            rel_html = "/".join(clean_parts + [clean_file + ".html"])
            dest_path = os.path.join(output_root, rel_html)

            url = basepath + "/".join(clean_parts) + "/"

            # Extract title
            with open(source_path, "r") as f:
                title = extract_title(f.read())

            # Section = top-level clean folder
            section = clean_parts[0] if clean_parts else "Home"

            is_index = clean_file == "index"
            slug = clean_parts[-1] if clean_parts else "home"

            pages.append(
                {
                    "source_path": source_path,
                    "dest_path": dest_path,
                    "url": url,
                    "title": title,
                    "section": section.replace("-", " ").title(),
                    "is_index": is_index,
                    "slug": slug,
                    "weight": min(orders) if orders else 999,
                    "parent": clean_parts[-2] if len(clean_parts) > 1 else None,
                    "depth": len(clean_parts),
                }
            )

    return pages
