#!/usr/bin/env python3
"""N5動詞活用形穴埋めテストを3分割で生成するスクリプト"""

import random
import sys
import os

# generate_conjugations のロジックをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_conjugations import N5_VERBS, conjugate

# 【】内の動詞のふりがな（動詞→ruby付きHTML）
VERB_RUBY = {
    "会う": "<ruby>会<rt>あ</rt></ruby>う", "開く": "<ruby>開<rt>あ</rt></ruby>く", "開ける": "<ruby>開<rt>あ</rt></ruby>ける",
    "上げる": "<ruby>上<rt>あ</rt></ruby>げる", "遊ぶ": "<ruby>遊<rt>あそ</rt></ruby>ぶ", "浴びる": "<ruby>浴<rt>あ</rt></ruby>びる",
    "洗う": "<ruby>洗<rt>あら</rt></ruby>う", "ある": "ある", "歩く": "<ruby>歩<rt>ある</rt></ruby>く",
    "言う": "<ruby>言<rt>い</rt></ruby>う", "居る": "<ruby>居<rt>い</rt></ruby>る", "要る": "<ruby>要<rt>い</rt></ruby>る",
    "歌う": "<ruby>歌<rt>うた</rt></ruby>う", "売る": "<ruby>売<rt>う</rt></ruby>る", "置く": "<ruby>置<rt>お</rt></ruby>く",
    "押す": "<ruby>押<rt>お</rt></ruby>す", "泳ぐ": "<ruby>泳<rt>およ</rt></ruby>ぐ", "終わる": "<ruby>終<rt>お</rt></ruby>わる",
    "買う": "<ruby>買<rt>か</rt></ruby>う", "返す": "<ruby>返<rt>かえ</rt></ruby>す", "帰る": "<ruby>帰<rt>かえ</rt></ruby>る",
    "掛かる": "<ruby>掛<rt>か</rt></ruby>かる", "掛ける": "<ruby>掛<rt>か</rt></ruby>ける", "書く": "<ruby>書<rt>か</rt></ruby>く",
    "貸す": "<ruby>貸<rt>か</rt></ruby>す", "聞く": "<ruby>聞<rt>き</rt></ruby>く", "切る": "<ruby>切<rt>き</rt></ruby>る",
    "着る": "<ruby>着<rt>き</rt></ruby>る", "曇る": "<ruby>曇<rt>くも</rt></ruby>る", "消す": "<ruby>消<rt>け</rt></ruby>す",
    "消える": "<ruby>消<rt>き</rt></ruby>える", "困る": "<ruby>困<rt>こま</rt></ruby>る", "答える": "<ruby>答<rt>こた</rt></ruby>える",
    "咲く": "<ruby>咲<rt>さ</rt></ruby>く", "差す": "<ruby>差<rt>さ</rt></ruby>す", "死ぬ": "<ruby>死<rt>し</rt></ruby>ぬ",
    "閉まる": "<ruby>閉<rt>し</rt></ruby>まる", "閉める": "<ruby>閉<rt>し</rt></ruby>める", "締める": "<ruby>締<rt>し</rt></ruby>める",
    "知る": "<ruby>知<rt>し</rt></ruby>る", "吸う": "<ruby>吸<rt>す</rt></ruby>う", "住む": "<ruby>住<rt>す</rt></ruby>む",
    "座る": "<ruby>座<rt>すわ</rt></ruby>る", "立つ": "<ruby>立<rt>た</rt></ruby>つ", "食べる": "<ruby>食<rt>た</rt></ruby>べる",
    "頼む": "<ruby>頼<rt>たの</rt></ruby>む", "出す": "<ruby>出<rt>だ</rt></ruby>す", "違う": "<ruby>違<rt>ちが</rt></ruby>う",
    "使う": "<ruby>使<rt>つか</rt></ruby>う", "着く": "<ruby>着<rt>つ</rt></ruby>く", "疲れる": "<ruby>疲<rt>つか</rt></ruby>れる",
    "付ける": "<ruby>付<rt>つ</rt></ruby>ける", "勤める": "<ruby>勤<rt>つと</rt></ruby>める", "作る": "<ruby>作<rt>つく</rt></ruby>る",
    "出かける": "<ruby>出<rt>で</rt></ruby>かける", "出る": "<ruby>出<rt>で</rt></ruby>る", "飛ぶ": "<ruby>飛<rt>と</rt></ruby>ぶ",
    "止まる": "<ruby>止<rt>と</rt></ruby>まる", "取る": "<ruby>取<rt>と</rt></ruby>る", "撮る": "<ruby>撮<rt>と</rt></ruby>る",
    "鳴く": "<ruby>鳴<rt>な</rt></ruby>く", "無くす": "<ruby>無<rt>な</rt></ruby>くす", "習う": "<ruby>習<rt>なら</rt></ruby>う",
    "並ぶ": "<ruby>並<rt>なら</rt></ruby>ぶ", "並べる": "<ruby>並<rt>なら</rt></ruby>べる", "脱ぐ": "<ruby>脱<rt>ぬ</rt></ruby>ぐ",
    "寝る": "<ruby>寝<rt>ね</rt></ruby>る", "登る": "<ruby>登<rt>のぼ</rt></ruby>る", "飲む": "<ruby>飲<rt>の</rt></ruby>む",
    "乗る": "<ruby>乗<rt>の</rt></ruby>る", "晴れる": "<ruby>晴<rt>は</rt></ruby>れる", "曲がる": "<ruby>曲<rt>ま</rt></ruby>がる",
    "待つ": "<ruby>待<rt>ま</rt></ruby>つ", "磨く": "<ruby>磨<rt>みが</rt></ruby>く", "見せる": "<ruby>見<rt>み</rt></ruby>せる",
    "見る": "<ruby>見<rt>み</rt></ruby>る", "持つ": "<ruby>持<rt>も</rt></ruby>つ", "休む": "<ruby>休<rt>やす</rt></ruby>む",
    "呼ぶ": "<ruby>呼<rt>よ</rt></ruby>ぶ", "読む": "<ruby>読<rt>よ</rt></ruby>む", "来る": "<ruby>来<rt>く</rt></ruby>る",
    "分かる": "<ruby>分<rt>わ</rt></ruby>かる", "渡す": "<ruby>渡<rt>わた</rt></ruby>す", "渡る": "<ruby>渡<rt>わた</rt></ruby>る",
    "忘れる": "<ruby>忘<rt>わす</rt></ruby>れる", "やる": "やる",
    "勉強する": "<ruby>勉強<rt>べんきょう</rt></ruby>する", "結婚する": "<ruby>結婚<rt>けっこん</rt></ruby>する",
    "散歩する": "<ruby>散歩<rt>さんぽ</rt></ruby>する", "仕事する": "<ruby>仕事<rt>しごと</rt></ruby>する",
    "質問する": "<ruby>質問<rt>しつもん</rt></ruby>する", "洗濯する": "<ruby>洗濯<rt>せんたく</rt></ruby>する",
    "掃除する": "<ruby>掃除<rt>そうじ</rt></ruby>する", "電話する": "<ruby>電話<rt>でんわ</rt></ruby>する",
    "練習する": "<ruby>練習<rt>れんしゅう</rt></ruby>する", "料理する": "<ruby>料理<rt>りょうり</rt></ruby>する",
    "旅行する": "<ruby>旅行<rt>りょこう</rt></ruby>する", "コピーする": "コピーする", "テストする": "テストする",
    "教える": "<ruby>教<rt>おし</rt></ruby>える", "覚える": "<ruby>覚<rt>おぼ</rt></ruby>える",
    "生まれる": "<ruby>生<rt>う</rt></ruby>まれる", "起きる": "<ruby>起<rt>お</rt></ruby>きる",
    "降りる": "<ruby>降<rt>お</rt></ruby>りる", "借りる": "<ruby>借<rt>か</rt></ruby>りる", "変える": "<ruby>変<rt>か</rt></ruby>える",
}

