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

    def test_double_quote_comma_space(self) -> None:
        self.assertEqual(
            m.convert(["apple", "banana"], '"', ", "),
            '"apple", "banana"',
        )

    def test_escapes_wrap_and_backslash(self) -> None:
        self.assertEqual(m.convert(["a'b"], "'", ","), r"'a\'b'")
        self.assertEqual(m.convert(['a"b'], '"', ","), r'"a\"b"')
        self.assertEqual(m.convert([r"a\b"], "'", ","), r"'a\\b'")


class BuildItemsTests(unittest.TestCase):
    def test_modes_from_query_english(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en", "default_mode": "sq_comma"}):
            payload = m.build_items("x\ny")
        self.assertEqual(len(payload["items"]), 4)
        self.assertEqual(payload["items"][0]["title"], "Single quotes + comma")
        self.assertEqual(payload["items"][0]["arg"], "'x','y'")
        self.assertEqual(payload["items"][1]["arg"], '"x","y"')
        self.assertTrue(payload["items"][0]["valid"])

    def test_chinese_ui(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "zh"}):
            payload = m.build_items("x\ny")
        self.assertEqual(payload["items"][0]["title"], "单引号 + 逗号")

    def test_default_mode_reorders(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en", "default_mode": "dq_comma"}):
            payload = m.build_items("x\ny")
        self.assertEqual(payload["items"][0]["arg"], '"x","y"')
        self.assertEqual(payload["items"][0]["title"], "Double quotes + comma")

    def test_empty_shows_invalid_item(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            with mock.patch.object(m, "read_clipboard", return_value=""):
                payload = m.build_items("")
        self.assertEqual(len(payload["items"]), 1)
        self.assertFalse(payload["items"][0]["valid"])
        self.assertEqual(payload["items"][0]["title"], "No text available")

    def test_clipboard_fallback(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "zh"}):
            with mock.patch.object(m, "read_clipboard", return_value="one\ntwo"):
                payload = m.build_items("   ")
        self.assertEqual(payload["items"][0]["arg"], "'one','two'")
        self.assertIn("剪贴板", payload["items"][0]["subtitle"])

    def test_main_prints_json(self) -> None:
        with mock.patch.dict(os.environ, {"ui_language": "en"}):
            with mock.patch.object(m.sys, "argv", ["filter.py", "a\nb"]):
                with mock.patch("builtins.print") as printed:
                    m.main()
        raw = printed.call_args[0][0]
        data = json.loads(raw)
        self.assertEqual(data["items"][0]["arg"], "'a','b'")


if __name__ == "__main__":
    unittest.main()
