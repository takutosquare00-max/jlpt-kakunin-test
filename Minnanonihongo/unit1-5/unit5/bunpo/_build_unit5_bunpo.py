#!/usr/bin/env python3
"""第5課 文法HTMLテスト一式の生成スクリプト。

Outputs (in same directory):
  bunpo01-e-place.html, bunpo02-de-vehicle.html, bunpo03-to-person.html
  bunpo04-dokoemo.html, bunpo05-itsu.html, bunpo06-yo.html
  bunpo-matome1.html, bunpo-matome2.html, bunpo-quickreview1.html

CSS/JSは共通テンプレート、色テーマと問題のみが差分。
方針: shared/bunpo-test-creation-guide.md
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

# 空欄
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

# ---------- JS（共通スニペット） ----------
JS_SHUFFLE_OPTIONS = r"""function shuffleAllOptions(){function r(n){if(n<=1)return 0;try{if(crypto&&crypto.getRandomValues){const lim=Math.floor(4294967296/n)*n,b=new Uint32Array(1);let x;do{crypto.getRandomValues(b);x=b[0]}while(x>=lim);return x%n}}catch(e){}return Math.floor(Math.random()*n)}function fy(a){for(let i=a.length-1;i>0;i--){const j=r(i+1),t=a[i];a[i]=a[j];a[j]=t}}function upd(o,e){const ks=Array.from(o.querySelectorAll('input[value="1"]')).map(inp=>{const k=inp.closest('.option').querySelector('.opt-key'),m=k&&k.textContent.match(/^(\d+)\./);return m?m[1]:''}).filter(Boolean);if(ks.length)e.innerHTML=e.innerHTML.replace(/正解：[0-9・]+/,'正解：'+ks.join('・'))}function rel(o,it,p){it.forEach(el=>o.appendChild(el));it.forEach((el,i)=>{const inp=el.querySelector('input'),lab=el.querySelector('label'),id=p+String.fromCharCode(97+i);inp.id=id;lab.setAttribute('for',id);el.querySelector('.opt-key').textContent=(i+1)+'.'});const e=o.nextElementSibling;if(e&&e.classList.contains('explanation'))upd(o,e);return it.findIndex(el=>el.querySelector('input[value="1"]'))}const cnt=[0,0,0,0];document.querySelectorAll('.options').forEach(o=>{const it=Array.from(o.children).filter(el=>el.classList.contains('option'));if(it.length<2)return;fy(it);const p=o.querySelector('input').name;let s=rel(o,it,p);let min=Math.min(...cnt.slice(0,it.length)),c=[];for(let i=0;i<it.length;i++)if(cnt[i]===min)c.push(i);const ideal=c[r(c.length)];if(s!==ideal&&cnt[s]>cnt[ideal]){const t=it[s];it[s]=it[ideal];it[ideal]=t;s=rel(o,it,p)}cnt[s]++})}"""

JS_SHUFFLE_QUESTIONS = r"""function shuffleQuestions(){const sec=document.getElementById('qSection');if(!sec)return;const qs=Array.from(sec.querySelectorAll(':scope > .question'));function r(n){if(n<=1)return 0;try{if(crypto&&crypto.getRandomValues){const lim=Math.floor(4294967296/n)*n,b=new Uint32Array(1);let x;do{crypto.getRandomValues(b);x=b[0]}while(x>=lim);return x%n}}catch(e){}return Math.floor(Math.random()*n)}for(let i=qs.length-1;i>0;i--){const j=r(i+1);[qs[i],qs[j]]=[qs[j],qs[i]]}qs.forEach(q=>sec.appendChild(q));qs.forEach((q,i)=>{const n=q.querySelector('.q-num');if(n)n.textContent=(i+1).toString()})}"""

JS_TIMER_SUBMIT = r"""function startTimer(){timerInterval=setInterval(()=>{if(paused)return;timeLeft--;const m=Math.floor(timeLeft/60),s=timeLeft%60,t=document.getElementById('timer');t.textContent=`${m}:${s.toString().padStart(2,'0')}`;document.getElementById('progress').style.width=(timeLeft/TIME_LIMIT*100)+'%';if(timeLeft<=60){t.className='timer danger'}else if(timeLeft<=300){t.className='timer warning'}else{t.className='timer'}if(timeLeft<=0){clearInterval(timerInterval);submitTest()}},1000)}
function submitTest(){if(submitted)return;submitted=true;clearInterval(timerInterval);let score=0;for(let i=1;i<=TOTAL;i++){const opts=Array.from(document.querySelectorAll(`input[name="q${i}"]`)),sel=opts.find(o=>o.checked);if(sel&&sel.value==='1')score++;opts.forEach(o=>{const w=o.closest('.option');if(o.value==='1')w.classList.add('correct');else if(o.checked)w.classList.add('wrong')});const exp=opts[0].closest('.question').querySelector('.explanation');if(exp)exp.classList.add('show')}const pct=Math.round(score/TOTAL*100),p=document.getElementById('resultPanel'),sc=document.getElementById('resultScore'),tt=document.getElementById('resultTitle');p.style.display='block';sc.textContent=`${score} / ${TOTAL}（${pct}%）`;sc.className='result-score '+(pct>=90?'excellent':pct>=70?'good':pct>=50?'fair':'poor');tt.textContent=pct>=90?'すばらしい！':pct>=70?'よくできました！':pct>=50?'もうすこし！':'がんばりましょう！';const used=TIME_LIMIT-timeLeft;document.getElementById('resultDetail').innerHTML=`<div class="result-item"><div class="label">せいかい</div><div class="value">${score}/${TOTAL}</div></div><div class="result-item"><div class="label">じかん</div><div class="value">${Math.floor(used/60)}分${used%60}秒</div></div>`;document.getElementById('submitBtn').disabled=true;document.getElementById('pauseBtn').disabled=true;p.scrollIntoView({behavior:'smooth'})}
startTimer();"""

JS_PAUSE = r"""function togglePause(){if(submitted)return;paused=!paused;const b=document.getElementById('pauseBtn'),t=document.getElementById('timer');b.textContent=paused?'▶':'⏸';b.setAttribute('aria-label',paused?'再開':'一時停止');if(paused){t.classList.add('paused');t.classList.remove('warning','danger')}else{t.classList.remove('paused');if(timeLeft<=60)t.classList.add('danger');else if(timeLeft<=300)t.classList.add('warning')}}"""

def script_block(total, with_shuffle_q=False):
    head = f"const TOTAL={total},TIME_LIMIT=600;let timeLeft=TIME_LIMIT,timerInterval,submitted=false,paused=false;"
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
    """1問。options = [(text, 0 or 1), ...]; dialogue = [(speaker, text), ...] or None"""
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
                with_shuffle_q=False, section_title=None, lead=None):
    theme = THEMES[theme_key]
    sec_open = '<div class="section" id="qSection">' if with_shuffle_q else '<div class="section">'
    sec_title_html = f'<div class="section-title">{section_title}</div>\n' if section_title else ''
    lead_html = f'<p class="section-lead">{lead}</p>\n' if lead else ''
    qs_html = ''.join(render_question(q, i+1) for i, q in enumerate(questions))
    js = script_block(count, with_shuffle_q=with_shuffle_q)
    html = f"""<!DOCTYPE html>

