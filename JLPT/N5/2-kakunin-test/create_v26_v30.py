#!/usr/bin/env python3
"""N5確認テスト v26-v30 作成（既存v1-v25と重複なし）"""
import re
import random

# テンプレート（v25ベース）
TEMPLATE = open("n5-10min-test-v25.html", encoding="utf-8").read()

# v26-v30 の全問題（既存と重複しないよう新規作成）
TESTS = {
    26: {
        "q1": ('まいにち　<strong>新聞</strong>を　よみます。', [("しんぶん",1),("しんぶん",0),("しんぷん",0),("じんぶん",0)], "しんぶん"),
        "q2": ('きょう　<strong>雑誌</strong>を　かいました。', [("ざっし",1),("ざし",0),("ざつし",0),("ざしゅ",0)], "ざっし"),
        "q3": ('まいにち　<strong>りょうり</strong>を　します。', [("料里",0),("料理",1),("料利",0),("料裡",0)], "料理"),
        "q4": ('らいねん　にほん（　）　りょこうに　いきます。', [("を",0),("で",0),("へ",1),("が",0)], "へ"),
        "q5": ('この　ほんは　（　）から、おもしろいです。', [("ながい",0),("あたらしい",0),("むずかしい",0),("たのしい",1)], "たのしい"),
        "q6": ('この　コーヒーは　<strong>あまい</strong>です。', [
            ("この　コーヒーは　しょっぱくないです。",0),
            ("この　コーヒーは　にがいです。",0),
            ("この　コーヒーは　さとうが　たくさん　はいっています。",1),
            ("この　コーヒーは　つめたいです。",0)
        ], "さとうがたくさん"),
        "q7": ('なん（　）　がっこうに　いきますか。', [("を",0),("が",0),("に",0),("で",1)], "で"),
        "q8": ('まいしゅう　なんようび（　）　やすみますか。', [("を",0),("が",0),("に",1),("で",0)], "に"),
        "q9": ('わたしは　＿＿　＿＿　★　＿＿　かきます。', [
            ("まいにち",0),("よる",0),("にっきを",1),("へやで",0)
        ], "にっきを", "わたしは　まいにち　よる　★にっきを　へやで　かきます。"),
        "q10_passage": "わたしの ともだちは やまださんです。やまださんは だいがくの がくせいです。まいにち じてんしゃで だいがくに いきます。にほんごの べんきょうが すきです。",
        "q10": ("やまださんは なんの べんきょうが すきですか。", [("えいご",0),("にほんご",1),("すうがく",0),("れきし",0)], "にほんご"),
    },
    27: {
        "q1": ('あした　<strong>旅行</strong>に　いきます。', [("りょこう",1),("たびこう",0),("りょこ",0),("りょうこう",0)], "りょこう"),
        "q2": ('この　<strong>部屋</strong>は　ひろいです。', [("へや",1),("ぶや",0),("へおや",0),("べや",0)], "へや"),
        "q3": ('まいにち　<strong>しんぶん</strong>を　よみます。', [("新文",0),("新聞",1),("申聞",0),("新聞",0)], "新聞"),
        "q4": ('きのう　スーパー（　）　くだものを　かいました。', [("を",0),("で",1),("へ",0),("が",0)], "で"),
        "q5": ('わたしは　コーヒー（　）　きらいです。', [("を",0),("が",1),("に",0),("で",0)], "が"),
        "q6": ('この　へやは　<strong>くらい</strong>です。', [
            ("この　へやは　あかるいです。",0),
            ("この　へやは　あたたかいです。",0),
            ("この　へやは　あかるくないです。",1),
            ("この　へやは　ひろいです。",0)
        ], "あかるくない"),
        "q7": ('へや（　）　エアコンが　あります。', [("を",0),("に",1),("で",0),("が",0)], "に"),
        "q8": ('だれ（　）　にほんごを　おしえますか。', [("を",0),("が",0),("に",1),("で",0)], "に"),
        "q9": ('わたしは　＿＿　＿＿　★　＿＿　いきました。', [
            ("きのう",0),("バスで",1),("えきに",0),("3じに",0)
        ], "バスで", "わたしは　きのう　3じに　★バスで　えきに　いきました。"),
        "q10_passage": "すずきさんは かいしゃいんです。まいにち 7じに おきます。8じに いえを でます。でんしゃで かいしゃに いきます。1じかん かかります。",
        "q10": ("すずきさんは なんじに おきますか。", [("6じ",0),("7じ",1),("8じ",0),("9じ",0)], "7じ"),
    },
    28: {
        "q1": ('まいにち　<strong>料理</strong>を　つくります。', [("りょうり",1),("りょり",0),("りょうい",0),("りょうり",0)], "りょうり"),
        "q2": ('あの　<strong>建物</strong>は　びょういんです。', [("たてもの",1),("けんぶつ",0),("たてぶつ",0),("けんもの",0)], "たてもの"),
        "q3": ('きょう　<strong>てんき</strong>が　いいです。', [("天気",1),("転機",0),("電気",0),("天機",0)], "天気"),
        "q4": ('まいにち　パン（　）　あさごはんを　たべます。', [("を",0),("が",0),("に",0),("と",1)], "と"),
        "q5": ('つくえの　上（　）　ペンが　あります。', [("を",0),("で",0),("に",1),("が",0)], "に"),
        "q6": ('この　りょうりは　<strong>からい</strong>です。', [
            ("この　りょうりは　あまいです。",0),
            ("この　りょうりは　しおが　たくさん　はいっています。",1),
            ("この　りょうりは　つめたいです。",0),
            ("この　りょうりは　あついです。",0)
        ], "しおがたくさん"),
        "q7": ('きのう　ともだち（　）　えいがを　みました。', [("を",0),("が",0),("と",1),("で",0)], "と"),
        "q8": ('まいあさ　なに（　）　たべますか。', [("が",0),("を",1),("に",0),("で",0)], "を"),
        "q9": ('わたしは　＿＿　＿＿　★　＿＿　かえります。', [
            ("まいにち",0),("6じに",0),("バスで",1),("いえに",0)
        ], "バスで", "わたしは　まいにち　6じに　★バスで　いえに　かえります。"),
        "q10_passage": "たなかさんは まいあさ 6じに おきます。7じに あさごはんを たべます。8じに いえを でます。じてんしゃで がっこうに いきます。20ぷん かかります。",
        "q10": ("たなかさんは なんの のりもので がっこうに いきますか。", [("バス",0),("でんしゃ",0),("じてんしゃ",1),("あるいて",0)], "じてんしゃ"),
    },
    29: {
        "q1": ('きょう　<strong>洗濯</strong>を　します。', [("せんたく",1),("あらたく",0),("せんだく",0),("せんたき",0)], "せんたく"),
        "q2": ('まいにち　<strong>自転車</strong>で　がっこうに　いきます。', [("じてんしゃ",1),("じでんしゃ",0),("じてんちゃ",0),("じでんちゃ",0)], "じてんしゃ"),
        "q3": ('まいにち　<strong>しょくじ</strong>を　します。', [("食時",0),("食事",1),("食自",0),("食事",0)], "食事"),
        "q4": ('にちようび　うみ（　）　およぎます。', [("を",0),("で",1),("へ",0),("が",0)], "で"),
        "q5": ('この　みかんは　（　）です。', [("あおい",0),("あかい",0),("きいろい",0),("あまい",1)], "あまい"),
        "q6": ('この　ほんは　<strong>むずかしい</strong>です。', [
            ("この　ほんは　やさしいです。",0),
            ("この　ほんは　かんたんです。",0),
            ("この　ほんは　わかりにくいです。",1),
            ("この　ほんは　おもしろいです。",0)
        ], "わかりにくい"),
        "q7": ('らいしゅう　とうきょう（　）　いきます。', [("を",0),("で",0),("へ",1),("が",0)], "へ"),
        "q8": ('なんじ（　）　しごとが　はじまりますか。', [("を",0),("が",0),("に",1),("で",0)], "に"),
        "q9": ('わたしは　＿＿　＿＿　★　＿＿　たべます。', [
            ("まいにち",0),("12じに",0),("レストランで",1),("ひるごはんを",0)
        ], "レストランで", "わたしは　まいにち　12じに　★レストランで　ひるごはんを　たべます。"),
        "q10_passage": "やまもとさんは にほんの せんせいです。まいにち でんしゃで がっこうに いきます。がっこうで にほんごを おしえます。3じに いえに かえります。",
        "q10": ("やまもとさんは がっこうで なにを おしえますか。", [("えいご",0),("すうがく",0),("にほんご",1),("れきし",0)], "にほんご"),
    },
    30: {
        "q1": ('あの　<strong>喫茶店</strong>で　コーヒーを　のみます。', [("きっさてん",1),("きつさてん",0),("きっさでん",0),("きさてん",0)], "きっさてん"),
        "q2": ('きょう　<strong>宿題</strong>が　あります。', [("しゅくだい",1),("しゅくたい",0),("しゅくだえ",0),("しゅくだい",1)], "しゅくだい"),
        "q3": ('まいにち　<strong>りょこう</strong>の　ほんを　よみます。', [("旅交",0),("旅行",1),("旅行",0),("旅高",0)], "旅行"),
        "q4": ('まいあさ　ミルク（　）　のみます。', [("が",0),("を",1),("に",0),("で",0)], "を"),
        "q5": ('この　かばんは　（　）から、もてません。', [("かるい",0),("おもい",1),("ちいさい",0),("おおきい",0)], "おもい"),
        "q6": ('この　みちは　<strong>せまい</strong>です。', [
            ("この　みちは　ひろいです。",0),
            ("この　みちは　ひろくないです。",1),
            ("この　みちは　ながいです。",0),
            ("この　みちは　みじかいです。",0)
        ], "ひろくない"),
        "q7": ('しゅくだいを　（　）　まえに　べんきょうします。', [("する",0),("して",0),("する",0),("する",0)], "する"),  # するの
        "q7": ('へやに　エアコン（　）　あります。', [("を",0),("が",1),("に",0),("で",0)], "が"),
        "q8": ('いつ（　）　にほんに　きますか。', [("を",0),("が",0),("に",1),("で",0)], "に"),
        "q9": ('わたしは　＿＿　＿＿　★　＿＿　いきます。', [
            ("あした",0),("ともだちと",0),("えいがを",1),("みに",0)
        ], "えいがを", "わたしは　あした　ともだちと　★えいがを　みに　いきます。"),
        "q10_passage": "こんしゅうの にちようび、わたしは ははと デパートへ いきます。ははは ふくが ほしいです。わたしは くつを かいます。それから レストランで ひるごはんを たべます。",
        "q10": ("わたしは デパートで なにを かいますか。", [("ふく",0),("くつ",1),("ひるごはん",0),("かばん",0)], "くつ"),
    },
}