# 後ろの言葉ごとの文型テンプレート (blank, suffix, verb)
# テンプレート: (文の前半, 穴埋めの後, 動詞のヒント) ※ふりがな付き
TEMPLATES = {
    'ない': [
        ('<ruby>今日<rt>きょう</rt></ruby>は（　）ない。【{verb}】', 'ない'),
        ('<ruby>明日<rt>あした</rt></ruby>は（　）ない。【{verb}】', 'ない'),
        ('もう（　）ない。【{verb}】', 'ない'),
    ],
    'よう': [
        ('<ruby>一緒<rt>いっしょ</rt></ruby>に（　）よう。【{verb}】', 'よう'),
        ('<ruby>明日<rt>あした</rt></ruby>（　）よう。【{verb}】', 'よう'),
        ('<ruby>今度<rt>こんど</rt></ruby>（　）よう。【{verb}】', 'よう'),
    ],
    'う': [
        ('<ruby>安<rt>やす</rt></ruby>ければ（　）う。【{verb}】', 'う'),
        ('<ruby>時間<rt>じかん</rt></ruby>があれば（　）う。【{verb}】', 'う'),
        ('<ruby>明日<rt>あした</rt></ruby>（　）う。【{verb}】', 'う'),
    ],
    'ます': [
        ('<ruby>毎日<rt>まいにち</rt></ruby>（　）ます。【{verb}】', 'ます'),
        ('よく（　）ます。【{verb}】', 'ます'),
        ('<ruby>今日<rt>きょう</rt></ruby>（　）ます。【{verb}】', 'ます'),
    ],
    'た': [
        ('<ruby>昨日<rt>きのう</rt></ruby>（　）た。【{verb}】', 'た'),
        ('<ruby>先週<rt>せんしゅう</rt></ruby>（　）た。【{verb}】', 'た'),
        ('さっき（　）た。【{verb}】', 'た'),
    ],
    'の': [
        ('（　）のが<ruby>好<rt>す</rt></ruby>きです。【{verb}】', 'の'),
        ('（　）のが<ruby>得意<rt>とくい</rt></ruby>です。【{verb}】', 'の'),
        ('（　）のを<ruby>忘<rt>わす</rt></ruby>れました。【{verb}】', 'の'),
    ],
    'こと': [
        ('（　）ことができます。【{verb}】', 'こと'),
        ('（　）ことが<ruby>好<rt>す</rt></ruby>きです。【{verb}】', 'こと'),
        ('（　）ことを<ruby>勉強<rt>べんきょう</rt></ruby>しています。【{verb}】', 'こと'),
    ],
    'ば': [
        ('（　）ば、いいです。【{verb}】', 'ば'),
        ('（　）ば、<ruby>分<rt>わ</rt></ruby>かります。【{verb}】', 'ば'),
        ('（　）ば、できます。【{verb}】', 'ば'),
    ],
}


