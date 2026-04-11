#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N2読解.md から読解テスト用 HTML を生成する。"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "N2読解.md"
IMG_DIR = ROOT / "文章用画像"
OUT_PATH = ROOT / "n2-reading-test.html"

HEADER_RE = re.compile(
    r"^(?P<level>#{2,3})\s+No\.(?P<num>\d+)（p\.(?P<page>\d+)）(?P<title>.*)$"
)
SECTION_WEEK_HEADER_RE = re.compile(r"^##\s+(第[1-9]週.+)$")
Q_START_RE = re.compile(r"^\*\*(問題[１２]|問\d?)\*\*\s*(.*)$")
ANSWER_RE = re.compile(r"^\*\*答え[：:](?P<rest>.+?)\*\*")
OPT_RE = re.compile(r"^(\d+)\.\s+(.*)$")
FOOTNOTE_LINE_RE = re.compile(
    r"^\s*(?:[-*•]\s+)?（※[0-9０-９]*）"
)

Q_TIMER_SEC = 300


def extract_footnote_lines(block: str) -> list[str]:
    lines = block.splitlines()
    cut = len(lines)
    for i, line in enumerate(lines):
        if Q_START_RE.match(line):
            cut = i
            break
    out: list[str] = []
    for line in lines[:cut]:
        if FOOTNOTE_LINE_RE.match(line):
            t = line.strip()
            if t.startswith(("- ", "* ", "• ")):
                t = t.split(None, 1)[-1] if len(t) > 2 else t
            out.append(t)
    return out


def footnotes_to_html(lines: list[str]) -> str:
    if not lines:
        return ""
    parts = []
    for t in lines:
        esc = html_lib.escape(t).replace("\n", "<br>\n")
        parts.append(f"<p>{esc}</p>")
    return f'<div class="passage-notes">{"".join(parts)}</div>'


def resolve_image_paths_split(page: int) -> tuple[list[str], list[str]]:
    rel = "文章用画像"
    if page == 87:
        primary: list[str] = []
        secondary: list[str] = []
        if (IMG_DIR / "p87-1.png").exists():
            primary.append(f"{rel}/p87-1.png")
        if (IMG_DIR / "p87-2.png").exists():
            secondary.append(f"{rel}/p87-2.png")
        return primary, secondary
    candidates = [
        f"p{page}.png",
        f"p{page}.jpg",
        f"p{page}.jpeg",
        f"{page:03d}.png",
        f"{page:03d}.jpg",
    ]
    for name in candidates:
        if (IMG_DIR / name).exists():
            return [f"{rel}/{name}"], []
    return [], []


def figures_html(paths: list[str], page: int, extra_class: str = "") -> str:
    cls = "passage-img" + (f" {extra_class}" if extra_class else "")
    parts: list[str] = []
    for src in paths:
        parts.append(
            f'<figure class="{cls.strip()}"><img src="{html_lib.escape(src)}" '
            f'alt="p.{page} 本文" loading="lazy"></figure>'
        )
    return "".join(parts)


GRAPH_STEM_SKIP_LINE = re.compile(r"^[-*•]\s*[ABC]\s")
GRAPH_STEM_SKIP_CONTAINS = re.compile(r"（グラフ1")


def clean_no34_graph_stem(stem: str) -> str:
    out: list[str] = []
    for line in stem.split("\n"):
        t = line.strip()
        if GRAPH_STEM_SKIP_LINE.match(t):
            continue
        if GRAPH_STEM_SKIP_CONTAINS.search(t):
            continue
        out.append(line)
    return "\n".join(out).strip()


def parse_answers(answer_line: str) -> dict[str, int]:
    out: dict[str, int] = {}
    s = answer_line.strip()
    for m in re.finditer(r"問\s*(\d)\s*[：:　\s]*(\d)", s):
        out[f"問{m.group(1)}"] = int(m.group(2))
    m = re.search(r"問\s*[：:　\s]+(\d)(?!\d)", s)
    if m and "問1" not in out and "問2" not in out:
        out["問"] = int(m.group(1))
    for m in re.finditer(r"問題\s*([１２])\s*[：:　\s]*(\d)", s):
        key = "問題１" if m.group(1) == "１" else "問題２"
        out[key] = int(m.group(2))
    return out