# v30のq7を修正（重複していた）
TESTS[30]["q7"] = ('へやに　エアコン（　）　あります。', [("を",0),("が",1),("に",0),("で",0)], "が")

def shuffle_options(opts, correct_idx):
    """正解位置をランダムに"""
    correct = opts[correct_idx]
    wrongs = [o for i,o in enumerate(opts) if i!=correct_idx]
    pos = random.randint(0, 3)
    new_opts = wrongs[:pos] + [correct] + wrongs[pos:]
    new_correct_idx = pos
    return new_opts, new_correct_idx + 1

def build_options_html(opts, qnum, correct_pos):
    ids = ['a','b','c','d']
    html = ""
    for i, (text, _) in enumerate(opts):
        val = "1" if i+1 == correct_pos else "0"
        html += f'<div class="option"><input type="radio" name="q{qnum}" id="q{qnum}{ids[i]}" value="{val}"><label for="q{qnum}{ids[i]}">{i+1}. {text}</label></div>\n'
    return html

def create_test(version):
    random.seed(version)
    data = TESTS[version]
    
    content = TEMPLATE
    content = content.replace("確認テスト25", f"確認テスト{version}")
    content = content.replace("テスト25", f"テスト{version}")
    
    # Q1
    opts, pos = shuffle_options(data["q1"][1], 0)
    content = re.sub(
        r'(<span class="q-num">1</span>)[^<]+</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>',
        f'\\1{data["q1"][0]}</div>\n<div class="options">\n{build_options_html(opts, 1, pos)}</div>\n<div class="explanation">✅ 正解：{pos}.  {data["q1"][2]} — 「{data["q1"][0].split("strong>")[1].split("<")[0]}」は「{data["q1"][2]}」と読みます。</div>',
        content, count=1, flags=re.DOTALL
    )
    
    # Q2
    opts, pos = shuffle_options(data["q2"][1], 0)
    content = re.sub(
        r'(<span class="q-num">2</span>)[^<]+</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>',
        f'\\1{data["q2"][0]}</div>\n<div class="options">\n{build_options_html(opts, 2, pos)}</div>\n<div class="explanation">✅ 正解：{pos}.  {data["q2"][2]} — 「{data["q2"][0].split("strong>")[1].split("<")[0]}」は「{data["q2"][2]}」と読みます。</div>',
        content, count=1, flags=re.DOTALL
    )
    
    # Q3
    opts, pos = shuffle_options(data["q3"][1], 1)
    content = re.sub(
        r'(<span class="q-num">3</span>)[^<]+</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>',
        f'\\1{data["q3"][0]}</div>\n<div class="options">\n{build_options_html(opts, 3, pos)}</div>\n<div class="explanation">✅ 正解：{pos}.  {data["q3"][2]} — 「{data["q3"][0].split("strong>")[1].split("<")[0]}」は「{data["q3"][2]}」と書きます。</div>',
        content, count=1, flags=re.DOTALL
    )
    
    # Q4-Q5, Q7-Q8
    for q, key in [(4,"q4"),(5,"q5"),(7,"q7"),(8,"q8")]:
        d = data[key]
        correct_idx = next(i for i,(_,v) in enumerate(d[1]) if v==1)
        opts, pos = shuffle_options(d[1], correct_idx)
        old = re.search(rf'<span class="q-num">{q}</span>.*?</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>', content, re.DOTALL)
        if old:
            expl = f'✅ 正解：{pos}. {d[2]} — '
            if "で" in d[2]: expl += "動作の場所には「で」を使います。"
            elif "へ" in d[2]: expl += "方向を表す「へ」を使います。"
            elif "に" in d[2]: expl += "時・相手・場所を表す「に」を使います。"
            elif "を" in d[2]: expl += "対象を表す「を」を使います。"
            elif "が" in d[2]: expl += "存在の主体を表す「が」を使います。"
            elif "と" in d[2]: expl += "一緒に行動する相手を表す「と」を使います。"
            else: expl += "文脈に合う助詞です。"
            new = f'<span class="q-num">{q}</span>{d[0]}</div>\n<div class="options">\n{build_options_html(opts, q, pos)}</div>\n<div class="explanation">{expl}</div>'
            content = content.replace(old.group(0), new, 1)
    
    # Q6
    d = data["q6"]
    correct_idx = next(i for i,(_,v) in enumerate(d[1]) if v==1)
    opts, pos = shuffle_options(d[1], correct_idx)
    old = re.search(r'<span class="q-num">6</span>.*?</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>', content, re.DOTALL)
    if old:
        new = f'<span class="q-num">6</span>{d[0]}</div>\n<div class="options">\n{build_options_html(opts, 6, pos)}</div>\n<div class="explanation">✅ 正解：{pos} — 類義表現です。</div>'
        content = content.replace(old.group(0), new, 1)
    
    # Q9
    d = data["q9"]
    correct_idx = next(i for i,(_,v) in enumerate(d[1]) if v==1)
    opts, pos = shuffle_options(d[1], correct_idx)
    old = re.search(r'<span class="q-num">9</span>.*?</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>', content, re.DOTALL)
    if old:
        new = f'<span class="q-num">9</span>わたしは　＿＿　＿＿　★　＿＿　{"かきます。" if "かきます" in d[3] else "いきました。" if "いきました" in d[3] else "かえります。" if "かえります" in d[3] else "たべます。" if "たべます" in d[3] else "のみます。"}</div>\n<div class="options">\n{build_options_html(opts, 9, pos)}</div>\n<div class="explanation">✅ 正解：{pos}.  {d[2]} — 「{d[3]}」4つ全て使用。</div>'
        content = content.replace(old.group(0), new, 1)
    
    # Q10
    passage = data["q10_passage"]
    d = data["q10"]
    correct_idx = next(i for i,(_,v) in enumerate(d[1]) if v==1)
    opts, pos = shuffle_options(d[1], correct_idx)
    content = re.sub(
        r'<div class="reading-passage">.*?</div>',
        f'<div class="reading-passage">\n{passage}\n</div>',
        content, count=1, flags=re.DOTALL
    )
    old = re.search(r'<span class="q-num">10</span>.*?</div>\s*<div class="options">.*?</div>\s*<div class="explanation">.*?</div>', content, re.DOTALL)
    if old:
        new = f'<span class="q-num">10</span>{d[0]}</div>\n<div class="options">\n{build_options_html(opts, 10, pos)}</div>\n<div class="explanation">✅ 正解：{pos} — 本文にあります。</div>'
        content = content.replace(old.group(0), new, 1)
    
    with open(f"n5-10min-test-v{version}.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created n5-10min-test-v{version}.html")

if __name__ == "__main__":
    for v in range(26, 31):
        create_test(v)