<html lang="ja">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>{title}</title>
<style>{css(theme)}</style>
</head>
<body>

<div class="container"><header><h1>{title}</h1><div class="header-info"><div class="timer-group"><div class="timer" id="timer">10:00</div><button aria-label="一時停止" class="pause-btn" id="pauseBtn" onclick="togglePause()" type="button">⏸</button></div><div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div><div class="score-badge" id="scoreBadge">{R('全','ぜん')}{count}{R('問','もん')}</div></div></header>

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
# ---- 問題定義 ----
# ======================================================================

# 共通リード（個別文法用）
LEAD = f'（　）に{R("入","はい")}る{R("正","ただ")}しいものはどれですか。'

# ---------- bunpo01 〜へ（移動の方向） ----------
BUNPO01 = [
    Q(f'わたしは{R("京都","きょうと")}{BLANK}{R("行","い")}きます。',
      [('へ',1),('で',0),('と',0),('に',0)],
      '✅ 正解：1 — 場所＋「へ」で移動の方向を表します。「に」も可だが教科書では「へ」を学習。'),
    Q(f'6{R("時","じ")}に　うち{BLANK}{R("帰","かえ")}ります。',
      [('へ',1),('を',0),('で',0),('と',0)],
      '✅ 正解：1 — 「帰ります」の前は方向の「へ」。'),
    Q(f'ミラーさんは　{R("毎日","まいにち")}　{R("会社","かいしゃ")}{BLANK}{R("行","い")}きます。',
      [('へ',1),('と',0),('が',0),('を',0)],
      '✅ 正解：1 — 場所（会社）＋「へ」＋ 行きます。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('へ',1),('で',0),('と',0),('に',0)],
      '✅ 正解：1 — 質問にも「どこへ」と方向の「へ」を使います。',
      dialogue=[('A', f'あした　どこ{BLANK}{R("行","い")}きますか。'),
                ('B', f'{R("奈良","なら")}へ{R("行","い")}きます。')]),
    Q(f'きのう　わたしは{R("奈良","なら")}{BLANK}{R("行","い")}きました。',
      [('へ',1),('に',0),('で',0),('と',0)],
      '✅ 正解：1 — 過去形「行きました」でも方向は「へ」。'),
    Q(f'{R("来月","らいげつ")}　{R("国","くに")}{BLANK}{R("帰","かえ")}ります。',
      [('へ',1),('に',0),('で',0),('と',0)],
      '✅ 正解：1 — 「国へ 帰ります」。'),
    Q(f'3{R("月","がつ")}25{R("日","にち")}に　{R("日本","にほん")}{BLANK}{R("来","き")}ました。',
      [('へ',1),('に',0),('で',0),('と',0)],
      '✅ 正解：1 — 「来ます」の前も方向の「へ」。'),
    Q(f'「うちへ {R("帰","かえ")}ります」の「へ」の{R("読","よ")}み{R("方","かた")}はどれですか。',
      [('え',1),('へ',0),('ね',0),('て',0)],
      '✅ 正解：1 — 助詞の「へ」は「え」と読みます。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは　{R("日本","にほん")}に　{R("来","き")}ます。',0),
       (f'わたしは　{R("日本","にほん")}へ　{R("来","き")}ます。',1),
       (f'わたしは　{R("日本","にほん")}で　{R("来","き")}ます。',0),
       (f'わたしは　{R("日本","にほん")}を　{R("来","き")}ます。',0)],
      '✅ 正解：2 — 第5課では「場所＋へ＋来ます」を学習します。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('へ',1),('と',0),('を',0),('が',0)],
      '✅ 正解：1 — 行き先は「へ」。',
      dialogue=[('A', f'{R("日曜日","にちようび")}　どこへ　{R("行","い")}きますか。'),
                ('B', f'{R("美術館","びじゅつかん")}{BLANK}{R("行","い")}きます。')]),
]

