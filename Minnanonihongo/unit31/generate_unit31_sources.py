#!/usr/bin/env python3
"""Generate unit31-fukushu-a.html and unit31-kanji-vocab-quiz.html for 第31課（意向・つもり・予定）."""
from __future__ import annotations

import random
import sys
from pathlib import Path

_MINNA_ROOT = Path(__file__).resolve().parents[1]
if str(_MINNA_ROOT) not in sys.path:
    sys.path.insert(0, str(_MINNA_ROOT))
from shared.fukushu_lead_unit31 import fukushu_section_lead_paragraph

DIR = Path(__file__).resolve().parent

# unit31.md「クイズ用メタデータ」/ unit31-fukushu-question-list.md / unit31-vocabulary-kanji-list.md と同期（変更時は _build_unit31_merged_quiz_parts.py の F・K・チャンクも合わせる）
FUKUSHU_QUESTION_COUNT = 40
KANJI_QUESTION_COUNT = 40
FUKUSHU_WHOLE_PAGE_TIME_SEC = 45 * 60
KANJI_WHOLE_PAGE_TIME_SEC = KANJI_QUESTION_COUNT * 40

STYLE_BLOCK = r"""<style>
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
header{background:linear-gradient(135deg,#2b6cb0 0%,#2c5282 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(43,108,176,.4)}
header h1{font-size:1.45em;margin-bottom:4px}
.header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}
.timer.warning{color:#ffd700;animation:pulse 1s infinite}
.timer.danger{color:#ff4757;animation:pulse .5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}
.score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}
.section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-title{font-size:1.1em;font-weight:bold;color:#2b6cb0;border-left:4px solid #2b6cb0;padding-left:12px;margin-bottom:16px}
.section-lead{font-size:1.05em;font-weight:500;color:#2d3748;line-height:1.65;margin-bottom:18px}
.question{padding:16px 0;border-bottom:1px solid #e2e8f0}
.question:last-child{border-bottom:none}
.q-num{display:inline-block;background:#2b6cb0;color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}
.q-text{font-size:1.05em;margin-bottom:12px;font-weight:500}
.options{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}
@media(max-width:600px){.options{grid-template-columns:1fr}}
.option{position:relative;display:flex;min-height:0}
.option input{display:none}
.option label{flex:1;display:flex;align-items:center;gap:8px;padding:12px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;touch-action:manipulation;-webkit-user-select:none;user-select:none;min-height:48px;width:100%;box-sizing:border-box}
.option .opt-key{flex:0 0 auto;min-width:1.75em;text-align:right;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.4;align-self:center}
.option .opt-body{flex:1;min-width:0;line-height:1.65;align-self:center}
.option label:hover{border-color:#2b6cb0;background:#f0f7ff}
.option input:checked+label{border-color:#2b6cb0;background:#e8f2fc;color:#1a365d;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.reading-passage{background:#f7fafc;border-left:3px solid #2b6cb0;padding:16px;margin:12px 0;border-radius:0 8px 8px 0;font-size:.95em;line-height:1.9}
.dialogue{margin:8px 0 12px;padding:14px 16px;background:#f7fafc;border-left:3px solid #2b6cb0;border-radius:0 8px 8px 0;font-size:1.02em;line-height:1.85}
.dialogue p{margin:0 0 .55em;padding:0}
.dialogue p:last-child{margin-bottom:0}
.dialogue .sp{font-weight:700;color:#2c5282;margin-right:.15em}
.btn-submit{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#2b6cb0 0%,#2c5282 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(43,108,176,.4)}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
.result-panel{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}
.result-panel h2{font-size:1.8em;margin-bottom:8px}
.result-score{font-size:3em;font-weight:bold;margin:16px 0}
.result-score.excellent{color:#48bb78}
.result-score.good{color:#2b6cb0}
.result-score.fair{color:#ed8936}
.result-score.poor{color:#fc8181}
.result-detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}
.result-item{background:#f7fafc;padding:12px;border-radius:8px}
.result-item .label{font-size:.8em;color:#718096}
.result-item .value{font-size:1.2em;font-weight:bold}
.explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}
.explanation.show{display:block}
ruby{ruby-align:center}
rt{font-size:0.55em;font-weight:400;line-height:1.1}
.option label ruby rt{font-size:0.5em}
.subq{margin-top:14px;padding-top:12px;border-top:1px dashed #cbd5e0}
.subq:first-of-type{margin-top:10px;border-top:none;padding-top:0}
.subq-label{font-size:.95em;font-weight:600;color:#2b6cb0;margin-bottom:8px}
.blank-paren{display:inline-block;color:#c05621;font-weight:700;white-space:nowrap}
.blank-paren .blank-n{font-weight:700}
</style>"""


def opt_block(q: int, correct: str, w: list[str], explain: str) -> str:
    labels = ["a", "b", "c", "d"]
    bodies = [correct, w[0], w[1], w[2]]
    parts = []
    for i, (lab, body, val) in enumerate(zip(labels, bodies, ["1", "0", "0", "0"])):
        parts.append(
            f'<div class="option"><input type="radio" name="q{q}" id="q{q}{lab}" value="{val}">'
            f'<label for="q{q}{lab}"><span class="opt-key">{i+1}.</span><span class="opt-body">{body}</span></label></div>'
        )
    return (
        '<div class="options">\n'
        + "\n".join(parts)
        + f'\n</div><div class="explanation">✅ {explain}</div>'
    )


