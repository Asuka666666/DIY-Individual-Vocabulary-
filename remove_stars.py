from __future__ import annotations

import argparse
from pathlib import Path


def remove_stars_in_details(html_text: str) -> str:
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html_text, "html.parser")

    for details in soup.find_all("details"):
        for text_node in details.find_all(string=True):
            if not isinstance(text_node, NavigableString):
                continue
            if "*" in text_node:
                text_node.replace_with(text_node.replace("*", ""))

    return str(soup)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove '*' characters inside all <details> elements."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(Path(__file__).with_name("不熟单词.html")),
        help="Path to the input HTML file (default: 不熟单词.html next to this script).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path. If omitted, the input file is overwritten.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    html_text = input_path.read_text(encoding="utf-8")
    updated_text = remove_stars_in_details(html_text)

    output_path = Path(args.output) if args.output else input_path
    output_path.write_text(updated_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