# ---------- bunpo02 〜で（交通手段） ----------
BUNPO02 = [
    Q(f'わたしは　タクシー{BLANK}うちへ{R("帰","かえ")}ります。',
      [('で',1),('と',0),('へ',0),('に',0)],
      '✅ 正解：1 — 交通手段は「で」。'),
    Q(f'ミラーさんは{R("地下鉄","ちかてつ")}{BLANK}{R("会社","かいしゃ")}へ{R("行","い")}きます。',
      [('で',1),('へ',0),('に',0),('と',0)],
      '✅ 正解：1 — 交通手段（地下鉄）＋で。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('で',1),('に',0),('と',0),('へ',0)],
      '✅ 正解：1 — 「新幹線で」＝交通手段。',
      dialogue=[('A', f'{R("何","なん")}で　{R("東京","とうきょう")}へ{R("行","い")}きますか。'),
                ('B', f'{R("新幹線","しんかんせん")}{BLANK}{R("行","い")}きます。')]),
    Q(f'きのう　わたしは{R("自転車","じてんしゃ")}{BLANK}スーパーへ{R("行","い")}きました。',
      [('で',1),('と',0),('を',0),('に',0)],
      '✅ 正解：1 — 自転車（乗り物）＋で。'),
    Q(f'{R("飛行機","ひこうき")}{BLANK}{R("北海道","ほっかいどう")}へ{R("行","い")}きました。',
      [('で',1),('と',0),('へ',0),('に',0)],
      '✅ 正解：1 — 飛行機（乗り物）＋で。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('で',1),('と',0),('を',0),('が',0)],
      '✅ 正解：1 — バス（乗り物）＋で。',
      dialogue=[('A', f'{R("何","なん")}で　{R("学校","がっこう")}へ{R("行","い")}きますか。'),
                ('B', f'バス{BLANK}{R("行","い")}きます。')]),
    Q(f'{R("駅","えき")}から{BLANK}{R("会社","かいしゃ")}へ{R("行","い")}きます。',
      [(R("歩","ある")+"いて",1),(R("歩","ある")+"いてで",0),(R("歩","ある")+"くで",0),(R("歩","ある")+"きで",0)],
      '✅ 正解：1 — 「歩いて」の前後に「で」はつけません。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは{R("電車","でんしゃ")}に　うちへ{R("帰","かえ")}ります。',0),
       (f'わたしは{R("電車","でんしゃ")}を　うちへ{R("帰","かえ")}ります。',0),
       (f'わたしは{R("電車","でんしゃ")}で　うちへ{R("帰","かえ")}ります。',1),
       (f'わたしは{R("電車","でんしゃ")}と　うちへ{R("帰","かえ")}ります。',0)],
      '✅ 正解：3 — 乗り物＋「で」。「に／を／と」は不可。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('で',1),('と',0),('に',0),('を',0)],
      '✅ 正解：1 — 船（乗り物）＋で。',
      dialogue=[('A', f'{R("何","なん")}で{R("九州","きゅうしゅう")}へ{R("行","い")}きますか。'),
                ('B', f'{R("船","ふね")}{BLANK}{R("行","い")}きます。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("駅","えき")}から{R("歩","ある")}いてで{R("帰","かえ")}りました。',0),
       (f'{R("駅","えき")}から{R("歩","ある")}いて{R("帰","かえ")}りました。',1),
       (f'{R("駅","えき")}から{R("歩","ある")}くで{R("帰","かえ")}りました。',0),
       (f'{R("駅","えき")}から{R("歩","ある")}くて{R("帰","かえ")}りました。',0)],
      '✅ 正解：2 — 「歩いて」は単独で使い、「で」をつけません。',
      one_col=True),
]

