#!/usr/bin/env python3
"""Unit tests for filter.py (no Alfred / clipboard required)."""

from __future__ import annotations

import json
import os
import unittest
from unittest import mock

import filter as m


class SplitLinesTests(unittest.TestCase):
    def test_skips_blank_lines(self) -> None:
        text = "\n a \n\n\tb\n\n"
        self.assertEqual(m.split_lines(text), [" a ", "\tb"])

    def test_normalizes_crlf(self) -> None:
        self.assertEqual(m.split_lines("a\r\nb\rc"), ["a", "b", "c"])


class ConvertTests(unittest.TestCase):
    def test_single_quote_comma(self) -> None:
        self.assertEqual(
            m.convert(["apple", "banana"], "'", ","),
            "'apple','banana'",
        )

    def test_no_wrap(self) -> None:
        self.assertEqual(m.convert(["a", "b"], "", ";"), "a;b")
        self.assertEqual(m.convert(["a", "b"], "", ", "), "a, b")

    def test_escapes_wrap_and_backslash(self) -> None:
        self.assertEqual(m.convert(["a'b"], "'", ","), r"'a\'b'")
        self.assertEqual(m.convert(['a"b'], '"', ","), r'"a\"b"')
        self.assertEqual(m.convert([r"a\b"], "'", ","), r"'a\\b'")


class ParseModesTests(unittest.TestCase):
    def test_parse_with_title_and_escape(self) -> None:
        text = "'||,\\s||Nice\n||;||Semi\n# comment\n"
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            modes = m.parse_modes(text)
        self.assertEqual(len(modes), 2)
        self.assertEqual(modes[0].wrap, "'")
        self.assertEqual(modes[0].separator, ", ")
        self.assertEqual(modes[0].title, "Nice")
        self.assertEqual(modes[1].wrap, "")
        self.assertEqual(modes[1].separator, ";")
        self.assertEqual(modes[1].title, "Semi")

    def test_auto_title(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            modes = m.parse_modes("||:")
        self.assertEqual(modes[0].title, "Join with :")


class BuildItemsTests(unittest.TestCase):
    def test_default_modes_include_join_only(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}, clear=False):
            os.environ.pop("custom_modes", None)
            payload = m.build_items("x\ny")
        args = [i["arg"] for i in payload["items"]]
        self.assertIn("'x','y'", args)
        self.assertIn('"x","y"', args)
        self.assertIn("x,y", args)
        self.assertIn("x;y", args)
        self.assertIn("x: y", args)

    def test_custom_modes_override(self) -> None:
        custom = "||-||dash join\n'||.||dotted quotes"
        with mock.patch.dict(
            os.environ,
            {"ui_language": "en", "custom_modes": custom},
        ):
            payload = m.build_items("a\nb")
        self.assertEqual(len(payload["items"]), 2)
        self.assertEqual(payload["items"][0]["arg"], "a-b")
        self.assertEqual(payload["items"][0]["title"], "dash join")
        self.assertEqual(payload["items"][1]["arg"], "'a'.'b'")

    def test_empty_shows_invalid_item(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            with mock.patch.object(m, "read_clipboard", return_value=""):
                payload = m.build_items("")
        self.assertEqual(len(payload["items"]), 1)
        self.assertFalse(payload["items"][0]["valid"])
        self.assertEqual(payload["items"][0]["title"], "No text available")

    def test_clipboard_fallback(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "zh"}):
            os.environ.pop("custom_modes", None)
            with mock.patch.object(m, "read_clipboard", return_value="one\ntwo"):
                payload = m.build_items("   ")
        self.assertEqual(payload["items"][0]["arg"], "'one','two'")
        self.assertIn("剪贴板", payload["items"][0]["subtitle"])

    def test_main_prints_json(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            os.environ.pop("custom_modes", None)
            with mock.patch.object(m.sys, "argv", ["filter.py", "a\nb"]):
                with mock.patch("builtins.print") as printed:
                    m.main()
        raw = printed.call_args[0][0]
        data = json.loads(raw)
        self.assertEqual(data["items"][0]["arg"], "'a','b'")


if __name__ == "__main__":
    unittest.main()