def get_blank_form(verb, nai_form, suffix):
    """後ろの言葉(suffix)に対する穴埋めの正解を返す"""
    c = conjugate(verb, nai_form)
    if not c:
        return None

    if suffix == 'ない':
        full = c['ない']
        return full[:-2] if full.endswith('ない') else None  # 会わない→会わ
    if suffix == 'よう':
        full = c['よう']
        if full.endswith('よう'):
            return full[:-2]  # 見よう→見, 食べよう→食べ
        return full[:-1] if full.endswith('う') else full  # 会おう→会お
    if suffix == 'う':
        full = c['よう']
        if full.endswith('よう'):
            return full[:-2]  # 見よう→見
        return full[:-1] if full.endswith('う') else full  # 買おう→買お
    if suffix == 'ます':
        full = c['ます']
        return full[:-2] if full.endswith('ます') else None  # 会います→会い
    if suffix == 'た':
        full = c['た']
        if full.endswith('た'):
            return full[:-1]  # 会った→会っ, 書いた→書い
        if full.endswith('だ'):
            return full[:-1]  # 泳いだ→泳い
        return full
    if suffix in ('の', 'こと'):
        return c['の']  # 辞書形
    if suffix == 'ば':
        full = c['ば']
        return full[:-1] if full.endswith('ば') else None  # 会えば→会え
    return None


