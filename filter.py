#!/usr/bin/env python3
"""Alfred Script Filter: multiline text → single line with wrap/separator modes."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import List, Tuple


MODES: List[Tuple[str, str, str, str]] = [
    # title, subtitle_hint, wrap, separator
    ("单引号 + 逗号", "每行用 ' 包裹，以 , 分隔", "'", ","),
    ("双引号 + 逗号", '每行用 " 包裹，以 , 分隔', '"', ","),
    ("单引号 + 逗号空格", "每行用 ' 包裹，以 ,␠ 分隔", "'", ", "),
    ("双引号 + 逗号空格", '每行用 " 包裹，以 ,␠ 分隔', '"', ", "),
]


def read_clipboard() -> str:
    try:
        return subprocess.check_output(["pbpaste"], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_input_text(query: str) -> Tuple[str, str]:
    """Return (text, source_label). Prefer non-empty Alfred query, else clipboard."""
    if query.strip():
        return query, "输入"
    clip = read_clipboard()
    if clip.strip():
        return clip, "剪贴板"
    return "", ""


def split_lines(text: str) -> List[str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # 去掉首尾空行，保留中间空行会显得奇怪，统一丢弃纯空白行
    return [line for line in lines if line.strip() != ""]


def escape_line(line: str, wrap: str) -> str:
    # 先转义反斜杠，再转义包裹符，便于粘贴到代码/SQL 等场景
    return line.replace("\\", "\\\\").replace(wrap, f"\\{wrap}")


def convert(lines: List[str], wrap: str, separator: str) -> str:
    return separator.join(f"{wrap}{escape_line(line, wrap)}{wrap}" for line in lines)


def preview(text: str, limit: int = 120) -> str:
    one = text.replace("\n", "⏎")
    if len(one) <= limit:
        return one
    return one[: limit - 1] + "…"


def item(
    title: str,
    subtitle: str,
    arg: str,
    valid: bool = True,
) -> dict:
    return {
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": valid,
        "text": {"copy": arg, "largetype": arg},
    }


def build_items(query: str) -> dict:
    text, source = get_input_text(query)
    if not text.strip():
        return {
            "items": [
                item(
                    "没有可用文本",
                    "请先复制多行文本到剪贴板，或在关键词后粘贴文本",
                    "",
                    valid=False,
                )
            ]
        }

    lines = split_lines(text)
    if not lines:
        return {
            "items": [
                item(
                    "没有有效行",
                    "文本为空或全是空白行",
                    "",
                    valid=False,
                )
            ]
        }

    items = []
    for title, hint, wrap, separator in MODES:
        result = convert(lines, wrap, separator)
        subtitle = f"{hint} · {len(lines)} 行 · 来自{source} · {preview(result)}"
        items.append(item(title, subtitle, result))

    return {"items": items}


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(build_items(query), ensure_ascii=False))


if __name__ == "__main__":
    main()