EXPLAIN_Q2_SPLIT = re.compile(
    r"(?m)^(?=(?:問題２|問2)(?:（[^）]*）)?[：:])"
)


def extract_explanation_raw(block: str) -> str:
    """`> **[解説]**` から始まる引用ブロックを `---` まで読み取る。"""
    lines = block.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^>\s*\*\*\[解説\]\*\*(.*)$", ln)
        if m:
            tag = m.group(1).strip()
            if tag and not re.fullmatch(r"（[^）]+）", tag):
                out.append(tag)
            i += 1
            while i < len(lines):
                L = lines[i]
                if L.strip() == "---":
                    break
                if L.startswith("> "):
                    out.append(L[2:])
                elif L.startswith(">"):
                    d = L[1:].lstrip()
                    out.append(d)
                else:
                    if not L.strip():
                        i += 1
                        continue
                    break
                i += 1
            break
        i += 1
    return "\n".join(out).strip()


def split_explanation_for_questions(raw: str, n_questions: int) -> list[str]:
    if n_questions <= 0:
        return []
    if not raw.strip():
        return [""] * n_questions
    raw = raw.strip()
    if n_questions == 1:
        return [raw]
    parts = EXPLAIN_Q2_SPLIT.split(raw, maxsplit=1)
    if len(parts) == 2:
        a, b = parts[0].strip(), parts[1].strip()
        return [a, b] + [""] * (n_questions - 2)
    return [raw] + [""] * (n_questions - 1)


def markdown_inline_bold_to_html(text: str) -> str:
    if not text.strip():
        return ""
    chunks = re.split(r"(\*\*[^*]+\*\*)", text)
    sb: list[str] = []
    for ch in chunks:
        if ch.startswith("**") and ch.endswith("**") and len(ch) >= 4:
            inner = ch[2:-2]
            sb.append("<strong>" + html_lib.escape(inner) + "</strong>")
        else:
            sb.append(html_lib.escape(ch).replace("\n", "<br>\n"))
    return "".join(sb)


def build_explanation_panel(q: dict, scored: bool, correct: int | None) -> str:
    body = (q.get("explain_md") or "").strip()
    note_html = ""
    if body:
        note_html = (
            '<div class="explanation-note">'
            f"{markdown_inline_bold_to_html(body)}"
            "</div>"
        )
    if scored and correct is not None:
        return (
            '<div class="explanation">'
            '<div class="explanation-answer">'
            f"正解：{correct}. {html_lib.escape(q['options'][correct - 1])}"
            "</div>"
            f"{note_html}"
            "</div>"
        )
    frag = (
        '<div class="explanation no-key">'
        "採点用の答えは md に含まれていません。教材の正解表で確認してください。"
    )
    if note_html:
        frag += note_html
    frag += "</div>"
    return frag