# ---------- bunpo03 〜と V／一人で（同伴） ----------
BUNPO03 = [
    Q(f'わたしは{R("友達","ともだち")}{BLANK}{R("京都","きょうと")}へ{R("行","い")}きました。',
      [('と',1),('で',0),('に',0),('へ',0)],
      '✅ 正解：1 — 同伴の人＋「と」。'),
    Q(f'{R("家族","かぞく")}{BLANK}{R("日本","にほん")}へ{R("来","き")}ました。',
      [('と',1),('で',0),('を',0),('が',0)],
      '✅ 正解：1 — 家族（人）＋と＋来ました。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('と',1),('で',0),('に',0),('へ',0)],
      '✅ 正解：1 — 「だれと」と同じく答えも「（人）と」。',
      dialogue=[('A', f'だれ{BLANK}{R("東京","とうきょう")}へ{R("行","い")}きますか。'),
                ('B', f'{R("山田","やまだ")}さんと{R("行","い")}きます。')]),
    Q(f'{R("来週","らいしゅう")}　わたしは{R("彼女","かのじょ")}{BLANK}{R("奈良","なら")}へ{R("行","い")}きます。',
      [('と',1),('で',0),('へ',0),('に',0)],
      '✅ 正解：1 — 彼女（人）＋と。'),
    Q(f'「{R("一人","ひとり")}で　{R("京都","きょうと")}へ　{R("行","い")}きます」の{R("意味","いみ")}はどれですか。',
      [(f'{R("友達","ともだち")}と{R("行","い")}きます。',0),
       (f'{R("家族","かぞく")}と{R("行","い")}きます。',0),
       (f'わたし{R("一人","ひとり")}だけで{R("行","い")}きます。',1),
       (f'{R("二人","ふたり")}で{R("行","い")}きます。',0)],
      '✅ 正解：3 — 「一人で」＝自分だけで（誰とも一緒ではない）。「と」はつきません。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('と',1),('で',0),('が',0),('に',0)],
      '✅ 正解：1 — 「会社の人」（人）＋と。',
      dialogue=[('A', f'きのう{R("大阪城","おおさかじょう")}へ{R("行","い")}きましたか。'),
                ('B', f'はい、{R("会社","かいしゃ")}の{R("人","ひと")}{BLANK}{R("行","い")}きました。')]),
    Q(f'「I will go alone.」を{R("表","あらわ")}す{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは{R("一人","ひとり")}で{R("行","い")}きます。',1),
       (f'わたしは{R("一人","ひとり")}と{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}へ{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}に{R("行","い")}きます。',0)],
      '✅ 正解：1 — 「一人で」は固定表現。「と」は使いません。',
      one_col=True),
    Q(f'ミラーさんは{R("彼女","かのじょ")}{BLANK}{R("神戸","こうべ")}へ{R("行","い")}きました。',
      [('と',1),('で',0),('を',0),('に',0)],
      '✅ 正解：1 — 「（人）と」で同伴を表します。'),
]

# ---------- bunpo04 どこ〔へ〕も + 否定 ----------
BUNPO04 = [
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('へも',1),('に',0),('でも',0),('と',0)],
      '✅ 正解：1 — 「どこ＋へ＋も＋否定」で「どこにも行かない」。',
      dialogue=[('A', f'{R("日曜日","にちようび")}　どこへ{R("行","い")}きましたか。'),
                ('B', f'どこ{BLANK}{R("行","い")}きませんでした。')]),
    Q(f'きのう　どこへも{R("行","い")}き{BLANK}。',
      [('ません',0),('ませんでした',1),('ます',0),('ました',0)],
      '✅ 正解：2 — 「きのう」（過去）＋ 否定の過去形「ませんでした」。'),
    Q(f'あした　どこへも{R("行","い")}き{BLANK}。',
      [('ません',1),('ませんでした',0),('ます',0),('ました',0)],
      '✅ 正解：1 — 「あした」（未来）＋ 否定の非過去「ません」。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きます。',0),
       (f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きました。',0),
       (f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きませんでした。',1),
       (f'{R("日曜日","にちようび")}　どこ{R("行","い")}きませんでした。',0)],
      '✅ 正解：3 — 「どこへも」は必ず否定文と一緒に使います。',
      one_col=True),
    Q(f'「どこへも{R("行","い")}きませんでした」の{R("意味","いみ")}はどれですか。',
      [(f'どこかへ{R("行","い")}きました。',0),
       (f'どこにも　{R("出","で")}かけませんでした。',1),
       (f'{R("一","ひと")}つの{R("場所","ばしょ")}に{R("行","い")}きました。',0),
       (f'これから　どこかへ{R("行","い")}きます。',0)],
      '✅ 正解：2 — 「疑問詞＋も＋否定」で全否定（一つも〜ない）。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('どこへも',1),('どこも',0),('どこへ',0),('どこに',0)],
      '✅ 正解：1 — 「どこへも 行きませんでした」のかたちで全否定。',
      dialogue=[('A', f'{R("先週","せんしゅう")}の{R("日曜日","にちようび")}　どこへ{R("行","い")}きましたか。'),
                ('B', f'{BLANK}{R("行","い")}きませんでした。')]),
    Q(f'「どこへも」の「も」の{R("使","つか")}い{R("方","かた")}として{R("正","ただ")}しいものはどれですか。',
      [(f'どこかへ{R("行","い")}く。',0),
       (f'ある{R("場所","ばしょ")}だけに{R("行","い")}く。',0),
       (f'どの{R("場所","ばしょ")}にも{R("行","い")}かない（{R("全否定","ぜんひてい")}）。',1),
       (f'たくさんの{R("場所","ばしょ")}に{R("行","い")}く。',0)],
      '✅ 正解：3 — 「疑問詞＋も」＋否定 ＝ ぜんぶ否定。',
      one_col=True),
    Q(f'どこ{BLANK}{R("行","い")}きません。',
      [('でも',0),('にも',0),('へも',1),('をも',0)],
      '✅ 正解：3 — 場所への移動なので「へ」＋ も。「へも」が正解。'),
]