def get_wrong_options(verb, nai_form, correct_ans, suffix, n=3):
    """正解以外の選択肢をnつ生成（4択のため最低3つ）"""
    c = conjugate(verb, nai_form)
    if not c:
        return []

    candidates = []
    if c['ない'].endswith('ない'):
        candidates.append(c['ない'][:-2])
    if c['よう'].endswith('よう'):
        candidates.append(c['よう'][:-2])
    elif c['よう'].endswith('う'):
        candidates.append(c['よう'][:-1])
    if c['ます'].endswith('ます'):
        candidates.append(c['ます'][:-2])
    if c['た'].endswith(('た', 'だ')):
        candidates.append(c['た'][:-1])
    candidates.append(c['の'])
    if c['ば'].endswith('ば'):
        candidates.append(c['ば'][:-1])
    if c.get('命令'):
        candidates.append(c['命令'])

    wrong = [x for x in dict.fromkeys(candidates) if x and x != correct_ans]
    random.shuffle(wrong)
    # 4択のため3つ必要。足りない場合は類似形を追加（例：語幹+ん、語幹+り等）
    if len(wrong) < n and wrong:
        stem = wrong[0][:-1] if len(wrong[0]) > 1 else wrong[0]
        for suffix in ['ん', 'り', 'ま', 'ら']:
            if len(wrong) >= n:
                break
            fake = stem + suffix
            if fake != correct_ans and fake not in wrong:
                wrong.append(fake)
    return wrong[:n]


def build_question(verb, nai_form, suffix_type, q_num):
    """1問分のHTMLを生成"""
    # 意向形は五段→う、一段→よう でテンプレートを選択
    if suffix_type == '意向':
        c = conjugate(verb, nai_form)
        suffix_type = 'う' if c and c['よう'].endswith('う') else 'よう'
    templates = TEMPLATES[suffix_type]
    template, suffix = random.choice(templates)
    verb_ruby = VERB_RUBY.get(verb, verb)
    sentence = template.format(verb=verb_ruby)

    correct = get_blank_form(verb, nai_form, suffix_type)
    if not correct:
        return None

    wrongs = get_wrong_options(verb, nai_form, correct, suffix_type, 3)

    options = [correct] + wrongs
    random.shuffle(options)
    correct_idx = options.index(correct)

    # 活用形の説明
    form_names = {
        'ない': '未然形',
        'よう': '未然形（意向）',
        'う': '未然形（意向）',
        '意向': '未然形（意向）',
        'ます': '連用形',
        'た': '連用形',
        'の': '連体形',
        'こと': '連体形',
        'ば': '仮定形',
    }
    form_name = form_names.get(suffix_type, '')

    opt_html = []
    for i, opt in enumerate(options):
        val = '1' if opt == correct else '0'
        opt_html.append(
            f'<div class="option"><input type="radio" name="q{q_num}" id="q{q_num}{chr(97+i)}" value="{val}">'
            f'<label for="q{q_num}{chr(97+i)}">{opt}</label></div>'
        )

    expl = f'✅ 正解：{correct}<br>活用形：{form_name}。「{correct}」＋「{suffix_type}」'
    # ふりがなは必要に応じて追加。今回はシンプルに
    return {
        'sentence': sentence,
        'options': '\n'.join(opt_html),
        'explanation': expl,
        'correct_idx': correct_idx,
    }