def extract_questions(block: str) -> tuple[list[dict], dict[str, int]]:
    lines = block.splitlines()
    answers: dict[str, int] = {}
    for line in lines:
        am = ANSWER_RE.match(line)
        if am:
            answers.update(parse_answers(am.group("rest")))

    questions: list[dict] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = Q_START_RE.match(line)
        if not m:
            i += 1
            continue

        label_raw = m.group(1)
        rest = m.group(2).strip()
        stem_lines = [rest] if rest else []
        i += 1
        while i < len(lines):
            if OPT_RE.match(lines[i]):
                break
            if Q_START_RE.match(lines[i]) or ANSWER_RE.match(lines[i]):
                break
            if lines[i].strip() == "---":
                break
            stem_lines.append(lines[i])
            i += 1
        stem = "\n".join(sl for sl in stem_lines if sl is not None).strip()

        options: list[str] = []
        while i < len(lines):
            om = OPT_RE.match(lines[i])
            if not om:
                break
            options.append(om.group(2).strip())
            i += 1

        if label_raw in ("問題1", "問題１"):
            label = "問題１"
        elif label_raw in ("問題2", "問題２"):
            label = "問題２"
        elif label_raw.startswith("問"):
            label = label_raw
        else:
            label = label_raw

        if len(options) < 2 and "グラフ" in stem:
            options = ["グラフ1", "グラフ2", "グラフ3", "グラフ4"]
            answers["問"] = 3
            answers["問1"] = 3

        if len(options) >= 2:
            questions.append(
                {
                    "label": label,
                    "stem": stem,
                    "options": options[:4] if len(options) >= 4 else options,
                }
            )
        continue

    return questions, answers


def split_blocks(text: str) -> list[dict]:
    """No.XX で分割し、直前の「第N週」見出しを section_title に付与。"""
    lines = text.splitlines()
    blocks: list[dict] = []
    current: dict | None = None
    buf: list[str] = []
    last_section_title = "その他"

    def flush():
        nonlocal current, buf
        if current is not None:
            current["body"] = "\n".join(buf)
            blocks.append(current)
        current = None
        buf = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## N2読解2"):
            last_section_title = ""
            continue
        wm = SECTION_WEEK_HEADER_RE.match(stripped)
        if wm:
            last_section_title = wm.group(1).strip()
            continue
        m = HEADER_RE.match(line)
        if m:
            flush()
            title_part = m.group("title").strip()
            if re.match(r"^第[1-9]週", title_part):
                sec_t = title_part
            else:
                sec_t = last_section_title if last_section_title else "N2読解2"
            current = {
                "num": int(m.group("num")),
                "page": int(m.group("page")),
                "title": title_part,
                "section_title": sec_t,
            }
            buf = []
            continue
        if current is not None:
            buf.append(line)
    flush()
    return blocks


def answer_for_question(q: dict, answers: dict[str, int]) -> int | None:
    label = q["label"]
    keys = [label]
    if label == "問題１":
        keys.extend(["問題1", "問1"])
    elif label == "問題２":
        keys.extend(["問題2", "問2"])
    elif label == "問1":
        keys.append("問題１")
    elif label == "問2":
        keys.append("問題２")
    elif label == "問":
        keys.extend(["問", "問1"])

    for k in keys:
        if k in answers:
            return answers[k]
    return None


