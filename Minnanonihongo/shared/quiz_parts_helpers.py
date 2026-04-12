# -*- coding: utf-8 -*-
"""パート結合用 PARTS タプルの生成（復習・漢字のチャンク件数から）。"""

# 結合後の unit{N}-quiz-part*.html 共通。minna-unit-quiz-workflow.md §1.1 に合わせる。
PART_QUIZ_TIME_LIMIT_SECONDS = 15 * 60


def build_parts_from_chunk_sizes(
    f_chunks: tuple[int, ...],
    k_chunks: tuple[int, ...],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    復習・漢字をそれぞれ連番区間に分割し、パートごとの (f_range, k_range) を返す。

    例: f_chunks=(10,11,10,10), k_chunks=(8,8,8,8)
        → [((1,10),(1,8)), ((11,21),(9,16)), ...]
    """
    if len(f_chunks) != len(k_chunks):
        raise ValueError("f_chunks と k_chunks の長さは等しい必要があります")
    parts: list[tuple[tuple[int, int], tuple[int, int]]] = []
    f_lo, k_lo = 1, 1
    for fw, kw in zip(f_chunks, k_chunks):
        f_hi = f_lo + fw - 1
        k_hi = k_lo + kw - 1
        parts.append(((f_lo, f_hi), (k_lo, k_hi)))
        f_lo, k_lo = f_hi + 1, k_hi + 1
    return parts


def part_time_limit_seconds(
    total_questions: int,
    *,
    seconds_per_question: int = 50,
    minimum_seconds: int = 120,
) -> int:
    """
    1 パート内の総問数から TIME_LIMIT（秒）を求める（可変）。

    結合パート HTML では `PART_QUIZ_TIME_LIMIT_SECONDS`（15 分固定）を使う。本関数は
    単体 HTML や旧スクリプト向けに残す。
    """
    if total_questions < 1:
        raise ValueError("total_questions は 1 以上")
    return max(minimum_seconds, total_questions * seconds_per_question)
