#!/usr/bin/env python3
"""第3課 文法HTMLテスト一式の生成スクリプト。

Outputs (in same directory):
  bunpo01-koko-soko-asoko-doko.html
  bunpo02-kochira-sochira-achira-dochira.html
  bunpo03-wa-basho-desu.html
  bunpo04-doko-no-n.html
  bunpo05-ikura.html
  bunpo-matome1.html, bunpo-matome2.html, bunpo-quickreview1.html

CSS/JSは共通テンプレート、色テーマと問題のみが差分。
方針: shared/bunpo-test-creation-guide.md
語彙制約: L1〜L3まで（動詞・〜時／〜から など L4以降は不可）
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent

# ---------- テーマカラー ----------
THEMES = {
    'blue':   dict(c1='#2b6cb0', c2='#2c5282', hover='#f0f7ff', check='#e8f2fc',
                   check_txt='#1a365d', dialog_bg='#f7fafc', dialog_brd='#2b6cb0',
                   dialog_txt='#1a365d'),
    'purple': dict(c1='#6b46c1', c2='#553c9a', hover='#f5f0ff', check='#ede4ff',
                   check_txt='#322659', dialog_bg='#f7fafc', dialog_brd='#6b46c1',
                   dialog_txt='#322659'),
    'orange': dict(c1='#dd6b20', c2='#c05621', hover='#fff8f0', check='#feebc8',
                   check_txt='#7b341e', dialog_bg='#fff8f0', dialog_brd='#dd6b20',
                   dialog_txt='#7b341e'),
}

# ---------- ruby helper ----------
def R(kanji, kana):
    return f'<ruby>{kanji}<rt>{kana}</rt></ruby>'

BLANK = '<span class="blank-paren">（　　　）</span>'

# ---------- CSS ----------
def css(theme):
    t = theme
    return (
        "*{margin:0;padding:0;box-sizing:border-box}"
        "html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}"
        "body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}"
        ".container{max-width:800px;margin:0 auto;padding:20px}"
        f"header{{background:linear-gradient(135deg,{t['c1']} 0%,{t['c2']} 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(0,0,0,.18)}}"
        "header h1{font-size:1.45em;margin-bottom:4px}"
        ".header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}"
        ".timer-group{display:flex;align-items:center;gap:8px}"
        ".timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}"
        ".timer.warning{color:#ffd700;animation:pulse 1s infinite}"
        ".timer.danger{color:#ff4757;animation:pulse .5s infinite}"
        ".timer.paused{color:#cbd5e0;animation:none}"
        ".pause-btn{background:rgba(255,255,255,.25);border:none;color:#fff;width:36px;height:36px;border-radius:50%;font-size:1em;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s;padding:0;line-height:1;touch-action:manipulation;-webkit-user-select:none;user-select:none}"
        ".pause-btn:hover{background:rgba(255,255,255,.4)}"
        ".pause-btn:active{transform:scale(.95)}"
        ".pause-btn:disabled{opacity:.4;cursor:not-allowed}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}"
        ".progress-bar{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}"
        ".progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}"
        ".score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}"
        ".section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}"
        f".section-title{{font-size:1.1em;font-weight:bold;color:{t['c1']};border-left:4px solid {t['c1']};padding-left:12px;margin-bottom:16px}}"
        ".section-lead{font-size:1.05em;font-weight:500;color:#2d3748;line-height:1.65;margin-bottom:18px}"
        ".question{padding:16px 0;border-bottom:1px solid #e2e8f0}"
        ".question:last-child{border-bottom:none}"
        f".q-num{{display:inline-block;background:{t['c1']};color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}}"
        ".q-text{font-size:1.05em;margin-bottom:12px;font-weight:500}"
        ".options{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}"
        "@media(max-width:600px){.options{grid-template-columns:1fr}}"
        ".option{position:relative;display:flex;min-height:0}"
        ".option input{display:none}"
        ".option label{flex:1;display:flex;align-items:center;gap:8px;padding:12px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;touch-action:manipulation;-webkit-user-select:none;user-select:none;min-height:48px;width:100%;box-sizing:border-box}"
        ".option .opt-key{flex:0 0 auto;min-width:1.75em;text-align:right;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.4;align-self:center}"
        ".option .opt-body{flex:1;min-width:0;line-height:1.65;align-self:center;word-break:break-word}"
        f".option label:hover{{border-color:{t['c1']};background:{t['hover']}}}"
        f".option input:checked+label{{border-color:{t['c1']};background:{t['check']};color:{t['check_txt']};font-weight:600}}"
        ".option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}"
        ".option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}"
        f".btn-submit{{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,{t['c1']} 0%,{t['c2']} 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}}"
        ".btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.2)}"
        ".btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}"
        ".result-panel{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}"
        ".result-panel h2{font-size:1.8em;margin-bottom:8px}"
        ".result-score{font-size:3em;font-weight:bold;margin:16px 0}"
        ".result-score.excellent{color:#48bb78}"
        f".result-score.good{{color:{t['c1']}}}"
        ".result-score.fair{color:#ed8936}"
        ".result-score.poor{color:#fc8181}"
        ".result-detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}"
        ".result-item{background:#f7fafc;padding:12px;border-radius:8px}"
        ".result-item .label{font-size:.8em;color:#718096}"
        ".result-item .value{font-size:1.2em;font-weight:bold}"
        ".explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}"
        ".explanation.show{display:block}"
        f".dialogue{{margin:6px 0 12px;padding:14px 16px;background:{t['dialog_bg']};border-left:3px solid {t['dialog_brd']};border-radius:0 8px 8px 0;font-size:1.02em;line-height:1.9}}"
        ".dialogue p{margin:0 0 .5em;padding:0}"
        ".dialogue p:last-child{margin-bottom:0}"
        f".dialogue .sp{{font-weight:700;color:{t['dialog_txt']};margin-right:.2em}}"
        "ruby{ruby-align:center}"
        "rt{font-size:.55em;font-weight:400;line-height:1.1}"
        ".blank-paren{display:inline-block;color:#c05621;font-weight:700;white-space:nowrap}"
    )

# ---------- JS ----------
JS_SHUFFLE_OPTIONS = r"""function shuffleAllOptions(){function r(n){if(n<=1)return 0;try{if(crypto&&crypto.getRandomValues){const lim=Math.floor(4294967296/n)*n,b=new Uint32Array(1);let x;do{crypto.getRandomValues(b);x=b[0]}while(x>=lim);return x%n}}catch(e){}return Math.floor(Math.random()*n)}function fy(a){for(let i=a.length-1;i>0;i--){const j=r(i+1),t=a[i];a[i]=a[j];a[j]=t}}function upd(o,e){const ks=Array.from(o.querySelectorAll('input[value="1"]')).map(inp=>{const k=inp.closest('.option').querySelector('.opt-key'),m=k&&k.textContent.match(/^(\d+)\./);return m?m[1]:''}).filter(Boolean);if(ks.length)e.innerHTML=e.innerHTML.replace(/正解：[0-9・]+/,'正解：'+ks.join('・'))}function rel(o,it,p){it.forEach(el=>o.appendChild(el));it.forEach((el,i)=>{const inp=el.querySelector('input'),lab=el.querySelector('label'),id=p+String.fromCharCode(97+i);inp.id=id;lab.setAttribute('for',id);el.querySelector('.opt-key').textContent=(i+1)+'.'});const e=o.nextElementSibling;if(e&&e.classList.contains('explanation'))upd(o,e);return it.findIndex(el=>el.querySelector('input[value="1"]'))}const cnt=[0,0,0,0];document.querySelectorAll('.options').forEach(o=>{const it=Array.from(o.children).filter(el=>el.classList.contains('option'));if(it.length<2)return;fy(it);const p=o.querySelector('input').name;let s=rel(o,it,p);let min=Math.min(...cnt.slice(0,it.length)),c=[];for(let i=0;i<it.length;i++)if(cnt[i]===min)c.push(i);const ideal=c[r(c.length)];if(s!==ideal&&cnt[s]>cnt[ideal]){const t=it[s];it[s]=it[ideal];it[ideal]=t;s=rel(o,it,p)}cnt[s]++})}"""

JS_SHUFFLE_QUESTIONS = r"""function shuffleQuestions(){const sec=document.getElementById('qSection');if(!sec)return;const qs=Array.from(sec.querySelectorAll(':scope > .question'));function r(n){if(n<=1)return 0;try{if(crypto&&crypto.getRandomValues){const lim=Math.floor(4294967296/n)*n,b=new Uint32Array(1);let x;do{crypto.getRandomValues(b);x=b[0]}while(x>=lim);return x%n}}catch(e){}return Math.floor(Math.random()*n)}for(let i=qs.length-1;i>0;i--){const j=r(i+1);[qs[i],qs[j]]=[qs[j],qs[i]]}qs.forEach(q=>sec.appendChild(q));qs.forEach((q,i)=>{const n=q.querySelector('.q-num');if(n)n.textContent=(i+1).toString()})}"""

JS_TIMER_SUBMIT = r"""function startTimer(){timerInterval=setInterval(()=>{if(paused)return;timeLeft--;const m=Math.floor(timeLeft/60),s=timeLeft%60,t=document.getElementById('timer');t.textContent=`${m}:${s.toString().padStart(2,'0')}`;document.getElementById('progress').style.width=(timeLeft/TIME_LIMIT*100)+'%';if(timeLeft<=60){t.className='timer danger'}else if(timeLeft<=300){t.className='timer warning'}else{t.className='timer'}if(timeLeft<=0){clearInterval(timerInterval);submitTest()}},1000)}
function submitTest(){if(submitted)return;submitted=true;clearInterval(timerInterval);let score=0;for(let i=1;i<=TOTAL;i++){const opts=Array.from(document.querySelectorAll(`input[name="q${i}"]`)),sel=opts.find(o=>o.checked);if(sel&&sel.value==='1')score++;opts.forEach(o=>{const w=o.closest('.option');if(o.value==='1')w.classList.add('correct');else if(o.checked)w.classList.add('wrong')});const exp=opts[0].closest('.question').querySelector('.explanation');if(exp)exp.classList.add('show')}const pct=Math.round(score/TOTAL*100),p=document.getElementById('resultPanel'),sc=document.getElementById('resultScore'),tt=document.getElementById('resultTitle');p.style.display='block';sc.textContent=`${score} / ${TOTAL}（${pct}%）`;sc.className='result-score '+(pct>=90?'excellent':pct>=70?'good':pct>=50?'fair':'poor');tt.textContent=pct>=90?'すばらしい！':pct>=70?'よくできました！':pct>=50?'もうすこし！':'がんばりましょう！';const used=TIME_LIMIT-timeLeft;document.getElementById('resultDetail').innerHTML=`<div class="result-item"><div class="label">せいかい</div><div class="value">${score}/${TOTAL}</div></div><div class="result-item"><div class="label">じかん</div><div class="value">${Math.floor(used/60)}分${used%60}秒</div></div>`;document.getElementById('submitBtn').disabled=true;document.getElementById('pauseBtn').disabled=true;p.scrollIntoView({behavior:'smooth'})}
startTimer();"""

JS_PAUSE = r"""function togglePause(){if(submitted)return;paused=!paused;const b=document.getElementById('pauseBtn'),t=document.getElementById('timer');b.textContent=paused?'▶':'⏸';b.setAttribute('aria-label',paused?'再開':'一時停止');if(paused){t.classList.add('paused');t.classList.remove('warning','danger')}else{t.classList.remove('paused');if(timeLeft<=60)t.classList.add('danger');else if(timeLeft<=300)t.classList.add('warning')}}"""

def script_block(total, with_shuffle_q=False, time_limit=600):
    head = f"const TOTAL={total},TIME_LIMIT={time_limit};let timeLeft=TIME_LIMIT,timerInterval,submitted=false,paused=false;"
    pieces = [head, JS_PAUSE]
    if with_shuffle_q:
        pieces.append(JS_SHUFFLE_QUESTIONS)
    pieces.append(JS_SHUFFLE_OPTIONS)
    if with_shuffle_q:
        pieces.append("try{shuffleQuestions();shuffleAllOptions()}catch(e){}")
    else:
        pieces.append("try{shuffleAllOptions()}catch(e){}")
    pieces.append(JS_TIMER_SUBMIT)
    return "\n".join(pieces)

# ---------- 問題レンダリング ----------
def Q(text, options, expl, *, one_col=False, dialogue=None):
    return dict(text=text, options=options, expl=expl, one_col=one_col, dialogue=dialogue)

def render_question(q, idx):
    qtext = f'<div class="q-text"><span class="q-num">{idx}</span>{q["text"]}</div>'
    dlg = ''
    if q.get('dialogue'):
        lines = ''.join(f'<p><span class="sp">{sp}：</span>{txt}</p>' for sp, txt in q['dialogue'])
        dlg = f'<div class="dialogue">{lines}</div>\n'
    opts_style = ' style="grid-template-columns:1fr"' if q.get('one_col') else ''
    opt_html = ''
    for i, (txt, val) in enumerate(q['options']):
        suf = chr(ord('a') + i)
        opt_html += (
            f'<div class="option"><input id="q{idx}{suf}" name="q{idx}" type="radio" value="{val}"/>'
            f'<label for="q{idx}{suf}"><span class="opt-key">{i+1}.</span><span class="opt-body">{txt}</span></label></div>\n'
        )
    return (
        f'<div class="question">\n{qtext}\n{dlg}<div class="options"{opts_style}>\n{opt_html}</div>\n'
        f'<div class="explanation">{q["expl"]}</div>\n</div>\n'
    )

def render_file(filename, *, title, count, theme_key, questions,
                with_shuffle_q=False, section_title=None, lead=None,
                timer_display='10:00', time_limit=600):
    theme = THEMES[theme_key]
    sec_open = '<div class="section" id="qSection">' if with_shuffle_q else '<div class="section">'
    sec_title_html = f'<div class="section-title">{section_title}</div>\n' if section_title else ''
    lead_html = f'<p class="section-lead">{lead}</p>\n' if lead else ''
    qs_html = ''.join(render_question(q, i+1) for i, q in enumerate(questions))
    js = script_block(count, with_shuffle_q=with_shuffle_q, time_limit=time_limit)
    html = f"""<!DOCTYPE html>

