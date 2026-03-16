#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""マークダウンから全100問のHTMLを生成"""

import re

MD_PATH = '/Users/hayashi./datax/Business/school/J.TEST/202603student/202603ゴイさん/0315ゴイさんjtest_AC_解答.md'
HTML_PATH = '/Users/hayashi./datax/Business/school/J.TEST/202603student/jtest-ac-0315-goi.html'

# 解答一覧から正解を取得（マークダウンの表）
ANSWERS_TABLE = {
    1:1,2:4,3:1,4:2,5:3,6:3,7:3,8:2,9:1,10:4,
    11:3,12:1,13:2,14:1,15:2,16:1,17:3,18:1,19:4,20:3,
    21:3,22:3,23:4,24:1,25:1,26:2,27:4,28:3,29:3,30:1,
    31:2,32:3,33:3,34:4,35:4,36:1,37:2,38:3,39:2,40:4,
    41:1,42:4,43:1,44:4,45:4,46:2,47:2,48:4,49:3,50:2,51:1,
    52:4,53:3,54:4,55:2,56:1,57:2,58:3,59:1,60:2,
    61:2,62:3,63:4,64:1,65:3,66:4,67:1,68:2,69:2,70:2,
    71:3,72:4,73:4,74:1,75:2,
}

def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def parse_markdown():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = re.split(r'\n---\n', content)
    questions = {}
    
    for block in blocks:
        m = re.search(r'\*\*\((\d+)\)\*\*', block)
        if not m:
            continue
        qnum = int(m.group(1))
        if qnum > 100:
            continue
        
        # 問題文: **(N)** の直後から選択肢/解答の前まで
        # 選択肢は \n　1　 または \n\n　1　 で始まる。記述式は \n\n> で解答が始まる
        q_text_match = re.search(r'\*\*\(\d+\)\*\*\s*(.+?)(?=\n\s*　[1234]　|\n\n> |\Z)', block, re.DOTALL)
        q_text = q_text_match.group(1).strip() if q_text_match else ''
        q_text = re.sub(r'\n+', '<br>', q_text)
        q_text = q_text.replace('<u>', '<strong>').replace('</u>', '</strong>')
        
        # 選択肢（1-75のみ）: 　1　opt 形式（同一行・複数行対応）
        opts_match = re.findall(r'　([1234])　([^\n]*?)(?=　[1234]　|\n\s*　[1234]　|$|\n\n)', block)
        options = []
        if opts_match:
            for _, opt in sorted(opts_match, key=lambda x: int(x[0])):
                opt = opt.strip()
                if opt and len(options) < 4:
                    options.append(opt)
        
        # 解答: > ★ **解答：1　xxx** または > ★ **解答：xxx** または > ★ **解答例：xxx**（記述式）
        ans_match = re.search(r'> \*?\*?★\s*\*?\*?解答[例]?[：:]\s*(\d)　([^*\n]+?)(?:\*\*)?(?=\n|$)', block)
        if ans_match:
            ans_num = int(ans_match.group(1))
            ans_text = ans_match.group(2).strip()
        else:
            ans_match2 = re.search(r'> \*?\*?★\s*\*?\*?解答[例]?[：:]\s*(.+?)(?:\*\*)?(?=\n|$)', block, re.DOTALL)
            ans_text = ans_match2.group(1).strip() if ans_match2 else ''
            ans_num = 1
        
        # 解説
        expl_m = re.search(r'> ◆ 解説[：:](.+?)(?=\n\n|\n> |\Z)', block, re.DOTALL)
        expl = expl_m.group(1).strip() if expl_m else ''
        expl = re.sub(r'\n+', ' ', expl).replace('　', ' ')
        
        questions[qnum] = {
            'text': q_text,
            'options': options,
            'ans_num': ans_num,
            'ans_text': ans_text,
            'explanation': expl,
        }
    
    return questions

def gen_mc_question(qnum, q_text, options, ans_num, explanation):
    ans = ANSWERS_TABLE.get(qnum, ans_num)
    opts_html = []
    for i, opt in enumerate(options, 1):
        v = '1' if ans == i else '0'
        lid = f'q{qnum}{chr(96+i)}'
        opt_esc = opt.replace('<ruby>', '\uE001').replace('</ruby>', '\uE002').replace('<rt>', '\uE003').replace('</rt>', '\uE004')
        opt_esc = escape_html(opt_esc).replace('\uE001', '<ruby>').replace('\uE002', '</ruby>').replace('\uE003', '<rt>').replace('\uE004', '</rt>')
        opts_html.append(f'<div class="option"><input type="radio" name="q{qnum}" id="{lid}" value="{v}"><label for="{lid}">{i}. {opt_esc}</label></div>')
    
    ans_opt = options[ans-1] if ans <= len(options) else ''
    expl_esc = escape_html(explanation)
    return f'''<div class="question">
<div class="q-text"><span class="q-num">{qnum}</span>{q_text}</div>
<div class="options">
{chr(10).join(opts_html)}
</div>
<div class="explanation">✅ 正解：{ans}. {ans_opt} — {expl_esc}</div>
</div>'''