# ---------- bunpo05 いつ ----------
BUNPO05 = [
    Q(f'{BLANK}{R("日本","にほん")}へ{R("来","き")}ましたか。',
      [('いつ',1),('どこ',0),('だれ',0),('なんで',0)],
      '✅ 正解：1 — 「来ました（過去）」と聞かれているので、時を聞く「いつ」。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いつ',1),('どこ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 答えが「来週」なので、時を聞く「いつ」。',
      dialogue=[('A', f'{BLANK}{R("京都","きょうと")}へ{R("行","い")}きますか。'),
                ('B', f'{R("来週","らいしゅう")}{R("行","い")}きます。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'いつに　{R("日本","にほん")}へ{R("来","き")}ましたか。',0),
       (f'いつ　{R("日本","にほん")}へ{R("来","き")}ましたか。',1),
       (f'いつで　{R("日本","にほん")}へ{R("来","き")}ましたか。',0),
       (f'いつへ　{R("日本","にほん")}へ{R("来","き")}ましたか。',0)],
      '✅ 正解：2 — 「いつ」は「に」をとりません。そのまま使います。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いつ',1),('どこ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 誕生日（日付）を聞くときも「いつ」。',
      dialogue=[('A', f'{R("誕生日","たんじょうび")}は{BLANK}ですか。'),
                ('B', f'6{R("月","がつ")}13{R("日","にち")}です。')]),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [(R("来年","らいねん"),1),(R("去年","きょねん"),0),(R("今日","きょう"),0),(R("きのう","きのう"),0)],
      '✅ 正解：1 — 「3月に帰る」未来の予定なので「来年」が自然。',
      dialogue=[('A', f'いつ{R("国","くに")}へ{R("帰","かえ")}りますか。'),
                ('B', f'{BLANK}の3{R("月","がつ")}に{R("帰","かえ")}ります。')]),
    Q(f'「いつ{R("来","き")}ましたか」に{R("対","たい")}する{R("正","ただ")}しい{R("答","こた")}えはどれですか。',
      [(f'3{R("月","がつ")}25{R("日","にち")}に{R("来","き")}ました。',1),
       (f'{R("京都","きょうと")}に{R("来","き")}ました。',0),
       (f'{R("電車","でんしゃ")}で{R("来","き")}ました。',0),
       (f'{R("一人","ひとり")}で{R("来","き")}ました。',0)],
      '✅ 正解：1 — 「いつ」＝時。日付で答えます。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いつ',1),('どこ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 答えが「先月」なので時を聞く「いつ」。',
      dialogue=[('A', f'{BLANK}{R("北海道","ほっかいどう")}へ{R("行","い")}きましたか。'),
                ('B', f'{R("先月","せんげつ")}{R("行","い")}きました。')]),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いつ',1),('どこ',0),('だれ',0),('なに',0)],
      '✅ 正解：1 — 「8月17日に来ました」なので時を聞く「いつ」。',
      dialogue=[('A', f'{BLANK}{R("日本","にほん")}へ{R("来","き")}ましたか。'),
                ('B', f'8{R("月","がつ")}17{R("日","にち")}に{R("来","き")}ました。')]),
    Q(f'「いつ」は{R("何","なに")}を{R("聞","き")}くときに{R("使","つか")}いますか。',
      [(f'{R("場所","ばしょ")}',0),(f'{R("人","ひと")}',0),(f'{R("交通手段","こうつうしゅだん")}',0),(f'{R("時","とき")}・{R("日付","ひづけ")}',1)],
      '✅ 正解：4 — 「いつ」は時・日付を聞く疑問詞です。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'あなたの{R("誕生日","たんじょうび")}は　いつですか。',1),
       (f'あなたの{R("誕生日","たんじょうび")}は　いつにですか。',0),
       (f'あなたの{R("誕生日","たんじょうび")}は　いつへですか。',0),
       (f'あなたの{R("誕生日","たんじょうび")}は　いつでですか。',0)],
      '✅ 正解：1 — 「いつですか」が自然な形。',
      one_col=True),
]

# ---------- bunpo06 Sよ ----------
BUNPO06 = [
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('と',0)],
      '✅ 正解：1 — 相手が知らない情報を強く伝えるときは「よ」。',
      dialogue=[('A', f'この{R("電車","でんしゃ")}は{R("甲子園","こうしえん")}へ{R("行","い")}きますか。'),
                ('B', f'いいえ、{R("次","つぎ")}の{R("普通","ふつう")}です{BLANK}。')]),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('に',0)],
      '✅ 正解：1 — 相手が知らない情報（誕生日）を教える＝「よ」。',
      dialogue=[('A', f'{R("田中","たなか")}さんの{R("誕生日","たんじょうび")}は　いつですか。'),
                ('B', f'4{R("月","がつ")}10{R("日","にち")}です{BLANK}。')]),
    Q(f'「よ」の{R("使","つか")}い{R("方","かた")}として{R("正","ただ")}しいものはどれですか。',
      [(f'{R("質問","しつもん")}するときに{R("使","つか")}う。',0),
       (f'{R("相手","あいて")}が{R("知","し")}らない{R("情報","じょうほう")}を{R("教","おし")}えるときに{R("使","つか")}う。',1),
       (f'{R("自分","じぶん")}が{R("知","し")}らないことを{R("聞","き")}くときに{R("使","つか")}う。',0),
       (f'{R("命令","めいれい")}するときに{R("使","つか")}う。',0)],
      '✅ 正解：2 — 「よ」は相手が知らない情報・自分の判断を強く伝える終助詞。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('と',0)],
      '✅ 正解：1 — Aが知らない情報を伝える＝「よ」。',
      dialogue=[('A', f'あした{R("京都","きょうと")}へ{R("行","い")}きますか。'),
                ('B', f'いいえ、{R("来週","らいしゅう")}{R("行","い")}きます{BLANK}。')]),
    Q(f'{R("相手","あいて")}が{R("知","し")}らない{R("情報","じょうほう")}を{R("強","つよ")}く{R("言","い")}いたいとき、{R("文","ぶん")}の{R("最後","さいご")}に{R("何","なに")}をつけますか。',
      [('か',0),('よ',1),('と',0),('に',0)],
      '✅ 正解：2 — 「よ」を文末に置きます。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('に',0)],
      '✅ 正解：1 — 相手（道を聞く人）が知らない場所を教える＝「よ」。',
      dialogue=[('A', f'すみません、{R("駅","えき")}は　どこですか。'),
                ('B', f'あそこです{BLANK}。')]),
]

