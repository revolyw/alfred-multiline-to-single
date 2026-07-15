#!/usr/bin/env python3
"""Alfred Script Filter: multiline text → single line with wrap/separator modes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Mode:
    title: str
    hint: str
    wrap: str
    separator: str


# Default catalog (also used as Workflow Configuration placeholder).
# Format per line: WRAPPER||SEPARATOR||optional title
DEFAULT_CUSTOM_MODES = """\
# WRAPPER||SEPARATOR||optional title
# Leave WRAPPER empty for no quotes. Escapes: \\s = space, \\t = tab, \\\\ = backslash
'||,||Single quotes + comma
"||,||Double quotes + comma
'||,\\s||Single quotes + comma+space
"||,\\s||Double quotes + comma+space
||,||Join with comma
||;||Join with semicolon
||:\\s||Join with colon+space
"""

STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "no_text": "No text available",
        "no_text_sub": "Copy multiline text first, or pass text after the keyword",
        "no_lines": "No valid lines",
        "no_lines_sub": "Input is empty or only blank lines",
        "no_modes": "No modes configured",
        "no_modes_sub": "Add lines in Workflow Configuration → Custom modes",
        "source_query": "query",
        "source_clipboard": "clipboard",
        "lines_unit": "lines",
        "wrap_join": "Wrap with {wrap} and join with {sep}",
        "join_only": "Join with {sep}",
        "auto_title_wrap": "{wrap}…{wrap} + {sep}",
        "auto_title_join": "Join with {sep}",
    },
    "zh": {
        "no_text": "没有可用文本",
        "no_text_sub": "请先复制多行文本到剪贴板，或在关键词后粘贴文本",
        "no_lines": "没有有效行",
        "no_lines_sub": "文本为空或全是空白行",
        "no_modes": "未配置模式",
        "no_modes_sub": "请在 Workflow Configuration → Custom modes 中添加行",
        "source_query": "输入",
        "source_clipboard": "剪贴板",
        "lines_unit": "行",
        "wrap_join": "每行用 {wrap} 包裹，以 {sep} 分隔",
        "join_only": "以 {sep} 分隔（无包裹）",
        "auto_title_wrap": "{wrap}…{wrap} + {sep}",
        "auto_title_join": "分隔符 {sep}",
    },
}


def ui_language() -> str:
    lang = os.environ.get("ui_language", "en").strip().lower()
    return lang if lang in STRINGS else "en"


def t(key: str) -> str:
    lang = ui_language()
    return STRINGS[lang].get(key) or STRINGS["en"][key]


def visible_sep(sep: str) -> str:
    if sep == "":
        return "∅"
    return sep.replace(" ", "␠").replace("\t", "↹")


def unescape(value: str) -> str:
    """Interpret \\s \\t \\n \\\\ and \\| inside WRAPPER/SEPARATOR fields."""
    out: List[str] = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "\\" and i + 1 < len(value):
            nxt = value[i + 1]
            mapping = {
                "s": " ",
                "t": "\t",
                "n": "\n",
                "\\": "\\",
                "|": "|",
            }
            out.append(mapping.get(nxt, nxt))
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def auto_title(wrap: str, separator: str) -> str:
    sep = visible_sep(separator)
    if wrap:
        return t("auto_title_wrap").format(wrap=wrap, sep=sep)
    return t("auto_title_join").format(sep=sep)


def auto_hint(wrap: str, separator: str) -> str:
    sep = visible_sep(separator)
    if wrap:
        return t("wrap_join").format(wrap=wrap, sep=sep)
    return t("join_only").format(sep=sep)


def parse_modes(text: str) -> List[Mode]:
    modes: List[Mode] = []
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p for p in line.split("||")]
        if len(parts) == 1:
            # Allow WRAPPER||SEPARATOR typed with missing trailing parts
            wrap, separator, title = parts[0], "", ""
        elif len(parts) == 2:
            wrap, separator, title = parts[0], parts[1], ""
        else:
            wrap, separator, title = parts[0], parts[1], "||".join(parts[2:]).strip()

        wrap = unescape(wrap)
        separator = unescape(separator)
        title = title.strip()
        if not title:
            title = auto_title(wrap, separator)
        modes.append(Mode(title=title, hint=auto_hint(wrap, separator), wrap=wrap, separator=separator))
    return modes


def configured_modes() -> List[Mode]:
    raw = os.environ.get("custom_modes")
    if raw is None or raw.strip() == "":
        raw = DEFAULT_CUSTOM_MODES
    return parse_modes(raw)


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
    if not wrap:
        return line
    return line.replace("\\", "\\\\").replace(wrap, f"\\{wrap}")


def convert(lines: List[str], wrap: str, separator: str) -> str:
    if wrap:
        return separator.join(f"{wrap}{escape_line(line, wrap)}{wrap}" for line in lines)
    return separator.join(lines)


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
                item(t("no_text"), t("no_text_sub"), "", valid=False)
            ]
        }

    lines = split_lines(text)
    if not lines:
        return {
            "items": [
                item(t("no_lines"), t("no_lines_sub"), "", valid=False)
            ]
        }

    modes = configured_modes()
    if not modes:
        return {
            "items": [
                item(t("no_modes"), t("no_modes_sub"), "", valid=False)
            ]
        }

    items = []
    for mode in modes:
        result = convert(lines, mode.wrap, mode.separator)
        subtitle = (
            f"{mode.hint} · {len(lines)} {t('lines_unit')} · "
            f"{source} · {preview(result)}"
        )
        items.append(item(mode.title, subtitle, result))

    return {"items": items}


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(build_items(query), ensure_ascii=False))


if __name__ == "__main__":
    main()
