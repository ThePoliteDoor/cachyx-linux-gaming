import sys


def get_base_path():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not base_path.endswith("/"):
        base_path += "/"
    return base_path
