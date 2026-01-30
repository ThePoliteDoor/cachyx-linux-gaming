import os
import re


def clean_label(name):
    return re.sub(r"^\d+[-_]", "", name).replace("-", " ").title()


def build_sidebar_from_pages(pages):
    tree = build_tree(pages)
    return render_sidebar(tree)


def new_node():
    return {"_page": None, "_children": {}}


def build_tree(pages):
    tree = {}

    for page in pages:
        if not page["is_index"]:
            continue

        # e.g. guides/battlenet/index.md → ["guides", "battlenet"]
        rel = os.path.relpath(page["source_path"], "content")
        parts = rel.split(os.sep)[:-1]

        node = tree
        for part in parts:
            node = node.setdefault(part, {})

        node["_page"] = page

    return tree


def render_sidebar(tree, is_root=True):
    html = ["<ul>"]

    if is_root:
        html.append('<li><a href="/">Home</a></li>')

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
            html.append(
                f'<a href="{page["url"]}">{page["slug"].replace("-", " ").title()}</a>'
            )
        else:
            # Section label = cleaned folder name
            label = clean_label(key)
            html.append(f"<span>{label}</span>")

        children = {
            k: v
            for k, v in node.items()
            if isinstance(v, dict) and not k.startswith("_")
        }
        if children:
            html.append(render_sidebar(children, is_root=False))

        html.append("</li>")

    html.append("</ul>")
    return "\n".join(html)
