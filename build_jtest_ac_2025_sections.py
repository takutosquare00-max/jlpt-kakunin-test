#!/usr/bin/env python3
"""jtest-ac-2025.html（ゴイさん）をセクション別HTMLに分割し、jlpt-kakunin-test-deploy に出力する。"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_HTML = ROOT.parent / "J.TEST/202603student/ゴイさん/jtest-ac-2025.html"

CSS_BLOCK = """*{margin:0;padding:0;box-sizing:border-box}
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
.progress-fill{height:100%;background:#000;border-radius:2px;transition:width .2s}
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
.option label rt,.q-text rt,.reading-passage rt{font-size:.55em;line-height:1.3}
.option label:hover{border-color:#38b2ac;background:#f0ffff}
.option input:checked+label{border-color:#38b2ac;background:#e6fffa;color:#234e52;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.reading-passage{background:#f5f5f5;border-left:3px solid #000;padding:16px;margin:12px 0;border-radius:0 8px 8px 0;font-size:.95em;line-height:1.9;white-space:pre-wrap;border:1px solid #000;color:#000}
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
.explanation{display:none;margin-top:8px;padding:10px;background:#f5f5f5;border-radius:8px;font-size:.9em;border-left:3px solid #000;border:1px solid #000;color:#000}
.explanation.show{display:block}
.question.readonly .answer-box{display:none;background:#f0f0f0;padding:10px;margin:8px 0;border-radius:8px;border:1px solid #000;font-weight:bold}
.question.readonly .answer-box.show{display:block}
.question.readonly .explanation{margin-top:8px}
.submit-section{padding:16px 24px 24px;margin-bottom:20px}
.submit-section .btn-submit{margin-top:0}
"""

FOOTER_MCQ = """</div>
<div class="section submit-section">
<button class="btn-submit" id="submitBtn" onclick="submitTest()">採点する</button>
</div>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>
"""

FOOTER_READONLY = """</div>
<div class="section submit-section">
<button class="btn-submit" id="submitBtn" onclick="submitTest()">解説を表示</button>
</div>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>
"""

SECTIONS = [
    {
        "file": "jtest-ac-2025-sec01-goi-a.html",
        "title": "過去問J.TEST A-C 2025年7月度 語彙A 20問（10分）",
        "h1": "過去問J.TEST A-C 2025年7月度【語彙A 20問】（10分）",
        "timer": "10:00",
        "time_sec": 600,
        "badge": "語彙A 20問",
        "q_start": 1,
        "q_end": 20,
        "mode": "mcq",
        "score_label": "文法・語彙A",
    },
    {
        "file": "jtest-ac-2025-sec02-goi-b.html",
        "title": "過去問J.TEST A-C 2025年7月度 語彙B 10問（5分）",
        "h1": "過去問J.TEST A-C 2025年7月度【語彙B 10問】（5分）",
        "timer": "5:00",
        "time_sec": 300,
        "badge": "語彙B 10問",
        "q_start": 21,
        "q_end": 30,
        "mode": "mcq",
        "score_label": "文法・語彙B",
    },
    {
        "file": "jtest-ac-2025-sec03-goi-c.html",
        "title": "過去問J.TEST A-C 2025年7月度 語彙C 10問（5分）",
        "h1": "過去問J.TEST A-C 2025年7月度【語彙C 10問】（5分）",
        "timer": "5:00",
        "time_sec": 300,
        "badge": "語彙C 10問",
        "q_start": 31,
        "q_end": 40,
        "mode": "mcq",
        "score_label": "文法・語彙C",
    },
    {
        "file": "jtest-ac-2025-sec04-dokkai.html",
        "title": "過去問J.TEST A-C 2025年7月度 読解 20問（38分）",
        "h1": "過去問J.TEST A-C 2025年7月度【読解 20問】（38分）",
        "timer": "38:00",
        "time_sec": 2280,
        "badge": "読解 20問",
        "q_start": 41,
        "q_end": 60,
        "mode": "mcq",
        "score_label": "読解",
    },
    {
        "file": "jtest-ac-2025-sec05-kanji-a.html",
        "title": "過去問J.TEST A-C 2025年7月度 漢字A 15問（7分）",
        "h1": "過去問J.TEST A-C 2025年7月度【漢字A 15問】（7分）",
        "timer": "7:00",
        "time_sec": 420,
        "badge": "漢字A 15問",
        "q_start": 61,
        "q_end": 75,
        "mode": "mcq",
        "score_label": "漢字A",
    },
    {
        "file": "jtest-ac-2025-sec06-kanji-b.html",
        "title": "過去問J.TEST A-C 2025年7月度 漢字B 15問（7分）",
        "h1": "過去問J.TEST A-C 2025年7月度【漢字B 15問】（7分）",
        "timer": "7:00",
        "time_sec": 420,
        "badge": "漢字B 15問",
        "mode": "readonly",
        "readonly_label": "漢字B",
    },
    {
        "file": "jtest-ac-2025-sec07-kisshutsu.html",
        "title": "過去問J.TEST A-C 2025年7月度 記述 10問（8分）",
        "h1": "過去問J.TEST A-C 2025年7月度【記述 10問】（8分）",
        "timer": "8:00",
        "time_sec": 480,
        "badge": "記述 10問",
        "mode": "readonly",
        "readonly_label": "記述",
    },
]


def extract_section_bodies(html: str) -> list[str]:
    start = html.find('<div class="section">')
    end = html.find("\n\n<button class=\"btn-submit\"")
    if start == -1 or end == -1:
        raise ValueError("Could not find section block or submit button")
    block = html[start:end]
    parts = re.split(r"(?=<div class=\"section\"><div class=\"section-title\">)", block)
    return [p for p in parts if p.strip()]


def fix_q90_q100(html: str) -> str:
    html = re.sub(
        r'(<div class="q-text"><span class="q-num">90</span>細かいところまで<strong>描写</strong>されている。)<br>[\s\S]*?</div>(?=\s*<div class="answer-box">)',
        r"\1</div>",
        html,
    )
    html = re.sub(
        r'(<div class="q-text"><span class="q-num">100</span>[\s\S]*?<ruby>飲<rt>の</rt></ruby>みすぎてしまう。)<br>[\s\S]*?</div>(?=\s*<div class="answer-box">)',
        r"\1</div>",
        html,
    )
    return html


def script_mcq(q_start: int, q_end: int, time_sec: int, score_label: str) -> str:
    total = q_end - q_start + 1
    return f"""<script>
const Q_START={q_start},Q_END={q_end},TOTAL={total},TIME_LIMIT={time_sec};
let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){{
timerInterval=setInterval(()=>{{
timeLeft--;
const m=Math.floor(timeLeft/60),s=timeLeft%60;
const el=document.getElementById('timer');
el.textContent=`${{m}}:${{s.toString().padStart(2,'0')}}`;
document.getElementById('progress').style.width=`${{(timeLeft/TIME_LIMIT)*100}}%`;
if(timeLeft<=60)el.className='timer danger';
else if(timeLeft<=300)el.className='timer warning';
if(timeLeft<=0){{clearInterval(timerInterval);submitTest();}}
}},1000);
}}
function submitTest(){{
if(submitted)return;submitted=true;
clearInterval(timerInterval);
let correct=0;
for(let i=Q_START;i<=Q_END;i++){{
const sel=document.querySelector(`input[name="q${{i}}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${{i}}"]`);
if(sel&&sel.value==='1'){{correct++;}}
if(opts.length){{opts.forEach(o=>{{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
}});}}
}}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
document.querySelectorAll('.answer-box').forEach(e=>e.classList.add('show'));
const pct=TOTAL>0?Math.round((correct/TOTAL)*100):0;
const panel=document.getElementById('resultPanel');
const title=document.getElementById('resultTitle');
const score=document.getElementById('resultScore');
const detail=document.getElementById('resultDetail');
panel.style.display='block';
score.textContent=`${{correct}} / ${{TOTAL}}（${{pct}}%）`;
if(pct>=90){{title.textContent='🎉 素晴らしい！';score.className='result-score excellent';}}
else if(pct>=70){{title.textContent='👍 よくできました！';score.className='result-score good';}}
else if(pct>=50){{title.textContent='📝 もう少し！';score.className='result-score fair';}}
else{{title.textContent='💪 がんばりましょう！';score.className='result-score poor';}}
const timeUsed=TIME_LIMIT-timeLeft;
detail.innerHTML=`
<div class="result-item"><div class="label">{score_label}</div><div class="value">${{correct}}/${{TOTAL}}</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${{Math.floor(timeUsed/60)}}分${{timeUsed%60}}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({{behavior:'smooth'}});
}}
startTimer();
</script>
"""


def script_readonly(time_sec: int, label: str) -> str:
    return f"""<script>
const TIME_LIMIT={time_sec};
let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){{
timerInterval=setInterval(()=>{{
timeLeft--;
const m=Math.floor(timeLeft/60),s=timeLeft%60;
const el=document.getElementById('timer');
el.textContent=`${{m}}:${{s.toString().padStart(2,'0')}}`;
document.getElementById('progress').style.width=`${{(timeLeft/TIME_LIMIT)*100}}%`;
if(timeLeft<=60)el.className='timer danger';
else if(timeLeft<=300)el.className='timer warning';
if(timeLeft<=0){{clearInterval(timerInterval);submitTest();}}
}},1000);
}}
function submitTest(){{
if(submitted)return;submitted=true;
clearInterval(timerInterval);
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
document.querySelectorAll('.answer-box').forEach(e=>e.classList.add('show'));
const panel=document.getElementById('resultPanel');
const title=document.getElementById('resultTitle');
const score=document.getElementById('resultScore');
panel.style.display='block';
title.textContent='✅ 完了';
score.textContent='解説を表示しました';
score.className='result-score good';
const timeUsed=TIME_LIMIT-timeLeft;
document.getElementById('resultDetail').innerHTML=`
<div class="result-item"><div class="label">{label}</div><div class="value">採点対象外（自己採点）</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${{Math.floor(timeUsed/60)}}分${{timeUsed%60}}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({{behavior:'smooth'}});
}}
startTimer();
</script>
"""


def build_page(meta: dict, section_html: str) -> str:
    head = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>{meta["title"]}</title>
<style>
{CSS_BLOCK}
</style>
</head>
<body>
<div class="container">
<header>
<h1>{meta["h1"]}</h1>
<div class="header-info">
<div class="timer" id="timer">{meta["timer"]}</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">{meta["badge"]}</div>
</div>
</header>

"""
    if meta["mode"] == "mcq":
        footer = FOOTER_MCQ
        script = script_mcq(meta["q_start"], meta["q_end"], meta["time_sec"], meta["score_label"])
    else:
        footer = FOOTER_READONLY
        script = script_readonly(meta["time_sec"], meta["readonly_label"])

    return head + section_html.strip() + "\n" + footer + "\n" + script + "\n</body>\n</html>\n"


def patch_full_html_meta(src: str) -> str:
    if 'apple-mobile-web-app-capable' in src:
        return src
    return src.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">',
        1,
    )


def main() -> None:
    raw = SRC_HTML.read_text(encoding="utf-8")
    raw = fix_q90_q100(raw)
    bodies = extract_section_bodies(raw)
    if len(bodies) != len(SECTIONS):
        raise SystemExit(f"Expected {len(SECTIONS)} sections, got {len(bodies)}")

    for body, meta in zip(bodies, SECTIONS, strict=True):
        page = build_page(meta, fix_q90_q100(body))
        out = ROOT / meta["file"]
        out.write_text(page, encoding="utf-8")
        print("Wrote", out)

    full_out = ROOT / "jtest-ac-2025.html"
    full_out.write_text(patch_full_html_meta(raw), encoding="utf-8")
    print("Wrote", full_out)


if __name__ == "__main__":
    main()