def subq_html(q: int, mark: str, explain_tail: str, correct: str, wrong: list[str]) -> str:
    exp = f"正解：1 — {explain_tail}。"
    return (
        f'<div class="subq"><div class="q-text"><span class="q-num">{q}</span>'
        f'<span class="blank-paren">（<span class="blank-n">{mark}</span>　　　　）</span>に　'
        f'{rb("入", "はい")}るのは</div>'
        + opt_block(q, correct, wrong, exp)
        + "</div>"
    )


def num_q(q: int, display: str, correct: str, wrong: list[str], expl: str) -> str:
    return f"""<div class="question">
<div class="q-text"><span class="q-num">{q}</span>{display}</div>
{opt_block(q, correct, wrong, expl)}
</div>
"""


def fukushu_footer() -> str:
    js = r"""
<button class="btn-submit" id="submitBtn" onclick="submitTest()"><ruby>採点<rt>さいてん</rt></ruby>する</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2><div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう<ruby>一度<rt>いちど</rt></ruby></button>
</div></div>

<script>
const TOTAL=__TOTAL__,TIME_LIMIT=__TIME__;
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
else el.className='timer';
if(timeLeft<=0){clearInterval(timerInterval);submitTest();}
},1000);
}
function submitTest(){
if(submitted)return;submitted=true;
clearInterval(timerInterval);
let correct=0;
for(let i=1;i<=TOTAL;i++){
const sel=document.querySelector(`input[name="q${i}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${i}"]`);
if(sel&&sel.value==='1'){correct++;}
opts.forEach(o=>{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
});
}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
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
<div class="result-item"><div class="label">せいかい</div><div class="value">${correct}/${TOTAL}</div></div>
<div class="result-item"><div class="label">じかん</div><div class="value">${Math.floor(timeUsed/60)}分${timeUsed%60}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({behavior:'smooth'});
}
startTimer();
</script>

</body></html>
"""
    return js.replace("__TOTAL__", str(FUKUSHU_QUESTION_COUNT)).replace(
        "__TIME__", str(FUKUSHU_WHOLE_PAGE_TIME_SEC)
    )


def _split_question_at_ellipsis(sentence: str) -> str:
    """問題4・5の設問を、……の直前で改行して2行表示にする。"""
    sep = "……"
    if sep not in sentence:
        return sentence
    i = sentence.index(sep)
    return f"{sentence[:i].rstrip()}<br>{sentence[i:]}"


def rb(word: str, yomi: str) -> str:
    """
    漢字の塊にだけ <ruby> を付け、送りがな・ひらがな・カタカナはベースの外に出す。
    よみは word の左から対応づくものとする（次セグメントのかながよみ中に現れる位置で区切る）。
    対応できないときは従来どおり全体を 1 つの ruby にまとめる。
    """
    import re

    if not word:
        return word
    if not yomi:
        return word if not re.search(r"[\u4e00-\u9fff々]", word) else f"<ruby>{word}<rt></rt></ruby>"

    hira = r"[\u3041-\u3096\u30fc]"
    kata = r"[ァ-ヶー]"
    kanji = r"[\u4e00-\u9fff々]"
    segs = re.findall(rf"(?:{kanji})+|(?:{hira})+|(?:{kata})+", word)
    if not segs or not any(re.search(kanji, s) for s in segs):
        return word

    yi = 0
    out: list[str] = []
    for i, seg in enumerate(segs):
        if re.fullmatch(rf"(?:{hira})+|(?:{kata})+", seg):
            if yi + len(seg) > len(yomi) or yomi[yi : yi + len(seg)] != seg:
                return f"<ruby>{word}<rt>{yomi}</rt></ruby>"
            yi += len(seg)
            out.append(seg)
            continue
        nk = None
        for j in range(i + 1, len(segs)):
            s2 = segs[j]
            if re.fullmatch(rf"(?:{hira})+|(?:{kata})+", s2):
                nk = s2
                break
        if nk is not None:
            pos = yomi.find(nk, yi)
            if pos == -1:
                return f"<ruby>{word}<rt>{yomi}</rt></ruby>"
            rk = yomi[yi:pos]
            yi = pos
        else:
            rk = yomi[yi:]
            yi = len(yomi)
        out.append(f"<ruby>{seg}<rt>{rk}</rt></ruby>")
    if yi != len(yomi):
        return f"<ruby>{word}<rt>{yomi}</rt></ruby>"
    return "".join(out)


