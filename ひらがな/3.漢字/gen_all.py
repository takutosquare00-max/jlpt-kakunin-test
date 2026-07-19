#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kanji-data を使って二年生〜六年生のHTMLを生成"""

import json
import os

# kakijun.com の学年別漢字（順序・unicode準拠）
# 形式: (漢字, unicode_hex, 画数)
def load_grade_data():
    # Grade 2: 160 chars from kakijun
    g2 = "刀丸弓工才万引牛今元戸午公止少心切太内父分方毛友外兄古広矢市台冬半母北用羽会回交光考行合寺自色西多池地当同肉米毎何角汽近形言谷作社図声走体弟売麦来里画岩京国姉知長直店東歩妹明門夜科海活計後室首秋春食星前茶昼点南風思家夏記帰原高紙時弱書通馬魚教強黄黒細週雪船組鳥野理雲絵間場晴朝答道買番遠園楽新数電話歌語算読聞鳴線親頭顔曜"
    # Grade 3: 200 chars
    g3 = "丁区化反予央去号皿仕写主申世他打代皮氷平由礼安曲血向死次式守州全有羊両列医究局君決住助身対投豆坂返役委育泳岸苦具幸始使事実者昔取受所注定波板表服物放味命油和屋界客急級係県研指持拾重昭乗神相送待炭柱追度畑発美秒品負面洋院員荷起宮庫根酒消真息速庭島配倍病勉旅流悪球祭習終宿章商進深族第帳笛転都動部問飲運温開階寒期軽湖港歯集暑勝植短着等登湯童悲筆遊葉陽落暗意感漢業詩想鉄農福路駅銀鼻様緑練横談調箱館橋整薬題"
    # Grade 4: 200 chars  
    g4 = "士欠氏不夫以加功札史司失必付辺包末未民令衣印各共好成争仲兆伝灯老位囲改完希求芸告材児初臣折束低努兵別利良冷労英果芽官季泣協径固刷参治周松卒底的典毒念府法牧例胃栄紀軍型建昨祝省信浅単飛変便約勇要案害挙訓郡候航差殺残借笑席倉孫帯徒特梅粉脈浴料連副望陸貨械救健康菜産唱清巣側停堂得敗票街覚喜給極景結最散順焼象隊達貯然博飯費無満量愛塩試辞照節戦続置腸働関管旗察種静説漁歴億課器賞選熱標養輪機積録観験類願鏡議競"
    # Grade 5: 185 chars
    g5 = "久支比仏圧永可刊旧句示犯布弁因仮件再在舌団任応快技均災志似序状条判防余易往価河居券効妻枝舎述承招性制版肥非武逆限故厚査政祖則退独保迷益桜恩格個耕財師修素造能破俵容留移液眼規基寄許経険現混採授術常情責設接断張貧婦務率略提統備評富復報貿営過賀検減証税絶測属貸程解幹義禁群鉱罪資飼準勢損墓豊夢預演慣境構際雑酸製精銭総増像態適銅徳複綿領確潔賛質敵導編暴衛興築燃輸講謝績額職織識護"
    # Grade 6: 181 chars
    g6 = "干己寸亡尺収仁片穴冊処庁幼宇灰危机吸后至存宅我系孝困私否批忘卵乱沿延拡供呼刻若宗垂担宙忠届乳拝並宝枚律映革看巻皇紅砂姿城専宣染泉洗奏段派肺背株胸降骨座蚕射従純除将針値展党討納俳班秘陛朗異域郷済視捨推盛窓探著頂脳閉訪密訳郵翌欲割揮貴筋勤敬裁策詞衆就善装創尊痛晩補棒絹源署傷蒸誠聖暖賃腹幕盟裏閣疑誤穀誌磁障層認暮模遺劇権熟諸蔵誕潮論激憲鋼樹縦操糖奮厳縮優覧簡難臨警臓"

    def parse_grade(s, strokes_from_kanji=None):
        """漢字文字列を(漢字,unicode,画数)のリストに変換"""
        result = []
        for ch in s:
            u = hex(ord(ch))[2:]
            # kanji-dataから画数を取得（後で）
            strokes = strokes_from_kanji.get(ch, 8) if strokes_from_kanji else 8
            result.append((ch, u, strokes))
        return result

    return {
        2: (g2, parse_grade(g2)),
        3: (g3, parse_grade(g3)),
        4: (g4, parse_grade(g4)),
        5: (g5, parse_grade(g5)),
        6: (g6, parse_grade(g6)),
    }

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kanji_data = {}
    kanji_path = "/tmp/kanji.json"
    if os.path.exists(kanji_path):
        try:
            with open(kanji_path, "r", encoding="utf-8") as f:
                kanji_data = json.load(f)
        except Exception as e:
            print(f"kanji.json load error: {e}")

    def get_reading(ch):
        if ch in kanji_data:
            k = kanji_data[ch]
            kun = k.get("readings_kun", [])[:1]
            on = k.get("readings_on", [])[:1]
            kun_clean = [r.split(".")[0].split("-")[0].replace("!","") for r in kun if r and len(r) < 10]
            on_clean = [r for r in on if r and len(r) <= 4]
            parts = kun_clean + on_clean
            return "・".join(parts[:2]) if parts else ch
        return ch

    def get_strokes(ch):
        if ch in kanji_data:
            return kanji_data[ch].get("strokes", 8)
        return 8

    grades_data = load_grade_data()
    for grade, (chars, parsed) in grades_data.items():
        # Update strokes from kanji_data
        kanji_list = [(ch, u, get_strokes(ch)) for ch, u, _ in parsed]
        grade_name = ["", "", "二年生-N4", "三年生-N4", "四年生-N4", "五年生-N3", "六年生-N3"][grade]

        # Build KANJI array
        lines = []
        for ch, u, strokes in kanji_list:
            reading = get_reading(ch)
            lines.append(f"  {{ch:'{ch}',reading:'{reading}',unicode:'{u}',strokes:{strokes}}}")
        kanji_js = ",\n".join(lines)

        dir_path = os.path.join(base_dir, f"{grade}.{grade_name}")
        os.makedirs(dir_path, exist_ok=True)

        html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>漢字（{grade_name}）筆順 学習プリント</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding-bottom: 30px; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; -webkit-touch-callout: none; }}
  h1 {{ margin: 18px 0 8px; font-size: 1.9rem; color: #2e7d32; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }}
  .kanji-grid {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; max-width: 520px; width: 95%; margin: 8px auto; }}
  .kanji-grid .cell {{ background: #fff; border: 2px solid #ddd; border-radius: 8px; text-align: center; font-size: 1.1rem; padding: 5px 0; cursor: pointer; transition: all .2s; user-select: none; }}
  .kanji-grid .cell:hover {{ background: #e8f5e9; transform: scale(1.05); }}
  .kanji-grid .cell.active {{ background: #c8e6c9; border-color: #2e7d32; font-weight: bold; }}
  .mode-tabs {{ display: flex; gap: 4px; margin: 10px 0 6px; }}
  .mode-tab {{ padding: 6px 16px; border: 2px solid #2e7d32; border-radius: 20px; background: #fff; color: #2e7d32; cursor: pointer; font-size: .9rem; font-family: inherit; transition: all .2s; }}
  .mode-tab.active {{ background: #2e7d32; color: #fff; }}
  #learnArea {{ width: 95%; max-width: 900px; margin: 0 auto; }}
  .stroke-section {{ display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; align-items: stretch; margin-bottom: 16px; }}
  .big-char-panel {{ background: #fff; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 16px; text-align: center; width: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  .big-char-panel .reading {{ font-size: 2.2rem; color: #888; margin-bottom: 0; }}
  .big-char-panel .big-char {{ font-size: 10rem; line-height: 1; color: #333; }}
  .big-char-panel .stroke-count {{ font-size: 1rem; color: #2e7d32; margin-top: 4px; font-weight: bold; }}
  .stroke-order-panel {{ background: #fff; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 16px; text-align: center; flex: 1; min-width: 300px; max-width: 580px; }}
  .stroke-order-panel h2 {{ font-size: 1.05rem; color: #555; margin-bottom: 8px; }}
  .nazorigaki-img-wrap {{ margin: 8px auto; border: 2px solid #ccc; border-radius: 10px; overflow: hidden; background: #fafafa; position: relative; cursor: crosshair; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; -webkit-touch-callout: none; }}
  .nazorigaki-img-wrap img {{ display: block; width: 100%; height: auto; max-width: 100%; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; -webkit-touch-callout: none; pointer-events: none; }}
  .nazorigaki-img-wrap canvas {{ position: absolute; top: 0; left: 0; pointer-events: auto; touch-action: none; }}
  .btn-clear {{ background: #f44336; color: #fff; margin-top: 8px; }}
  .btn-clear:hover {{ background: #c62828; }}
  .btn-row {{ display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 8px; }}
  .btn {{ padding: 7px 16px; border: none; border-radius: 8px; font-size: .95rem; cursor: pointer; transition: all .2s; font-family: inherit; }}
  .btn-prev {{ background: #2196f3; color: #fff; }}
  .btn-prev:hover {{ background: #1565c0; }}
  .btn-next {{ background: #2e7d32; color: #fff; }}
  .btn-next:hover {{ background: #1b5e20; }}
  .quiz-panel {{ background: #fff; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 20px; text-align: center; width: 95%; max-width: 500px; display: none; }}
  .quiz-panel h2 {{ font-size: 1.3rem; color: #555; margin-bottom: 12px; }}
  .quiz-question {{ font-size: 5rem; color: #333; margin: 10px 0; }}
  .quiz-choices {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 16px auto; max-width: 360px; }}
  .quiz-choice {{ padding: 14px; border: 2px solid #ddd; border-radius: 12px; font-size: 1.2rem; cursor: pointer; transition: all .2s; background: #fafafa; font-family: inherit; }}
  .quiz-choice:hover {{ border-color: #2e7d32; background: #e8f5e9; }}
  .quiz-choice.correct {{ background: #c8e6c9; border-color: #4caf50; }}
  .quiz-choice.wrong {{ background: #ffcdd2; border-color: #f44336; }}
  .quiz-score {{ font-size: 1.1rem; color: #666; margin: 10px 0; }}
  .quiz-feedback {{ font-size: 1.2rem; min-height: 1.5em; margin: 8px 0; }}
  footer {{ margin: 20px 0; color: #999; font-size: .8rem; }}
  @media (max-width: 640px) {{ .kanji-grid {{ grid-template-columns: repeat(8, 1fr); }} .stroke-section {{ flex-direction: column; align-items: center; }} .big-char-panel {{ width: 95%; }} .stroke-order-panel {{ min-width: auto; width: 95%; }} }}
</style>
</head>
<body>
<h1>漢字（{grade_name}）</h1>
<div class="mode-tabs">
  <button class="mode-tab active" onclick="setMode('learn')">学習モード</button>
  <button class="mode-tab" onclick="setMode('quiz')">クイズモード</button>
</div>
<div class="kanji-grid" id="kanjiGrid"></div>
<div id="learnArea">
  <div class="stroke-section">
    <div class="big-char-panel">
      <p class="reading" id="readingDisplay">-</p>
      <p class="big-char" id="charDisplay">-</p>
      <p class="stroke-count" id="strokeCount">-画</p>
      <div class="btn-row" style="margin-top:10px;">
        <button class="btn btn-prev" onclick="prevChar()">◀ 前</button>
        <button class="btn btn-next" onclick="nextChar()">次 ▶</button>
      </div>
    </div>
    <div class="stroke-order-panel">
      <h2>ひつじゅん・れんしゅう（なぞりがき）</h2>
      <p style="font-size:.85rem;color:#777;margin-bottom:8px;">© <a href="https://kakijun.com/" target="_blank" rel="noopener">漢字書き順辞典</a> 筆順画像を使用</p>
      <div class="nazorigaki-img-wrap" id="nazorigakiWrap">
        <img id="nazorigakiImg" src="" alt="ひつじゅん・れんしゅう" draggable="false" />
        <canvas id="nazorigakiCanvas"></canvas>
      </div>
      <div class="btn-row">
        <button class="btn btn-clear" onclick="clearNazorigakiCanvas()">けす</button>
      </div>
    </div>
  </div>
</div>
<div class="quiz-panel" id="quizArea">
  <h2>漢字（{grade_name}）クイズ</h2>
  <p class="quiz-score" id="quizScore">正解: 0 / 0</p>
  <p class="quiz-question" id="quizQuestion">-</p>
  <p class="quiz-feedback" id="quizFeedback">&nbsp;</p>
  <div class="quiz-choices" id="quizChoices"></div>
  <div class="btn-row" style="margin-top:14px;">
    <button class="btn btn-next" id="btnNextQuiz" onclick="nextQuiz()" style="display:none;">次の問題 ▶</button>
  </div>
</div>
<footer>漢字（{grade_name}） 学習プリント ― © <a href="https://kakijun.com/" target="_blank" rel="noopener" style="color:#999;">漢字書き順辞典</a></footer>
<script>
const KANJI = [
{kanji_js}
];
let currentIndex = 0; let mode = 'learn'; let quizCorrect = 0, quizTotal = 0, quizAnswered = false;
const KAKIJUN_BASE = 'https://kakijun.com/kanjiphoto/worksheet/1/kanji-kakijun-worksheet-1-';
function buildGrid() {{ const grid = document.getElementById('kanjiGrid'); grid.innerHTML = ''; KANJI.forEach((k, i) => {{ const div = document.createElement('div'); div.className = 'cell'; div.textContent = k.ch; div.onclick = () => {{ currentIndex = i; updateDisplay(); }}; grid.appendChild(div); }}); }}
function highlightGrid() {{ const ch = KANJI[currentIndex].ch; document.querySelectorAll('.kanji-grid .cell').forEach((c, i) => {{ c.classList.toggle('active', KANJI[i].ch === ch); }}); }}
function updateDisplay() {{ const k = KANJI[currentIndex]; document.getElementById('charDisplay').textContent = k.ch; document.getElementById('readingDisplay').textContent = k.reading; document.getElementById('strokeCount').textContent = k.strokes + '画'; highlightGrid(); const img = document.getElementById('nazorigakiImg'); img.src = KAKIJUN_BASE + k.unicode + '.png'; img.alt = k.ch + ' の書き順'; clearNazorigakiCanvas(); if (img.complete && img.naturalWidth) resizeNazorigakiCanvas(); }}
function resizeNazorigakiCanvas() {{ const canvas = document.getElementById('nazorigakiCanvas'); const wrap = document.getElementById('nazorigakiWrap'); const rect = wrap.getBoundingClientRect(); if (rect.width < 10 || rect.height < 10) return; const dpr = window.devicePixelRatio || 1; const w = Math.round(rect.width * dpr); const h = Math.round(rect.height * dpr); if (canvas.width !== w || canvas.height !== h) {{ canvas.width = w; canvas.height = h; canvas.style.width = rect.width + 'px'; canvas.style.height = rect.height + 'px'; }} }}
function clearNazorigakiCanvas() {{ const canvas = document.getElementById('nazorigakiCanvas'); const ctx = canvas.getContext('2d'); ctx.clearRect(0, 0, canvas.width, canvas.height); }}
function setupNazorigakiDrawing() {{ const canvas = document.getElementById('nazorigakiCanvas'); const ctx = canvas.getContext('2d'); let drawing = false; canvas.addEventListener('touchstart', e => e.preventDefault(), {{ passive: false }}); canvas.addEventListener('pointerdown', e => {{ drawing = true; ctx.beginPath(); const r = canvas.getBoundingClientRect(); ctx.moveTo((e.clientX-r.left)*canvas.width/r.width, (e.clientY-r.top)*canvas.height/r.height); canvas.setPointerCapture(e.pointerId); }}); canvas.addEventListener('pointermove', e => {{ if (!drawing) return; const r = canvas.getBoundingClientRect(); ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#333'; ctx.lineTo((e.clientX-r.left)*canvas.width/r.width, (e.clientY-r.top)*canvas.height/r.height); ctx.stroke(); }}); canvas.addEventListener('pointerup', () => drawing = false); canvas.addEventListener('pointerleave', () => drawing = false); }}
function initNazorigakiCanvas() {{ const img = document.getElementById('nazorigakiImg'); const wrap = document.getElementById('nazorigakiWrap'); wrap.addEventListener('contextmenu', e => e.preventDefault()); function syncCanvas() {{ resizeNazorigakiCanvas(); }} img.addEventListener('load', syncCanvas); window.addEventListener('resize', syncCanvas); new ResizeObserver(syncCanvas).observe(wrap); syncCanvas(); setupNazorigakiDrawing(); }}
function prevChar() {{ currentIndex = (currentIndex - 1 + KANJI.length) % KANJI.length; updateDisplay(); }}
function nextChar() {{ currentIndex = (currentIndex + 1) % KANJI.length; updateDisplay(); }}
function setMode(m) {{ mode = m; document.querySelectorAll('.mode-tab').forEach(t => t.classList.toggle('active', t.textContent.includes(m==='learn'?'学習':'クイズ'))); document.getElementById('learnArea').style.display = m==='learn' ? 'block' : 'none'; document.getElementById('quizArea').style.display = m==='quiz' ? 'block' : 'none'; if (m==='quiz') {{ quizCorrect=0; quizTotal=0; nextQuiz(); }} }}
function nextQuiz() {{ quizAnswered = false; document.getElementById('quizFeedback').innerHTML = '&nbsp;'; document.getElementById('btnNextQuiz').style.display = 'none'; const qi = Math.floor(Math.random()*KANJI.length); const {{ch, reading}} = KANJI[qi]; const mainReading = reading.split('・')[0]; const type = Math.random() < 0.5 ? 'k2r' : 'r2k'; let question, answer, pool; if (type==='k2r') {{ question = ch; answer = mainReading; pool = KANJI.map(k => k.reading.split('・')[0]); }} else {{ question = mainReading; answer = ch; pool = KANJI.map(k => k.ch); }} const choices = genChoices(answer, pool); document.getElementById('quizQuestion').textContent = question; document.getElementById('quizScore').textContent = `正解: ${{quizCorrect}} / ${{quizTotal}}`; const div = document.getElementById('quizChoices'); div.innerHTML = ''; choices.forEach(c => {{ const btn = document.createElement('button'); btn.className = 'quiz-choice'; btn.textContent = c; btn.onclick = () => checkAnswer(btn, c, answer); div.appendChild(btn); }}); }}
function genChoices(correct, pool) {{ const s = new Set([correct]); while (s.size < 4) s.add(pool[Math.floor(Math.random()*pool.length)]); return shuffle([...s]); }}
function shuffle(a) {{ for (let i=a.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]; }} return a; }}
function checkAnswer(btn, sel, cor) {{ if (quizAnswered) return; quizAnswered = true; quizTotal++; if (sel===cor) {{ quizCorrect++; btn.classList.add('correct'); document.getElementById('quizFeedback').textContent='⭕ 正解！'; document.getElementById('quizFeedback').style.color='#4caf50'; }} else {{ btn.classList.add('wrong'); document.getElementById('quizFeedback').textContent=`❌ 不正解… 正解は「${{cor}}」`; document.getElementById('quizFeedback').style.color='#f44336'; document.querySelectorAll('.quiz-choice').forEach(b=>{{ if(b.textContent===cor) b.classList.add('correct'); }}); }} document.getElementById('quizScore').textContent=`正解: ${{quizCorrect}} / ${{quizTotal}}`; document.getElementById('btnNextQuiz').style.display='inline-block'; }}
document.addEventListener('keydown', e => {{ if (mode==='learn') {{ if (e.key==='ArrowLeft') prevChar(); else if (e.key==='ArrowRight') nextChar(); }} }});
buildGrid(); updateDisplay(); initNazorigakiCanvas();
</script>
</body>
</html>'''

        out_path = os.path.join(dir_path, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created: {out_path} ({len(kanji_list)} kanji)")

if __name__ == "__main__":
    main()
