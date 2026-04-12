#!/usr/bin/env python3
"""
Merge split ranges of unit31-fukushu-a.html + unit31-kanji-vocab-quiz.html into
combined part HTML files（パート数＝チャンク列の長さ）。

PARTS はチャンク件数定数（unit31.md / generate_unit31_sources.py と同期）から生成。
minna-unit-quiz-workflow.md §1.1: 各パート 復習+漢字 が 18〜20 問、TIME_LIMIT 15 分固定。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

_MINNA_ROOT = Path(__file__).resolve().parents[1]
if str(_MINNA_ROOT) not in sys.path:
    sys.path.insert(0, str(_MINNA_ROOT))
from shared.fukushu_lead_unit31 import (
    FUKUSHU_LEAD_FRAGMENTS,
    fukushu_dokkai_lead_paragraph,
    fukushu_hyou_lead_paragraph,
    iter_fukushu_segments,
)
from shared.quiz_parts_helpers import (
    PART_QUIZ_TIME_LIMIT_SECONDS,
    build_parts_from_chunk_sizes,
)

DIR = Path(__file__).resolve().parent
FUKUSHU = DIR / "unit31-fukushu-a.html"
KANJI = DIR / "unit31-kanji-vocab-quiz.html"

FUKUSHU_QUESTION_COUNT = 40
KANJI_QUESTION_COUNT = 40
FUKUSHU_PART_CHUNK_SIZES = (10, 10, 10, 10)
KANJI_PART_CHUNK_SIZES = (10, 10, 10, 10)
assert sum(FUKUSHU_PART_CHUNK_SIZES) == FUKUSHU_QUESTION_COUNT
assert sum(KANJI_PART_CHUNK_SIZES) == KANJI_QUESTION_COUNT
for _fc, _kc in zip(FUKUSHU_PART_CHUNK_SIZES, KANJI_PART_CHUNK_SIZES):
    _t = _fc + _kc
    assert 18 <= _t <= 20, (_fc, _kc, _t)
PARTS = build_parts_from_chunk_sizes(FUKUSHU_PART_CHUNK_SIZES, KANJI_PART_CHUNK_SIZES)

KANJI_SECTION_LEAD = (
    '<ruby>次<rt>つぎ</rt></ruby>の<ruby>漢字<rt>かんじ</rt></ruby>の<ruby>読<rt>よ</rt></ruby>みとして'
    '<ruby>正<rt>ただ</rt></ruby>しいものはどれですか。'
)

_KAIWA_HEADING_P = re.compile(
    r'<p style="font-weight:600;margin-bottom:8px;color:#4a5568">会話（[^）]+）</p>\s*',
)


def strip_kaiwa_headings(html: str) -> str:
    return _KAIWA_HEADING_P.sub("", html)


def extract_fukushu_reading_passages(fuk_html: str) -> tuple[str, str]:
    """（スケジュール表・読解本文）単体 fukushu HTML から抽出。設問 div には含まれない。"""
    soup = BeautifulSoup(fuk_html, "html.parser")
    schedule = ""
    dokkai = ""
    for rp in soup.select("div.reading-passage"):
        t = rp.get_text(" ", strip=True)
        if "スケジュール" in t:
            schedule = str(rp)
        elif "九州" in t and "東京" in t:
            dokkai = str(rp)
    return schedule, dokkai


def build_merged_fukushu_sections_html(
    f_lo: int,
    f_hi: int,
    by_q: dict[int, list],
    schedule_html: str,
    dokkai_html: str,
) -> str:
    """题型が変わるたびに div.section を分け、リード・表・読解本文を単体 fukushu と同順で挿入する。"""
    segments = iter_fukushu_segments(f_lo, f_hi)
    off = 0
    sections: list[str] = []
    for seg_key, qnums in segments:
        nseg = len(qnums)
        a, b = off + 1, off + nseg
        off += nseg
        title = f'<div class="section-title">復習A（問題 {a}–{b}）</div>'
        bl: list[str] = [title]
        if seg_key == "hyou":
            bl.append(fukushu_hyou_lead_paragraph())
            if schedule_html:
                bl.append(schedule_html)
        elif seg_key == "dokkai":
            bl.append(fukushu_dokkai_lead_paragraph())
            if dokkai_html:
                bl.append(dokkai_html)
        elif seg_key == "ikou":
            bl.append(f'<p class="section-lead">{FUKUSHU_LEAD_FRAGMENTS["ikou"]}</p>')
        elif seg_key == "kaiwa":
            bl.append(f'<p class="section-lead">{FUKUSHU_LEAD_FRAGMENTS["kaiwa"]}</p>')
        elif seg_key == "bun":
            bl.append(f'<p class="section-lead">{FUKUSHU_LEAD_FRAGMENTS["bun_omo"]}</p>')
        else:
            raise AssertionError(f"unknown segment {seg_key!r}")
        for q in qnums:
            bl.append("".join(str(node) for node in by_q[q]))
        sections.append(f'<div class="section">\n{"".join(bl)}\n</div>')
    return strip_kaiwa_headings("".join(sections))


def _qnum_from_element(el) -> int | None:
    inp = el.find("input", attrs={"name": re.compile(r"^q\d+$")})
    if not inp or not inp.get("name"):
        return None
    return int(inp["name"][1:])


def iter_fukushu_units(soup: BeautifulSoup) -> list:
    units: list[tuple[int, list]] = []
    for sec in soup.select("div.container > div.section"):
        for div in sec.find_all("div", class_="question", recursive=False):
            subqs = div.find_all("div", class_="subq", recursive=False)
            if subqs:
                prelude_nodes: list = []
                for child in div.children:
                    if getattr(child, "name", None) == "div" and "subq" in (child.get("class") or []):
                        break
                    if isinstance(child, NavigableString) and not str(child).strip():
                        continue
                    prelude_nodes.append(child)
                for i, sq in enumerate(subqs):
                    qn = _qnum_from_element(sq)
                    if qn is None:
                        continue
                    if i == 0:
                        units.append((qn, prelude_nodes + [sq]))
                    else:
                        units.append((qn, [sq]))
            else:
                qn = _qnum_from_element(div)
                if qn is None:
                    continue
                units.append((qn, [div]))
    return units


def extract_kanji_questions(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    sec = soup.select_one("div.section")
    if not sec:
        return []
    out: list[str] = []
    for art in sec.find_all("div", class_="question", recursive=False):
        out.append(str(art))
    return out


def renumber_kanji_fragment(frag: str, old_q: int, new_q: int) -> str:
    frag = frag.replace(f'name="q{old_q}"', f'name="q{new_q}"')
    frag = frag.replace(f'<span class="q-num">{old_q}</span>', f'<span class="q-num">{new_q}</span>')
    suf = re.escape(str(old_q))
    frag = re.sub(rf'id="q{suf}([1-4])"', rf'id="q{new_q}\1"', frag)
    frag = re.sub(rf'for="q{suf}([1-4])"', rf'for="q{new_q}\1"', frag)
    return frag


def replace_q_number(html: str, old: int, new: int) -> str:
    if old == new:
        return html
    os = str(old)
    html = re.sub(rf'(?<![0-9])name="q{os}"(?![0-9])', f'name="q{new}"', html)
    html = re.sub(rf'(?<![0-9])id="q{os}([a-d])"', rf'id="q{new}\1"', html)
    html = re.sub(rf'(?<![0-9])for="q{os}([a-d])"', rf'for="q{new}\1"', html)
    html = re.sub(rf'(?<![0-9])id="q{os}([1-4])"', rf'id="q{new}\1"', html)
    html = re.sub(rf'(?<![0-9])for="q{os}([1-4])"', rf'for="q{new}\1"', html)
    html = html.replace(f'<span class="q-num">{old}</span>', f'<span class="q-num">{new}</span>')
    return html


def collapse_part_to_sequence(html: str, ordered_old: list[int]) -> str:
    mapping = {old: i + 1 for i, old in enumerate(ordered_old)}
    temp_base = 900_000
    for old in sorted(mapping.keys(), reverse=True):
        html = replace_q_number(html, old, temp_base + old)
    for old, new in mapping.items():
        html = replace_q_number(html, temp_base + old, new)
    return html


def merged_styles() -> str:
    f = FUKUSHU.read_text(encoding="utf-8")
    k = KANJI.read_text(encoding="utf-8")
    m1 = re.search(r"<style>(.*?)</style>", f, re.S)
    m2 = re.search(r"<style>(.*?)</style>", k, re.S)
    s1 = m1.group(1) if m1 else ""
    s2 = m2.group(1) if m2 else ""
    seen: set[str] = set()
    lines_out: list[str] = []
    for block in (s1, s2):
        for line in block.splitlines():
            t = line.strip()
            if not t or t in seen:
                continue
            seen.add(t)
            lines_out.append(line)
    return "\n".join(lines_out)


def build_part(
    part_idx: int,
    fuk_range: tuple[int, int],
    kan_range: tuple[int, int],
) -> str:
    fuk_html = FUKUSHU.read_text(encoding="utf-8")
    kan_html = KANJI.read_text(encoding="utf-8")

    fsoup = BeautifulSoup(fuk_html, "html.parser")
    units = iter_fukushu_units(fsoup)
    by_q = {qn: nodes for qn, nodes in units}

    f_lo, f_hi = fuk_range
    k_lo, k_hi = kan_range

    for n in range(f_lo, f_hi + 1):
        if n not in by_q:
            raise SystemExit(f"Fukushu q{n} not found")

    sched_html, dokkai_html = extract_fukushu_reading_passages(fuk_html)
    fukushu_sections = build_merged_fukushu_sections_html(
        f_lo, f_hi, by_q, sched_html, dokkai_html
    )

    kan_questions = extract_kanji_questions(kan_html)
    if len(kan_questions) != KANJI_QUESTION_COUNT:
        raise SystemExit(f"Expected {KANJI_QUESTION_COUNT} kanji questions, got {len(kan_questions)}")

    k_frags = kan_questions[k_lo - 1 : k_hi]

    total = (f_hi - f_lo + 1) + (k_hi - k_lo + 1)
    k_renumbered: list[str] = []
    for i, frag in enumerate(k_frags):
        old_n = k_lo + i
        new_n = f_hi + 1 + (old_n - k_lo)
        k_renumbered.append(renumber_kanji_fragment(frag, old_n, new_n))

    n_fuk = f_hi - f_lo + 1
    k_title = f'<div class="section-title">漢字・語彙（問題 {n_fuk + 1}–{total}）</div>'
    k_lead = f'<p class="section-lead">{KANJI_SECTION_LEAD}</p>'

    body_section = f"""{fukushu_sections}