def generate_html(questions, part_num, output_path):
    """HTMLファイルを生成"""
    total = len(questions)
    time_limit = 15  # 全テスト15分

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>N5動詞 活用形テスト{part_num}（{total}問・{time_limit}分）</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}html{{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}}body{{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}}.container{{max-width:800px;margin:0 auto;padding:20px}}header{{background:linear-gradient(135deg,#8b5cf6 0%,#6d28d9 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(139,92,246,0.4)}}header h1{{font-size:1.5em;margin-bottom:4px}}.header-info{{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}}.timer{{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}}.timer.warning{{color:#ffd700;animation:pulse 1s infinite}}.timer.danger{{color:#ff4757;animation:pulse .5s infinite}}@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.6}}}}.progress-bar{{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}}.progress-fill{{height:100%;background:#fff;border-radius:4px;transition:width .3s}}.score-badge{{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}}.section{{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}.section-title{{font-size:1.1em;font-weight:bold;color:#6d28d9;border-left:4px solid #8b5cf6;padding-left:12px;margin-bottom:16px}}.question{{padding:16px 0;border-bottom:1px solid #e2e8f0}}.question:last-child{{border-bottom:none}}.q-num{{display:inline-block;background:#8b5cf6;color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}}.q-text{{font-size:1.05em;margin-bottom:12px;font-weight:500}}.options{{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}}@media(max-width:600px){{.options{{grid-template-columns:1fr}}}}.option{{display:flex;flex-direction:column;position:relative;min-height:0}}.option input{{display:none}}.option label{{display:block;flex:1;min-height:52px;padding:10px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;line-height:1.65;touch-action:manipulation;-webkit-user-select:none;user-select:none}}.option label:hover{{border-color:#8b5cf6;background:#f5f3ff}}.option input:checked+label{{border-color:#8b5cf6;background:#ede9fe;color:#5b21b6;font-weight:600}}.option.correct label{{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}}.option.wrong label{{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}}.btn-submit{{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#8b5cf6 0%,#6d28d9 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}}.btn-submit:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(139,92,246,0.4)}}.btn-submit:disabled{{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}}.result-panel{{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}}.result-panel h2{{font-size:1.8em;margin-bottom:8px}}.result-score{{font-size:3em;font-weight:bold;margin:16px 0}}.result-score.excellent{{color:#48bb78}}.result-score.good{{color:#38b2ac}}.result-score.fair{{color:#ed8936}}.result-score.poor{{color:#fc8181}}.result-detail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}}.result-item{{background:#f7fafc;padding:12px;border-radius:8px}}.result-item .label{{font-size:.8em;color:#718096}}.result-item .value{{font-size:1.2em;font-weight:bold}}.explanation{{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}}.explanation.show{{display:block}}
ruby{{ruby-align:center}}rt{{font-size:.55em;line-height:1.3}}
</style>
</head>
<body>
<div class="container">
<header>
<h1>N5<ruby>動詞<rt>どうし</rt></ruby> <ruby>活用形<rt>かつようけい</rt></ruby>テスト{part_num}（{total}<ruby>問<rt>もん</rt></ruby>・{time_limit}<ruby>分<rt>ぷん</rt></ruby>）</h1>
<div class="header-info">
<div class="timer" id="timer">{time_limit}:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge">全{total}<ruby>問<rt>もん</rt></ruby></div>
</div>
</header>

<div class="section">
<div class="section-title">（　）に入れるのに<ruby>最も<rt>もっとも</rt></ruby>よいものを<ruby>選<rt>えら</rt></ruby>んでください</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>動詞<rt>どうし</rt></ruby>の<ruby>基本形<rt>きほんけい</rt></ruby>（<ruby>辞書形<rt>じしょけい</rt></ruby>）は【】で<ruby>示<rt>しめ</rt></ruby>しています。<br>
<ruby>続<rt>つづ</rt></ruby>く<ruby>言葉<rt>ことば</rt></ruby>：A ない・よう・（う）　｜　B ます・た　｜　C と・。　｜　D の・こと　｜　E ば　｜　F。（!）</p>

'''

    for i, q in enumerate(questions, 1):
        html += f'''
<div class="question">
<div class="q-text"><span class="q-num">{i}</span>{q['sentence']}</div>
<div class="options">
{q['options']}
</div>
<div class="explanation">{q['explanation']}</div>
</div>
'''

    html += f'''
</div>

<button class="btn-submit" id="submitBtn" onclick="submitTest()"><ruby>採点<rt>さいてん</rt></ruby>する</button>
<div class="result-panel" id="resultPanel"><h2 id="resultTitle"></h2><div class="result-score" id="resultScore"></div><div class="result-detail" id="resultDetail"></div><button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう<ruby>一度<rt>いちど</rt></ruby></button></div>
</div>

<script>
const TOTAL={total},TIME_LIMIT={time_limit*60};let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){{timerInterval=setInterval(()=>{{timeLeft--;const m=Math.floor(timeLeft/60),s=timeLeft%60;const el=document.getElementById('timer');el.textContent=`${{m}}:${{s.toString().padStart(2,'0')}}`;document.getElementById('progress').style.width=`${{(timeLeft/TIME_LIMIT)*100}}%`;if(timeLeft<=60)el.className='timer danger';else if(timeLeft<=180)el.className='timer warning';if(timeLeft<=0){{clearInterval(timerInterval);submitTest();}}}},1000);}}
function submitTest(){{if(submitted)return;submitted=true;clearInterval(timerInterval);let correct=0;for(let i=1;i<=TOTAL;i++){{const sel=document.querySelector(`input[name="q${{i}}"]:checked`);const opts=document.querySelectorAll(`input[name="q${{i}}"]`);let ok=false;if(sel&&sel.value==='1'){{ok=true;correct++;}}opts.forEach(o=>{{const p=o.parentElement;if(o.value==='1')p.classList.add('correct');else if(o.checked)p.classList.add('wrong');}});}}document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));const pct=Math.round((correct/TOTAL)*100);const panel=document.getElementById('resultPanel');panel.style.display='block';const score=document.getElementById('resultScore');score.textContent=`${{correct}} / ${{TOTAL}}（${{pct}}%）`;const title=document.getElementById('resultTitle');if(pct>=90){{title.textContent='🎉 素晴らしい！';score.className='result-score excellent';}}else if(pct>=70){{title.textContent='👍 よくできました！';score.className='result-score good';}}else if(pct>=50){{title.textContent='📝 もう少し！';score.className='result-score fair';}}else{{title.textContent='💪 がんばりましょう！';score.className='result-score poor';}}const t=TIME_LIMIT-timeLeft;document.getElementById('resultDetail').innerHTML=`<div class="result-item"><div class="label"><ruby>正解数<rt>せいかいすう</rt></ruby></div><div class="value">${{correct}}/${{TOTAL}}</div></div><div class="result-item"><div class="label"><ruby>所要時間<rt>しょようじかん</rt></ruby></div><div class="value">${{Math.floor(t/60)}}<ruby>分<rt>ぷん</rt></ruby>${{t%60}}<ruby>秒<rt>びょう</rt></ruby></div></div>`;document.getElementById('submitBtn').disabled=true;panel.scrollIntoView({{behavior:'smooth'}});}}
startTimer();
</script>
</body>
</html>
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {output_path}")