def gen_readonly_question(qnum, q_text, ans_text, explanation):
    expl_esc = escape_html(explanation)
    return f'''<div class="question readonly">
<div class="q-text"><span class="q-num">{qnum}</span>{q_text}</div>
<div class="answer-box">★ 解答：{ans_text}</div>
<div class="explanation">◆ 解説：{expl_esc}</div>
</div>'''

def main():
    questions = parse_markdown()
    print(f'Parsed {len(questions)} questions')
    
    # 既存のgenerate_jtest_ac_htmlの構造を参考に、全100問のHTMLを生成
    # 1-75: 選択式（インタラクティブ）
    # 76-100: 記述式（読み取り専用）
    
    # jtest-fg-20260308-sard.html と同様の形式
    HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>過去問J.TEST A-C 2026年3月度（80分・全100問）</title>
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
</style>
</head>
<body>
<div class="container">
<header>
<h1>過去問J.TEST A-C 2026年3月度（80分・全100問）</h1>
<div class="header-info">
<div class="timer" id="timer">80:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">全100問</div>
</div>
</header>
'''
    
    out = [HTML_TEMPLATE]
    
    # 1. 文法・語彙 A (1-20)
    out.append('<div class="section"><div class="section-title">1 文法・語彙問題 A（20問）</div>')
    for q in range(1, 21):
        if q in questions and questions[q]['options']:
            out.append(gen_mc_question(q, questions[q]['text'], questions[q]['options'], questions[q]['ans_num'], questions[q]['explanation']))
    out.append('</div>')
    
    # 2. 文法・語彙 B (21-30)
    out.append('<div class="section"><div class="section-title">文法・語彙問題 B（10問）</div>')
    for q in range(21, 31):
        if q in questions and questions[q]['options']:
            out.append(gen_mc_question(q, questions[q]['text'], questions[q]['options'], questions[q]['ans_num'], questions[q]['explanation']))
    out.append('</div>')
    
    # 3. 文法・語彙 C (31-40)
    out.append('<div class="section"><div class="section-title">文法・語彙問題 C（10問）</div>')
    for q in range(31, 41):
        if q in questions and questions[q]['options']:
            out.append(gen_mc_question(q, questions[q]['text'], questions[q]['options'], questions[q]['ans_num'], questions[q]['explanation']))
    out.append('</div>')
    
    # 4. 読解 (41-60)
    out.append('<div class="section"><div class="section-title">2 読解問題（20問）</div>')
    for q in range(41, 61):
        if q in questions and questions[q]['options']:
            out.append(gen_mc_question(q, questions[q]['text'], questions[q]['options'], questions[q]['ans_num'], questions[q]['explanation']))
    out.append('</div>')
    
    # 5. 漢字A (61-75)
    out.append('<div class="section"><div class="section-title">3 漢字問題 A（15問）</div>')
    for q in range(61, 76):
        if q in questions and questions[q]['options']:
            out.append(gen_mc_question(q, questions[q]['text'], questions[q]['options'], questions[q]['ans_num'], questions[q]['explanation']))
    out.append('</div>')
    
    # 6. 漢字B (76-90) - 記述式
    out.append('<div class="section"><div class="section-title">漢字問題 B（15問）</div>')
    for q in range(76, 91):
        if q in questions:
            out.append(gen_readonly_question(q, questions[q]['text'], questions[q]['ans_text'], questions[q]['explanation']))
    out.append('</div>')
    
    # 7. 記述問題 (91-100)
    out.append('<div class="section"><div class="section-title">4 記述問題（10問）</div>')
    for q in range(91, 101):
        if q in questions:
            out.append(gen_readonly_question(q, questions[q]['text'], questions[q]['ans_text'], questions[q]['explanation']))
    out.append('</div>')
    
    out.append('''<button class="btn-submit" id="submitBtn" onclick="submitTest()">採点する</button>
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
</html>''')
    
    html = '\n'.join(out)
    html = html.replace('&lt;br&gt;', '<br>')
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: {HTML_PATH}')

if __name__ == '__main__':
    main()