def build_html(blocks: list[dict]) -> tuple[str, int, int, int]:
    q_global = 0
    scored_q = 0
    n_blocks = len(blocks)

    hub_cards: list[str] = []
    block_players: list[str] = []

    for bi, b in enumerate(blocks):
        qs, ans = extract_questions(b["body"])
        raw_ex = extract_explanation_raw(b["body"])
        ex_parts = split_explanation_for_questions(raw_ex, len(qs))
        for j, q in enumerate(qs):
            q["explain_md"] = ex_parts[j] if j < len(ex_parts) else ""
        n_questions = len(qs)

        full_title_plain = f'No.{b["num"]:02d}（p.{b["page"]}）{b["title"]}'
        title_attr = html_lib.escape(full_title_plain, quote=True)
        sec_esc = html_lib.escape(b["section_title"], quote=True)
        pick_label = (
            f'No.{b["num"]:02d} — {b["title"]}（p.{b["page"]}・{n_questions}問）'
        )
        pick_esc = html_lib.escape(pick_label)
        hub_cards.append(
            f'<button type="button" class="btn-pick-example" data-block="{bi}" '
            f'title="{sec_esc}">{pick_esc}</button>'
        )

        slides: list[str] = []
        imgs_top, imgs_after_q = resolve_image_paths_split(b["page"])
        if imgs_top:
            img_tags = figures_html(imgs_top, b["page"])
        else:
            img_tags = (
                f'<p class="img-missing">画像が見つかりません（p.{b["page"]}）</p>'
            )
        notes_html = footnotes_to_html(extract_footnote_lines(b["body"]))

        # 本文画像・米印注はブロック先頭に 1 回だけ（設問ごとには繰り返さない）
        passage_once = (
            f'<div class="q-slide block-passage-once">'
            f'<div class="slide-card slide-card-passage">'
            f'<div class="passage-images">{img_tags}</div>{notes_html}'
            f"</div></div>"
        )
        slides.append(passage_once)

        for q in qs:
            q_global += 1
            gid = q_global
            correct = answer_for_question(q, ans)
            if correct is not None:
                scored_q += 1

            stem_raw = q["stem"]
            if b["num"] == 34:
                stem_raw = clean_no34_graph_stem(stem_raw)
            stem_esc = html_lib.escape(stem_raw).replace("\n", "<br>\n")
            opts_html = []
            for idx, opt in enumerate(q["options"], start=1):
                oid = f"q{gid}_{idx}"
                is_correct = correct == idx if correct is not None else False
                data_ok = "1" if is_correct else "0"
                opt_esc = html_lib.escape(opt)
                opts_html.append(
                    f'<div class="option" data-correct="{data_ok}">'
                    f'<input type="radio" name="q{gid}" id="{oid}" value="{idx}">'
                    f'<label for="{oid}">{idx}. {opt_esc}</label></div>'
                )

            scored = correct is not None
            explain = build_explanation_panel(q, scored, correct)

            after_opts = ""
            if b["num"] == 34 and imgs_after_q:
                after_opts = figures_html(
                    imgs_after_q,
                    b["page"],
                    extra_class="passage-img-after-options",
                )

            q_html = (
                f'<div class="question" data-qid="{gid}" '
                f'data-scored="{"1" if scored else "0"}">'
                f'<div class="q-stem-row"><span class="q-num">{gid}</span>'
                f'<div class="q-stem">{stem_esc}</div></div>'
                f'<div class="options">{" ".join(opts_html)}</div>'
                f"{after_opts}{explain}</div>"
            )

            slides.append(
                f'<div class="q-slide" data-slide-index="{len(slides)}">'
                f'<div class="slide-card slide-card-question">{q_html}</div></div>'
            )

        block_players.append(
            f'<div class="block-player" id="block-player-{bi}" '
            f'data-player-title="{title_attr}" hidden>{"".join(slides)}</div>'
        )

    total_q = q_global

    css = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