def main():
    random.seed(42)

    # 後ろの言葉の種類（意向形は う/よう を動詞タイプで使い分け）
    suffix_types = ['ない', '意向', 'ます', 'た', 'の', 'こと', 'ば']

    # 各動詞に1つずつ suffix を割り当て（バランスよく）
    verb_suffix_pairs = []
    for i, (verb, nai_form) in enumerate(N5_VERBS):
        st = suffix_types[i % len(suffix_types)]
        verb_suffix_pairs.append((verb, nai_form, st))

    random.shuffle(verb_suffix_pairs)

    # 3分割
    n = len(verb_suffix_pairs)
    part1 = verb_suffix_pairs[:36]
    part2 = verb_suffix_pairs[36:71]
    part3 = verb_suffix_pairs[71:]

    deploy_dir = os.path.join(os.path.dirname(__file__), '..', 'jlpt-kakunin-test-deploy')
    os.makedirs(deploy_dir, exist_ok=True)

    for part_num, pairs in enumerate([part1, part2, part3], 1):
        questions = []
        for i, (verb, nai_form, suffix_type) in enumerate(pairs):
            q = build_question(verb, nai_form, suffix_type, i + 1)
            if q:
                questions.append(q)
            else:
                # フォールバック: 別のsuffixで試す
                for st in suffix_types:
                    if st != suffix_type:
                        q = build_question(verb, nai_form, st, i + 1)
                        if q:
                            questions.append(q)
                            break

        if questions:
            out_path = os.path.join(deploy_dir, f'n5-doushi-katsuyokei-test-{part_num}.html')
            generate_html(questions, part_num, out_path)


if __name__ == '__main__':
    main()
