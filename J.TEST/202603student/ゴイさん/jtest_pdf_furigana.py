#!/usr/bin/env python3
"""
PDF（スキャン画像）のふりがな方針: まず全ルビを除去し、付与ルールを適用する。
md_to_jtest_html.py および pdf_ruby_normalize から利用。
"""

from __future__ import annotations

import re
from pathlib import Path

from jtest_pdf_furigana_rules import ordered_rules


def strip_all_ruby(text: str) -> str:
    """<ruby>…<rt>…</rt></ruby> を基底文字列に戻す（入れ子も繰り返し処理）。"""
    pattern = re.compile(r"<ruby>((?:[^<]|<(?!/?ruby))*)<rt>[^<]*</rt></ruby>", re.DOTALL)
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub(lambda m: m.group(1), text)
    return text


def apply_pdf_furigana(text: str) -> str:
    """平文（ルビなし）に、PDFに基づくルビのみ付与。ルールは長い一致を先に適用。"""
    out = text
    for old, new in ordered_rules():
        if old not in out:
            continue
        out = out.replace(old, new)
    return out


def apply_to_text(md: str) -> str:
    """MD 読み込み直後用: 既存ルビを捨ててから PDF 準拠で付け直す。"""
    return apply_pdf_furigana(strip_all_ruby(md))


def main() -> None:
    root = Path(__file__).resolve().parent
    path = root / "jtest-ac-2025.md"
    raw = path.read_text(encoding="utf-8")
    path.write_text(apply_to_text(raw), encoding="utf-8")
    print("Updated", path)


if __name__ == "__main__":
    main()
