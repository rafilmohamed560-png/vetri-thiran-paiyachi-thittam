from __future__ import annotations

import html
import re


def sanitize_text(text: str) -> str:
    """Normalize common typographic characters and remove unsafe control chars."""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
        "\u2026": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.strip()


def format_html_preview(text: str) -> str:
    safe = html.escape(sanitize_text(text))
    blocks = []
    for paragraph in re.split(r"\n\s*\n", safe):
        if not paragraph.strip():
            continue
        lines = paragraph.splitlines()
        if len(lines) == 1 and (
            lines[0].isupper()
            or re.match(r"^\d+(?:\.\d+)*\.?\s+", lines[0])
        ):
            blocks.append(f"<h3>{lines[0]}</h3>")
        else:
            blocks.append(f"<p>{'<br>'.join(lines)}</p>")
    return "\n".join(blocks)