def build_fukushu() -> str:
    parts: list[str] = []
    parts.append(
        """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>みんなの日本語 31 クイズ（復習）</title>
"""
    )
    parts.append(STYLE_BLOCK)
    parts.append(
        f"""</head>
<body>
<div class="container">
<header>
<h1>みんなの<ruby>日本語<rt>にほんご</rt></ruby> 31 クイズ（<ruby>復習<rt>ふくしゅう</rt></ruby>）</h1>
<div class="header-info">
<div class="timer" id="timer">__TIMER__</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge"><ruby>全<rt>ぜん</rt></ruby>__FNUM__<ruby>問<rt>もん</rt></ruby></div>
</div>
</header>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>１</div>
{fukushu_section_lead_paragraph(1, 4)}
"""
    )

    # 教材「問題」126 の 1)〜4) — 設問・選択肢は漢字＋ふりがな
    ishou = [
        (
            rb("買います", "かいます"),
            rb("買おう", "かおう"),
            [rb("買", "か") + "よう", rb("買う", "かう"), rb("買いましょう", "かいましょう")],
        ),
        (
            rb("歩きます", "あるきます"),
            rb("歩こう", "あるこう"),
            [rb("歩きよう", "あるきよう"), rb("歩く", "あるく"), rb("歩きましょう", "あるきましょう")],
        ),
        (
            rb("急ぎます", "いそぎます"),
            rb("急ごう", "いそごう"),
            [rb("急ぎよう", "いそぎよう"), rb("急ぐ", "いそぐ"), rb("急ぎましょう", "いそぎましょう")],
        ),
        (
            rb("直します", "なおします"),
            rb("直そう", "なおそう"),
            [rb("直しよう", "なおしよう"), rb("直す", "なおす"), rb("直しましょう", "なおしましょう")],
        ),
    ]
    for i, (m, cor, wr) in enumerate(ishou, start=1):
        parts.append(
            num_q(
                i,
                f'「{m}」の<ruby>意向形<rt>いこうけい</rt></ruby>はどれですか。',
                cor,
                wr,
                f"正解：1 — 「{m}」→「{cor}」。",
            )
        )

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>練習<rt>れんしゅう</rt></ruby>A</div>
{fukushu_section_lead_paragraph(5, 14)}
"""
    )
    # 練習A 第1表の残り＋第2・第3表（F に +10）
    rennshuu_a_extra = [
        (
            rb("待ちます", "まちます"),
            rb("待とう", "まとう"),
            [rb("待ちよう", "まちよう"), rb("待つ", "まつ"), rb("待ちましょう", "まちましょう")],
        ),
        (
            rb("遊びます", "あそびます"),
            rb("遊ぼう", "あそぼう"),
            [rb("遊びよう", "あそびよう"), rb("遊ぶ", "あそぶ"), rb("遊びましょう", "あそびましょう")],
        ),
        (
            rb("休みます", "やすみます"),
            rb("休もう", "やすもう"),
            [rb("休みよう", "やすみよう"), rb("休む", "やすむ"), rb("休みましょう", "やすみましょう")],
        ),
        (
            rb("乗ります", "のります"),
            rb("乗ろう", "のろう"),
            [rb("乗りよう", "のりよう"), rb("乗る", "のる"), rb("乗りましょう", "のりましょう")],
        ),
        (
            rb("帰ります", "かえります"),
            rb("帰ろう", "かえろう"),
            [rb("帰よう", "かえよう"), rb("帰る", "かえる"), rb("帰りましょう", "かえりましょう")],
        ),
        (
            rb("覚えます", "おぼえます"),
            rb("覚えよう", "おぼえよう"),
            [rb("覚えろう", "おぼえろう"), rb("覚える", "おぼえる"), rb("覚えましょう", "おぼえましょう")],
        ),
        (
            rb("見ます", "みます"),
            rb("見よう", "みよう"),
            [rb("見る", "みる"), rb("見ます", "みます"), rb("見ましょう", "みましょう")],
        ),
        (
            rb("来ます", "きます"),
            rb("来よう", "こよう"),
            [rb("来よう", "きよう"), rb("来る", "くる"), rb("来ます", "きます")],
        ),
        (
            rb("します", "します"),
            rb("しよう", "しよう"),
            [rb("する", "する"), rb("します", "します"), rb("しましょう", "しましょう")],
        ),
        (
            rb("休憩します", "きゅうけいします"),
            rb("休憩しよう", "きゅうけいしよう"),
            [
                rb("休憩する", "きゅうけいする"),
                rb("休憩します", "きゅうけいします"),
                rb("休憩しましょう", "きゅうけいしましょう"),
            ],
        ),
    ]
    for i, (m, cor, wr) in enumerate(rennshuu_a_extra, start=5):
        parts.append(
            num_q(
                i,
                f'「{m}」の<ruby>意向形<rt>いこうけい</rt></ruby>はどれですか。',
                cor,
                wr,
                f"正解：1 — 「{m}」→「{cor}」。",
            )
        )

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>２</div>
{fukushu_section_lead_paragraph(15, 19)}
"""
    )

    p2 = [
        (
            15,
            f'{rb("明日", "あした")}　レストランへ　<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>。'
            f'{rb("一緒", "いっしょ")}に　どうですか。',
            "①",
            f'「{rb("行きます", "いきます")}」',
            rb("行きます", "いきます"),
            [rb("行こう", "いこう"), rb("行きましょう", "いきましょう"), rb("行って", "いって")],
        ),
        (
            16,
            f'{rb("将来", "しょうらい")}　{rb("自分", "じぶん")}の　{rb("会社", "かいしゃ")}を　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            "①",
            f'「{rb("作ろう", "つくろう")}」',
            rb("作ろう", "つくろう"),
            [rb("作ります", "つくります"), rb("作って", "つくって"), rb("作る", "つくる")],
        ),
        (
            17,
            f'{rb("来月", "らいげつ")}　{rb("車", "くるま")}を　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>つもりです。',
            "①",
            f'「{rb("買う", "かう")}」（{rb("辞書形", "じしょけい")}）',
            rb("買う", "かう"),
            [rb("買おう", "かおう"), rb("買います", "かいます"), rb("買った", "かった")],
        ),
        (
            18,
            f'レポートは　まだ　<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>いません。',
            "①",
            f'「{rb("書いて", "かいて")}」',
            rb("書いて", "かいて"),
            [rb("書き", "かき"), rb("書こう", "かこう"), rb("書く", "かく")],
        ),
        (
            19,
            f'お{rb("正月", "しょうがつ")}は　{rb("家族", "かぞく")}と　{rb("温泉", "おんせん")}へ　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            "①",
            f'「{rb("行こう", "いこう")}」',
            rb("行こう", "いこう"),
            [rb("行きます", "いきます"), rb("行って", "いって"), rb("行きましょう", "いきましょう")],
        ),
    ]
    for q, dlg, mark, et, cor, wr in p2:
        parts.append('<div class="question">\n<div class="dialogue">\n')
        parts.append(f"<p>{dlg}</p>\n")
        parts.append("</div>\n")
        parts.append(subq_html(q, mark, et, cor, wr))
        parts.append("</div>\n")

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>３</div>
{fukushu_section_lead_paragraph(20, 24)}
"""
    )

    # 問題126・練習A と語が重複する行は出さない（同一小問の重複回避）
    hyou = [
        (
            rb("踊ります", "おどります"),
            rb("踊ろう", "おどろう"),
            [rb("踊りよう", "おどりよう"), rb("踊ります", "おどります"), rb("踊る", "おどる")],
        ),
        (
            rb("探します", "さがします"),
            rb("探そう", "さがそう"),
            [rb("探します", "さがします"), rb("探す", "さがす"), rb("探しましょう", "さがしましょう")],
        ),
        (
            rb("寝ます", "ねます"),
            rb("寝よう", "ねよう"),
            [rb("寝ます", "ねます"), rb("寝る", "ねる"), rb("寝ましょう", "ねましょう")],
        ),
        (
            rb("続けます", "つづけます"),
            rb("続けよう", "つづけよう"),
            [rb("続けます", "つづけます"), rb("続ける", "つづける"), rb("続けましょう", "つづけましょう")],
        ),
        (
            rb("決めます", "きめます"),
            rb("決めよう", "きめよう"),
            [rb("決めます", "きめます"), rb("決める", "きめる"), rb("決めましょう", "きめましょう")],
        ),
    ]
    for i, (m, cor, wr) in enumerate(hyou, start=20):
        parts.append(
            num_q(
                i,
                f'「{m}」の<ruby>意向形<rt>いこうけい</rt></ruby>はどれですか。',
                cor,
                wr,
                f"正解：1 — 「{m}」→「{cor}」。",
            )
        )

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>４</div>
{fukushu_section_lead_paragraph(25, 28)}
"""
    )

    p4 = [
        (
            25,
            f'どこの　パソコンを　{rb("買います", "かいます")}か。　……パワー{rb("電気", "でんき")}の　パソコンを　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            rb("買おう", "かおう"),
            [rb("買う", "かう"), rb("買います", "かいます"), rb("買った", "かった")],
            f'「{rb("買おう", "かおう")}」。',
        ),
        (
            26,
            f'どんな　{rb("家", "いえ")}を　{rb("作ります", "つくります")}か。　……{rb("両親", "りょうしん")}と　{rb("一緒", "いっしょ")}に　'
            f'{rb("住める", "すめる")}　{rb("家", "いえ")}を　<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            rb("作ろう", "つくろう"),
            [rb("作る", "つくる"), rb("作ります", "つくります"), rb("作って", "つくって")],
            f'「{rb("作ろう", "つくろう")}」。',
        ),
        (
            27,
            f'ホテルは　どう　しますか。　……{rb("駅", "えき")}の　{rb("近", "ちか")}くの　ホテルを　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            rb("予約しよう", "よやくしよう"),
            [rb("予約します", "よやくします"), rb("予約する", "よやくする"), rb("取ろう", "とろう")],
            f'「{rb("予約しよう", "よやくしよう")}」。',
        ),
        (
            28,
            f'{rb("日曜日", "にちようび")}の　{rb("朝", "あさ")}は　{rb("何", "なに")}を　しますか。　……{rb("教会", "きょうかい")}へ　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>と　{rb("思", "おも")}って　います。',
            rb("行こう", "いこう"),
            [rb("行きます", "いきます"), rb("行って", "いって"), rb("行きましょう", "いきましょう")],
            f'「{rb("行こう", "いこう")}」。',
        ),
    ]
    for q, sentence, cor, wr, tail in p4:
        expl = f"正解：1 — {tail}"
        body = _split_question_at_ellipsis(sentence)
        parts.append(f"""<div class="question">
<div class="q-text"><span class="q-num">{q}</span>{body}</div>
{opt_block(q, cor, wr, expl)}
</div>
""")

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>５</div>
{fukushu_section_lead_paragraph(29, 32)}
"""
    )

    p5 = [
        (
            29,
            f'{rb("誰", "だれ")}に　{rb("引越し", "ひっこし")}を　{rb("手伝", "てつだ")}って　{rb("貰", "もら")}いますか。　……'
            f'{rb("会社", "かいしゃ")}の　{rb("人", "ひと")}に　<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>つもりです。',
            rb("手伝ってもらう", "てつだってもらう"),
            [
                rb("手伝います", "てつだいます"),
                rb("手伝う", "てつだう"),
                rb("手伝ってあげる", "てつだってあげる"),
            ],
            f'「{rb("手伝ってもらう", "てつだってもらう")}」。',
        ),
        (
            30,
            f'{rb("夏休み", "なつやすみ")}に　{rb("国", "くに")}へ　{rb("帰", "かえ")}りますか。　……いいえ、クリスマスまで　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>つもりです。',
            rb("帰らない", "かえらない"),
            [rb("帰ります", "かえります"), rb("帰らなかった", "かえらなかった"), rb("帰ろう", "かえろう")],
            f'「{rb("帰らない", "かえらない")}」。',
        ),
        (
            31,
            f'{rb("明日", "あした")}の　{rb("朝", "あさ")}　{rb("何時", "なんじ")}ごろ　{rb("出掛", "でか")}けますか。　……７{rb("時", "じ")}ごろ　'
            f'<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>つもりです。',
            rb("出かける", "でかける"),
            [rb("出かけます", "でかけます"), rb("出かけよう", "でかけよう"), rb("出かけて", "でかけて")],
            f'「{rb("出かける", "でかける")}」（{rb("辞書形", "じしょけい")}）。',
        ),
        (
            32,
            f'{rb("旅行", "りょこう")}に　あの　{rb("大", "おお")}きい　カメラを　{rb("持", "も")}って　{rb("行", "い")}きますか。　……いいえ、'
            f'{rb("重", "おも")}いですから、　<span class="blank-paren">（<span class="blank-n">①</span>　　　　）</span>つもりです。',
            rb("持って行かない", "もっていかない"),
            [rb("持って行きます", "もっていきます"), rb("持って行こう", "もっていこう"), rb("持たない", "もたない")],
            f'「{rb("持って行かない", "もっていかない")}」。',
        ),
    ]
    for q, sentence, cor, wr, tail in p5:
        expl = f"正解：1 — {tail}"
        body = _split_question_at_ellipsis(sentence)
        parts.append(f"""<div class="question">