<html lang="ja">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>{title}</title>
<style>{css(theme)}</style>
</head>
<body>

<div class="container"><header><h1>{title}</h1><div class="header-info"><div class="timer-group"><div class="timer" id="timer">{timer_display}</div><button aria-label="一時停止" class="pause-btn" id="pauseBtn" onclick="togglePause()" type="button">⏸</button></div><div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div><div class="score-badge" id="scoreBadge">{R('全','ぜん')}{count}{R('問','もん')}</div></div></header>

{sec_open}
{sec_title_html}{lead_html}{qs_html}</div>

<button class="btn-submit" id="submitBtn" onclick="submitTest()">{R('採点','さいてん')}する</button>
<div class="result-panel" id="resultPanel"><h2 id="resultTitle"></h2><div class="result-score" id="resultScore"></div><div class="result-detail" id="resultDetail"></div></div>
</div>
<script>{js}</script>
</body>
</html>
"""
    (OUT / filename).write_text(html, encoding='utf-8')

# ======================================================================
# ---- 共通リード ----
# ======================================================================
LEAD = f'（　）に{R("入","はい")}る{R("正","ただ")}しいものはどれですか。'

# ======================================================================
# ---- bunpo01 ここ／そこ／あそこ／どこ ----
# ======================================================================
BUNPO01 = [
    # Q1: どこ vs 他の疑問詞
    Q(f'すみません、エレベーターは{BLANK}ですか。……あそこです。',
      [('どこ',1),('どれ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 場所をたずねる時は「どこ」を使います。「どれ」は物、「だれ」は人、「なん」は名前・物。'),

    # Q2: どこ vs 他
    Q(f'ミラーさんは{BLANK}ですか。……{R("会議室","かいぎしつ")}です。',
      [('どこ',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — 人が「どこ」にいるかをたずねます。答えが場所（会議室）なので「どこ」。'),

    # Q3: どこ vs 他
    Q(f'{R("自動販売機","じどうはんばいき")}は{BLANK}ですか。……ロビーです。',
      [('どこ',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — 場所をたずねる「どこ」。答えは「ロビー」（場所）。'),

    # Q4: 答えの形（場所が入る）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('あそこ',1),('ミラーさん',0),('1,500{R0}'.format(R0=R("円","えん")),0),('アメリカ{R0}'.format(R0=R("人","じん")),0)],
      '✅ 正解：1 — 場所をたずねられたら、場所のことば（あそこ）で答えます。',
      one_col=True,
      dialogue=[('A', f'トイレは　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q5: ここ（はなす人のところ）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。〔Aは{R("受付","うけつけ")}の{R("前","まえ")}に{R("立","た")}って、{R("自分","じぶん")}の{R("場所","ばしょ")}を{R("指","ゆび")}さして　{R("言","い")}う〕',
      [('ここ',1),('あそこ',0),('どこ',0),('それ',0)],
      '✅ 正解：1 — 「ここ」は、はなしている人が　いる場所を　ゆびします。',
      dialogue=[('A', f'{BLANK}は　{R("受付","うけつけ")}です。'),
                ('B', f'ありがとうございます。')]),

    # Q6: あそこ（遠い場所）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。〔Aと　Bから　{R("遠","とお")}い{R("場所","ばしょ")}に　{R("食堂","しょくどう")}がある〕',
      [('あそこ',1),('ここ',0),('それ',0),('どれ',0)],
      '✅ 正解：1 — 「あそこ」は、はなす人にも　きく人にも　とおい場所を　ゆびします。',
      dialogue=[('A', f'{R("食堂","しょくどう")}は　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q7: ここ vs あそこ 概念
    Q(f'「ここ」の　いみとして　{R("正","ただ")}しいものはどれですか。',
      [(f'はなしている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',1),
       (f'きいている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',0),
       (f'はなしている　{R("人","ひと")}にも　きいている　{R("人","ひと")}にも　{R("遠","とお")}い　{R("場所","ばしょ")}',0),
       (f'{R("名前","なまえ")}が　わからない　{R("場所","ばしょ")}',0)],
      '✅ 正解：1 — 「ここ」＝はなし手の場所、「そこ」＝きき手の場所、「あそこ」＝両方からとおい場所。',
      one_col=True),

    # Q8: 「あそこ」の意味
    Q(f'「あそこ」の　いみとして　{R("正","ただ")}しいものはどれですか。',
      [(f'はなしている　{R("人","ひと")}にも　きいている　{R("人","ひと")}にも　{R("遠","とお")}い　{R("場所","ばしょ")}',1),
       (f'はなしている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',0),
       (f'きいている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',0),
       (f'{R("名前","なまえ")}が　わからない　{R("場所","ばしょ")}',0)],
      '✅ 正解：1 — 「あそこ」は、はなす人にも　きく人にも　とおい場所。',
      one_col=True),

    # Q9: 正しい文を選ぶ — どこは主語にできない
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'ここは　{R("教室","きょうしつ")}です。',1),
       (f'ここの　{R("教室","きょうしつ")}です。',0),
       (f'ここに　{R("教室","きょうしつ")}です。',0),
       (f'ここで　{R("教室","きょうしつ")}です。',0)],
      '✅ 正解：1 — 「ここは Nです」で「ここはNだ」を表します。「の／に／で」は不可。',
      one_col=True),

    # Q10: 答えとして自然なもの
    Q(f'「{R("会議室","かいぎしつ")}は　どこですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'あそこです。',1),
       (f'ミラーさんです。',0),
       (f'1,500{R("円","えん")}です。',0),
       (f'アメリカ{R("人","じん")}です。',0)],
      '✅ 正解：1 — 「どこ」（場所）に対する答えは場所のことば。',
      one_col=True),
]

# ======================================================================
# ---- bunpo02 こちら／そちら／あちら／どちら ----
# ======================================================================
BUNPO02 = [
    # Q1: お国はどちら
    Q(f'お{R("国","くに")}は{BLANK}ですか。……アメリカです。',
      [('どちら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 「お国」など、ていねいに聞きたいときは「どちら」を使います。'),

    # Q2: 会社はどちら
    Q(f'{R("会社","かいしゃ")}は{BLANK}ですか。……IMCです。',
      [('どちら',1),('どこ',0),('どれ',0),('いくら',0)],
      '✅ 正解：1 — 会社・大学・うちなどを聞くときは「どちら」がていねい。'),

    # Q3: 大学はどちら
    Q(f'{R("大学","だいがく")}は{BLANK}ですか。……さくら{R("大学","だいがく")}です。',
      [('どちら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 大学のなまえを聞くときも「どちら」。'),

    # Q4: うちはどちら
    Q(f'うちは{BLANK}ですか。……バンコクです。',
      [('どちら',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — うち（住まい）も「どちら」でていねいに聞きます。'),

    # Q5: 「どちら」の意味
    Q(f'「どちら」は　どんな　いみですか。',
      [(f'「どこ」の　ていねいな　{R("言","い")}い{R("方","かた")}',1),
       (f'「どれ」の　ていねいな　{R("言","い")}い{R("方","かた")}',0),
       (f'「だれ」の　ていねいな　{R("言","い")}い{R("方","かた")}',0),
       (f'「いくら」の　ていねいな　{R("言","い")}い{R("方","かた")}',0)],
      '✅ 正解：1 — 「どちら」は場所をていねいに聞く言い方。',
      one_col=True),

    # Q6: あちら（指す）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。〔Bは　{R("遠","とお")}い{R("場所","ばしょ")}を　ゆびさして　{R("言","い")}う〕',
      [('あちら',1),('こちら',0),('そちら',0),('どちら',0)],
      '✅ 正解：1 — 「あちら」は「あそこ」のていねいな言い方。とおい場所をゆびします。',
      dialogue=[('A', f'エレベーターは　どちらですか。'),
                ('B', f'{BLANK}です。')]),

    # Q7: こちら（はなす人の場所）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。〔Aは{R("自分","じぶん")}の　いる　{R("場所","ばしょ")}を　ゆびさして　{R("言","い")}う〕',
      [('こちら',1),('そちら',0),('あちら',0),('どちら',0)],
      '✅ 正解：1 — 「こちら」は「ここ」のていねいな言い方。はなしている人の場所。',
      dialogue=[('A', f'{R("事務所","じむしょ")}は　{BLANK}です。'),
                ('B', f'ありがとうございます。')]),

    # Q8: 答えとして自然なもの
    Q(f'「お{R("国","くに")}は　どちらですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'ドイツです。',1),
       (f'1,500{R("円","えん")}です。',0),
       (f'ミラーさんです。',0),
       (f'{R("学生","がくせい")}です。',0)],
      '✅ 正解：1 — 「お国は どちらですか」に対しては、国のなまえで答えます。',
      one_col=True),

    # Q9: ていねいな言い方
    Q(f'もっとも　ていねいな　{R("文","ぶん")}はどれですか。',
      [(f'お{R("国","くに")}は　どちらですか。',1),
       (f'お{R("国","くに")}は　どこですか。',0),
       (f'お{R("国","くに")}は　どれですか。',0),
       (f'お{R("国","くに")}は　なんですか。',0)],
      '✅ 正解：1 — 「お国は」のあとは、ていねいな「どちら」。',
      one_col=True),

    # Q10: こちら・そちら・あちらの関係
    Q(f'「こちら」「そちら」「あちら」「どちら」と　{R("同","おな")}じ　いみの　ことばを　えらんで　ください。「こちら」=（　）',
      [('ここ',1),('そこ',0),('あそこ',0),('どこ',0)],
      '✅ 正解：1 — こちら＝ここ、そちら＝そこ、あちら＝あそこ、どちら＝どこ（すべてていねい）。'),
]

# ======================================================================
# ---- bunpo03 Nは場所です（〜はどこですか） ----
# ======================================================================
BUNPO03 = [
    # Q1: トイレはどこ — 答え：あそこです
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('あそこ',1),('ミラーさん',0),('アメリカ{R0}'.format(R0=R("人","じん")),0),('1,500{R0}'.format(R0=R("円","えん")),0)],
      '✅ 正解：1 — 「どこ」（場所）に対する答えは場所のことば。',
      one_col=True,
      dialogue=[('A', f'トイレは　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q2: 山田さんはどこ — 会議室
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [(f'{R("会議室","かいぎしつ")}',1),
       (f'{R("学生","がくせい")}',0),
       (f'アメリカ{R("人","じん")}',0),
       (f'1,500{R("円","えん")}',0)],
      '✅ 正解：1 — 「やまださんはどこですか」には場所で答えます。',
      one_col=True,
      dialogue=[('A', f'{R("山田","やまだ")}さんは　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q3: 自動販売機は…（2階）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('2{R0}'.format(R0=R("階","かい")),1),
       (f'ミラーさん',0),
       (f'アメリカ{R("人","じん")}',0),
       (f'1,500{R("円","えん")}',0)],
      '✅ 正解：1 — 場所をたずねたら、場所（階）で答えます。',
      one_col=True,
      dialogue=[('A', f'{R("自動販売機","じどうはんばいき")}は　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q4: テレーザちゃんは…
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [(f'{R("教室","きょうしつ")}',1),
       (f'1,500{R("円","えん")}',0),
       (f'アメリカ{R("人","じん")}',0),
       (f'{R("学生","がくせい")}',0)],
      '✅ 正解：1 — 場所をたずねた答え（教室）。',
      one_col=True,
      dialogue=[('A', f'テレーザちゃんは　どこですか。'),
                ('B', f'{BLANK}です。')]),

    # Q5: 食堂は地下
    Q(f'{R("食堂","しょくどう")}は{BLANK}です。',
      [(f'{R("地下","ちか")}',1),
       (f'ミラーさん',0),
       (f'1,500{R("円","えん")}',0),
       (f'{R("学生","がくせい")}',0)],
      '✅ 正解：1 — 「食堂は〜です」の〜は場所。地下（場所）が入る。',
      one_col=True),

    # Q6: 会議室のかぎは事務所です
    Q(f'{R("会議室","かいぎしつ")}の　かぎは{BLANK}です。',
      [(f'{R("事務所","じむしょ")}',1),
       (f'1,500{R("円","えん")}',0),
       (f'ミラーさん',0),
       (f'アメリカ{R("人","じん")}',0)],
      '✅ 正解：1 — 場所をたずねた答え（事務所＝場所）。',
      one_col=True),

    # Q7: 〜はどこですか
    Q(f'ミラーさんは{BLANK}ですか。',
      [('どこ',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — 場所を聞くときは「どこ」。'),

    # Q8: 答えのパターン
    Q(f'「{R("受付","うけつけ")}は　どこですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'1{R("階","かい")}です。',1),
       (f'ミラーさんです。',0),
       (f'1,500{R("円","えん")}です。',0),
       (f'アメリカ{R("人","じん")}です。',0)],
      '✅ 正解：1 — 「どこ」に対しては場所で答えます。「1階」が正解。',
      one_col=True),

    # Q9: 正しい文
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("受付","うけつけ")}は　ここです。',1),
       (f'{R("受付","うけつけ")}が　ここです。',0),
       (f'{R("受付","うけつけ")}に　ここです。',0),
       (f'{R("受付","うけつけ")}の　ここです。',0)],
      '✅ 正解：1 — 「Nは ここです」。主題のしるしは「は」。',
      one_col=True),

    # Q10: 質問と答えのペア
    Q(f'{R("正","ただ")}しい　ペアはどれですか。',
      [(f'A：エレベーターは　どこですか。 / B：あそこです。',1),
       (f'A：エレベーターは　どこですか。 / B：ミラーさんです。',0),
       (f'A：エレベーターは　どこですか。 / B：1,500{R("円","えん")}です。',0),
       (f'A：エレベーターは　どこですか。 / B：{R("学生","がくせい")}です。',0)],
      '✅ 正解：1 — 「どこですか」（場所）には「あそこ／2階」など場所で答えます。',
      one_col=True),
]

# ======================================================================
# ---- bunpo04 どこのN／〜のN（産地・所属） ----
# ======================================================================
BUNPO04 = [
    # Q1: どこの車ですか
    Q(f'これは{BLANK}の　{R("車","くるま")}ですか。……ドイツの　{R("車","くるま")}です。',
      [('どこ',1),('どちら',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 産地を聞くときは「どこの N」。'),

    # Q2: 日本の N
    Q(f'これは　{R("日本","にほん")}{BLANK}　カメラです。',
      [('の',1),('と',0),('は',0),('が',0)],
      '✅ 正解：1 — 「国名＋の＋N」で「〜のN」（産地・所有）。'),

    # Q3: 何の会社ですか
    Q(f'パワー{R("電気","でんき")}は{BLANK}の　{R("会社","かいしゃ")}ですか。……コンピューターの　{R("会社","かいしゃ")}です。',
      [(f'{R("何","なん")}',1),('どこ',0),('だれ',0),('どちら',0)],
      '✅ 正解：1 — 会社の「しゅるい」を聞くときは「何の」。「どこの会社」は場所を聞きます。'),

    # Q4: 答え：（国名）のです
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('フランス',1),('1,500{R0}'.format(R0=R("円","えん")),0),(R("学生","がくせい"),0),('ミラーさん',0)],
      '✅ 正解：1 — 「どこのですか」に対しては国の名前で答えます。',
      one_col=True,
      dialogue=[('A', f'この　ネクタイは　どこのですか。'),
                ('B', f'{BLANK}のです。')]),

    # Q5: ワインは日本のです
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [(f'{R("日本","にほん")}',1),('1,500{R0}'.format(R0=R("円","えん")),0),(R("学生","がくせい"),0),('ミラーさん',0)],
      '✅ 正解：1 — ワインの産地として国の名前で答えます。',
      one_col=True,
      dialogue=[('A', f'この　ワインは　どこのですか。'),
                ('B', f'{BLANK}のです。')]),

    # Q6: イタリアの靴
    Q(f'これは　イタリア{BLANK}　{R("靴","くつ")}です。',
      [('の',1),('と',0),('は',0),('が',0)],
      '✅ 正解：1 — 「国名＋の＋N」。'),

    # Q7: どこのワインですか
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('どこ',1),('どれ',0),('だれ',0),(f'{R("何","なん")}',0)],
      '✅ 正解：1 — 「どこのワイン」で産地を聞きます。',
      dialogue=[('A', f'これは　{BLANK}の　ワインですか。'),
                ('B', f'{R("日本","にほん")}のです。')]),

    # Q8: 正しい文
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'これは　ドイツの　{R("車","くるま")}です。',1),
       (f'これは　ドイツが　{R("車","くるま")}です。',0),
       (f'これは　ドイツは　{R("車","くるま")}です。',0),
       (f'これは　ドイツに　{R("車","くるま")}です。',0)],
      '✅ 正解：1 — 産地は「国名＋の＋N」。「が／は／に」は不可。',
      one_col=True),

    # Q9: パワー電気は何の会社
    Q(f'パワー{R("電気","でんき")}は　コンピューター{BLANK}　{R("会社","かいしゃ")}です。',
      [('の',1),('と',0),('は',0),('が',0)],
      '✅ 正解：1 — 「Nの会社」で「Nを作る／うる会社」。'),

    # Q10: どこのくつ
    Q(f'「これは　どこの　{R("靴","くつ")}ですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'イタリアの　{R("靴","くつ")}です。',1),
       (f'ミラーさんです。',0),
       (f'1,500{R("円","えん")}です。',0),
       (f'{R("学生","がくせい")}です。',0)],
      '✅ 正解：1 — 「どこの N」に対しては「国名＋の＋N」で答えます。',
      one_col=True),
]

# ======================================================================
# ---- bunpo05 いくらですか／値段・大きな数 ----
# ======================================================================
BUNPO05 = [
    # Q1: いくらですか — ネクタイ
    Q(f'この　ネクタイは{BLANK}ですか。……1,500{R("円","えん")}です。',
      [('いくら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 値段（ねだん）を聞くときは「いくら」。'),

    # Q2: いくらですか — 時計
    Q(f'この　{R("時計","とけい")}は{BLANK}ですか。……18,600{R("円","えん")}です。',
      [('いくら',1),('どこ',0),('だれ',0),(f'{R("何","なん")}',0)],
      '✅ 正解：1 — 値段は「いくら」。'),

    # Q3: いくらの答えとして自然
    Q(f'「この　カメラは　いくらですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'25,800{R("円","えん")}です。',1),
       (f'{R("食堂","しょくどう")}です。',0),
       (f'アメリカです。',0),
       (f'ミラーさんです。',0)],
      '✅ 正解：1 — 「いくら」（値段）には「〜円」で答えます。',
      one_col=True),

    # Q4: 13,000円の読み方
    Q(f'13,000{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('いちまんさんぜんえん',1),
       ('いちまんさんびゃくえん',0),
       ('じゅうさんまんえん',0),
       ('じゅうさんせんえん',0)],
      '✅ 正解：1 — 13,000＝1万＋3千。「いちまんさんぜんえん」。',
      one_col=True),

    # Q5: 4,500,000円の読み方
    Q(f'4,500,000{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('よんひゃくごじゅうまんえん',1),
       ('よんせんごひゃくえん',0),
       ('よんまんごせんえん',0),
       ('よんまんごひゃくえん',0)],
      '✅ 正解：1 — 4,500,000＝450万＝「よんひゃくごじゅうまんえん」。',
      one_col=True),

    # Q6: 7,300円
    Q(f'7,300{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('ななせんさんびゃくえん',1),
       ('ななまんさんびゃくえん',0),
       ('ななひゃくさんじゅうえん',0),
       ('しちまんさんびゃくえん',0)],
      '✅ 正解：1 — 7,300＝7千3百。「ななせんさんびゃくえん」。',
      one_col=True),

    # Q7: 143,000円
    Q(f'143,000{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('じゅうよんまんさんぜんえん',1),
       ('ひゃくよんじゅうさんせんえん',0),
       ('じゅうよんせんえん',0),
       ('いちまんよんせんえん',0)],
      '✅ 正解：1 — 143,000＝14万3千。「じゅうよんまんさんぜんえん」。',
      one_col=True),

    # Q8: いくら（dialogue）
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いくら',1),('どこ',0),('だれ',0),(f'{R("何","なん")}',0)],
      '✅ 正解：1 — 答えが「3,200円」なので、値段を聞く「いくら」。',
      dialogue=[('A', f'この　ワインは　{BLANK}ですか。'),
                ('B', f'3,200{R("円","えん")}です。')]),

    # Q9: 2,500円の読み方
    Q(f'2,500{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('にせんごひゃくえん',1),
       ('にひゃくごじゅうえん',0),
       ('にせんごじゅうえん',0),
       ('にまんごひゃくえん',0)],
      '✅ 正解：1 — 2,500＝2千5百。「にせんごひゃくえん」。',
      one_col=True),

    # Q10: 質問と答えの正しいペア
    Q(f'{R("正","ただ")}しい　ペアはどれですか。',
      [(f'A：この　{R("車","くるま")}は　いくらですか。 / B：1,800,000{R("円","えん")}です。',1),
       (f'A：この　{R("車","くるま")}は　いくらですか。 / B：ドイツの　{R("車","くるま")}です。',0),
       (f'A：この　{R("車","くるま")}は　いくらですか。 / B：ミラーさんの　{R("車","くるま")}です。',0),
       (f'A：この　{R("車","くるま")}は　いくらですか。 / B：あそこです。',0)],
      '✅ 正解：1 — 「いくら」（値段）には「〜円」で答えます。',
      one_col=True),
]

# ======================================================================
# ---- まとめ1（①②③ミックス・12問・シャッフル） ----
# ======================================================================
MATOME1 = [
    # ① ここ系
    Q(f'すみません、エレベーターは{BLANK}ですか。……あそこです。',
      [('どこ',1),('どれ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 場所を聞くときは「どこ」。'),
    Q(f'「ここ」の　いみとして　{R("正","ただ")}しいものはどれですか。',
      [(f'はなしている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',1),
       (f'きいている　{R("人","ひと")}の　いる　{R("場所","ばしょ")}',0),
       (f'はなしている　{R("人","ひと")}にも　きいている　{R("人","ひと")}にも　{R("遠","とお")}い　{R("場所","ばしょ")}',0),
       (f'{R("名前","なまえ")}が　わからない　{R("場所","ばしょ")}',0)],
      '✅ 正解：1 — 「ここ」＝はなし手の場所。',
      one_col=True),
    Q(f'{R("自動販売機","じどうはんばいき")}は{BLANK}ですか。……ロビーです。',
      [('どこ',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — 場所を聞くときは「どこ」。'),
    # ② こちら系
    Q(f'お{R("国","くに")}は{BLANK}ですか。……アメリカです。',
      [('どちら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — お国・うち・会社・大学はていねいに「どちら」を使う。'),
    Q(f'{R("大学","だいがく")}は{BLANK}ですか。……さくら{R("大学","だいがく")}です。',
      [('どちら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 大学を聞くときも「どちら」。'),
    Q(f'もっとも　ていねいな　{R("文","ぶん")}はどれですか。',
      [(f'お{R("国","くに")}は　どちらですか。',1),
       (f'お{R("国","くに")}は　どこですか。',0),
       (f'お{R("国","くに")}は　どれですか。',0),
       (f'お{R("国","くに")}は　なんですか。',0)],
      '✅ 正解：1 — 「お国」のあとは「どちら」がていねい。',
      one_col=True),
    # ③ Nは場所です
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('あそこ',1),('ミラーさん',0),('1,500{R0}'.format(R0=R("円","えん")),0),('アメリカ{R0}'.format(R0=R("人","じん")),0)],
      '✅ 正解：1 — 場所を聞かれたら場所のことばで答える。',
      one_col=True,
      dialogue=[('A', f'トイレは　どこですか。'),
                ('B', f'{BLANK}です。')]),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [(f'{R("会議室","かいぎしつ")}',1),
       (f'{R("学生","がくせい")}',0),
       (f'アメリカ{R("人","じん")}',0),
       (f'1,500{R("円","えん")}',0)],
      '✅ 正解：1 — 「どこ」に対しては場所で答える（会議室）。',
      one_col=True,
      dialogue=[('A', f'{R("山田","やまだ")}さんは　どこですか。'),
                ('B', f'{BLANK}です。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("受付","うけつけ")}は　ここです。',1),
       (f'{R("受付","うけつけ")}が　ここです。',0),
       (f'{R("受付","うけつけ")}に　ここです。',0),
       (f'{R("受付","うけつけ")}の　ここです。',0)],
      '✅ 正解：1 — 主題は「は」、述語は「ここ／そこ／あそこ＋です」。',
      one_col=True),
    # ミックス
    Q(f'「お{R("国","くに")}は　どちらですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'ドイツです。',1),
       (f'1,500{R("円","えん")}です。',0),
       (f'ミラーさんです。',0),
       (f'{R("学生","がくせい")}です。',0)],
      '✅ 正解：1 — お国を聞かれたら国のなまえで答える。',
      one_col=True),
    Q(f'「こちら」と　{R("同","おな")}じ　いみの　ことばはどれですか。',
      [('ここ',1),('そこ',0),('あそこ',0),('どこ',0)],
      '✅ 正解：1 — こちら＝ここ（ていねい）。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。〔Bは　{R("遠","とお")}い{R("場所","ばしょ")}を　ゆびさして　{R("言","い")}う〕',
      [('あちら',1),('こちら',0),('そちら',0),('どちら',0)],
      '✅ 正解：1 — 「あちら」＝「あそこ」（ていねい）。',
      dialogue=[('A', f'エレベーターは　どちらですか。'),
                ('B', f'{BLANK}です。')]),
]

# ======================================================================
# ---- クイック復習1（①②③復習・8問・オレンジ） ----
# ======================================================================
QUICK1 = [
    # ①
    Q(f'すみません、トイレは{BLANK}ですか。……あそこです。',
      [('どこ',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — 場所を聞くときは「どこ」。'),
    Q(f'ミラーさんは{BLANK}ですか。……{R("会議室","かいぎしつ")}です。',
      [('どこ',1),('どれ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 人がいる場所を聞くときも「どこ」。'),
    # ②
    Q(f'お{R("国","くに")}は{BLANK}ですか。……インドネシアです。',
      [('どちら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — お国はていねいに「どちら」。'),
    Q(f'うちは{BLANK}ですか。……ベルリンです。',
      [('どちら',1),('どれ',0),('だれ',0),('いくら',0)],
      '✅ 正解：1 — うちもていねいに「どちら」。'),
    # ③
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('2{R0}'.format(R0=R("階","かい")),1),
       (f'ミラーさん',0),
       (f'1,500{R("円","えん")}',0),
       (f'アメリカ{R("人","じん")}',0)],
      '✅ 正解：1 — 「どこ」に対しては場所（2階）で答える。',
      one_col=True,
      dialogue=[('A', f'{R("自動販売機","じどうはんばいき")}は　どこですか。'),
                ('B', f'{BLANK}です。')]),
    Q(f'{R("食堂","しょくどう")}は{BLANK}です。',
      [(f'{R("地下","ちか")}',1),
       (f'ミラーさん',0),
       (f'1,500{R("円","えん")}',0),
       (f'{R("学生","がくせい")}',0)],
      '✅ 正解：1 — 「食堂は〜です」の〜には場所が入る（地下）。',
      one_col=True),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("受付","うけつけ")}は　ここです。',1),
       (f'{R("受付","うけつけ")}が　ここです。',0),
       (f'{R("受付","うけつけ")}に　ここです。',0),
       (f'{R("受付","うけつけ")}の　ここです。',0)],
      '✅ 正解：1 — 主題は「は」。',
      one_col=True),
    # mix
    Q(f'「こちら」「そちら」「あちら」「どちら」と　{R("同","おな")}じ　いみの　ことばを　えらんで　ください。「あちら」=（　）',
      [('あそこ',1),('ここ',0),('そこ',0),('どこ',0)],
      '✅ 正解：1 — あちら＝あそこ（ていねい）。'),
]

# ======================================================================
# ---- まとめ2（④⑤ミックス・12問・シャッフル） ----
# ======================================================================
MATOME2 = [
    # ④ どこのN
    Q(f'これは{BLANK}の　{R("車","くるま")}ですか。……ドイツの　{R("車","くるま")}です。',
      [('どこ',1),('どちら',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 産地を聞くときは「どこの N」。'),
    Q(f'これは　{R("日本","にほん")}{BLANK}　カメラです。',
      [('の',1),('と',0),('は',0),('が',0)],
      '✅ 正解：1 — 「国名＋の＋N」。'),
    Q(f'パワー{R("電気","でんき")}は{BLANK}の　{R("会社","かいしゃ")}ですか。……コンピューターの　{R("会社","かいしゃ")}です。',
      [(f'{R("何","なん")}',1),('どこ',0),('だれ',0),('どちら',0)],
      '✅ 正解：1 — 会社のしゅるいを聞くときは「何の」。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('フランス',1),('1,500{R0}'.format(R0=R("円","えん")),0),(R("学生","がくせい"),0),('ミラーさん',0)],
      '✅ 正解：1 — 「どこのですか」には国名で答える。',
      one_col=True,
      dialogue=[('A', f'この　ネクタイは　どこのですか。'),
                ('B', f'{BLANK}のです。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'これは　イタリアの　{R("靴","くつ")}です。',1),
       (f'これは　イタリアが　{R("靴","くつ")}です。',0),
       (f'これは　イタリアは　{R("靴","くつ")}です。',0),
       (f'これは　イタリアに　{R("靴","くつ")}です。',0)],
      '✅ 正解：1 — 産地は「国名＋の＋N」。',
      one_col=True),
    Q(f'パワー{R("電気","でんき")}は　コンピューター{BLANK}　{R("会社","かいしゃ")}です。',
      [('の',1),('と',0),('は',0),('が',0)],
      '✅ 正解：1 — 「Nの会社」で「Nを作る／うる会社」。'),
    # ⑤ いくら
    Q(f'この　ネクタイは{BLANK}ですか。……1,500{R("円","えん")}です。',
      [('いくら',1),('どこ',0),('どれ',0),('だれ',0)],
      '✅ 正解：1 — 値段は「いくら」。'),
    Q(f'13,000{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('いちまんさんぜんえん',1),
       ('いちまんさんびゃくえん',0),
       ('じゅうさんまんえん',0),
       ('じゅうさんせんえん',0)],
      '✅ 正解：1 — 13,000＝1万3千。',
      one_col=True),
    Q(f'4,500,000{R("円","えん")}の　{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('よんひゃくごじゅうまんえん',1),
       ('よんせんごひゃくえん',0),
       ('よんまんごせんえん',0),
       ('よんまんごひゃくえん',0)],
      '✅ 正解：1 — 4,500,000＝450万。',
      one_col=True),
    Q(f'「この　カメラは　いくらですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'25,800{R("円","えん")}です。',1),
       (f'{R("食堂","しょくどう")}です。',0),
       (f'アメリカです。',0),
       (f'ミラーさんです。',0)],
      '✅ 正解：1 — 値段は「〜円」で答える。',
      one_col=True),
    # mix
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いくら',1),('どこ',0),('だれ',0),(f'{R("何","なん")}',0)],
      '✅ 正解：1 — 答えが「3,200円」なので「いくら」。',
      dialogue=[('A', f'この　ワインは　{BLANK}ですか。'),
                ('B', f'3,200{R("円","えん")}です。')]),
    Q(f'「これは　どこの　{R("靴","くつ")}ですか」の　{R("答","こた")}えとして　{R("正","ただ")}しいものはどれですか。',
      [(f'イタリアの　{R("靴","くつ")}です。',1),
       (f'ミラーさんです。',0),
       (f'1,500{R("円","えん")}です。',0),
       (f'{R("学生","がくせい")}です。',0)],
      '✅ 正解：1 — 「どこのN」には「国名＋の＋N」で答える。',
      one_col=True),
]

# ======================================================================
# ---- ファイル生成 ----
# ======================================================================
def build_all():
    # 個別文法（青・10分）
    render_file('bunpo01-koko-soko-asoko-doko.html',
        title=f'L3 {R("文法","ぶんぽう")}① ここ／そこ／あそこ／どこ（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO01,
        section_title=f'A. ここ／そこ／あそこ／どこ（{R("場所","ばしょ")}{R("代名詞","だいめいし")}）',
        lead=LEAD)

    render_file('bunpo02-kochira-sochira-achira-dochira.html',
        title=f'L3 {R("文法","ぶんぽう")}② こちら／そちら／あちら／どちら（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO02,
        section_title=f'B. こちら／そちら／あちら／どちら（ていねいな{R("言","い")}い{R("方","かた")}）',
        lead=LEAD)

    render_file('bunpo03-wa-basho-desu.html',
        title=f'L3 {R("文法","ぶんぽう")}③ Nは{R("場所","ばしょ")}です／〜はどこですか（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO03,
        section_title=f'C. Nは{R("場所","ばしょ")}です（{R("場所","ばしょ")}を{R("尋","たず")}ねる・{R("答","こた")}える）',
        lead=LEAD)

    render_file('bunpo04-doko-no-n.html',
        title=f'L3 {R("文法","ぶんぽう")}④ どこのN／〜のN（{R("産地","さんち")}・{R("所有","しょゆう")}）（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO04,
        section_title=f'D. どこのN／{R("国名","こくめい")}＋の＋N',
        lead=LEAD)

    render_file('bunpo05-ikura.html',
        title=f'L3 {R("文法","ぶんぽう")}⑤ いくらですか／{R("値段","ねだん")}（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO05,
        section_title=f'E. いくらですか／{R("大","おお")}きな{R("数","かず")}（〜{R("千","せん")}・〜{R("万","まん")}）',
        lead=LEAD)

    # まとめ（紫・10分・シャッフル）
    render_file('bunpo-matome1.html',
        title=f'L3 1{R("回目","かいめ")}まとめテスト（10{R("分","ふん")}・12{R("問","もん")}）',
        count=12, theme_key='purple', questions=MATOME1,
        with_shuffle_q=True, lead=LEAD)

    render_file('bunpo-matome2.html',
        title=f'L3 2{R("回目","かいめ")}まとめテスト（10{R("分","ふん")}・12{R("問","もん")}）',
        count=12, theme_key='purple', questions=MATOME2,
        with_shuffle_q=True, lead=LEAD)

    # クイック復習（オレンジ）
    render_file('bunpo-quickreview1.html',
        title=f'L3 2{R("回目","かいめ")}クイック{R("復習","ふくしゅう")}テスト（10{R("分","ふん")}・8{R("問","もん")}）',
        count=8, theme_key='orange', questions=QUICK1,
        section_title=f'1{R("回目","かいめ")}の{R("復習","ふくしゅう")}（ここ／そこ／あそこ／どこ・こちら/そちら/あちら/どちら・Nは{R("場所","ばしょ")}です）',
        lead=LEAD)

if __name__ == '__main__':
    build_all()
    print('Generated 8 bunpo files in', OUT)
