#!/usr/bin/env python3
"""
jtest-ac-2025.md 用: 全ルビをいったん捨て、PDF（スキャン画像）準拠で再付与。
ルール本体は jtest_pdf_furigana / jtest_pdf_furigana_rules。
"""

from __future__ import annotations

from jtest_pdf_furigana import apply_pdf_furigana, strip_all_ruby


def apply_to_text(md: str) -> str:
    return apply_pdf_furigana(strip_all_ruby(md))


def main() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parent
    path = root / "jtest-ac-2025.md"
    raw = path.read_text(encoding="utf-8")
    path.write_text(apply_to_text(raw), encoding="utf-8")
    print("Updated", path)


if __name__ == "__main__":
    main()
