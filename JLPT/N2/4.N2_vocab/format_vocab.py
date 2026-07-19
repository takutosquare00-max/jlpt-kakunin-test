#!/usr/bin/env python3
"""Clean up MarkItDown-converted JLPT N2 vocab list into uniform tables."""

import re
from pathlib import Path

RAW = Path(__file__).with_name("VocabList.N2.raw.md")
OUTPUT = Path(__file__).with_name("VocabList.N2.md")

SKIP_PATTERNS = [
    re.compile(r"^JLPT Resources"),
    re.compile(r"^JLPT N2 Vocab"),
    re.compile(r"^This is not a cumulative"),
    re.compile(r"^\d+$"),
]


def should_skip(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    return any(p.search(s) for p in SKIP_PATTERNS)


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r"-+", c) or not c for c in cells)


def parse_table_row(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    cells = [c.strip() for c in s.strip("|").split("|")]
    if is_separator(cells):
        return None
    if cells and cells[0] == "Kanji" and len(cells) > 1 and "Hiragana" in cells[1]:
        return None
    return cells


def is_english(text: str) -> bool:
    if not text:
        return False
    if re.search(r"[ぁ-んァ-ヶ一-龯]", text):
        return False
    return bool(re.search(r"[a-zA-Z(]", text))


def is_japanese(text: str) -> bool:
    return bool(re.search(r"[ぁ-んァ-ヶ一-龯]", text))


def merge_english(*parts: str) -> str:
    merged = " ".join(p.strip() for p in parts if p and p.strip())
    return re.sub(r"\s+", " ", merged).strip()


def cells_to_fields(cells: list[str]) -> tuple[str, str, str]:
    while len(cells) < 4:
        cells.append("")
    return cells[0], cells[1], merge_english(cells[2], cells[3], *cells[4:])


def parse_plain_line(line: str) -> tuple[str, str, str] | None:
    s = line.strip()
    m = re.match(r"^([一-龯々〆ヵヶ]+[^\s|]*)\s+([ぁ-んァ-ヶー/（）()=・]+)\s+(.+)$", s)
    if m and is_english(m.group(3)):
        return m.group(1), m.group(2), m.group(3)
    m = re.match(r"^([一-龯々〆ヵヶ]+[^\s|]*)\s+([ぁ-んァ-ヶー/（）()=・]+)$", s)
    if m:
        return m.group(1), m.group(2), ""
    m = re.match(r"^([ぁ-んァ-ヶー/（）()=・]+)\s+(.+)$", s)
    if m and is_english(m.group(2)):
        return "", m.group(1), m.group(2)
    return None


def collect_lines(path: Path) -> list[str]:
    return [ln for ln in path.read_text(encoding="utf-8").splitlines() if not should_skip(ln)]


def next_meaningful(lines: list[str], start: int, step: int, used: set[int]) -> int | None:
    i = start
    while 0 <= i < len(lines):
        if i in used:
            return None
        s = lines[i].strip()
        if not s:
            i += step
            continue
        if parse_table_row(s) is not None:
            return None
        return i
    return None


def scan_english(lines: list[str], start: int, step: int, used: set[int]) -> tuple[str, set[int]]:
    consumed: set[int] = set()
    parts: list[str] = []
    i = start
    while 0 <= i < len(lines):
        if i in used or i in consumed:
            break
        s = lines[i].strip()
        if not s:
            i += step
            continue
        cells = parse_table_row(s)
        if cells is not None:
            break
        if s.startswith("|"):
            i += step
            continue
        if is_english(s):
            parts.append(s)
            consumed.add(i)
            i += step
            continue
        break
    if step < 0:
        parts.reverse()
    return merge_english(*parts), consumed


def nearby_english(lines: list[str], idx: int, used: set[int]) -> tuple[str, set[int]]:
    back, back_used = scan_english(lines, idx - 1, -1, used)
    fwd, fwd_used = scan_english(lines, idx + 1, 1, used)
    return merge_english(back, fwd), back_used | fwd_used


def parse_vocab(lines: list[str]) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    used: set[int] = set()
    n = len(lines)

    i = 0
    while i < n:
        if i in used:
            i += 1
            continue

        line = lines[i].strip()
        cells = parse_table_row(line)

        if cells is not None:
            kanji, hiragana, english = cells_to_fields(cells)

            if not kanji and hiragana and not english:
                prev_i = next_meaningful(lines, i - 1, -1, used)
                prev2_i = next_meaningful(lines, i - 2, -1, used) if prev_i is not None else None
                if (
                    prev_i is not None
                    and is_english(lines[prev_i].strip())
                    and prev2_i is not None
                    and is_japanese(lines[prev2_i].strip())
                    and parse_plain_line(lines[prev2_i].strip()) is None
                ):
                    entries.append(("", lines[prev2_i].strip() + hiragana, lines[prev_i].strip()))
                    used.update({i, prev_i, prev2_i})
                    i += 1
                    continue

                if (
                    prev_i is not None
                    and is_japanese(lines[prev_i].strip())
                    and parse_plain_line(lines[prev_i].strip()) is None
                    and not is_english(lines[prev_i].strip())
                ):
                    hiragana = lines[prev_i].strip() + hiragana
                    used.add(prev_i)

            if not english:
                extra, consumed = nearby_english(lines, i, used)
                english = merge_english(english, extra)
                used |= consumed

            if kanji or hiragana or english:
                entries.append((kanji, hiragana, english))
            used.add(i)
            i += 1
            continue

        plain = parse_plain_line(line)
        if plain:
            kanji, hiragana, english = plain
            if not english:
                extra, consumed = nearby_english(lines, i, used)
                english = extra
                used |= consumed
            entries.append((kanji, hiragana, english))
            used.add(i)
            i += 1
            continue

        if is_japanese(line):
            nxt = next_meaningful(lines, i + 1, 1, used)
            if nxt is not None and is_english(lines[nxt].strip()):
                hiragana = line
                english = lines[nxt].strip()
                used.update({i, nxt})
                frag_i = nxt + 1
                while frag_i < n:
                    frag_line = lines[frag_i].strip()
                    if not frag_line:
                        frag_i += 1
                        continue
                    frag_cells = parse_table_row(frag_line)
                    if frag_cells:
                        fk, fh, fe = cells_to_fields(frag_cells)
                        if not fk and fh and not fe:
                            hiragana += fh
                            used.add(frag_i)
                            frag_i += 1
                            continue
                    break
                entries.append(("", hiragana, english))
            i += 1
            continue

        if is_english(line):
            used.add(i)
        i += 1

    return entries


def merge_greeting_fragments(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    known = ["いっていらっしゃい", "いってらっしゃい", "いってまいります"]
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(entries):
        k, h, e = entries[i]
        if not k and not e and h and any(h.startswith(t[:4]) for t in known):
            buf = h
            j = i + 1
            while j < len(entries) and not entries[j][0] and not entries[j][2] and entries[j][1]:
                buf += entries[j][1]
                j += 1
            for token in known:
                while token in buf:
                    before, _, after = buf.partition(token)
                    if before:
                        out.append(("", before, ""))
                    out.append(("", token, ""))
                    buf = after
            if buf:
                out.append(("", buf, e))
            i = j
            continue
        out.append((k, h, e))
        i += 1
    return out


def merge_idea_split(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(entries):
        k, h, e = entries[i]
        if (
            not k
            and h.endswith("/アイ")
            and i + 1 < len(entries)
            and entries[i + 1][1] == "ディア"
            and not entries[i + 1][0]
        ):
            out.append(("", h + "ディア", e or entries[i + 1][2]))
            i += 2
            continue
        if not k and h == "ディア" and not e and out and out[-1][1].endswith("/アイ"):
            out[-1] = (out[-1][0], out[-1][1] + "ディア", out[-1][2])
            i += 1
            continue
        out.append((k, h, e))
        i += 1
    return out


def merge_verb_tail_fragments(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """Merge PDF splits like 引っ繰り返 + す/る tail rows."""
    tails = {
        "す": ("引っ繰り返す", "ひっくりかえす"),
        "る": ("引っ繰り返る", "ひっくりかえる"),
    }
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(entries):
        k, h, e = entries[i]
        if (
            (not k and h == "引っ繰り返" or k == "引っ繰り返")
            and i + 1 < len(entries)
            and entries[i + 1][0] in tails
            and not entries[i + 1][1]
        ):
            kanji, hiragana = tails[entries[i + 1][0]]
            english = merge_english(e, entries[i + 1][2])
            out.append((kanji, hiragana, english))
            i += 2
            continue
        if k in tails and not h:
            i += 1
            continue
        out.append((k, h, e))
        i += 1
    return out


def merge_katakana_splits(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(entries):
        k, h, e = entries[i]
        if h == "レクリェーショ" and i + 1 < len(entries) and entries[i + 1][1] == "ン":
            out.append(("", "レクリェーション", e or entries[i + 1][2]))
            i += 2
            continue
        if h == "ンレジャー":
            out.append(("", "レジャー", e))
            i += 1
            continue
        out.append((k, h, e))
        i += 1
    return out


def build_raw_lookup(raw_text: str) -> dict[tuple[str, str], str]:
    lookup: dict[tuple[str, str], str] = {}
    lines = [ln for ln in raw_text.splitlines() if not should_skip(ln)]
    for i, line in enumerate(lines):
        plain = parse_plain_line(line.strip())
        if plain and plain[2]:
            lookup[(plain[0], plain[1])] = plain[2]
        cells = parse_table_row(line.strip())
        if not cells:
            continue
        kanji, hiragana, english = cells_to_fields(cells)
        if not (kanji or hiragana):
            continue
        if not english:
            english, _ = nearby_english(lines, i, set())
        if english:
            lookup[(kanji, hiragana)] = english
    return lookup


def fill_missing(entries: list[tuple[str, str, str]], lookup: dict[tuple[str, str], str]) -> list[tuple[str, str, str]]:
    out = []
    for kanji, hiragana, english in entries:
        if not english.strip():
            english = lookup.get((kanji, hiragana), lookup.get(("", hiragana), ""))
        out.append((kanji, hiragana, english))
    return out


def patch_known(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    forced = {
        ("預かる", "あずかる"): "to keep in custody,to receive on deposit,to take charge of",
        ("言い出す", "いいだす"): "to start talking,to speak,to tell,to propose,to suggest,to break the ice",
        ("有難い", "ありがたい"): "grateful,thankful,welcome,appreciated,evoking gratitude",
        ("分る", "わかる"): "to be understood",
        ("分かれる", "わかれる"): "to branch off,to diverge from,to fork,to split,to dispense,to scatter,to divide into",
    }
    patches = {
        ("炒る", "いる"): "to roast,to broil,to toast",
        ("", "いっていらっしゃい"): "go ahead / please go ahead",
        ("", "いってらっしゃい"): "see you / take care",
        ("", "いってまいります"): "I'm off / I'm going now",
        ("あひら", "あひら"): "archaic form of hiragana",
        ("お出掛け", "おでかけ"): "going out, outing",
        ("思いっ切り", "おもいっきり"): "very, much, with all one's strength",
        ("咥える", "くわえる"): "to hold in the mouth",
        ("棄てる", "すてる"): "to throw away, to abandon",
        ("清む", "すむ"): "to become clear (liquid)",
        ("滑れる", "ずれる"): "to slide, to slip, to be off",
        ("存ずる", "ぞんずる"): "to think, to believe (humble)",
        ("茶色い", "ちゃいろい"): "brown",
        ("通ずる", "つうずる"): "to lead to, to apply, to communicate",
        ("転々", "てんてん"): "moving from place to place",
        ("傾らか", "なだらか"): "gradual, gently sloping",
        ("×", "ばつ"): "wrong, incorrect",
        ("破く", "やぶく"): "to tear, to rip",
        ("引っ繰り返す", "ひっくりかえす"): "to turn over,to overturn,to knock over,to upset,to turn inside out",
        ("引っ繰り返る", "ひっくりかえる"): "to be overturned,to be upset,to topple over,to be reversed",
    }
    out = []
    for kanji, hiragana, english in entries:
        key = (kanji, hiragana)
        if key in forced:
            english = forced[key]
        elif not english.strip():
            english = patches.get(key, patches.get(("", hiragana), ""))
        out.append((kanji, hiragana, english))
    return out


def drop_garbage(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out = []
    for kanji, hiragana, english in entries:
        if not kanji and not hiragana and english.lower() in {"doubt", "answer)", "random"}:
            continue
        if english.startswith("|"):
            continue
        out.append((kanji, hiragana, english))
    return out


def render(entries: list[tuple[str, str, str]]) -> str:
    lines = [
        "# JLPT N2 Vocab List",
        "",
        "Source: [JLPT Resources – tanos.co.uk](http://www.tanos.co.uk/jlpt/)",
        "",
        "This is not a cumulative list. (It doesn't contain the vocab needed by JLPT N3 and below.)",
        "",
        "| Kanji | Hiragana | English |",
        "| --- | --- | --- |",
    ]
    for kanji, hiragana, english in entries:
        lines.append(
            f"| {kanji.replace('|', '\\|')} | {hiragana.replace('|', '\\|')} | {english.replace('|', '\\|')} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    raw_text = RAW.read_text(encoding="utf-8")
    entries = parse_vocab(collect_lines(RAW))
    entries = merge_idea_split(entries)
    entries = merge_greeting_fragments(entries)
    entries = merge_katakana_splits(entries)
    entries = merge_verb_tail_fragments(entries)
    entries = fill_missing(entries, build_raw_lookup(raw_text))
    entries = patch_known(entries)
    entries = drop_garbage(entries)
    OUTPUT.write_text(render(entries), encoding="utf-8")
    empty = sum(1 for _, _, e in entries if not e.strip())
    print(f"Wrote {len(entries)} entries ({empty} without english) to {OUTPUT}")


if __name__ == "__main__":
    main()