# ---------- まとめ1（①②③ミックス、12問、シャッフル） ----------
MATOME1 = [
    # へ系
    Q(f'わたしは{R("京都","きょうと")}{BLANK}{R("行","い")}きます。',
      [('へ',1),('で',0),('と',0),('に',0)],
      '✅ 正解：1 — 場所＋へ＋行きます。'),
    Q(f'{R("来月","らいげつ")}　{R("国","くに")}{BLANK}{R("帰","かえ")}ります。',
      [('へ',1),('に',0),('で',0),('と',0)],
      '✅ 正解：1 — 「帰ります」の前は方向の「へ」。'),
    Q(f'3{R("月","がつ")}25{R("日","にち")}に{R("日本","にほん")}{BLANK}{R("来","き")}ました。',
      [('へ',1),('に',0),('で',0),('と',0)],
      '✅ 正解：1 — 「来ます」の前も方向の「へ」。'),
    # で系
    Q(f'わたしは　タクシー{BLANK}うちへ{R("帰","かえ")}ります。',
      [('で',1),('と',0),('へ',0),('に',0)],
      '✅ 正解：1 — 交通手段＋で。'),
    Q(f'{R("飛行機","ひこうき")}{BLANK}{R("北海道","ほっかいどう")}へ{R("行","い")}きました。',
      [('で',1),('と',0),('へ',0),('に',0)],
      '✅ 正解：1 — 飛行機（乗り物）＋で。'),
    Q(f'{R("駅","えき")}から{BLANK}{R("会社","かいしゃ")}へ{R("行","い")}きます。',
      [(R("歩","ある")+"いて",1),(R("歩","ある")+"いてで",0),(R("歩","ある")+"くで",0),(R("歩","ある")+"きで",0)],
      '✅ 正解：1 — 「歩いて」は「で」をつけません。'),
    # と系
    Q(f'わたしは{R("友達","ともだち")}{BLANK}{R("京都","きょうと")}へ{R("行","い")}きました。',
      [('と',1),('で',0),('に',0),('へ',0)],
      '✅ 正解：1 — 同伴の人＋と。'),
    Q(f'{R("家族","かぞく")}{BLANK}{R("日本","にほん")}へ{R("来","き")}ました。',
      [('と',1),('で',0),('を',0),('が',0)],
      '✅ 正解：1 — 家族（人）＋と。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは{R("一人","ひとり")}で{R("行","い")}きます。',1),
       (f'わたしは{R("一人","ひとり")}と{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}へ{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}に{R("行","い")}きます。',0)],
      '✅ 正解：1 — 「一人で」は固定表現。「と」は不要。',
      one_col=True),
    # 会話混合
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('と',1),('で',0),('に',0),('へ',0)],
      '✅ 正解：1 — 答えが「山田さんと」なので質問にも「だれと」。',
      dialogue=[('A', f'だれ{BLANK}{R("東京","とうきょう")}へ{R("行","い")}きますか。'),
                ('B', f'{R("山田","やまだ")}さんと{R("行","い")}きます。')]),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('で',1),('と',0),('に',0),('へ',0)],
      '✅ 正解：1 — 新幹線（乗り物）＋で。',
      dialogue=[('A', f'{R("何","なん")}で{R("東京","とうきょう")}へ{R("行","い")}きますか。'),
                ('B', f'{R("新幹線","しんかんせん")}{BLANK}{R("行","い")}きます。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは{R("家族","かぞく")}で{R("日本","にほん")}へ{R("来","き")}ました。',0),
       (f'わたしは{R("家族","かぞく")}と{R("日本","にほん")}へ{R("来","き")}ました。',1),
       (f'わたしは{R("家族","かぞく")}に{R("日本","にほん")}へ{R("来","き")}ました。',0),
       (f'わたしは{R("家族","かぞく")}を{R("日本","にほん")}へ{R("来","き")}ました。',0)],
      '✅ 正解：2 — 同伴の人（家族）＋と。',
      one_col=True),
]

