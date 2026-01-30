def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found in markdown")


def strip_frontmatter(markdown):
    if markdown.startswith("---"):
        parts = markdown.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return markdown
