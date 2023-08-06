from pathlib import Path

__all__ = ["static_dir"]
base = Path(__file__).parent


def get_base_dir():
    return str(base)


def get_js_path(full=False):
    if full:
        return str(base / "js" / "elfinder.full.js")
    else:
        return str(base / "js" / "elfinder.min.js")


def get_html_path():
    return str(base / "elfinder.html")