# ---------- クイック復習1（8問、オレンジ、①②③復習） ----------
QUICK1 = [
    Q(f'わたしは{R("京都","きょうと")}{BLANK}{R("行","い")}きます。',
      [('へ',1),('で',0),('と',0),('に',0)],
      '✅ 正解：1 — 場所＋へ＝方向。'),
    Q(f'6{R("時","じ")}に　うち{BLANK}{R("帰","かえ")}ります。',
      [('へ',1),('を',0),('で',0),('と',0)],
      '✅ 正解：1 — 「帰ります」の前は「へ」。'),
    Q(f'わたしは{R("電車","でんしゃ")}{BLANK}{R("会社","かいしゃ")}へ{R("行","い")}きます。',
      [('で',1),('と',0),('に',0),('へ',0)],
      '✅ 正解：1 — 乗り物＋で。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('で',1),('と',0),('に',0),('を',0)],
      '✅ 正解：1 — バス（乗り物）＋で。',
      dialogue=[('A', f'{R("何","なん")}で{R("学校","がっこう")}へ{R("行","い")}きますか。'),
                ('B', f'バス{BLANK}{R("行","い")}きます。')]),
    Q(f'{R("家族","かぞく")}{BLANK}{R("日本","にほん")}へ{R("来","き")}ました。',
      [('と',1),('で',0),('を',0),('が',0)],
      '✅ 正解：1 — 同伴の人＋と。'),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('と',1),('で',0),('に',0),('へ',0)],
      '✅ 正解：1 — 「だれと」と聞かれているので「（人）と」。',
      dialogue=[('A', f'だれ{BLANK}{R("大阪","おおさか")}へ{R("行","い")}きますか。'),
                ('B', f'{R("友達","ともだち")}と{R("行","い")}きます。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("駅","えき")}から{R("歩","ある")}いてで{R("帰","かえ")}りました。',0),
       (f'{R("駅","えき")}から{R("歩","ある")}いて{R("帰","かえ")}りました。',1),
       (f'{R("駅","えき")}から{R("歩","ある")}くで{R("帰","かえ")}りました。',0),
       (f'{R("駅","えき")}から{R("歩","ある")}くて{R("帰","かえ")}りました。',0)],
      '✅ 正解：2 — 「歩いて」に「で」はつけない。',
      one_col=True),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'わたしは{R("一人","ひとり")}と{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}で{R("行","い")}きます。',1),
       (f'わたしは{R("一人","ひとり")}へ{R("行","い")}きます。',0),
       (f'わたしは{R("一人","ひとり")}に{R("行","い")}きます。',0)],
      '✅ 正解：2 — 「一人で」は固定表現。',
      one_col=True),
]

# ---------- まとめ2（④⑤⑥ミックス、12問、シャッフル） ----------
MATOME2 = [
    # どこへも
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('へも',1),('に',0),('でも',0),('と',0)],
      '✅ 正解：1 — どこ＋へ＋も＋否定。',
      dialogue=[('A', f'{R("日曜日","にちようび")}　どこへ{R("行","い")}きましたか。'),
                ('B', f'どこ{BLANK}{R("行","い")}きませんでした。')]),
    Q(f'きのう　どこへも{R("行","い")}き{BLANK}。',
      [('ません',0),('ませんでした',1),('ます',0),('ました',0)],
      '✅ 正解：2 — 過去の否定。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きます。',0),
       (f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きました。',0),
       (f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きませんでした。',1),
       (f'{R("日曜日","にちようび")}　どこへも{R("行","い")}きました{R("か","か")}。',0)],
      '✅ 正解：3 — 「どこへも」は必ず否定文で使う。',
      one_col=True),
    Q(f'「どこへも」の「も」の{R("使","つか")}い{R("方","かた")}として{R("正","ただ")}しいものはどれですか。',
      [(f'どこかへ{R("行","い")}く。',0),
       (f'どの{R("場所","ばしょ")}にも{R("行","い")}かない。',1),
       (f'ある{R("場所","ばしょ")}だけに{R("行","い")}く。',0),
       (f'たくさん{R("行","い")}く。',0)],
      '✅ 正解：2 — 疑問詞＋も＋否定＝全否定。',
      one_col=True),
    # いつ
    Q(f'{BLANK}{R("日本","にほん")}へ{R("来","き")}ましたか。',
      [('いつ',1),('どこ',0),('だれ',0),('なんで',0)],
      '✅ 正解：1 — 時を聞く「いつ」。'),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'いつに　{R("日本","にほん")}へ{R("来","き")}ましたか。',0),
       (f'いつ　{R("日本","にほん")}へ{R("来","き")}ましたか。',1),
       (f'いつで　{R("日本","にほん")}へ{R("来","き")}ましたか。',0),
       (f'いつへ　{R("日本","にほん")}へ{R("来","き")}ましたか。',0)],
      '✅ 正解：2 — 「いつ」に「に」はつかない。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('いつ',1),('どこ',0),('だれ',0),('なん',0)],
      '✅ 正解：1 — 答えが「6月13日」なので「いつ」。',
      dialogue=[('A', f'{R("誕生日","たんじょうび")}は{BLANK}ですか。'),
                ('B', f'6{R("月","がつ")}13{R("日","にち")}です。')]),
    Q(f'「いつ{R("来","き")}ましたか」に{R("対","たい")}する{R("正","ただ")}しい{R("答","こた")}えはどれですか。',
      [(f'3{R("月","がつ")}25{R("日","にち")}に{R("来","き")}ました。',1),
       (f'{R("京都","きょうと")}に{R("来","き")}ました。',0),
       (f'{R("電車","でんしゃ")}で{R("来","き")}ました。',0),
       (f'{R("一人","ひとり")}で{R("来","き")}ました。',0)],
      '✅ 正解：1 — 「いつ」は時。日付で答える。',
      one_col=True),
    # よ
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('と',0)],
      '✅ 正解：1 — 相手が知らない情報を伝える終助詞「よ」。',
      dialogue=[('A', f'この{R("電車","でんしゃ")}は{R("甲子園","こうしえん")}へ{R("行","い")}きますか。'),
                ('B', f'いいえ、{R("次","つぎ")}の{R("普通","ふつう")}です{BLANK}。')]),
    Q(f'「よ」の{R("使","つか")}い{R("方","かた")}として{R("正","ただ")}しいものはどれですか。',
      [(f'{R("質問","しつもん")}するときに{R("使","つか")}う。',0),
       (f'{R("相手","あいて")}が{R("知","し")}らない{R("情報","じょうほう")}を{R("教","おし")}える。',1),
       (f'{R("自分","じぶん")}が{R("知","し")}らないことを{R("聞","き")}く。',0),
       (f'{R("命令","めいれい")}する。',0)],
      '✅ 正解：2 — 「よ」は新情報を相手に伝える終助詞。',
      one_col=True),
    Q(f'{BLANK}に{R("入","はい")}るものはどれですか。',
      [('よ',1),('か',0),('ね',0),('に',0)],
      '✅ 正解：1 — Aが知らない情報を伝える＝「よ」。',
      dialogue=[('A', f'あした{R("京都","きょうと")}へ{R("行","い")}きますか。'),
                ('B', f'いいえ、{R("来週","らいしゅう")}{R("行","い")}きます{BLANK}。')]),
    Q(f'{R("正","ただ")}しい{R("文","ぶん")}はどれですか。',
      [(f'あの{R("店","みせ")}は　あそこですよ。',1),
       (f'あの{R("店","みせ")}は　あそこですか。',0),
       (f'あの{R("店","みせ")}は　あそこですね。',0),
       (f'あの{R("店","みせ")}は　あそこですと。',0)],
      '✅ 正解：1 — 相手が知らないことを教える＝「よ」。',
      one_col=True),
]