<div class="section">
{k_title}
{k_lead}
{"".join(k_renumbered)}
</div>"""

    ordered_old = list(range(f_lo, f_hi + 1)) + [
        f_hi + 1 + (n - k_lo) for n in range(k_lo, k_hi + 1)
    ]
    body_section = collapse_part_to_sequence(body_section, ordered_old)

    time_limit = PART_QUIZ_TIME_LIMIT_SECONDS
    tm, ts = divmod(time_limit, 60)
    minutes = time_limit // 60

    title = f"みんなの日本語 31 パート{part_idx}（{minutes}分・{total}問）"
    styles = merged_styles()

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<style>
{styles}
.subq + .dialogue{{margin-top:calc(8px + 2.55em)}}
</style>
</head>
<body>
<div class="container">
<header>
<h1>みんなの<ruby>日本語<rt>にほんご</rt></ruby> 31 クイズ（パート{part_idx}・{minutes}分・{total}<ruby>問<rt>もん</rt></ruby>）</h1>
<div class="header-info">
<div class="timer" id="timer">{tm}:{ts:02d}</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge"><ruby>全<rt>ぜん</rt></ruby>{total}<ruby>問<rt>もん</rt></ruby></div>
</div>
</header>
{body_section}
<button class="btn-submit" id="submitBtn" onclick="submitTest()"><ruby>採点<rt>さいてん</rt></ruby>する</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2><div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
</div>
</div>
<script>
const TOTAL={total},TIME_LIMIT={time_limit};
let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function shuffleAllOptions(){{
function randBelow(n){{
if(n<=1)return 0;
try{{
if(typeof crypto!=='undefined'&&crypto.getRandomValues){{
const lim=Math.floor(4294967296/n)*n;
const buf=new Uint32Array(1);
let x;
do{{crypto.getRandomValues(buf);x=buf[0];}}while(x>=lim);
return x%n;
}}
}}catch(e){{}}
return Math.floor(Math.random()*n);
}}
function fisherYates(arr){{
for(let i=arr.length-1;i>0;i--){{
const j=randBelow(i+1);
const t=arr[i];arr[i]=arr[j];arr[j]=t;
}}
}}
function relabel(optsDiv,items,isLetter,prefix){{
items.forEach(function(el){{optsDiv.appendChild(el);}});
items.forEach(function(el,idx){{
const inp=el.querySelector('input[type="radio"]');
const lbl=el.querySelector('label');
if(!inp||!lbl)return;
const suf=isLetter?String.fromCharCode(97+idx):String(idx+1);
const newId=prefix+suf;
inp.id=newId;
lbl.setAttribute('for',newId);
const key=el.querySelector('.opt-key');
if(key)key.textContent=(idx+1)+'.';
}});
const explain=optsDiv.nextElementSibling;
if(explain&&explain.classList&&explain.classList.contains('explanation')){{
const correctInp=optsDiv.querySelector('input[type="radio"][value="1"]');
if(correctInp){{
const opt=correctInp.closest('.option');
if(opt){{
const keyEl=opt.querySelector('.opt-key');
if(keyEl){{
const mk=keyEl.textContent.match(/^(\\d+)\\./);
if(mk)explain.textContent=explain.textContent.replace(/正解：\\d+/,'正解：'+mk[1]);
}}
}}
}}
}}
return items.findIndex(function(el){{return el.querySelector('input[type="radio"][value="1"]');}});
}}
const posCounts=[0,0,0,0];
document.querySelectorAll('.options').forEach(function(optsDiv){{
const items=Array.prototype.filter.call(optsDiv.children,function(el){{
return el.classList&&el.classList.contains('option');
}});
const n=items.length;
if(n<2)return;
fisherYates(items);
const sample=optsDiv.querySelector('input[type="radio"]');
if(!sample)return;
const prefix=sample.name;
if(!prefix)return;
const firstInp=items[0].querySelector('input[type="radio"]');
if(!firstInp)return;
const sid=firstInp.id;
if(!sid||!sid.startsWith(prefix))return;
const firstSuffix=sid.slice(prefix.length);
const isLetter=/^[a-d]$/.test(firstSuffix);
let slot=relabel(optsDiv,items,isLetter,prefix);
if(slot<0)return;
let minC=9999;
for(let i=0;i<n;i++)minC=Math.min(minC,posCounts[i]);
const cand=[];
for(let i=0;i<n;i++)if(posCounts[i]===minC)cand.push(i);
const ideal=cand[randBelow(cand.length)];
if(slot!==ideal&&posCounts[slot]>posCounts[ideal]){{
const t=items[slot];items[slot]=items[ideal];items[ideal]=t;
slot=relabel(optsDiv,items,isLetter,prefix);
if(slot<0)return;
}}
posCounts[slot]++;
}});
}}
try{{shuffleAllOptions();}}catch(e){{}}
function startTimer(){{
timerInterval=setInterval(()=>{{
timeLeft--;
const m=Math.floor(timeLeft/60),s=timeLeft%60;
const el=document.getElementById('timer');
el.textContent=`${{m}}:${{s.toString().padStart(2,'0')}}`;
document.getElementById('progress').style.width=`${{(timeLeft/TIME_LIMIT)*100}}%`;
if(timeLeft<=60)el.className='timer danger';
else if(timeLeft<=300)el.className='timer warning';
else el.className='timer';
if(timeLeft<=0){{clearInterval(timerInterval);submitTest();}}
}},1000);
}}
function submitTest(){{
if(submitted)return;submitted=true;
if(timerInterval)clearInterval(timerInterval);
let correct=0;
for(let i=1;i<=TOTAL;i++){{
const sel=document.querySelector(`input[name="q${{i}}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${{i}}"]`);
if(sel&&sel.value==='1'){{correct++;}}
opts.forEach(o=>{{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
}});
}}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
const pct=Math.round((correct/TOTAL)*100);
const panel=document.getElementById('resultPanel');
const title=document.getElementById('resultTitle');
const score=document.getElementById('resultScore');
const detail=document.getElementById('resultDetail');
panel.style.display='block';
score.textContent=`${{correct}} / ${{TOTAL}}（${{pct}}%）`;
if(pct>=90){{title.textContent='🎉 すばらしい！';score.className='result-score excellent';}}
else if(pct>=70){{title.textContent='👍 よくできました！';score.className='result-score good';}}
else if(pct>=50){{title.textContent='📝 もうすこし！';score.className='result-score fair';}}
else{{title.textContent='💪 がんばりましょう！';score.className='result-score poor';}}
const timeUsed=TIME_LIMIT-timeLeft;
detail.innerHTML=`
<div class="result-item"><div class="label">せいかい</div><div class="value">${{correct}}/${{TOTAL}}</div></div>
<div class="result-item"><div class="label">じかん</div><div class="value">${{Math.floor(timeUsed/60)}}分${{timeUsed%60}}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({{behavior:'smooth'}});
}}
startTimer();
</script>
</body></html>
"""


def main() -> None:
    fsoup = BeautifulSoup(FUKUSHU.read_text(encoding="utf-8"), "html.parser")
    u = iter_fukushu_units(fsoup)
    if len(u) != FUKUSHU_QUESTION_COUNT:
        raise SystemExit(f"Expected {FUKUSHU_QUESTION_COUNT} fukushu units, got {len(u)}")

    for i, (fr, kr) in enumerate(PARTS, start=1):
        html = build_part(i, fr, kr)
        out = DIR / f"unit31-quiz-part{i}.html"
        out.write_text(html, encoding="utf-8")
        f_n = fr[1] - fr[0] + 1
        k_n = kr[1] - kr[0] + 1
        print(f"Wrote {out.name}  (復習 {f_n}問 + 漢字 {k_n}問 = {f_n + k_n}問)")


if __name__ == "__main__":
    main()
