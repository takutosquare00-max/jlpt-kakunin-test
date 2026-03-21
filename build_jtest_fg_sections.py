#!/usr/bin/env python3
"""jtest-fg-202603.html をセクションごとに分割した HTML を生成する"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "jtest-fg-202603.html"

# 60分の目安配分 合計60分（語彙A/B/C 各8分、読解18分、漢字A/B 各5分、短文8分）
# スライスは jtest-fg-202603.html の 0 始まり行インデックス [start, end)
# (start, end), title_short, slug, q_start, q_end, total, time_sec, label_ja
SECTIONS = [
    (70, 185, "語彙A 10問", "sec01-goi-a", 1, 10, 10, 8 * 60, "文法・語彙A"),
    (185, 301, "語彙B 10問", "sec02-goi-b", 11, 20, 10, 8 * 60, "文法・語彙B"),
    (301, 360, "語彙C 5問", "sec03-goi-c", 21, 25, 5, 8 * 60, "文法・語彙C"),
    (360, 475, "読解 10問", "sec04-dokkai", 26, 35, 10, 18 * 60, "読解"),
    (475, 535, "漢字A 5問", "sec05-kanji-a", 36, 40, 5, 5 * 60, "漢字A"),
    (535, 605, "漢字B 5問", "sec06-kanji-b", 41, 45, 5, 5 * 60, "漢字B"),
    (605, 675, "短文 5問", "sec07-tanbun", 46, 50, 5, 8 * 60, "短文作成"),
]

# </header> の直後の空行まで（次行の <div class="section"> は本文に含める）
HEADER_END = 70

FOOTER_LINES = """<div class="section submit-section">
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

H1_ORIG = "<h1>過去問J.TEST F-G 2026年3月度（60分・50問）</h1>"
TITLE_PATTERN = re.compile(r"<title>.*?</title>")
BADGE_ORIG = '<div class="score-badge" id="scoreBadge">全50問</div>'
TIMER_ORIG = '<div class="timer" id="timer">60:00</div>'


def fmt_timer(sec: int) -> str:
    m, s = sec // 60, sec % 60
    return f"{m}:{s:02d}"


def script_scorable(qs: int, qe: int, total: int, time_limit: int, label: str) -> str:
    return f"""
<script>
const Q_START={qs},Q_END={qe},TOTAL={total},TIME_LIMIT={time_limit};
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
let isCorrect=false;
if(sel&&sel.value==='1'){{isCorrect=true;correct++;}}
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
<div class="result-item"><div class="label">{label}</div><div class="value">${{correct}}/${{TOTAL}}</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${{Math.floor(timeUsed/60)}}分${{timeUsed%60}}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({{behavior:'smooth'}});
}}
startTimer();
</script>
</body>
</html>
"""


def main():
    text = SRC.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    base_header = "".join(lines[:HEADER_END])

    css_extra = (
        ".submit-section{padding:16px 24px 24px;margin-bottom:20px}\n"
        ".submit-section .btn-submit{margin-top:0}\n"
    )
    base_header = base_header.replace("</style>", css_extra + "</style>")

    for s, e, title_short, slug, qs, qe, total, tsec, label in SECTIONS:
        body = "".join(lines[s:e])
        minutes = tsec // 60
        h1 = f"過去問J.TEST F-G 2026年3月度【{title_short}】（{minutes}分）"
        page_title = f"J.TEST F-G 2026/03 {title_short}（{minutes}分）"
        badge = title_short
        timer = fmt_timer(tsec)

        header = base_header
        header = header.replace(H1_ORIG, f"<h1>{h1}</h1>")
        header = TITLE_PATTERN.sub(f"<title>{page_title}</title>", header, count=1)
        header = header.replace(BADGE_ORIG, f'<div class="score-badge" id="scoreBadge">{badge}</div>')
        header = header.replace(TIMER_ORIG, f'<div class="timer" id="timer">{timer}</div>')

        out = header + body + FOOTER_LINES
        out += script_scorable(qs, qe, total, tsec, label)

        out_path = ROOT / f"jtest-fg-202603-{slug}.html"
        out_path.write_text(out, encoding="utf-8")
        print("Wrote", out_path.name)


if __name__ == "__main__":
    main()
