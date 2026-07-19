#!/usr/bin/env python3
"""Merge n4-10min-test-v6..v10 into one HTML, grouped by skill; drop exact duplicate questions."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag

DIR = Path(__file__).resolve().parent
SOURCES = [DIR / f"n4-10min-test-v{i}.html" for i in range(6, 11)]
OUT = DIR / "n4-kakunin-v6-v10-summary-48.html"
TIME_LIMIT_SEC = 30 * 60

SECTION_SPECS = [
    ("1", "\u6f22\u5b57\u306e\u8aad\u307f"),
    ("2", "\u8a9e\u5f59"),
    ("3", "\u6587\u6cd5"),
    ("4", "\u8a00\u3044\u63db\u3048"),
    ("5", "\u6587\u306e\u7d44\u307f\u7acb\u3066"),
    ("6", "\u8aad\u89e3"),
]
SEC_FIELDS = ("kanji", "vocab", "gram", "para", "sent", "read")


def extract_sections(html: str) -> str:
    m = re.search(
        r"</header>\s*(.*?)\s*<button\s+class=\"btn-submit\"",
        html,
        re.DOTALL,
    )
    if not m:
        raise ValueError("Could not find section block")
    return m.group(1).strip()


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def question_fingerprint(q_div: BeautifulSoup) -> str:
    parts: list[str] = []
    rp = q_div.find("div", class_="reading-passage")
    if rp:
        parts.append(norm_text(rp.get_text(" ", strip=True)))
    qtext = q_div.find("div", class_="q-text")
    if qtext:
        qt = BeautifulSoup(str(qtext), "html.parser")
        for s in qt.find_all("span", class_="q-num"):
            s.decompose()
        parts.append(norm_text(qt.get_text(" ", strip=True)))
    opts = q_div.find("div", class_="options")
    if opts:
        for lab in opts.find_all("label"):
            parts.append(norm_text(lab.get_text(" ", strip=True)))
    return "|".join(parts)


def intro_after_title(section: BeautifulSoup) -> str:
    parts: list[str] = []
    seen_title = False
    for el in section.children:
        if not getattr(el, "name", None):
            continue
        if el.name == "div" and "section-title" in (el.get("class") or []):
            seen_title = True
            continue
        if not seen_title:
            continue
        if el.name == "p":
            parts.append(str(el))
        elif el.name == "div" and "question" in (el.get("class") or []):
            break
    return "\n".join(parts)


def renumber_question_div(q_div: BeautifulSoup, n: int) -> None:
    for inp in q_div.find_all("input", type="radio"):
        inp["name"] = f"q{n}"
        oid = inp.get("id") or ""
        m = re.fullmatch(r"q\d+([a-d])", oid)
        if m:
            inp["id"] = f"q{n}{m.group(1)}"
    for lab in q_div.find_all("label"):
        fid = lab.get("for") or ""
        m = re.fullmatch(r"q\d+([a-d])", fid)
        if m:
            lab["for"] = f"q{n}{m.group(1)}"
    num = q_div.find("span", class_="q-num")
    if num:
        num.string = str(n)


def collect_questions_by_skill() -> tuple[list[str], list[list[BeautifulSoup]]]:
    per_skill: list[list[BeautifulSoup]] = [[] for _ in range(6)]
    for path in SOURCES:
        body = extract_sections(path.read_text(encoding="utf-8"))
        soup = BeautifulSoup(body, "html.parser")
        secs = soup.find_all("div", class_="section")
        if len(secs) != 6:
            raise ValueError(f"{path.name}: expected 6 sections, got {len(secs)}")
        for si, sec in enumerate(secs):
            for q in sec.find_all("div", class_="question"):
                per_skill[si].append(q)

    v1_body = extract_sections(SOURCES[0].read_text(encoding="utf-8"))
    soup1 = BeautifulSoup(v1_body, "html.parser")
    v1_secs = soup1.find_all("div", class_="section")
    intros = [intro_after_title(s) for s in v1_secs]

    return intros, per_skill


def dedupe_globally_ordered(
    per_skill: list[list[BeautifulSoup]],
) -> tuple[list[list[str]], int]:
    """First occurrence in skill order (もんだい1→6, each v6→v10) wins."""
    seen: set[str] = set()
    out: list[list[str]] = [[] for _ in range(6)]
    raw = 0
    for si in range(6):
        for q in per_skill[si]:
            raw += 1
            qd = BeautifulSoup(str(q), "html.parser").find("div", class_="question")
            if not qd:
                raise ValueError("missing .question")
            fp = question_fingerprint(qd)
            if fp in seen:
                continue
            seen.add(fp)
            out[si].append(str(qd))
    kept = sum(len(out[si]) for si in range(6))
    return out, raw - kept


def count_questions_in_fragment(html_frag: str) -> int:
    frag = BeautifulSoup(html_frag, "html.parser")
    root = frag.find()
    if root and "reading-bundle" in (root.get("class") or []):
        return len(root.find_all("div", class_="question", recursive=False))
    return len(frag.find_all("div", class_="question"))


def _mondai6_first_question(path: Path) -> BeautifulSoup:
    body = extract_sections(path.read_text(encoding="utf-8"))
    soup = BeautifulSoup(body, "html.parser")
    secs = soup.find_all("div", class_="section")
    if len(secs) < 6:
        raise ValueError(f"{path.name}: expected 6 sections")
    qs = secs[5].find_all("div", class_="question", recursive=False)
    if not qs:
        raise ValueError(f"{path.name}: no reading questions")
    return BeautifulSoup(str(qs[0]), "html.parser").find("div", class_="question")


def _reading_passage_contents(q_div: BeautifulSoup) -> str:
    rp = q_div.find("div", class_="reading-passage")
    if not rp:
        return ""
    return rp.decode_contents()


def _strip_reading_passage(q_div: BeautifulSoup) -> BeautifulSoup:
    qd = BeautifulSoup(str(q_div), "html.parser").find("div", class_="question")
    if not qd:
        raise ValueError("missing .question")
    rp = qd.find("div", class_="reading-passage")
    if rp:
        rp.decompose()
    return qd


def _add_reading_question(
    soup: BeautifulSoup,
    bundle: Tag,
    q_text: str,
    choices: list[tuple[str, str]],
    explanation: str,
) -> None:
    """choices: (\"1. ...\", \"0\"|\"1\") を4つ。正解は1つだけ \"1\"。"""
    q = soup.new_tag("div", attrs={"class": "question"})
    qt = soup.new_tag("div", attrs={"class": "q-text"})
    nspan = soup.new_tag("span", attrs={"class": "q-num"})
    nspan.string = "0"
    qt.append(nspan)
    qt.append(q_text)
    q.append(qt)
    opts = soup.new_tag("div", attrs={"class": "options"})
    letters = "abcd"
    for i, (lab_text, val) in enumerate(choices):
        oid = f"q0{letters[i]}"
        opt = soup.new_tag("div", attrs={"class": "option"})
        inp = soup.new_tag(
            "input",
            attrs={"type": "radio", "name": "q0", "id": oid, "value": val},
        )
        lab = soup.new_tag("label", attrs={"for": oid})
        lab.string = lab_text
        opt.append(inp)
        opt.append(lab)
        opts.append(opt)
    q.append(opts)
    ex = soup.new_tag("div", attrs={"class": "explanation"})
    ex.string = explanation
    q.append(ex)
    bundle.append(q)


def merged_reading_bundles() -> list[str]:
    """\u8a18\u4e8b1\uff1a\u5730\u57df\u306e\u6848\u5185\uff08\u56f3\u66f8\u9928\u2192\u55ab\u8336\u5e97\u2192\u30a2\u30eb\u30d0\u30a4\u30c8\uff09\u3002\u8a18\u4e8b2\uff1a\u697d\u3057\u307f\u30fb\u30a4\u30d9\u30f3\u30c8\uff08\u82b1\u898b\u2192\u30b3\u30f3\u30b5\u30fc\u30c8\uff09\u300243\u201347 \u306f\u672c\u6587\u306b\u5408\u308f\u305b\u3066\u5225\u51fa\u984c\u3002"""
    q_v7 = _mondai6_first_question(DIR / "n4-10min-test-v7.html")
    q_v8 = _mondai6_first_question(DIR / "n4-10min-test-v8.html")
    q_v9 = _mondai6_first_question(DIR / "n4-10min-test-v9.html")
    q_v6 = _mondai6_first_question(DIR / "n4-10min-test-v6.html")
    q_v10 = _mondai6_first_question(DIR / "n4-10min-test-v10.html")

    soup = BeautifulSoup("", "html.parser")
    b1 = soup.new_tag("div", attrs={"class": "reading-bundle"})
    rp1 = soup.new_tag("div", attrs={"class": "reading-passage"})
    # \u8a18\u4e8b1\uff1a\u56f3\u66f8\u9928 \u2192 \u55ab\u8336\u5e97 \u2192 \u30b3\u30f3\u30d3\u30cb\u6c42\u4eba
    inner1 = (
        _reading_passage_contents(q_v7)
        + "<br/><br/>"
        + _reading_passage_contents(q_v8)
        + "<br/><br/>"
        + _reading_passage_contents(q_v9)
    )
    rp1.append(BeautifulSoup(inner1, "html.parser"))
    b1.append(rp1)

    _add_reading_question(
        soup,
        b1,
        "\u56f3\u66f8\u9928\u3067\u672c\u3092\u501f\u308a\u308b\u3068\u304d\u3001\u4f55\u304c\u5fc5\u8981\u3067\u3059\u304b\u3002",
        [
            ("1. \u304a\u91d1\u3060\u3051", "0"),
            ("2. \u30ab\u30fc\u30c9", "1"),
            ("3. \u4f55\u3082\u3044\u308a\u307e\u305b\u3093", "0"),
            ("4. \u5b66\u751f\u8a3c\u3060\u3051", "0"),
        ],
        "\u2705 \u6b63\u89e3\uff1a2 \u2014 \u672c\u6587\u306b\u300c\u672c\u3092\u501f\u308a\u308b\u3068\u304d\u306f\u3001\u30ab\u30fc\u30c9\u304c\u5fc5\u8981\u3067\u3059\u300d\u3068\u3042\u308a\u307e\u3059\u3002",
    )
    _add_reading_question(
        soup,
        b1,
        "\u65b0\u3057\u3044\u55ab\u8336\u5e97\u306f\u3001\u3044\u3064\u958b\u304d\u307e\u3059\u304b\u3002",
        [
            ("1. \u4eca\u6708", "0"),
            ("2. \u6765\u6708", "1"),
            ("3. \u5148\u9031", "0"),
            ("4. \u6bce\u5e74", "0"),
        ],
        "\u2705 \u6b63\u89e3\uff1a2 \u2014 \u672c\u6587\u306b\u300c\u6765\u6708\u3001\u65b0\u3057\u3044\u55ab\u8336\u5e97\u304c\u99c5\u306e\u524d\u306b\u958b\u304d\u307e\u3059\u300d\u3068\u3042\u308a\u307e\u3059\u3002",
    )
    _add_reading_question(
        soup,
        b1,
        "\u30a2\u30eb\u30d0\u30a4\u30c8\u306e\u52e4\u52d9\u6642\u9593\u306b\u3064\u3044\u3066\u3001\u672c\u6587\u3068\u5408\u3063\u3066\u3044\u308b\u3082\u306e\u306f\u3069\u308c\u3067\u3059\u304b\u3002",
        [
            ("1. 1\u65e54\u6642\u9593\u304b\u3089\u3067\u304d\u308b", "1"),
            ("2. 1\u65e58\u6642\u9593\u50cd\u304f", "0"),
            ("3. \u90311\u56de\u3060\u3051\u3067\u3088\u3044", "0"),
            ("4. \u7d4c\u9a13\u304c3\u5e74\u4ee5\u4e0a\u5fc5\u8981", "0"),
        ],
        "\u2705 \u6b63\u89e3\uff1a1 \u2014 \u672c\u6587\u306b\u300c\u52e4\u52d9\u6642\u9593\u306f1\u65e54\u6642\u9593\u304b\u3089\u3067\u3059\u300d\u3068\u3042\u308a\u307e\u3059\u3002",
    )

    soup2 = BeautifulSoup("", "html.parser")
    b2 = soup2.new_tag("div", attrs={"class": "reading-bundle"})
    rp2 = soup2.new_tag("div", attrs={"class": "reading-passage"})
    # \u8a18\u4e8b2\uff1a\u6625\u306e\u82b1\u898b \u2192 \u9031\u672b\u306e\u30b3\u30f3\u30b5\u30fc\u30c8
    inner2 = _reading_passage_contents(q_v6) + "<br/><br/>" + _reading_passage_contents(q_v10)
    rp2.append(BeautifulSoup(inner2, "html.parser"))
    b2.append(rp2)

    _add_reading_question(
        soup2,
        b2,
        "\u82b1\u898b\u306b\u3064\u3044\u3066\u3001\u672c\u6587\u3068\u5408\u3063\u3066\u3044\u308b\u3082\u306e\u306f\u3069\u308c\u3067\u3059\u304b\u3002",
        [
            ("1. \u4e00\u4eba\u3067\u884c\u304f\u4eba\u304c\u591a\u3044", "0"),
            ("2. \u685c\u306e\u6728\u306e\u4e0b\u3067\u304a\u5f01\u5f53\u3092\u98df\u3079\u305f\u308a\u3059\u308b", "1"),
            ("3. \u685c\u306f1\u304b\u6708\u54b2\u304d\u307e\u3059", "0"),
            ("4. \u590f\u306b\u82b1\u898b\u3092\u3057\u307e\u3059", "0"),
        ],
        "\u2705 \u6b63\u89e3\uff1a2 \u2014 \u672c\u6587\u306b\u300c\u685c\u306e\u6728\u306e\u4e0b\u3067\u3001\u304a\u5f01\u5f53\u3092\u98df\u3079\u305f\u308a\u3001\u304a\u9152\u3092\u98f2\u3093\u3060\u308a\u3057\u307e\u3059\u300d\u3068\u3042\u308a\u307e\u3059\u3002",
    )
    _add_reading_question(
        soup2,
        b2,
        "\u30b3\u30f3\u30b5\u30fc\u30c8\u306e\u958b\u50ac\u6642\u9593\u3068\u3057\u3066\u3001\u672c\u6587\u3068\u5408\u3063\u3066\u3044\u308b\u3082\u306e\u306f\u3069\u308c\u3067\u3059\u304b\u3002",
        [
            ("1. \u5348\u524d10\u6642\u304b\u3089\u6b63\u5348\u307e\u3067", "0"),
            ("2. \u5348\u5f8c2\u6642\u304b\u30894\u6642\u307e\u3067", "1"),
            ("3. \u591c8\u6642\u304b\u308910\u6642\u307e\u3067", "0"),
            ("4. \u7d42\u65e5", "0"),
        ],
        "\u2705 \u6b63\u89e3\uff1a2 \u2014 \u672c\u6587\u306b\u300c\u5348\u5f8c2\u6642\u304b\u30894\u6642\u307e\u3067\u3067\u3059\u300d\u3068\u3042\u308a\u307e\u3059\u3002",
    )

    return [str(b1), str(b2)]


READING_SECTION_INTRO = (
    '<p style="color:#718096;font-size:.9em;margin-bottom:14px;line-height:1.6">'
    + "\u8aad\u89e3\u306f<b>\u8a18\u4e8b\u304c2\u672c</b>\u3042\u308a\u307e\u3059\u3002"
    + "<b>1\u672c\u76ee</b>\u306f\u3001\u56f3\u66f8\u9928\u30fb\u55ab\u8336\u5e97\u30fb\u30b3\u30f3\u30d3\u30cb\u306e\u30a2\u30eb\u30d0\u30a4\u30c8\u52df\u96c6\u306a\u3069\u3001"
    + "\u5730\u57df\u306e<b>\u65bd\u8a2d\u3084\u304a\u5e97\u306b\u3064\u3044\u3066\u306e\u6848\u5185</b>\u3067\u3059\uff08<b>3\u554f</b>\uff09\u3002"
    + "<b>2\u672c\u76ee</b>\u306f\u3001\u6625\u306e\u82b1\u898b\u3068\u5e02\u6c11\u4f1a\u9928\u306e\u30b3\u30f3\u30b5\u30fc\u30c8\u306a\u3069\u3001"
    + "<b>\u697d\u3057\u307f\u3084\u6587\u5316\u306e\u30a4\u30d9\u30f3\u30c8</b>\u306b\u3064\u3044\u3066\u3067\u3059\uff08<b>2\u554f</b>\uff09\u3002"
    + "\u540c\u3058\u8a18\u4e8b\u306b\u623b\u308a\u306a\u304c\u3089\u78ba\u8a8d\u3057\u3066\u3082\u5927\u4e08\u592b\u3067\u3059\u3002</p>\n"
)

BUNDLE_CSS = """
<style>
.reading-bundle{border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin-bottom:22px;background:#fafcff;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.reading-bundle .reading-passage{margin-bottom:8px}
.reading-bundle .question{padding-top:14px;margin-top:12px;border-top:1px solid #e2e8f0}
</style>
"""


def build_merged_body(intros: list[str], per_skill_html: list[list[str]]) -> str:
    parts: list[str] = []
    qn = 1
    for si, ((num, label), intro) in enumerate(zip(SECTION_SPECS, intros)):
        block = per_skill_html[si]
        if not block:
            continue
        cnt = sum(count_questions_in_fragment(qh) for qh in block)
        title = (
            f"\u3082\u3093\u3060\u3044{num} \u2014 {label}\uff08{cnt}\u554f\uff09"
        )
        block_q: list[str] = []
        for qh in block:
            frag = BeautifulSoup(qh, "html.parser")
            root = frag.find()
            if root and "reading-bundle" in (root.get("class") or []):
                for q_div in root.find_all("div", class_="question", recursive=False):
                    renumber_question_div(q_div, qn)
                    qn += 1
                block_q.append(str(root))
            else:
                q_div = frag.find("div", class_="question")
                if not q_div:
                    raise ValueError("missing .question")
                renumber_question_div(q_div, qn)
                block_q.append(str(q_div))
                qn += 1
        if si == 5:
            intro_block = READING_SECTION_INTRO
        else:
            intro_block = f"\n{intro}\n" if intro.strip() else "\n"
        parts.append(
            f'<div class="section">\n'
            f'<div class="section-title">{title}</div>'
            f"{intro_block}"
            f"{chr(10).join(block_q)}\n"
            f"</div>"
        )
    return "\n\n".join(parts)


def make_score_if_chain(counts: list[int]) -> str:
    chunks: list[str] = []
    acc = 0
    first = True
    for idx, n in enumerate(counts):
        if n == 0:
            continue
        acc += n
        field = SEC_FIELDS[idx]
        if first:
            chunks.append(f"if(i<={acc}){{if(ok)sec.{field}++;}}")
            first = False
        else:
            chunks.append(f"else if(i<={acc}){{if(ok)sec.{field}++;}}")
    return "".join(chunks)


def main() -> None:
    intros, per_skill = collect_questions_by_skill()
    per_skill_html, n_dup = dedupe_globally_ordered(per_skill)
    per_skill_html[5] = merged_reading_bundles()
    counts = [
        sum(count_questions_in_fragment(qh) for qh in per_skill_html[si])
        for si in range(6)
    ]
    total = sum(counts)
    if total == 0:
        raise ValueError("no questions left after deduplication")

    page_title = f"JLPT N4 6-10\u307e\u3068\u3081\u30c6\u30b9\u30c8\uff0830\u5206\u30fb{total}\u554f\uff09"

    time_limit_sec = TIME_LIMIT_SEC
    timer_display = "30:00"

    merged = build_merged_body(intros, per_skill_html)
    score_branch = make_score_if_chain(counts)

    v6 = SOURCES[0].read_text(encoding="utf-8")
    end_head = v6.index("</head>") + len("</head>")
    head = v6[:end_head]
    head = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{page_title}</title>",
        head,
        count=1,
    )
    head = head.replace("</head>", BUNDLE_CSS + "\n</head>")

    m90 = "\U0001f389 \u7d20\u6674\u3089\u3057\u3044\uff01"
    m70 = "\U0001f44d \u3088\u304f\u3067\u304d\u307e\u3057\u305f\uff01"
    m50 = "\U0001f4dd \u3082\u3046\u5c11\u3057\uff01"
    m00 = "\U0001f4aa \u304c\u3093\u3070\u308a\u307e\u3057\u3087\u3046\uff01"
    lbl_kanji = "\u6f22\u5b57\u306e\u8aad\u307f"
    lbl_vocab = "\u8a9e\u5f59"
    lbl_gram = "\u6587\u6cd5"
    lbl_para = "\u8a00\u3044\u63db\u3048"
    lbl_sent = "\u6587\u306e\u7d44\u307f\u7acb\u3066"
    lbl_read = "\u8aad\u89e3"
    lbl_time = "\u6240\u8981\u6642\u9593"
    btn_submit = "\u63a1\u70b9\u3059\u308b"

    shuffle_js = r"""
function shuffleArray(a){
for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
}
function relabelChoiceNumber(labelEl,idx){
if(!labelEl)return;
const t=labelEl.textContent.replace(/^[1-4][\.\uFF0E]\s*/u,"").trim();
labelEl.textContent=(idx+1)+". "+t;
}
function shuffleAllChoices(){
document.querySelectorAll(".question").forEach(q=>{
const box=q.querySelector(".options");
if(!box)return;
const opts=[...box.querySelectorAll(":scope > .option")];
if(opts.length<2)return;
opts.forEach(o=>{const inp=o.querySelector('input[type="radio"]');o._isCorrect=inp&&inp.value==="1";});
shuffleArray(opts);
const qname=opts[0].querySelector('input[type="radio"]').name;
const letters="abcdefghijklmnopqrstuvwxyz";
opts.forEach((o,i)=>{
const inp=o.querySelector('input[type="radio"]');
const lab=o.querySelector("label");
const suf=letters[i];
inp.name=qname;
inp.id=qname+suf;
if(lab)lab.setAttribute("for",inp.id);
inp.value=o._isCorrect?"1":"0";
delete o._isCorrect;
relabelChoiceNumber(lab,i);
});
box.replaceChildren(...opts);
const expl=q.querySelector(".explanation");
if(expl){expl.textContent=expl.textContent.replace(/\u6b63\u89e3\uff1a\s*[1-4](\s*[\.\uFF0E]\s*|\s*[—\u2014]\s*)/u,"\u6b63\u89e3\uff1a");}
});
}
"""
    script = (
        "<script>\nconst TOTAL="
        + str(total)
        + ",TIME_LIMIT="
        + str(time_limit_sec)
        + ";"
        + shuffle_js
        + """let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){
timerInterval=setInterval(()=>{timeLeft--;const m=Math.floor(timeLeft/60),s=timeLeft%60;const el=document.getElementById('timer');el.textContent=`${m}:${s.toString().padStart(2,'0')}`;document.getElementById('progress').style.width=`${(timeLeft/TIME_LIMIT)*100}%`;if(timeLeft<=60)el.className='timer danger';else if(timeLeft<=180)el.className='timer warning';if(timeLeft<=0){clearInterval(timerInterval);submitTest();}},1000);}
function submitTest(){
if(submitted)return;submitted=true;clearInterval(timerInterval);
let correct=0;const sec={kanji:0,vocab:0,gram:0,para:0,sent:0,read:0};
for(let i=1;i<=TOTAL;i++){const sel=document.querySelector(`input[name="q${i}"]:checked`);const opts=document.querySelectorAll(`input[name="q${i}"]`);let ok=false;if(sel&&sel.value==='1'){ok=true;correct++;}opts.forEach(o=>{const p=o.parentElement;if(o.value==='1')p.classList.add('correct');else if(o.checked)p.classList.add('wrong');});
__SCORE_BRANCH__
}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
const pct=Math.round((correct/TOTAL)*100);const panel=document.getElementById('resultPanel');panel.style.display='block';
const score=document.getElementById('resultScore');score.textContent=`${correct} / ${TOTAL}（${pct}%）`;
const title=document.getElementById('resultTitle');
__TITLE_BRANCH__
const t=TIME_LIMIT-timeLeft;document.getElementById('resultDetail').innerHTML=__RESULT_DETAIL__;
document.getElementById('submitBtn').disabled=true;panel.scrollIntoView({behavior:'smooth'});}
shuffleAllChoices();
startTimer();
</script>"""
    )
    script = script.replace("__SCORE_BRANCH__", score_branch)
    script = script.replace(
        "__TITLE_BRANCH__",
        "if(pct>=90){title.textContent="
        + json.dumps(m90)
        + ";score.className='result-score excellent';}else if(pct>=70){title.textContent="
        + json.dumps(m70)
        + ";score.className='result-score good';}else if(pct>=50){title.textContent="
        + json.dumps(m50)
        + ";score.className='result-score fair';}else{title.textContent="
        + json.dumps(m00)
        + ";score.className='result-score poor';}",
    )
    c0, c1, c2, c3, c4, c5 = counts
    rd = (
        "`<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_kanji)[1:-1]
        + f"</div><div class=\"value\">${{sec.kanji}}/{c0}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_vocab)[1:-1]
        + f"</div><div class=\"value\">${{sec.vocab}}/{c1}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_gram)[1:-1]
        + f"</div><div class=\"value\">${{sec.gram}}/{c2}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_para)[1:-1]
        + f"</div><div class=\"value\">${{sec.para}}/{c3}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_sent)[1:-1]
        + f"</div><div class=\"value\">${{sec.sent}}/{c4}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_read)[1:-1]
        + f"</div><div class=\"value\">${{sec.read}}/{c5}</div></div>"
        "<div class=\"result-item\"><div class=\"label\">"
        + json.dumps(lbl_time)[1:-1]
        + "</div><div class=\"value\">${Math.floor(t/60)}分${t%60}秒</div></div>`"
    )
    script = script.replace("__RESULT_DETAIL__", rd)

    badge = f"\u5168{total}\u554f\u30fb\u5236\u965030\u5206"
    h1 = page_title

    out = f"""{head}
<body>
<div class="container">
<header>
<h1>{h1}</h1>
<div class="header-info">
<div class="timer" id="timer">{timer_display}</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge">{badge}</div>
</div>
</header>

{merged}

<button class="btn-submit" id="submitBtn" onclick="submitTest()">{btn_submit}</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>

{script}
</body>
</html>
"""

    OUT.write_text(out, encoding="utf-8")
    print(f"Wrote {OUT} ({total} questions, removed {n_dup} duplicates)")


if __name__ == "__main__":
    main()