.test-header{background:#d81b60;color:#fff;padding:24px;border-radius:16px;margin-bottom:20px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(216,27,96,.35)}
.header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:0;flex-wrap:wrap}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums;color:#fff}
.timer.warning{color:#ffd700;animation:pulse 1s infinite}
.timer.danger{color:#ff4757;animation:pulse .5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}
.score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}
#view-hub[hidden]{display:none!important}
.floor-menu{margin-bottom:20px}
.menu-header{background:#d81b60;color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(216,27,96,.35)}
.menu-header h1{font-size:1.5em;margin:0;font-weight:700}
.section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-title{font-size:1.1em;font-weight:bold;color:#d81b60;border-left:4px solid #d81b60;padding-left:12px;margin-bottom:16px}
.example-picker{display:grid;gap:10px}
.btn-pick-example{
  display:block;width:100%;text-align:left;
  padding:14px 16px;
  background:#fff;
  color:#1a202c;
  border:2px solid #e2e8f0;
  border-radius:12px;
  font-size:1em;
  font-weight:600;
  cursor:pointer;
  transition:border-color .2s,background .2s,box-shadow .2s;
  touch-action:manipulation;
  line-height:1.45;
  word-break:break-word;
}
.btn-pick-example:hover{border-color:#d81b60;background:#fce4ec;box-shadow:0 2px 8px rgba(216,27,96,.12)}
#view-work[hidden]{display:none!important}
.work-nav-row{margin-bottom:12px}
.btn-back{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:10px 16px;background:#fff;color:#d81b60;border:2px solid #d81b60;border-radius:10px;font-size:.95em;font-weight:600;cursor:pointer;touch-action:manipulation;transition:background .2s,color .2s}
.btn-back:hover{background:#fce4ec}
#chromeBlockTitle{font-size:1.1em;font-weight:bold;color:#d81b60;border-left:4px solid #d81b60;padding-left:12px;margin-bottom:16px;line-height:1.45}
.btn-submit{display:block;width:100%;min-height:48px;padding:14px 16px;background:#d81b60;color:#fff;border:none;border-radius:12px;font-size:1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(216,27,96,.35)}
.btn-submit:disabled{opacity:.55;cursor:not-allowed;transform:none;box-shadow:none;background:#a0aec0}
.block-title{font-size:1.02rem;color:#d81b60;border-left:4px solid #d81b60;padding-left:12px;margin-bottom:14px}
.slide-card{background:#fff;border-radius:14px;padding:20px 18px;margin-bottom:8px;box-shadow:0 2px 10px rgba(0,0,0,.06)}
.passage-images{margin-bottom:16px}
.passage-img{margin:0 0 12px;text-align:center}
.passage-img img{max-width:100%;height:auto;border:1px solid #e2e8f0;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.passage-img-after-options{margin:16px 0 0;text-align:center}
.passage-img-after-options img{max-width:100%;height:auto;border:1px solid #e2e8f0;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.passage-notes{margin:0 0 16px;padding:14px 16px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;font-size:.88rem;color:#4a5568;line-height:1.65}
.passage-notes p{margin:0 0 .55em}
.passage-notes p:last-child{margin-bottom:0}
.img-missing{color:#c05621;font-size:.9rem;padding:12px;background:#fffaf0;border-radius:8px}
.block-player .q-slide{display:block;margin-bottom:20px}
.block-player .q-slide:last-child{margin-bottom:0}
.block-passage-once .slide-card-passage{padding-bottom:16px}
.slide-card-question{padding-top:16px;border-top:1px solid #edf2f7}
.block-passage-once + .q-slide .slide-card-question{border-top:none;padding-top:0}
.question{padding:12px 0 0;border-top:none}
.q-stem-row{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}
.q-num{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;min-width:36px;height:36px;padding:0 10px;background:#d81b60;color:#fff;border-radius:10px;font-weight:700;font-size:.95rem;line-height:1.2}
.q-stem{flex:1;min-width:0;font-size:1rem;line-height:1.75;font-weight:500}
.options{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:640px){.options{grid-template-columns:1fr}}
.option input{display:none}
.option label{display:flex;align-items:flex-start;min-height:48px;padding:12px 14px;border:2px solid #e2e8f0;border-radius:10px;cursor:pointer;transition:.15s;font-size:.95rem;touch-action:manipulation}
.option label:hover{border-color:#d81b60;background:#fce4ec}
.option input:checked+label{border-color:#d81b60;background:#fce4ec;color:#ad1457;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.option.picked-nokey label{border-color:#ad1457!important;background:#fff0f3!important;color:#880e4f!important}
.explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55;color:#744210}
.explanation.show{display:block}
.explanation.no-key{border-left-color:#a0aec0;color:#4a5568;background:#f7fafc}
.explanation-answer{font-weight:600}
.explanation-note{margin-top:8px;padding-top:8px;border-top:1px dashed #ecc94b;font-size:.92em;line-height:1.65;color:#5c4a21}
.score-result{margin-top:16px;padding:14px 18px;background:#fff;border-radius:12px;text-align:center;font-size:1.35em;font-weight:700;color:#1a202c;border:2px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.score-result[hidden]{display:none!important}
"""

    js = f"""
const Q_TIMER_SEC = {Q_TIMER_SEC};
const N_BLOCKS = {n_blocks};
const WARN_SEC = Math.max(60, Math.floor(Q_TIMER_SEC * 0.3));

let currentBlock = -1;
let timerInterval = null;
let timeLeft = Q_TIMER_SEC;
let submitted = false;

function clearQTimer() {{
  if (timerInterval) {{ clearInterval(timerInterval); timerInterval = null; }}
}}

function updateTimerUi() {{
  const el = document.getElementById('workTimer');
  const bar = document.getElementById('workProgress');
  if (!el || !bar) return;
  const t = Math.max(0, timeLeft);
  const m = Math.floor(t / 60);
  const s = t % 60;
  el.textContent = m + ':' + String(s).padStart(2, '0');
  el.className = 'timer';
  if (t <= 60) el.classList.add('danger');
  else if (t <= WARN_SEC) el.classList.add('warning');
  bar.style.width = (Q_TIMER_SEC ? (t / Q_TIMER_SEC) * 100 : 0) + '%';
}}

function startQTimer() {{
  clearQTimer();
  timeLeft = Q_TIMER_SEC;
  updateTimerUi();
  timerInterval = setInterval(() => {{
    if (submitted) return;
    timeLeft--;
    updateTimerUi();
    if (timeLeft <= 0) {{
      clearQTimer();
      submitTest();
    }}
  }}, 1000);
}}

function setWorkBadgeForBlock(bi) {{
  const badge = document.getElementById('workScoreBadge');
  if (!badge) return;
  const panel = document.getElementById('block-player-' + bi);
  const n = panel ? panel.querySelectorAll('.question').length : 0;
  badge.textContent = n ? ('この教材 ' + n + '問') : '—';
}}

function resetBlockQuestionUi(panel) {{
  if (!panel) return;
  panel.querySelectorAll('.question').forEach(el => {{
    el.querySelectorAll('input[type="radio"]').forEach(inp => {{ inp.checked = false; }});
    el.querySelectorAll('.option').forEach(o => {{
      o.classList.remove('correct', 'wrong', 'picked-nokey');
    }});
    el.querySelectorAll('.explanation').forEach(ex => ex.classList.remove('show'));
  }});
}}

function openBlock(bi) {{
  submitted = false;
  currentBlock = bi;
  document.getElementById('view-hub').setAttribute('hidden', '');
  document.getElementById('view-work').removeAttribute('hidden');
  for (let i = 0; i < N_BLOCKS; i++) {{
    const el = document.getElementById('block-player-' + i);
    if (!el) continue;
    if (i === bi) {{ el.removeAttribute('hidden'); }}
    else {{ el.setAttribute('hidden', ''); }}
  }}
  const panel = document.getElementById('block-player-' + bi);
  resetBlockQuestionUi(panel);
  const title = panel ? panel.getAttribute('data-player-title') : '';
  const ht = document.getElementById('chromeBlockTitle');
  if (ht) ht.textContent = title || '';
  setWorkBadgeForBlock(bi);
  const scoreOut = document.getElementById('scoreResult');
  if (scoreOut) {{
    scoreOut.textContent = '';
    scoreOut.setAttribute('hidden', '');
  }}
  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = false;
  startQTimer();
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function goHub() {{
  clearQTimer();
  submitted = false;
  currentBlock = -1;
  timeLeft = Q_TIMER_SEC;
  document.getElementById('view-work').setAttribute('hidden', '');
  document.getElementById('view-hub').removeAttribute('hidden');
  for (let i = 0; i < N_BLOCKS; i++) {{
    const el = document.getElementById('block-player-' + i);
    if (el) el.setAttribute('hidden', '');
  }}
  for (let i = 0; i < N_BLOCKS; i++) {{
    resetBlockQuestionUi(document.getElementById('block-player-' + i));
  }}
  const scoreOut = document.getElementById('scoreResult');
  if (scoreOut) {{
    scoreOut.textContent = '';
    scoreOut.setAttribute('hidden', '');
  }}
  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = false;
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function submitTest() {{
  if (submitted) return;
  if (currentBlock < 0) return;
  const workPanel = document.getElementById('block-player-' + currentBlock);
  if (!workPanel) return;
  submitted = true;
  clearQTimer();

  const blockQs = workPanel.querySelectorAll('.question');
  let nKeyed = 0;
  let correct = 0;
  blockQs.forEach(el => {{
    const scored = el.dataset.scored === '1';
    const sel = el.querySelector('input[type="radio"]:checked');
    const opts = el.querySelectorAll('.option');
    opts.forEach(o => {{
      o.classList.remove('correct', 'wrong', 'picked-nokey');
      if (scored) {{
        if (o.dataset.correct === '1') o.classList.add('correct');
        else if (sel && o.contains(sel)) o.classList.add('wrong');
      }} else if (sel && o.contains(sel)) {{
        o.classList.add('picked-nokey');
      }}
    }});
    el.querySelectorAll('.explanation').forEach(e => e.classList.add('show'));
    if (scored) {{
      nKeyed++;
      if (sel) {{
        const p = sel.closest('.option');
        if (p && p.dataset.correct === '1') correct++;
      }}
    }}
  }});

  const scoreOut = document.getElementById('scoreResult');
  if (scoreOut) {{
    if (nKeyed > 0) {{
      scoreOut.textContent = '正解 ' + correct + ' / ' + nKeyed;
      scoreOut.removeAttribute('hidden');
      scoreOut.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }} else {{
      scoreOut.textContent = '';
      scoreOut.setAttribute('hidden', '');
    }}
  }}

  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = true;
}}

document.addEventListener('DOMContentLoaded', () => {{
  document.querySelectorAll('.btn-pick-example').forEach(btn => {{
    btn.addEventListener('click', () => openBlock(parseInt(btn.dataset.block, 10)));
  }});
  document.getElementById('btnBackHub').addEventListener('click', goHub);
  document.getElementById('submitBtnWork').addEventListener('click', submitTest);
}});
"""

    hub_picker = "".join(hub_cards)
    players_html = "".join(block_players)

    html_out = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>N2 読解 練習テスト（全{total_q}問・教材{n_blocks}本）</title>
<style>{css}</style>
</head>
<body>
<div class="container">
<div id="view-hub" class="floor floor-menu">
<header class="menu-header">
<h1>N2 読解 練習テスト</h1>
</header>
<div class="section">
<div class="section-title">読解問題を選ぶ（全{total_q}問・教材{n_blocks}本）</div>
<div class="example-picker">
{hub_picker}
</div>
</div>
</div>

<div id="view-work" hidden>
<div class="work-nav-row">
<button type="button" class="btn-back" id="btnBackHub">← No.一覧</button>
</div>
<header class="test-header">
<div class="header-info">
<div class="timer" id="workTimer">5:00</div>
<div class="progress-bar"><div class="progress-fill" id="workProgress" style="width:100%"></div></div>
<div class="score-badge" id="workScoreBadge">—</div>
</div>
</header>
<h2 id="chromeBlockTitle"></h2>
{players_html}
<button type="button" class="btn-submit" id="submitBtnWork">採点する</button>
<div class="score-result" id="scoreResult" hidden></div>
</div>
</div>
<script>{js}</script>
</body>
</html>
"""
    return html_out, len(blocks), total_q, scored_q


def main() -> None:
    text = MD_PATH.read_text(encoding="utf-8")
    blocks = split_blocks(text)
    if not blocks:
        raise SystemExit("No blocks parsed; check markdown headers.")
    html_out, n_blocks, total_q, scored_q = build_html(blocks)
    OUT_PATH.write_text(html_out, encoding="utf-8")
    print(
        f"Wrote {OUT_PATH} ({n_blocks} passages, {total_q} questions, "
        f"{scored_q} with answer key)"
    )


if __name__ == "__main__":
    main()
