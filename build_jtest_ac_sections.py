#!/usr/bin/env python3
"""jtest-ac-202603.html をセクションごとに分割した HTML を生成する"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "jtest-ac-202603.html"

# 80分本試験の目安配分（合計80分・読解に圧倒的に厚め／語彙は短めにまとめる）
# (slice_start, slice_end), title_short, file_slug, q_start, q_end, total_scorable, time_sec, label_ja
# スライスは jtest-ac-202603.html の 0 始まり行インデックス [start, end)
# 先頭に time-budget-panel 等を足したら HEADER_END と各 start を grep で合わせ直すこと
SECTIONS = [
    (100, 302, "語彙A 20問", "sec01-goi-a", 1, 20, 20, 10 * 60, "文法・語彙A"),
    (302, 404, "語彙B 10問", "sec02-goi-b", 21, 30, 10, 5 * 60, "文法・語彙B"),
    (404, 506, "語彙C 10問", "sec03-goi-c", 31, 40, 10, 5 * 60, "文法・語彙C"),
    (506, 719, "読解 20問", "sec04-dokkai", 41, 60, 20, 38 * 60, "読解"),
    (719, 871, "漢字A 15問", "sec05-kanji-a", 61, 75, 15, 7 * 60, "漢字A"),
    (871, 948, "漢字B 15問", "sec06-kanji-b", 76, 90, 0, 7 * 60, "漢字B"),
    (948, 1000, "記述 10問", "sec07-kisshutsu", 91, 100, 0, 8 * 60, "記述"),
]

# </header> の直後の空行まで（time-budget-panel は含めない）
HEADER_END = 82
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


def script_readonly(time_limit: int, label: str) -> str:
    return f"""
<script>
const TIME_LIMIT={time_limit};
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
const detail=document.getElementById('resultDetail');
panel.style.display='block';
title.textContent='✅ 完了';
score.textContent='解説を表示しました';
score.className='result-score good';
const timeUsed=TIME_LIMIT-timeLeft;
detail.innerHTML=`
<div class="result-item"><div class="label">{label}</div><div class="value">採点対象外（自己採点）</div></div>
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


def script_kanji_b_only(time_limit: int) -> str:
    """漢字B 76-90 も readonly"""
    return f"""
<script>
const TIME_LIMIT={time_limit};
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
<div class="result-item"><div class="label">漢字B</div><div class="value">採点対象外（自己採点）</div></div>
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

    # inject submit-section CSS
    css_extra = (
        ".submit-section{padding:16px 24px 24px;margin-bottom:20px}\n"
        ".submit-section .btn-submit{margin-top:0}\n"
    )
    base_header = base_header.replace("</style>", css_extra + "</style>")

    for i, (s, e, title_short, slug, qs, qe, total, tsec, label) in enumerate(SECTIONS):
        body = "".join(lines[s:e])
        minutes = tsec // 60
        h1 = f"過去問J.TEST A-C 2026年3月度【{title_short}】（{minutes}分）"
        title = f"J.TEST A-C 2026/03 {title_short}（{minutes}分）"
        badge = title_short
        timer = fmt_timer(tsec)

        header = base_header
        header = header.replace(
            "<h1>過去問J.TEST A-C 2026年3月度（80分・全100問）</h1>",
            f"<h1>{h1}</h1>",
        )
        header = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", header, count=1)
        header = header.replace(
            '<div class="score-badge" id="scoreBadge">全100問</div>',
            f'<div class="score-badge" id="scoreBadge">{badge}</div>',
        )
        header = header.replace(
            '<div class="timer" id="timer">80:00</div>',
            f'<div class="timer" id="timer">{timer}</div>',
        )

        out = header + body + FOOTER_LINES

        if total > 0:
            out += script_scorable(qs, qe, total, tsec, label)
        elif slug == "sec06-kanji-b":
            out += script_kanji_b_only(tsec)
        else:
            out += script_readonly(tsec, label)

        out_path = ROOT / f"jtest-ac-202603-{slug}.html"
        out_path.write_text(out, encoding="utf-8")
        print("Wrote", out_path.name)


if __name__ == "__main__":
    main()