# ======================================================================
# ---- ファイル生成 ----
# ======================================================================
def build_all():
    # 個別文法（青）
    render_file('bunpo01-e-place.html',
        title=f'L5 {R("文法","ぶんぽう")}① 〜へ{R("行","い")}きます／{R("来","き")}ます／{R("帰","かえ")}ります（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO01,
        section_title=f'A. {R("場所","ばしょ")}＋へ＋{R("行","い")}きます／{R("来","き")}ます／{R("帰","かえ")}ります',
        lead=LEAD)

    render_file('bunpo02-de-vehicle.html',
        title=f'L5 {R("文法","ぶんぽう")}② 〜で{R("行","い")}きます（{R("交通手段","こうつうしゅだん")}）（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO02,
        section_title=f'B. {R("乗","の")}り{R("物","もの")}＋で＋{R("行","い")}きます／{R("来","き")}ます／{R("帰","かえ")}ります',
        lead=LEAD)

    render_file('bunpo03-to-person.html',
        title=f'L5 {R("文法","ぶんぽう")}③ 〜と V／{R("一人","ひとり")}で（10{R("分","ふん")}・8{R("問","もん")}）',
        count=8, theme_key='blue', questions=BUNPO03,
        section_title=f'C. {R("人","ひと")}＋と＋V／{R("一人","ひとり")}で（{R("同伴","どうはん")}）',
        lead=LEAD)

    render_file('bunpo04-dokoemo.html',
        title=f'L5 {R("文法","ぶんぽう")}④ どこ〔へ〕も＋{R("否定","ひてい")}（10{R("分","ふん")}・8{R("問","もん")}）',
        count=8, theme_key='blue', questions=BUNPO04,
        section_title=f'D. {R("疑問詞","ぎもんし")}＋も＋{R("否定","ひてい")}（{R("全否定","ぜんひてい")}）',
        lead=LEAD)

    render_file('bunpo05-itsu.html',
        title=f'L5 {R("文法","ぶんぽう")}⑤ いつ（10{R("分","ふん")}・10{R("問","もん")}）',
        count=10, theme_key='blue', questions=BUNPO05,
        section_title=f'E. いつ（{R("時","とき")}を{R("聞","き")}く{R("疑問詞","ぎもんし")}・「に」をとらない）',
        lead=LEAD)

    render_file('bunpo06-yo.html',
        title=f'L5 {R("文法","ぶんぽう")}⑥ S よ（10{R("分","ふん")}・6{R("問","もん")}）',
        count=6, theme_key='blue', questions=BUNPO06,
        section_title=f'F. S よ（{R("終助詞","しゅうじょし")}：{R("相手","あいて")}が{R("知","し")}らない{R("情報","じょうほう")}を{R("伝","つた")}える）',
        lead=LEAD)

    # まとめ（紫、シャッフル）
    render_file('bunpo-matome1.html',
        title=f'L5 1{R("回目","かいめ")}まとめテスト（10{R("分","ふん")}・12{R("問","もん")}）',
        count=12, theme_key='purple', questions=MATOME1,
        with_shuffle_q=True, lead=LEAD)

    render_file('bunpo-matome2.html',
        title=f'L5 2{R("回目","かいめ")}まとめテスト（10{R("分","ふん")}・12{R("問","もん")}）',
        count=12, theme_key='purple', questions=MATOME2,
        with_shuffle_q=True, lead=LEAD)

    # クイック復習（オレンジ）
    render_file('bunpo-quickreview1.html',
        title=f'L5 2{R("回目","かいめ")}クイック{R("復習","ふくしゅう")}テスト（10{R("分","ふん")}・8{R("問","もん")}）',
        count=8, theme_key='orange', questions=QUICK1,
        section_title=f'1{R("回目","かいめ")}の{R("復習","ふくしゅう")}（〜へ／〜で／〜と）',
        lead=LEAD)

if __name__ == '__main__':
    build_all()
    print('Generated 9 bunpo files in', OUT)
