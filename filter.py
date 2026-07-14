#!/usr/bin/env python3
"""Alfred Script Filter: multiline text → single line with wrap/separator modes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Dict, List, Tuple


Mode = Tuple[str, str, str, str]  # title_key, hint_key, wrap, separator

MODE_DEFS: List[Mode] = [
    ("mode_sq_comma", "hint_sq_comma", "'", ","),
    ("mode_dq_comma", "hint_dq_comma", '"', ","),
    ("mode_sq_comma_space", "hint_sq_comma_space", "'", ", "),
    ("mode_dq_comma_space", "hint_dq_comma_space", '"', ", "),
]

STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "mode_sq_comma": "Single quotes + comma",
        "mode_dq_comma": "Double quotes + comma",
        "mode_sq_comma_space": "Single quotes + comma+space",
        "mode_dq_comma_space": "Double quotes + comma+space",
        "hint_sq_comma": "Wrap each line with ' and join with ,",
        "hint_dq_comma": 'Wrap each line with " and join with ,',
        "hint_sq_comma_space": "Wrap each line with ' and join with ,␠",
        "hint_dq_comma_space": 'Wrap each line with " and join with ,␠',
        "no_text": "No text available",
        "no_text_sub": "Copy multiline text first, or pass text after the keyword",
        "no_lines": "No valid lines",
        "no_lines_sub": "Input is empty or only blank lines",
        "source_query": "query",
        "source_clipboard": "clipboard",
        "lines_unit": "lines",
    },
    "zh": {
        "mode_sq_comma": "单引号 + 逗号",
        "mode_dq_comma": "双引号 + 逗号",
        "mode_sq_comma_space": "单引号 + 逗号空格",
        "mode_dq_comma_space": "双引号 + 逗号空格",
        "hint_sq_comma": "每行用 ' 包裹，以 , 分隔",
        "hint_dq_comma": '每行用 " 包裹，以 , 分隔',
        "hint_sq_comma_space": "每行用 ' 包裹，以 ,␠ 分隔",
        "hint_dq_comma_space": '每行用 " 包裹，以 ,␠ 分隔',
        "no_text": "没有可用文本",
        "no_text_sub": "请先复制多行文本到剪贴板，或在关键词后粘贴文本",
        "no_lines": "没有有效行",
        "no_lines_sub": "文本为空或全是空白行",
        "source_query": "输入",
        "source_clipboard": "剪贴板",
        "lines_unit": "行",
    },
}


def ui_language() -> str:
    lang = os.environ.get("ui_language", "en").strip().lower()
    return lang if lang in STRINGS else "en"


def t(key: str) -> str:
    lang = ui_language()
    return STRINGS[lang].get(key) or STRINGS["en"][key]


def default_mode_id() -> str:
    value = os.environ.get("default_mode", "sq_comma").strip()
    allowed = {
        "sq_comma": "mode_sq_comma",
        "dq_comma": "mode_dq_comma",
        "sq_comma_space": "mode_sq_comma_space",
        "dq_comma_space": "mode_dq_comma_space",
    }
    return allowed.get(value, "mode_sq_comma")


def ordered_modes() -> List[Mode]:
    preferred = default_mode_id()
    preferred_modes = [m for m in MODE_DEFS if m[0] == preferred]
    others = [m for m in MODE_DEFS if m[0] != preferred]
    return preferred_modes + others


def read_clipboard() -> str:
    try:
        return subprocess.check_output(["pbpaste"], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_input_text(query: str) -> Tuple[str, str]:
    """Return (text, source_label). Prefer non-empty Alfred query, else clipboard."""
    if query.strip():
        return query, t("source_query")
    clip = read_clipboard()
    if clip.strip():
        return clip, t("source_clipboard")
    return "", ""


def split_lines(text: str) -> List[str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return [line for line in lines if line.strip() != ""]


def escape_line(line: str, wrap: str) -> str:
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
                    t("no_text"),
                    t("no_text_sub"),
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
                    t("no_lines"),
                    t("no_lines_sub"),
                    "",
                    valid=False,
                )
            ]
        }

    items = []
    for title_key, hint_key, wrap, separator in ordered_modes():
        result = convert(lines, wrap, separator)
        subtitle = (
            f"{t(hint_key)} · {len(lines)} {t('lines_unit')} · "
            f"{source} · {preview(result)}"
        )
        items.append(item(t(title_key), subtitle, result))

    return {"items": items}


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(build_items(query), ensure_ascii=False))


if __name__ == "__main__":
    main()