<div class="q-text"><span class="q-num">{q}</span>{body}</div>
{opt_block(q, cor, wr, expl)}
</div>
""")

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>問題<rt>もんだい</rt></ruby>６</div>
{fukushu_section_lead_paragraph(33, 36)}
"""
    )

    schedule_block = f"""<div class="reading-passage" lang="ja">
<p style="font-weight:600;margin-bottom:10px">４{rb("月", "がつ")}の　スケジュール</p>
<ul style="margin:0;padding-left:1.25em;line-height:1.9">
<li>1（{rb("火曜日", "かようび")}）　{rb("今日", "きょう")}</li>
<li>2（{rb("水曜日", "すいようび")}）　{rb("広島", "ひろしま")}へ　{rb("出張", "しゅっちょう")}</li>
<li>3（{rb("木曜日", "もくようび")}）　ミラーさんに　{rb("会", "あ")}う</li>
<li>4（{rb("金曜日", "きんようび")}）</li>
<li>5（{rb("土曜日", "どようび")}）　{rb("上野公園", "うえのこうえん")}で　お{rb("花見", "はなみ")}</li>
<li>6（{rb("日曜日", "にちようび")}）</li>
<li>7（{rb("月曜日", "げつようび")}）　{rb("会議", "かいぎ")}</li>
</ul>
</div>"""
    parts.append(schedule_block)

    p6 = [
        (
            33,
            f'{rb("予定", "よてい")}されている　{rb("会議", "かいぎ")}は　いつですか。',
            f'7（{rb("月曜日", "げつようび")}）',
            [f'1（{rb("火曜日", "かようび")}）', f'5（{rb("土曜日", "どようび")}）', f'3（{rb("木曜日", "もくようび")}）'],
            f'正解：1 — 1の　あとの　{rb("会議", "かいぎ")}は　7（{rb("月曜日", "げつようび")}）。',
        ),
        (
            34,
            f'{rb("今日", "きょう")}は　1（{rb("火曜日", "かようび")}）。{rb("翌日", "よくじつ")}、なにか　{rb("予定", "よてい")}は　ありますか。',
            f'{rb("広島", "ひろしま")}へ　{rb("出張", "しゅっちょう")}です',
            [
                f'ミラーさんに　{rb("会", "あ")}います',
                f'{rb("上野公園", "うえのこうえん")}へ　{rb("行", "い")}きます',
                f'{rb("休", "やす")}みです',
            ],
            f'正解：1 — {rb("翌日", "よくじつ")}（2・{rb("水曜日", "すいようび")}）は　{rb("出張", "しゅっちょう")}。',
        ),
        (
            35,
            f'ミラーさんとの　{rb("約束", "やくそく")}は　いつですか。',
            f'3（{rb("木曜日", "もくようび")}）',
            [
                f'2（{rb("水曜日", "すいようび")}）',
                f'5（{rb("土曜日", "どようび")}）',
                f'7（{rb("月曜日", "げつようび")}）',
            ],
            f'正解：1 — {rb("木曜日", "もくようび")}。',
        ),
        (
            36,
            f'5（{rb("土曜日", "どようび")}）の　お{rb("花見", "はなみ")}、{rb("行先", "いきさき")}は　どこですか。',
            rb("上野公園", "うえのこうえん"),
            [rb("神社", "じんじゃ"), "ホテル", rb("広島", "ひろしま")],
            f'正解：1 — {rb("上野公園", "うえのこうえん")}。',
        ),
    ]
    for q, sentence, cor, wr, expl in p6:
        parts.append(
            num_q(
                q,
                sentence,
                cor,
                wr,
                expl,
            )
        )

    reading_block = """<div class="reading-passage" lang="ja">
<ruby>私<rt>わたし</rt></ruby>は　<ruby>九州<rt>きゅうしゅう</rt></ruby>の　<ruby>小さい<rt>ちいさい</rt></ruby>　<ruby>村<rt>むら</rt></ruby>で　<ruby>生<rt>う</rt></ruby>まれた。<ruby>高校<rt>こうこう</rt></ruby>を　<ruby>卒業<rt>そつぎょう</rt></ruby>して、<ruby>東京<rt>とうきょう</rt></ruby>へ　<ruby>来<rt>き</rt></ruby>てから、もう　１０<ruby>年<rt>ねん</rt></ruby>になる。<ruby>今<rt>いま</rt></ruby>、<ruby>自動車会社<rt>じどうしゃがいしゃ</rt></ruby>で　<ruby>働<rt>はたら</rt></ruby>いている。<br>
<ruby>田舎<rt>いなか</rt></ruby>に　いたときは、<ruby>映画館<rt>えいがかん</rt></ruby>もないし、レストランもないし、<ruby>田舎<rt>いなか</rt></ruby>の　<ruby>生活<rt>せいかつ</rt></ruby>は　<ruby>嫌<rt>いや</rt></ruby>だと　<ruby>思<rt>おも</rt></ruby>った。でも、<ruby>最近<rt>さいきん</rt></ruby>、<ruby>疲<rt>つか</rt></ruby>れたときや　<ruby>寂<rt>さび</rt></ruby>しいとき、よく　<ruby>田舎<rt>いなか</rt></ruby>の　<ruby>青<rt>あお</rt></ruby>い　<ruby>空<rt>そら</rt></ruby>や　<ruby>緑<rt>みどり</rt></ruby>の　<ruby>山<rt>やま</rt></ruby>を　<ruby>思<rt>おも</rt></ruby>い<ruby>出<rt>だ</rt></ruby>す。<ruby>目<rt>め</rt></ruby>を　<ruby>閉<rt>と</rt></ruby>じると、<ruby>友<rt>とも</rt></ruby>だちと　<ruby>泳<rt>およ</rt></ruby>いだ　<ruby>川<rt>かわ</rt></ruby>の　<ruby>音<rt>おと</rt></ruby>が　<ruby>聞<rt>き</rt></ruby>こえる。<br>
<ruby>私<rt>わたし</rt></ruby>は　<ruby>来年<rt>らいねん</rt></ruby>の　<ruby>春<rt>はる</rt></ruby>、<ruby>会社<rt>かいしゃ</rt></ruby>を　やめて、<ruby>田舎<rt>いなか</rt></ruby>へ　<ruby>帰<rt>かえ</rt></ruby>るつもりだ。そして、<ruby>都会<rt>とかい</rt></ruby>の　<ruby>子<rt>こ</rt></ruby>どもたちが　<ruby>自由<rt>じゆう</rt></ruby>に　<ruby>遊<rt>あそ</rt></ruby>べる　「<ruby>山<rt>やま</rt></ruby>の<ruby>学校<rt>がっこう</rt></ruby>」を　いつか　<ruby>作<rt>つく</rt></ruby>ろうと　<ruby>思<rt>おも</rt></ruby>っている。
</div>"""

    parts.append(
        f"""</div>

<div class="section">
<div class="section-title"><ruby>復習<rt>ふくしゅう</rt></ruby> — <ruby>読解<rt>どっかい</rt></ruby></div>
{fukushu_section_lead_paragraph(37, 40)}
"""
    )

    parts.append(reading_block)

    dokkai = [
        (
            37,
            f'本文によると、この{rb("人", "ひと")}は　{rb("現在", "げんざい")}どこに　{rb("住", "す")}んでいますか。',
            rb("東京", "とうきょう"),
            [rb("九州", "きゅうしゅう"), rb("村", "むら"), rb("大阪", "おおさか")],
            f'正解：1 — {rb("東京", "とうきょう")}で　{rb("働", "はたら")}いている。',
        ),
        (
            38,
            f'こどものころ、{rb("田舎", "いなか")}の　{rb("生活", "せいかつ")}を　{rb("嫌", "いや")}だと　{rb("思", "おも")}ったのは　なぜですか。',
            f'{rb("映画館", "えいがかん")}もないし、レストランもないから',
            [
                f'{rb("働", "はたら")}くのが　{rb("嫌", "いや")}だったから',
                f'{rb("友", "とも")}だちがいなかったから',
                f'{rb("雨", "あめ")}が{rb("降", "ふ")}ったから',
            ],
            f'正解：1 — {rb("映画館", "えいがかん")}もないし、レストランもないし、…。',
        ),
        (
            39,
            f'{rb("今", "いま")}も、{rb("田舎", "いなか")}での　{rb("暮", "く")}らしは　{rb("嫌", "いや")}ですか。',
            f'いいえ、よく　{rb("思", "おも")}い{rb("出", "だ")}します',
            [
                f'はい、{rb("嫌", "いや")}です',
                f'はい、{rb("好き", "すき")}です',
                rb("分かりません", "わかりません"),
            ],
            f'正解：1 — {rb("疲", "つか")}れたときなどに　{rb("空", "そら")}や　{rb("山", "やま")}を　{rb("思", "おも")}い{rb("出", "だ")}す。',
        ),
        (
            40,
            f'{rb("故郷", "こきょう")}に　{rb("帰", "かえ")}ったあと、{rb("何", "なに")}を　してみたいと　{rb("考", "かんが")}えていますか。',
            f'「{rb("山", "やま")}の{rb("学校", "がっこう")}」を　{rb("作", "つく")}りたい',
            [
                f'{rb("会社", "かいしゃ")}を　{rb("作", "つく")}りたい',
                f'{rb("映画館", "えいがかん")}で{rb("働", "はたら")}きたい',
                f'{rb("東京", "とうきょう")}に　{rb("住", "す")}みたい',
            ],
            f'正解：1 — {rb("山", "やま")}の{rb("学校", "がっこう")}を　{rb("作", "つく")}ろうと　{rb("思", "おも")}っている。',
        ),
    ]

    for q, sentence, cor, wr, expl in dokkai:
        parts.append(
            f"""<div class="question">
<div class="q-text"><span class="q-num">{q}</span>{sentence}</div>
{opt_block(q, cor, wr, expl)}
</div>
"""
        )

    parts.append("</div>\n")
    parts.append(fukushu_footer())
    raw = "".join(parts)
    tm, ts = divmod(FUKUSHU_WHOLE_PAGE_TIME_SEC, 60)
    return raw.replace("__TIMER__", f"{tm}:{ts:02d}").replace(
        "__FNUM__", str(FUKUSHU_QUESTION_COUNT)
    )


