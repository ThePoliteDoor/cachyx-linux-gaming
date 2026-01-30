import os
import re


def clean_label(name):
    return re.sub(r"^\d+[-_]", "", name).replace("-", " ").title()


def build_sidebar_from_pages(pages, base_path):
    tree = build_tree(pages)
    return render_sidebar(tree, base_path)


def new_node():
    return {"_page": None, "_children": {}}


def build_tree(pages):
    tree = {}

    for page in pages:
        rel = os.path.relpath(page["source_path"], "content")
        parts = rel.split(os.sep)

        # remove index.md
        is_index = parts[-1] == "index.md"
        if is_index:
            parts = parts[:-1]

        node = tree
        for part in parts:
            node = node.setdefault(part, {})

        if is_index:
            node["_page"] = page
        else:
            node.setdefault("_children_pages", []).append(page)

    return tree


def render_sidebar(tree, base_path, is_root=True):
    html = ["<ul>"]

    if is_root:
        html.append(f'<li><a href="{base_path}">Home</a></li>')

    def node_weight(node):
        if "_page" in node and node["_page"]:
            return node["_page"].get("weight", 999)
        for v in node.values():
            if isinstance(v, dict) and v.get("_page"):
                return v["_page"].get("weight", 999)
        return 999

    for key, node in sorted(tree.items(), key=lambda item: node_weight(item[1])):
        if key.startswith("_") or not isinstance(node, dict):
            continue

        page = node.get("_page")
        html.append("<li>")

        if page:
            url = page["url"]

            # internal link → prepend base_path
            if url.startswith("/") and not url.startswith(base_path):
                url = base_path.rstrip("/") + url

            label = page["slug"].replace("-", " ").title()
            html.append(f'<a href="{url}">{label}</a>')
        else:
            # Section label (folder)
            label = clean_label(key)
            html.append(f"<span>{label}</span>")

        children = {
            k: v
            for k, v in node.items()
            if isinstance(v, dict) and not k.startswith("_")
        }

        if children:
            html.append(render_sidebar(children, base_path, is_root=False))

        html.append("</li>")

    html.append("</ul>")
    return "\n".join(html)
