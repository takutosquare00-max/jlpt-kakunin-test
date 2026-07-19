#!/usr/bin/env python3
"""jtest-ac-2025.md から jtest-ac-2025.html を生成（jtest-ac-202603.html と同様のレイアウト）"""

import html as html_lib
import re
from pathlib import Path

from pdf_ruby_normalize import apply_to_text

ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "jtest-ac-2025.md"
OUT_PATH = ROOT / "jtest-ac-2025.html"

ANSWERS = {
    1: 2, 2: 4, 3: 4, 4: 1, 5: 3, 6: 1, 7: 2, 8: 2, 9: 2, 10: 1,
    11: 2, 12: 4, 13: 4, 14: 3, 15: 4, 16: 4, 17: 3, 18: 1, 19: 3, 20: 2,
    21: 4, 22: 1, 23: 4, 24: 3, 25: 2, 26: 2, 27: 3, 28: 1, 29: 4, 30: 3,
    31: 4, 32: 1, 33: 2, 34: 4, 35: 4, 36: 2, 37: 1, 38: 2, 39: 3, 40: 1,
    41: 3, 42: 1, 43: 1, 44: 3, 45: 2, 46: 4, 47: 3, 48: 4, 49: 1, 50: 2,
    51: 1, 52: 1, 53: 4, 54: 4, 55: 4, 56: 3, 57: 3, 58: 3, 59: 1, 60: 2,
    61: 2, 62: 1, 63: 2, 64: 3, 65: 1, 66: 1, 67: 4, 68: 2, 69: 1, 70: 2,
    71: 3, 72: 3, 73: 1, 74: 4, 75: 2,
}
READING_ANSWERS = {
    76: "しま", 77: "けしき", 78: "ふうとう", 79: "そんけい", 80: "さかい",
    81: "たまご", 82: "ふたたび", 83: "いさま", 84: "えんかつ", 85: "ふっとう",
    86: "せまい", 87: "ひんぱん", 88: "つつしんで", 89: "はけん", 90: "びょうしゃ",
}
DESC_EXAMPLES = {
    91: "（例）（A）水泳　（B）泳いで",
    92: "（例）（A）なる　（B）安く",
    93: "（例）（A）ミス　（B）直し",
    94: "（例）（A）ところ　（B）調べ",
    95: "（例）（A）かかる　（B）買う",
    96: "山田さんに聞いてみてください。",
    97: "喜んでいるように見えた。",
    98: "会議室に入ってくるとたんに、",
    99: "面接を受けるにあたって、",
    100: "知りつつもお酒を",
}


