# -*- coding: utf-8 -*-
"""第31課復習クイズの section-lead 用 HTML（単体 fukushu HTML とパート結合で共通）。"""

from __future__ import annotations


def fukushu_segment_key(q: int) -> str:
    """パート結合時に復習ブロックを分割するための連続キー（表・読解・文・意向・会話）。"""
    if 33 <= q <= 36:
        return "hyou"
    if 37 <= q <= 40:
        return "dokkai"
    k = _fukushu_q_kind(q)
    if k in ("bun_omo", "bun_tsumori"):
        return "bun"
    return k


def iter_fukushu_segments(f_lo: int, f_hi: int) -> list[tuple[str, list[int]]]:
    """[ (セグメントキー, [通し番号…]), … ] 連続する同一キーをまとめる。"""
    qs = list(range(f_lo, f_hi + 1))
    if not qs:
        return []
    out: list[tuple[str, list[int]]] = []
    cur_k = fukushu_segment_key(qs[0])
    buf = [qs[0]]
    for q in qs[1:]:
        k = fukushu_segment_key(q)
        if k == cur_k:
            buf.append(q)
        else:
            out.append((cur_k, buf))
            cur_k, buf = k, [q]
    out.append((cur_k, buf))
    return out


def _fukushu_q_kind(q: int) -> str:
    """復習通し番号（1…40）に対応する設問タイプ（リード文切り替え用）。"""
    if 1 <= q <= 14 or 20 <= q <= 24:
        return "ikou"
    if 15 <= q <= 19:
        return "kaiwa"
    if 25 <= q <= 28:
        return "bun_omo"
    if 29 <= q <= 32:
        return "bun_tsumori"
    if 33 <= q <= 36:
        return "hyou"
    if 37 <= q <= 40:
        return "dokkai"
    return "ikou"


def _dedupe_consecutive_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if not out or out[-1] != line:
            out.append(line)
    return out


FUKUSHU_LEAD_FRAGMENTS: dict[str, str] = {
    "ikou": (
        "「〜ます」の<ruby>形<rt>かたち</rt></ruby>に<ruby>対応<rt>たいおう</rt></ruby>する"
        "<ruby>意向形<rt>いこうけい</rt></ruby>を<ruby>選<rt>えら</rt></ruby>びましょう。"
    ),
    "kaiwa": (
        "<ruby>会話<rt>かいわ</rt></ruby>の（　）に<ruby>入<rt>はい</rt></ruby>る"
        "<ruby>正<rt>ただ</rt></ruby>しいものはどれですか。"
    ),
    "bun_omo": (
        "<ruby>文<rt>ぶん</rt></ruby>の（　）に<ruby>入<rt>はい</rt></ruby>る"
        "<ruby>正<rt>ただ</rt></ruby>しいものを<ruby>選<rt>えら</rt></ruby>びましょう。"
    ),
    "bun_tsumori": (
        "<ruby>文<rt>ぶん</rt></ruby>の（　）に<ruby>入<rt>はい</rt></ruby>る"
        "<ruby>正<rt>ただ</rt></ruby>しいものを<ruby>選<rt>えら</rt></ruby>びましょう。"
    ),
    "hyou": (
        "<ruby>表<rt>ひょう</rt></ruby>の<ruby>内容<rt>ないよう</rt></ruby>に"
        "<ruby>合<rt>あ</rt></ruby>う<ruby>答<rt>こた</rt></ruby>えを<ruby>選<rt>えら</rt></ruby>びましょう。"
    ),
    "dokkai": (
        "<ruby>読<rt>よ</rt></ruby>んだ<ruby>文章<rt>ぶんしょう</rt></ruby>の<ruby>内容<rt>ないよう</rt></ruby>に"
        "<ruby>合<rt>あ</rt></ruby>うものを<ruby>選<rt>えら</rt></ruby>びましょう。"
    ),
}


def fukushu_section_lead_for_range(f_lo: int, f_hi: int) -> str:
    """パート内の復習タイプに応じた説明文（連続ブロック単位でまとめ、<br> で接続）。"""
    seen: list[str] = []
    prev: str | None = None
    for q in range(f_lo, f_hi + 1):
        k = _fukushu_q_kind(q)
        if k != prev:
            seen.append(k)
            prev = k
    lines = _dedupe_consecutive_lines([FUKUSHU_LEAD_FRAGMENTS[k] for k in seen])
    return "<br>".join(lines)


def fukushu_section_lead_paragraph(f_lo: int, f_hi: int) -> str:
    """<p class="section-lead">…</p> でラップした HTML。"""
    return f'<p class="section-lead">{fukushu_section_lead_for_range(f_lo, f_hi)}</p>'


def fukushu_top_lead_for_range(f_lo: int, f_hi: int) -> str:
    """
    パート先頭に置くリード（表・読解ブロックは別途、本文の直前に挿入するため除外）。
    """
    seen: list[str] = []
    prev: str | None = None
    for q in range(f_lo, f_hi + 1):
        k = _fukushu_q_kind(q)
        if k != prev:
            seen.append(k)
            prev = k
    top = [k for k in seen if k not in ("hyou", "dokkai")]
    if not top:
        return ""
    lines = _dedupe_consecutive_lines([FUKUSHU_LEAD_FRAGMENTS[k] for k in top])
    return "<br>".join(lines)


def fukushu_top_lead_paragraph(f_lo: int, f_hi: int) -> str:
    inner = fukushu_top_lead_for_range(f_lo, f_hi)
    return f'<p class="section-lead">{inner}</p>' if inner else ""


def fukushu_hyou_lead_paragraph() -> str:
    return f'<p class="section-lead">{FUKUSHU_LEAD_FRAGMENTS["hyou"]}</p>'


def fukushu_dokkai_lead_paragraph() -> str:
    return f'<p class="section-lead">{FUKUSHU_LEAD_FRAGMENTS["dokkai"]}</p>'