def build_kanji() -> str:
    # K＝40：単語の一部（式・帰り・お子さん・号・方／会話の月／読み物の村・子ども／脚注の新神戸）は出題せず、
    # 専門語彙を化学〜地学まで復活。旧72語リストの #67 コンピューター工学は恒久的に出題しない（vocabulary md と同期）。
    items = [
        # ── 単語 108（表の順・読みは教材表に合わせる）
        ("続ける", "つづける"),
        ("見つける", "みつける"),
        ("取る", "とる"),
        ("受ける", "うける"),
        ("申し込む", "もうしこむ"),
        ("休憩", "きゅうけい"),
        ("連休", "れんきゅう"),
        ("作文", "さくぶん"),
        ("発表", "はっぴょう"),
        ("展覧会", "てんらんかい"),
        ("結婚式", "けっこんしき"),
        ("葬式", "そうしき"),
        ("本社", "ほんしゃ"),
        ("支店", "してん"),
        ("教会", "きょうかい"),
        ("大学院", "だいがくいん"),
        ("動物園", "どうぶつえん"),
        ("温泉", "おんせん"),
        # ── 《会話》
        ("残る", "のこる"),
        ("入学試験", "にゅうがくしけん"),
        # ── 《読み物》
        ("卒業", "そつぎょう"),
        ("映画館", "えいがかん"),
        ("嫌", "いや"),
        ("空", "そら"),
        ("閉じる", "とじる"),
        ("都会", "とかい"),
        ("自由", "じゆう"),
        # ── 専門語彙（表を左→右、上→下の順。コンピューター工学は出題しない）
        ("医学", "いがく"),
        ("政治学", "せいじがく"),
        ("薬学", "やくがく"),
        ("国際関係学", "こくさいかんけいがく"),
        ("化学", "かがく"),
        ("法律学", "ほうりつがく"),
        ("生化学", "せいかがく"),
        ("経済学", "けいざいがく"),
        ("生物学", "せいぶつがく"),
        ("経営学", "けいえいがく"),
        ("農学", "のうがく"),
        ("社会学", "しゃかいがく"),
        ("地学", "ちがく"),
    ]
    assert len(items) == KANJI_QUESTION_COUNT
    all_yomi = [y for _, y in items]
    blocks = []
    for i, (word, yomi) in enumerate(items, start=1):
        pool = [all_yomi[j] for j in range(KANJI_QUESTION_COUNT) if j != i - 1]
        rng = random.Random(313131 + i)
        rng.shuffle(pool)
        wrong = pool[:3]
        # 読みクイズ：選択肢はひらがな（読み）のみ。漢字や <ruby> は出題語（kanji-prompt）側のみ。
        cor_opt = yomi
        w_opts = list(wrong)
        blocks.append(
            f"""<div class="question">
<div class="q-text"><span class="q-num">{i}</span></div>
<p class="kanji-prompt" lang="ja">{word}</p>
<div class="options">
<div class="option"><input type="radio" name="q{i}" id="q{i}1" value="1"><label for="q{i}1"><span class="opt-key">1.</span><span class="opt-body">{cor_opt}</span></label></div>
<div class="option"><input type="radio" name="q{i}" id="q{i}2" value="0"><label for="q{i}2"><span class="opt-key">2.</span><span class="opt-body">{w_opts[0]}</span></label></div>
<div class="option"><input type="radio" name="q{i}" id="q{i}3" value="0"><label for="q{i}3"><span class="opt-key">3.</span><span class="opt-body">{w_opts[1]}</span></label></div>
<div class="option"><input type="radio" name="q{i}" id="q{i}4" value="0"><label for="q{i}4"><span class="opt-key">4.</span><span class="opt-body">{w_opts[2]}</span></label></div>
</div>
<div class="explanation">✅ 正解：1 — {cor_opt}</div>
</div>"""
        )

    kstyle = r"""<style>
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
header{background:linear-gradient(135deg,#2b6cb0 0%,#2c5282 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(43,108,176,.4)}
header h1{font-size:1.45em;margin-bottom:4px}
.header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}
.timer.warning{color:#ffd700;animation:pulse 1s infinite}
.timer.danger{color:#ff4757;animation:pulse .5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}
.score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}
.section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-lead{font-size:1.05em;font-weight:500;color:#2d3748;line-height:1.65;margin-bottom:18px}
.section-title{font-size:1.1em;font-weight:bold;color:#2b6cb0;border-left:4px solid #2b6cb0;padding-left:12px;margin-bottom:16px}
.question{padding:16px 0;border-bottom:1px solid #e2e8f0}
.question:last-child{border-bottom:none}
.q-num{display:inline-block;background:#2b6cb0;color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}
.q-text{font-size:1.05em;margin-bottom:12px;font-weight:500}
.kanji-prompt{font-size:clamp(1.6rem,5vw,2.1rem);font-weight:700;text-align:center;margin:4px 0 12px;letter-spacing:.05em;color:#1a365d}
.options{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}
@media(max-width:600px){.options{grid-template-columns:1fr}}
.option{position:relative;display:flex;min-height:0}
.option input{display:none}
.option label{flex:1;display:flex;align-items:center;gap:8px;padding:12px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;touch-action:manipulation;-webkit-user-select:none;user-select:none;min-height:48px;width:100%;box-sizing:border-box}
.option .opt-key{flex:0 0 auto;min-width:1.75em;text-align:right;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.4;align-self:center}
.option .opt-body{flex:1;min-width:0;line-height:1.65;align-self:center;word-break:break-word}
.option label:hover{border-color:#2b6cb0;background:#f0f7ff}
.option input:checked+label{border-color:#2b6cb0;background:#e8f2fc;color:#1a365d;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.btn-submit{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#2b6cb0 0%,#2c5282 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(43,108,176,.4)}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
.result-panel{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}
.result-panel h2{font-size:1.8em;margin-bottom:8px}
.result-score{font-size:3em;font-weight:bold;margin:16px 0}
.result-score.excellent{color:#48bb78}
.result-score.good{color:#2b6cb0}
.result-score.fair{color:#ed8936}
.result-score.poor{color:#fc8181}
.result-detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}
.result-item{background:#f7fafc;padding:12px;border-radius:8px}
.result-item .label{font-size:.8em;color:#718096}
.result-item .value{font-size:1.2em;font-weight:bold}
.explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}
.explanation.show{display:block}
ruby{ruby-align:center}
rt{font-size:0.55em;font-weight:400;line-height:1.1}
.option label ruby rt{font-size:0.5em}
</style>"""

    km, ks = divmod(KANJI_WHOLE_PAGE_TIME_SEC, 60)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>みんなの日本語 31 漢字・語彙クイズ</title>
{kstyle}
</head>
<body>
<div class="container">
<header>
<h1>みんなの<ruby>日本語<rt>にほんご</rt></ruby> 31 <ruby>漢字<rt>かんじ</rt></ruby>・<ruby>語彙<rt>ごい</rt></ruby>クイズ</h1>
<div class="header-info">
<div class="timer" id="timer">{km}:{ks:02d}</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge"><ruby>全<rt>ぜん</rt></ruby>{KANJI_QUESTION_COUNT}<ruby>問<rt>もん</rt></ruby></div>
</div>
</header>

<div class="section">
<p class="section-lead"><ruby>次<rt>つぎ</rt></ruby>の<ruby>漢字<rt>かんじ</rt></ruby>の<ruby>読<rt>よ</rt></ruby>みとして<ruby>正<rt>ただ</rt></ruby>しいものはどれですか。</p>
<div class="section-title"><ruby>問題<rt>もんだい</rt></ruby>（{KANJI_QUESTION_COUNT}<ruby>問<rt>もん</rt></ruby>）</div>
{"".join(blocks)}
</div>
</div>
</body></html>
"""


def main() -> None:
    fuk = build_fukushu()
    (DIR / "unit31-fukushu-a.html").write_text(fuk, encoding="utf-8")
    kan = build_kanji()
    (DIR / "unit31-kanji-vocab-quiz.html").write_text(kan, encoding="utf-8")
    print("Wrote unit31-fukushu-a.html, unit31-kanji-vocab-quiz.html")


if __name__ == "__main__":
    main()