def bold_to_tags(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j == -1:
                out.append(html_lib.escape(s[i:]))
                break
            inner = s[i + 2 : j]
            # 区切り線「****...」など、空の ** は太字にせず ** として表示
            if inner:
                out.append("<strong>" + html_lib.escape(inner) + "</strong>")
            else:
                out.append(html_lib.escape("**"))
            i = j + 2
        else:
            nxt = s.find("**", i)
            if nxt == -1:
                out.append(html_lib.escape(s[i:]))
                break
            out.append(html_lib.escape(s[i:nxt]))
            i = nxt
    return "".join(out)


def line_to_html(line: str) -> str:
    """1行：**太字** と <ruby> を両立（ruby を一時退避してから ** を処理）。"""
    stripped = line.strip()
    if stripped and set(stripped) == {"*"}:
        # メールの「****...」区切りなど。** の連続は空太字と解釈され文字数が半分になるため
        return html_lib.escape(line)

    placeholders: list[str] = []

    def _sub_ruby(m: re.Match[str]) -> str:
        placeholders.append(m.group(0))
        return f"\x00RUBY{len(placeholders) - 1}\x00"

    s = re.sub(r"<ruby>.*?</ruby>", _sub_ruby, line, flags=re.DOTALL)
    s = bold_to_tags(s)
    for i, ph in enumerate(placeholders):
        s = s.replace(f"\x00RUBY{i}\x00", ph)
    return s


def text_to_html(text: str) -> str:
    if not text:
        return ""
    lines = text.split("\n")
    return "<br>\n".join(line_to_html(line) for line in lines)


def passage_text_to_html(text: str) -> str:
    """読解本文：MD の空行がそのままだと <br> が重なり行間が広すぎるため、連続改行を畳む。"""
    if not text:
        return ""
    t = text.strip()
    t = re.sub(r"\n{2,}", "\n", t)
    return text_to_html(t)


def _is_structural_line(stripped: str) -> bool:
    """ページ番号・見出し等。これ以降は選択肢の続き行に含めない。"""
    if not stripped:
        return False
    if re.match(r"^#{1,6}\s", stripped):
        return True
    if stripped == "---":
        return True
    if re.match(r"^-\s*\d+\s*-\s*$", stripped):
        return True
    return False


def split_four_options_from_line(line: str) -> list[tuple[int, str]] | None:
    s = line.strip()
    if not re.search(r"^[1-4]\s+", s):
        return None
    if not re.search(r"\s[1-4]\s", s):
        return None
    chunks = re.split(r"\s+(?=[1-4]\s)", s)
    opts = []
    for c in chunks:
        c = c.strip()
        m = re.match(r"^([1-4])\s+(.+)$", c)
        if not m:
            return None
        opts.append((int(m.group(1)), m.group(2).strip()))
    return opts if len(opts) == 4 else None


def split_options(block: str) -> tuple[str, list[tuple[int, str]]]:
    lines = [ln.rstrip() for ln in block.strip().split("\n")]
    # 1行に 1〜4 が並ぶパターン
    for i, line in enumerate(lines):
        ol = split_four_options_from_line(line.strip())
        if ol:
            stem = "\n".join(lines[:i]).strip()
            return stem, ol
    # 行頭が「数字+空白」の連続ブロック
    opt_start: int | None = None
    for i, line in enumerate(lines):
        if re.match(r"^[1-4]\s+", line.strip()):
            opt_start = i
            break
    if opt_start is None:
        return block.strip(), []
    stem = "\n".join(lines[:opt_start]).strip()
    opts: list[tuple[int, str]] = []
    for j in range(opt_start, len(lines)):
        stripped = lines[j].strip()
        if not stripped:
            continue
        if len(opts) >= 4 and _is_structural_line(stripped):
            break
        m = re.match(r"^([1-4])\s+(.+)$", stripped)
        if m:
            opts.append((int(m.group(1)), m.group(2).strip()))
        elif opts:
            n, t = opts[-1]
            opts[-1] = (n, t + " " + stripped)
    return stem, opts


def _passage_between_horizontal_rules(md_chunk: str) -> str:
    """行が単独の --- のみのときだけ区切りとみなす（表の | --- | では分割しない）。"""
    lines = md_chunk.split("\n")
    seps: list[int] = []
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            seps.append(i)
    if len(seps) >= 2:
        return "\n".join(lines[seps[0] + 1 : seps[1]]).strip()
    return ""


def _strip_md_heading_prefixes(text: str) -> str:
    out = []
    for ln in text.split("\n"):
        out.append(re.sub(r"^#{1,6}\s+", "", ln))
    return "\n".join(out)


def extract_reading_passages_for_first_question_only(md: str) -> dict[int, str]:
    """読解の本文は各「### 問題」ブロックの先頭の設問にだけ紐づける（同一本文の重複表示を防ぐ）。"""
    out: dict[int, str] = {}
    if "## 2 読解問題" not in md:
        return out
    sec = md.split("## 2 読解問題", 1)[1].split("## 3", 1)[0]
    chunks = re.split(r"(?=^### 問題\s*\d+)", sec, flags=re.MULTILINE)
    for ch in chunks:
        ch_st = ch.strip()
        if not ch_st.startswith("### 問題"):
            continue
        nums = [int(x) for x in re.findall(r"\*\*（(\d+)）\*\*", ch_st)]
        if not nums:
            continue
        passage = _passage_between_horizontal_rules(ch_st)
        if not passage:
            m0 = re.search(r"\*\*（\d+）\*\*", ch_st)
            if m0:
                head = ch_st[: m0.start()]
                head = re.sub(r"^### 問題\s*\d+\s*\n", "", head, count=1)
                head = re.sub(
                    r"^次の[^\n]*\n\s*答えは[^\n]*\n\s*",
                    "",
                    head,
                    count=1,
                    flags=re.MULTILINE,
                )
                passage = head.strip()
        passage = re.sub(r"\n-\s*\d+\s*-\s*$", "", passage)
        passage = _strip_md_heading_prefixes(passage)
        if passage:
            out[min(nums)] = passage
    return out


def parse_question_blocks(md: str) -> dict[int, str]:
    md = md.split("## 解答一覧")[0]
    matches = list(re.finditer(r"\*\*（(\d+)）\*\*", md))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        out[n] = md[start:end]
    return out


def parse_explanations(md: str) -> dict[int, str]:
    expl: dict[int, str] = {}
    if "## 解説" not in md:
        return expl
    part = md.split("## 解説", 1)[1]
    for line in part.split("\n"):
        m = re.match(r"\*\*（(\d+)）\s*(\d*)\*\*\s*[　\s]*(.*)$", line.strip())
        if m:
            n = int(m.group(1))
            expl[n] = m.group(3).strip()
    return expl


SECTIONS = [
    (1, 20, "1 文法・語彙問題 A（1〜20）"),
    (21, 30, "1 文法・語彙問題 B（21〜30）"),
    (31, 40, "1 文法・語彙問題 C（31〜40）"),
    (41, 60, "2 読解問題（41〜60）"),
    (61, 75, "3 漢字問題 A・B 語の書き（61〜75）"),
    (76, 90, "3 漢字問題 B 読み（76〜90）"),
    (91, 100, "4 記述問題（91〜100）"),
]


def build_html() -> str:
    raw = apply_to_text(MD_PATH.read_text(encoding="utf-8"))
    blocks = parse_question_blocks(raw)
    explanations = parse_explanations(raw)
    reading_passages = extract_reading_passages_for_first_question_only(raw)

    sections_html: list[str] = []
    for lo, hi, title in SECTIONS:
        buf: list[str] = []
        for n in range(lo, hi + 1):
            if n not in blocks:
                continue
            block = blocks[n]
            inner = re.sub(r"^\*\*（\d+）\*\*\s*", "", block, count=1, flags=re.MULTILINE)
            stem, opts = split_options(inner)
            stem_html = text_to_html(stem) if stem else ""
            exp = explanations.get(n, "")
            exp_html = text_to_html(exp) if exp else "（解説は MD の「解説」欄を参照）"

            passage_html = ""
            if 41 <= n <= 60 and n in reading_passages:
                passage_html = (
                    '<div class="reading-passage">'
                    + passage_text_to_html(reading_passages[n])
                    + "</div>\n"
                )

            if 1 <= n <= 75 and len(opts) == 4:
                correct = ANSWERS.get(n, 1)
                letters = ["a", "b", "c", "d"]
                opts_html = []
                for j, (onum, otext) in enumerate(opts):
                    val = "1" if onum == correct else "0"
                    oid = f"q{n}{letters[j]}"
                    label = text_to_html(f"{onum}. {otext}")
                    opts_html.append(
                        f'<div class="option"><input type="radio" name="q{n}" id="{oid}" value="{val}">'
                        f'<label for="{oid}">{label}</label></div>'
                    )
                buf.append(
                    f'<div class="question">\n'
                    + passage_html
                    + f'<div class="q-text"><span class="q-num">{n}</span>{stem_html}</div>\n'
                    f'<div class="options">\n' + "\n".join(opts_html) + "\n</div>\n"
                    f'<div class="explanation">◆ 正解：{correct} — {exp_html}</div>\n'
                    f"</div>"
                )
            elif 76 <= n <= 90:
                ans = READING_ANSWERS.get(n, "")
                buf.append(
                    f'<div class="question readonly">\n'
                    f'<div class="q-text"><span class="q-num">{n}</span>{stem_html}</div>\n'
                    f'<div class="answer-box">★ 解答：{html_lib.escape(ans)}</div>\n'
                    f'<div class="explanation">◆ 解説：{exp_html}</div>\n'
                    f"</div>"
                )
            elif 91 <= n <= 100:
                ex = DESC_EXAMPLES.get(n, "")
                buf.append(
                    f'<div class="question readonly">\n'
                    f'<div class="q-text"><span class="q-num">{n}</span>{stem_html}</div>\n'
                    f'<div class="answer-box">★ 例：{html_lib.escape(ex)}</div>\n'
                    f'<div class="explanation">◆ 解説：{exp_html}</div>\n'
                    f"</div>"
                )
            else:
                buf.append(
                    f'<div class="question">\n'
                    f'<div class="q-text"><span class="q-num">{n}</span>{stem_html}</div>\n'
                    f'<p class="explanation" style="display:block">（選択肢の解析に失敗しました。MD を参照）</p>\n'
                    f"</div>"
                )
        if buf:
            sections_html.append(
                f'<div class="section"><div class="section-title">{title}</div>\n'
                + "\n".join(buf)
                + "\n</div>"
            )

    body_content = "\n".join(sections_html)

    template = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>過去問J.TEST A-C 2025年7月度</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f5f5f5;color:#000;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
header{background:#f5f5f5;color:#000;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;border:2px solid #000;box-shadow:none}
header h1{font-size:1.5em;margin-bottom:4px}
.header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums;color:#000}
.timer.warning{color:#333;animation:pulse 1s infinite}
.timer.danger{color:#000;animation:pulse .5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:200px;height:8px;background:#f5f5f5;border:1px solid #000;border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#000;border-radius:2px;transition:width .3s}
.score-badge{background:#f5f5f5;color:#000;padding:4px 12px;border-radius:20px;font-size:.9em;border:1px solid #000}
.section{background:#f5f5f5;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #000;box-shadow:none}
.section-title{font-size:1.1em;font-weight:bold;color:#000;border-left:4px solid #000;padding-left:12px;margin-bottom:16px}
.question{padding:16px 0;border-bottom:1px solid #000}
.question:last-child{border-bottom:none}
.q-num{display:inline-block;background:#f5f5f5;color:#000;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px;border:2px solid #000}
.q-text{font-size:1.05em;margin-bottom:12px;font-weight:500;color:#000}
.options{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}
@media(max-width:600px){.options{grid-template-columns:1fr}}
.option{display:flex;flex-direction:column;position:relative;min-height:0}
.option input{display:none}
.option label{display:block;flex:1;min-height:52px;padding:10px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;line-height:1.65;touch-action:manipulation;-webkit-user-select:none;user-select:none;color:#1a202c;background:#fff}
ruby{ruby-align:center}
.reading-passage{background:#fff;border:1px solid #000;border-left:3px solid #000;padding:12px 14px;margin:0 0 14px;font-size:1em;line-height:1.65;white-space:normal;color:#111}
.option label rt,.q-text rt,.reading-passage rt{font-size:.5em;line-height:1.25}
.option label:hover{border-color:#38b2ac;background:#f0ffff}
.option input:checked+label{border-color:#38b2ac;background:#e6fffa;color:#234e52;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.btn-submit{display:block;width:100%;min-height:48px;padding:16px;background:#f5f5f5;color:#000;border:2px solid #000;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);background:#f5f5f5}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none}
.result-panel{background:#f5f5f5;border-radius:16px;padding:32px;text-align:center;border:2px solid #000;margin-top:24px;display:none}
.result-panel h2{font-size:1.8em;margin-bottom:8px;color:#000}
.result-score{font-size:3em;font-weight:bold;margin:16px 0;color:#000}
.result-score.excellent{color:#000}
.result-score.good{color:#000}
.result-score.fair{color:#000}
.result-score.poor{color:#000}
.result-detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}
.result-item{background:#f5f5f5;padding:12px;border-radius:8px;border:1px solid #000}
.result-item .label{font-size:.8em;color:#000}
.result-item .value{font-size:1.2em;font-weight:bold;color:#000}
.explanation{display:none;margin-top:8px;padding:10px;background:#fff;border-radius:8px;font-size:.9em;border:1px solid #000;color:#000}
.explanation.show{display:block}
.question.readonly .answer-box{display:none;background:#f0f0f0;padding:10px;margin:8px 0;border-radius:8px;border:1px solid #000;font-weight:bold}
.question.readonly .answer-box.show{display:block}
</style>
</head>
<body>
<div class="container">
<header>
<h1>過去問J.TEST A-C 2025年7月度</h1>
<div class="header-info">
<div class="timer" id="timer">80:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">全100問</div>
</div>
</header>

BODY_PLACEHOLDER

<button class="btn-submit" id="submitBtn" onclick="submitTest()">採点する</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>

<script>
const TOTAL=75,TIME_LIMIT=4800;
let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){
timerInterval=setInterval(()=>{
timeLeft--;
const m=Math.floor(timeLeft/60),s=timeLeft%60;
const el=document.getElementById('timer');
el.textContent=`${m}:${s.toString().padStart(2,'0')}`;
document.getElementById('progress').style.width=`${(timeLeft/TIME_LIMIT)*100}%`;
if(timeLeft<=60)el.className='timer danger';
else if(timeLeft<=300)el.className='timer warning';
if(timeLeft<=0){clearInterval(timerInterval);submitTest();}
},1000);
}
function submitTest(){
if(submitted)return;submitted=true;
clearInterval(timerInterval);
let correct=0;
const sections={grammarA:0,grammarAT:20,grammarB:0,grammarBT:10,grammarC:0,grammarCT:10,reading:0,readingT:20,kanji:0,kanjiT:15};
for(let i=1;i<=TOTAL;i++){
const sel=document.querySelector(`input[name="q${i}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${i}"]`);
let isCorrect=false;
if(sel&&sel.value==='1'){isCorrect=true;correct++;}
if(opts.length){opts.forEach(o=>{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
});}
if(i<=20){if(isCorrect)sections.grammarA++;}
else if(i<=30){if(isCorrect)sections.grammarB++;}
else if(i<=40){if(isCorrect)sections.grammarC++;}
else if(i<=60){if(isCorrect)sections.reading++;}
else{if(isCorrect)sections.kanji++;}
}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
document.querySelectorAll('.answer-box').forEach(e=>e.classList.add('show'));
const pct=Math.round((correct/TOTAL)*100);
const panel=document.getElementById('resultPanel');
const title=document.getElementById('resultTitle');
const score=document.getElementById('resultScore');
const detail=document.getElementById('resultDetail');
panel.style.display='block';
score.textContent=`${correct} / ${TOTAL}（${pct}%）`;
if(pct>=90){title.textContent='🎉 素晴らしい！';score.className='result-score excellent';}
else if(pct>=70){title.textContent='👍 よくできました！';score.className='result-score good';}
else if(pct>=50){title.textContent='📝 もう少し！';score.className='result-score fair';}
else{title.textContent='💪 がんばりましょう！';score.className='result-score poor';}
const timeUsed=TIME_LIMIT-timeLeft;
detail.innerHTML=`
<div class="result-item"><div class="label">文法・語彙A</div><div class="value">${sections.grammarA}/${sections.grammarAT}</div></div>
<div class="result-item"><div class="label">文法・語彙B</div><div class="value">${sections.grammarB}/${sections.grammarBT}</div></div>
<div class="result-item"><div class="label">文法・語彙C</div><div class="value">${sections.grammarC}/${sections.grammarCT}</div></div>
<div class="result-item"><div class="label">読解</div><div class="value">${sections.reading}/${sections.readingT}</div></div>
<div class="result-item"><div class="label">漢字A</div><div class="value">${sections.kanji}/${sections.kanjiT}</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${Math.floor(timeUsed/60)}分${timeUsed%60}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({behavior:'smooth'});
}
startTimer();
</script>
</body>
</html>
"""
    return template.replace("BODY_PLACEHOLDER", body_content)


def main():
    OUT_PATH.write_text(build_html(), encoding="utf-8")
    print("Wrote", OUT_PATH)


if __name__ == "__main__":
    main()
