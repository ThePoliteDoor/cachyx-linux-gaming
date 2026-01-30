import re

ORDER_RE = re.compile(r"^(\d+)[-_](.+)$")


def parse_ordered_name(name):
    """
    Returns (order, clean_name)
    """
    m = ORDER_RE.match(name)
    if m:
        return int(m.group(1)), m.group(2)
    return 999, name
