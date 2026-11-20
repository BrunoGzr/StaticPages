import os
import sys

from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_dir = os.path.join(PROJECT_ROOT, "static")
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    copy_static_to_public(static_dir, docs_dir)

    generate_pages_recursive(
        os.path.join(PROJECT_ROOT, "content"),
        os.path.join(PROJECT_ROOT, "template.html"),
        docs_dir,
        basepath,
    )


if __name__ == "__main__":
    main()
