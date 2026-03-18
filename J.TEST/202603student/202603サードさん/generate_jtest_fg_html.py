#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""J.TEST F-G 20260308サードさん用 HTMLテスト生成スクリプト"""

# 解答: 1-indexed
ANSWERS = {
    1:3, 2:2, 3:1, 4:4, 5:1, 6:2, 7:1, 8:3, 9:4, 10:4,
    11:3, 12:2, 13:4, 14:1, 15:2, 16:3, 17:1, 18:4, 19:3, 20:2,
    21:1, 22:4, 23:2, 24:1, 25:3,
    26:3, 27:2, 28:4, 29:2, 30:1, 31:3, 32:4, 33:2, 34:3, 35:1,
    36:2, 37:3, 38:1, 39:4, 40:2,
    41:4, 42:2, 43:6, 44:3, 45:1,
    46:6, 47:1, 48:5, 49:2, 50:3,
}

def opt_val(q_num, opt_idx):
    return '1' if ANSWERS.get(q_num) == opt_idx else '0'

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def escape_passage(s):
    """Passage用：rubyタグを保持したままエスケープ"""
    s = s.replace('<ruby>', '\uE001').replace('</ruby>', '\uE002').replace('<rt>', '\uE003').replace('</rt>', '\uE004')
    s = escape(s)
    s = s.replace('\uE001', '<ruby>').replace('\uE002', '</ruby>').replace('\uE003', '<rt>').replace('\uE004', '</rt>')
    return s

# 文法・語彙A (1-10)
QUESTIONS_A = [
    ('（<ruby>電話<rt>でんわ</rt></ruby>で）<br>ラオ：「チンさん、どこにいますか。まっていますよ」<br>チン：「ちかくです。すぐ（　　）へ行きます」', ['こんな', 'あそこ', 'そちら', 'あれ'], '指示語の問題。話し相手のいる方向・場所には「そちら」を使う。'),
    ('A：「これは、（　　）ですか」<br>B：「500円です」', ['なぜ', 'いくら', 'いつ', 'いくつ'], '値段を聞く「いくら」が正解。'),
    ('つぎでバス（　　）おります。', ['を', 'や', 'へ', 'か'], '「〜をおりる」は乗り物を降りる決まった表現。'),
    ('それとおなじかばん（　　）ほしいです。', ['で', 'に', 'と', 'が'], '「〜がほしい」の形で欲しいものを表す。'),
    ('ここで<ruby>電話<rt>でんわ</rt></ruby>を（　　）ください。', ['しないで', 'しなくて', 'する', 'すると'], '「〜ないでください」は禁止表現。'),
    ('きょねんのなつは、（　　）です。', ['あついのも', 'あつかった', 'あつくは', 'あつくて'], '過去の話なので形容詞の過去形「あつかった」。'),
    ('このぼうしは、3,000円ですが、あのくろい（　　）、2,000円です。', ['のは', 'のを', 'とは', 'とも'], '「の」は名詞の代わり。「あのくろいの」＝あの黒い帽子。'),
    ('あの<ruby>店<rt>みせ</rt></ruby>は、りんご（　　）みかんを<ruby>売<rt>う</rt></ruby>っています。', ['しか', 'も', 'や', 'だけ'], '「AやB」は例示の並列。'),
    ('ユンさんは、にくが（　　）から、<ruby>食<rt>た</rt></ruby>べないでしょう。', ['きらい', 'きらいで', 'きらいに', 'きらいだ'], '「〜から」の前は普通形。「きらいだ」が正解。'),
    ('テレビを（　　）ながら、ごはんを<ruby>食<rt>た</rt></ruby>べました。', ['見る', '見た', '見て', '見'], '「〜ながら」は動詞の語幹に接続。見ます→見。'),
]

# 文法・語彙B (11-20)
QUESTIONS_B = [
    ('きょうは、ふつかです。あしたは、（　　）です。', ['いつか', 'むいか', 'みっか', 'はつか'], 'ふつか（2日）の次はみっか（3日）。'),
    ('このかみを5（　　）コピーします。', ['にん', 'まい', 'ひき', 'ほん'], '紙は「まい」で数える。'),
    ('○○さんは、あのびょういんの（　　）です。', ['はこ', 'えいが', 'かびん', 'かんごし'], '病院で働く人は看護師。'),
    ('とても（　　）<ruby>本<rt>ほん</rt></ruby>を<ruby>読<rt>よ</rt></ruby>みました。', ['むずかしい', 'からい', 'うるさい', 'わかい'], '本を修飾できるのは「むずかしい」。'),
    ('わたしは、（　　）ラーメンが、すきです。', ['すずしい', 'からい', 'おもい', 'ひくい'], 'ラーメンの味に使うのは「からい」。'),
    ('つぎの<ruby>旅行<rt>りょこう</rt></ruby>は、（　　）ところへ行きたいです。', ['げんきな', 'じょうぶな', 'しずかな', 'ひまな'], '場所に使うのは「しずかな」。'),
    ('さかなには、（　　）がありません。', ['あし', 'とり', 'うみ', 'ねこ'], '魚には足がない。'),
    ('まち（　　）の<ruby>人<rt>ひと</rt></ruby>が、きのうのニュースの<ruby>話<rt>はなし</rt></ruby>をしています。', ['など', 'たち', 'ごろ', 'じゅう'], '「まちじゅう」＝町全体。'),
    ('（　　）でてがみを<ruby>書<rt>か</rt></ruby>きました。', ['バター', 'スプーン', 'ボールペン', 'セーター'], '手紙を書く道具はボールペン。'),
    ('<ruby>新<rt>あたら</rt></ruby>しいくつしたを（　　）。', ['はれます', 'はきます', 'のぼります', 'あけます'], 'くつしたは「はく」で身に着ける。'),
]

# 文法・語彙C (21-25)
QUESTIONS_C = [
    ('<strong>ひとつき</strong>まえに、ここへ来ました。', ['いっかげつ', 'いちねん', 'にかげつ', 'にねん'], '「ひとつき」＝「いっかげつ」＝1ヶ月。'),
    ('そこは、<strong>トイレ</strong>です。', ['かいだん', 'ろうか', 'げんかん', 'おてあらい'], '「トイレ」の日本語表現は「おてあらい」。'),
    ('<strong>すこしだけ</strong><ruby>休<rt>やす</rt></ruby>みましょう。', ['ゆっくり', 'ちょっと', 'みんなで', 'もっと'], '「すこしだけ」＝「ちょっと」。'),
    ('このお<ruby>茶<rt>ちゃ</rt></ruby>は、<strong>まずい</strong>です。', ['おいしくない', 'あつくない', 'やすくない', 'あまくない'], '「まずい」＝「おいしくない」。'),
    ('<strong><ruby>佐野<rt>さの</rt></ruby>ともうします</strong>。どうぞよろしく。', ['<ruby>佐野<rt>さの</rt></ruby>さん、はじめまして', '<ruby>佐野<rt>さの</rt></ruby>さんに<ruby>話<rt>はな</rt></ruby>します', 'わたしのなまえは、<ruby>佐野<rt>さの</rt></ruby>です', 'わたしは、<ruby>佐野<rt>さの</rt></ruby>さんの<ruby>友<rt>とも</rt></ruby>だちです'], '「〜ともうします」は自己紹介。「わたしのなまえは佐野です」と同義。'),
]

# 読解 (26-35) - passages and questions
READING_DATA = [
    ('''わたしは、ミゲルです。ことし、メキシコから<ruby>日本<rt>にほん</rt></ruby>へ来ました。<ruby>今<rt>いま</rt></ruby>、<ruby>東京<rt>とうきょう</rt></ruby>のレストランにつとめています。まえは、メキシコのレストランで、メキシコのりょうりをつくっていました。今も、レストランで、メキシコのりょうりをつくっていますが、わたしは、<ruby>日本<rt>にほん</rt></ruby>のりょうりもつくりたいです。おなじレストランで、<ruby>島田<rt>しまだ</rt></ruby>さんは、<ruby>日本<rt>にほん</rt></ruby>のりょうりをつくっています。<ruby>島田<rt>しまだ</rt></ruby>さんは、りょうりがじょうずですから、わたしは、<ruby>島田<rt>しまだ</rt></ruby>さんから、<ruby>日本<rt>にほん</rt></ruby>のりょうりをならっています。''',
     [
         ('「わたし」について、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['ことし、メキシコへ来ました。', '<ruby>今<rt>いま</rt></ruby>、しごとをしていません。', 'しごとで、メキシコのりょうりをつくっています。', '<ruby>東京<rt>とうきょう</rt></ruby>のレストランへ行きたいと、おもっています。'], '本文「今も、レストランで、メキシコのりょうりをつくっています」と一致。'),
         ('<ruby>島田<rt>しまだ</rt></ruby>さんについて、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['ミゲルさんといっしょにメキシコのりょうりをつくっています。', 'ミゲルさんに、<ruby>日本<rt>にほん</rt></ruby>のりょうりをおしえています。', 'メキシコのレストランで、ミゲルさんに会いました。', 'りょうりは、ミゲルさんよりへたです。'], '「島田さんから、日本のりょうりをならっています」＝島田さんが教えている。'),
     ]),
    ('''クミさんは、だいがくせいで、こんげつ、19さいになりました。クミさんの<ruby>大学<rt>だいがく</rt></ruby>に、<ruby>女<rt>おんな</rt></ruby>のがくせいのサッカーのチームがあります。とてもつよいチームです。クミさんは、そのチームに入って、サッカーをしています。
ケンさんは、クミさんのおとうとです。17さいです。スポーツは、あまりすきではありません。でも、おんがくがすきで、ピアノとバイオリンがじょうずです。ケンさんは、<ruby>来年<rt>らいねん</rt></ruby>、イタリアへ行きたいとおもっています。イタリア<ruby>人<rt>じん</rt></ruby>のせんせいに、おんがくをならいたいからです。''',
     [
         ('クミさんについて、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['もうすぐ、19さいのたんじょうびです。', 'ケンさんの、いもうとです。', '<ruby>男<rt>おとこ</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>たちとサッカーをしています。', '<ruby>大学<rt>だいがく</rt></ruby>でサッカーをしています。'], '「そのチームに入って、サッカーをしています」→大学でサッカー。'),
         ('ケンさんについて、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['いろいろなスポーツがすきです。', 'ピアノがじょうずです。', '<ruby>今<rt>いま</rt></ruby>、イタリアにいます。', '<ruby>大学<rt>だいがく</rt></ruby>で、おんがくの<ruby>勉強<rt>べんきょう</rt></ruby>をしています。'], '「ピアノとバイオリンがじょうずです」と一致。'),
     ]),
    ('''ノエルさんのメモ　あした（3/19） すること

<ruby>午前<rt>ごぜん</rt></ruby> 7:05        いえを<ruby>出<rt>で</rt></ruby>ます。
    7:10〜7:40   <ruby>駅<rt>えき</rt></ruby>のまえのきっさ<ruby>店<rt>てん</rt></ruby>であさごはんを<ruby>食<rt>た</rt></ruby>べます。
    7:45〜10:55  <ruby>電車<rt>でんしゃ</rt></ruby>としんかんせんで、<ruby>京都<rt>きょうと</rt></ruby>へ行きます。
   11:05〜11:55  <ruby>京都<rt>きょうと</rt></ruby><ruby>駅<rt>えき</rt></ruby>のちかくのレストランでひるごはんを<ruby>食<rt>た</rt></ruby>べます。
<ruby>午後<rt>ごご</rt></ruby>12:00〜12:55 ちかてつで、<ruby>森<rt>もり</rt></ruby>さんの<ruby>会社<rt>かいしゃ</rt></ruby>へ行きます。
    1:00〜3:30   <ruby>森<rt>もり</rt></ruby>さんの<ruby>会社<rt>かいしゃ</rt></ruby>で、<ruby>森<rt>もり</rt></ruby>さんとしごとの<ruby>話<rt>はなし</rt></ruby>をします。
    3:45〜5:00   きっさ<ruby>店<rt>てん</rt></ruby>で、じぶんの<ruby>会社<rt>かいしゃ</rt></ruby>にメールをします。
    5:30〜6:00   <ruby>京都<rt>きょうと</rt></ruby>のホテルへ行きます。
    6:30〜       ホテルでばんごはんを<ruby>食<rt>た</rt></ruby>べます。''',
     [
         ('ノエルさんは、ひるごはんのあと、まず<ruby>何<rt>なに</rt></ruby>をしますか。', ['ちかてつにのります。', 'ホテルへ行きます。', 'きっさ<ruby>店<rt>てん</rt></ruby>へ行きます。', '<ruby>森<rt>もり</rt></ruby>さんに会います。'], 'ひるごはんの後12:00〜「ちかてつで、森さんの会社へ」→まずちかてつに乗る。'),
         ('メモとあっているのは、どれですか。', ['いえを<ruby>出<rt>で</rt></ruby>るまえに、あさごはんを<ruby>食<rt>た</rt></ruby>べます。', 'あしたのよるにうちへかえります。', 'しんかんせんは、<ruby>午前<rt>ごぜん</rt></ruby><ruby>中<rt>じゅう</rt></ruby>に<ruby>京都<rt>きょうと</rt></ruby><ruby>駅<rt>えき</rt></ruby>につきます。', '<ruby>京都<rt>きょうと</rt></ruby><ruby>駅<rt>えき</rt></ruby>でしんかんせんにのります。'], '「7:45〜10:55 電車としんかんせんで京都へ」→午前中に京都着。'),
     ]),
    ('''リー→イム：「イムさん、ちかてつでもとまち<ruby>駅<rt>えき</rt></ruby>まで来ました。7ばんの<ruby>出口<rt>でぐち</rt></ruby>はなくなりましたか。6ばんと8ばんは、ありますが、7ばんがどこか、わかりません。」
イム→リー：「リーさん、すみません。『7ばんの<ruby>出口<rt>でぐち</rt></ruby>から<ruby>出<rt>で</rt></ruby>てください』と、わたしが言いましたが、ちがいました。7ばんの<ruby>出口<rt>でぐち</rt></ruby>は、5<ruby>月<rt>がつ</rt></ruby>のおわりまでしまっています。」
リー→イム：「そうですか。では、どこから<ruby>出<rt>で</rt></ruby>ますか。」
イム→リー：「6ばんの<ruby>出口<rt>でぐち</rt></ruby>を<ruby>出<rt>で</rt></ruby>て、50メートルくらいまえへあるいてください。おうだんほどうがありますから、わたってください。わたしたちの<ruby>会社<rt>かいしゃ</rt></ruby>は、そのすぐひだりです。」
リー→イム：「わかりました。すぐ行きます。」
イム→リー：「まっています。」''',
     [
         ('リーさんは、どこにいますか。', ['ちかてつの<ruby>駅<rt>えき</rt></ruby>と<ruby>駅<rt>えき</rt></ruby>の<ruby>間<rt>あいだ</rt></ruby>です。', 'イムさんの<ruby>会社<rt>かいしゃ</rt></ruby>です。', '7ばんの<ruby>出口<rt>でぐち</rt></ruby>の<ruby>外<rt>そと</rt></ruby>です。', 'もとまち<ruby>駅<rt>えき</rt></ruby>です。'], '「ちかてつでもとまち駅まで来ました」→もとまち駅にいる。'),
         ('リーさんは、このあと、まず<ruby>何<rt>なに</rt></ruby>をしますか。', ['もとまち<ruby>駅<rt>えき</rt></ruby>でイムさんをまちます。', '6ばんの<ruby>出口<rt>でぐち</rt></ruby>へ行きます。', 'おうだんほどうをわたります。', 'ちかてつにのります。'], 'イムの指示①6ばんの出口を出る→まず6番出口へ行く。'),
     ]),
    ('''わたしがすんでいるまちに、「まんまるマーケット」というところがありました。「まんまるマーケット」には、「ひろば」とながいたてものがありました。「ひろば」は、荷もたっていないひろいところで、いつもは、みんながすきなところをあるいたり、すきなところであそんだりしていました。でも、ときどき、ゆうめいな<ruby>人<rt>ひと</rt></ruby>が来て、うたをうたったり、おもしろい<ruby>話<rt>はなし</rt></ruby>をしたりしました。「ひろば」のちかくに、ながいたてものがありました。1かいしかないたてものでしたが、ちいさい<ruby>店<rt>みせ</rt></ruby>がたくさん入っていて、どの<ruby>店<rt>みせ</rt></ruby>も、そのすぐまえが「ひろば」でした。
「まんまるマーケット」は、10<ruby>年<rt>ねん</rt></ruby>まえになくなりました。<ruby>今<rt>いま</rt></ruby>は、<ruby>新<rt>あたら</rt></ruby>しいたてものがふたつたちました。ひとつは、おおきいアパートで、もうひとつは、1かいから10かいまでのデパートです。デパートには、まえよりもおおきくて、りっぱな<ruby>店<rt>みせ</rt></ruby>があります。でも、わたしは、あまり行かなくなりました。''',
     [
         ('「まんまるマーケット」について、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['10<ruby>年<rt>ねん</rt></ruby>まえに、できました。', '「ひろば」の<ruby>中<rt>なか</rt></ruby>に<ruby>店<rt>みせ</rt></ruby>がありました。', 'ときどき、ゆうめいな<ruby>人<rt>ひと</rt></ruby>が来ました。', 'ながいたてものの2かいにも<ruby>店<rt>みせ</rt></ruby>がありました。'], '「ときどき、ゆうめいな人が来て、うたをうたったり…」と一致。'),
         ('「わたし」について、<ruby>話<rt>はなし</rt></ruby>とあっているのは、どれですか。', ['「まんまるマーケット」があったまちにすんでいます。', 'よく「まんまるマーケット」で、うたをうたいました。', 'デパートのちかくのアパートにすんでいます。', 'まえは、あまり「まんまるマーケット」へ行きませんでした。'], '「わたしがすんでいるまちに、『まんまるマーケット』というところがありました」→今も同じまちに住んでいる。'),
     ]),
]

# 漢字A (36-40)
KANJI_A = [
    ('グエンさんのたんじょうびは、<strong>にがつ</strong>です。', ['五月', '二月', '四月', '一月'], '「にがつ」＝2月＝二月。'),
    ('ぜんぶで、<strong>ななせんろっぴゃく</strong><ruby>円<rt>えん</rt></ruby>です。', ['七千八百', '七万八千', '七千六百', '七万六千'], 'ななせんろっぴゃく＝7,600＝七千六百円。'),
    ('わたしの<strong>ちち</strong>は、60さいです。', ['父', '生', '先', '母'], '「ちち」＝父。'),
    ('高い<strong>き</strong>があります。', ['長', '天', '空', '木'], '「高い木」＝背の高い木（tree）。'),
    ('このどうぶつは、<strong>みみ</strong>がおおきいです。', ['目', '耳', '足', '手'], '「みみ」＝耳。'),
]

# 漢字B (41-45) - 6 options
KANJI_B = [
    ('<strong>火</strong>ようびに会いましょう。', ['ど', 'もく', 'すい', 'か', 'げつ', 'きん'], '「火」＝か（火曜日）。'),
    ('けさまで<strong>九</strong>時間ねました。', ['よ', 'く', 'に', 'さん', 'ろく', 'しち'], '「九」＝く（九時間）。'),
    ('つくえの<strong>下</strong>に、かばんがあります。', ['みぎ', 'うえ', 'ひだり', 'よこ', 'まえ', 'した'], '「下」＝した。'),
    ('わたしは、この<strong>花</strong>がすきです。', ['とり', 'さかな', 'はな', 'やま', 'ねこ', 'いぬ'], '「花」＝はな。'),
    ('<strong>古い</strong>いえがあります。', ['ふるい', 'あおい', 'しろい', 'おおきい', 'ちいさい', 'くろい'], '「古い」＝ふるい。'),
]

# 短文作成 (46-50) - 6 options
SENTENCE_ORDER = [
    ('きょうは、あさから【1. します　2. しごとを　3. よるまで】。', ['1(1→2→3)', '2(1→3→2)', '3(2→1→3)', '4(2→3→1)', '5(3→1→2)', '6(3→2→1)'], 'よるまで→しごとを→します。あさからよるまでしごとをします。'),
    ('マリーさんは、【1. あおい　2. ぼうしを　3. かぶって】います。', ['1(1→2→3)', '2(1→3→2)', '3(2→1→3)', '4(2→3→1)', '5(3→1→2)', '6(3→2→1)'], 'あおい→ぼうしを→かぶって。あおいぼうしをかぶっています。'),
    ('これからごはんを【1. から　2. てを　3. <ruby>食<rt>た</rt></ruby>べます】あらいましょう。', ['1(1→2→3)', '2(1→3→2)', '3(2→1→3)', '4(2→3→1)', '5(3→1→2)', '6(3→2→1)'], '食べます→から→てを。ごはんを食べますから、てをあらいましょう。'),
    ('バクさんは、【1. うたが　2. こえも　3. じょうずで】きれいです。', ['1(1→2→3)', '2(1→3→2)', '3(2→1→3)', '4(2→3→1)', '5(3→1→2)', '6(3→2→1)'], 'うたが→じょうずで→こえも。うたがじょうずでこえもきれいです。'),
    ('わたしのしごとは、<ruby>高<rt>たか</rt></ruby>いビルのまどの【1. する　2. そうじを　3. こと】です。', ['1(1→2→3)', '2(1→3→2)', '3(2→1→3)', '4(2→3→1)', '5(3→1→2)', '6(3→2→1)'], 'そうじを→する→こと。まどのそうじをすることです。'),
]

def gen_question_html(q_num, q_text, options, explanation, num_opts=4, passage=None):
    ans = ANSWERS[q_num]
    opts_html = []
    for i, opt in enumerate(options, 1):
        v = opt_val(q_num, i)
        lid = f'q{q_num}{chr(96+i)}'
        opts_html.append(f'<div class="option"><input type="radio" name="q{q_num}" id="{lid}" value="{v}"><label for="{lid}">{i}. {escape_passage(opt)}</label></div>')
    passage_div = ''
    if passage:
        passage_div = f'<div class="reading-passage">{escape_passage(passage).replace(chr(10), "<br>")}</div>'
    expl = f'<div class="explanation">✅ 正解：{ans}. {escape_passage(options[ans-1])} — {escape(explanation)}</div>'
    return f'''<div class="question">
{passage_div}
<div class="q-text"><span class="q-num">{q_num}</span>{q_text}</div>
<div class="options">
{chr(10).join(opts_html)}
</div>
{expl}
</div>'''

def main():
    out = []
    out.append('''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>過去問J.TEST F-G 2026年3月度（60分・50問）</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(102,126,234,0.4)}
header h1{font-size:1.5em;margin-bottom:4px}
.header-info{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}
.timer.warning{color:#ffd700;animation:pulse 1s infinite}
.timer.danger{color:#ff4757;animation:pulse .5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}
.score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}
.section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-title{font-size:1.1em;font-weight:bold;color:#667eea;border-left:4px solid #667eea;padding-left:12px;margin-bottom:16px}
.question{padding:16px 0;border-bottom:1px solid #e2e8f0}
.question:last-child{border-bottom:none}
.q-num{display:inline-block;background:#667eea;color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}
.q-text{font-size:1.05em;margin-bottom:12px;font-weight:500}
.options{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:stretch}
@media(max-width:600px){.options{grid-template-columns:1fr}}
.option{display:flex;flex-direction:column;position:relative;min-height:0}
.option input{display:none}
.option label{display:block;flex:1;min-height:52px;padding:10px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;line-height:1.65;touch-action:manipulation;-webkit-user-select:none;user-select:none}
ruby{ruby-align:center}
.option label rt,.q-text rt,.reading-passage rt{font-size:.55em;line-height:1.3}
.option label:hover{border-color:#667eea;background:#f7f8ff}
.option input:checked+label{border-color:#667eea;background:#eef0ff;color:#667eea;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.reading-passage{background:#f7fafc;border-left:3px solid #667eea;padding:16px;margin:12px 0;border-radius:0 8px 8px 0;font-size:.95em;line-height:1.9;white-space:pre-wrap}
.btn-submit{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(102,126,234,.4)}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
.result-panel{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}
.result-panel h2{font-size:1.8em;margin-bottom:8px}
.result-score{font-size:3em;font-weight:bold;margin:16px 0}
.result-score.excellent{color:#48bb78}
.result-score.good{color:#667eea}
.result-score.fair{color:#ed8936}
.result-score.poor{color:#fc8181}
.result-detail{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}
.result-item{background:#f7fafc;padding:12px;border-radius:8px}
.result-item .label{font-size:.8em;color:#718096}
.result-item .value{font-size:1.2em;font-weight:bold}
.explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}
.explanation.show{display:block}
</style>
</head>
<body>
<div class="container">
<header>
<h1>過去問J.TEST F-G 2026年3月度（60分・50問）</h1>
<div class="header-info">
<div class="timer" id="timer">60:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">全50問</div>
</div>
</header>
''')

    # Section A
    out.append('''<div class="section">
<div class="section-title">1 <ruby>文法<rt>ぶんぽう</rt></ruby>・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> A — （　）にいちばんいいものをいれてください（10問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>次<rt>つぎ</rt></ruby>の<ruby>文<rt>ぶん</rt></ruby>の（　）に1・2・3・4のなかからいちばんいいものをいれてください。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_A, 1):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Section B
    out.append('''<div class="section">
<div class="section-title">1 <ruby>文法<rt>ぶんぽう</rt></ruby>・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> B — （　）にいちばんいいものをいれてください（10問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>次<rt>つぎ</rt></ruby>の<ruby>文<rt>ぶん</rt></ruby>の（　）に1・2・3・4のなかからいちばんいいものをいれてください。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_B, 11):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Section C
    out.append('''<div class="section">
<div class="section-title">1 <ruby>文法<rt>ぶんぽう</rt></ruby>・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> C — だいたいおなじいみのものをえらんでください（5問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>次<rt>つぎ</rt></ruby>の<ruby>文<rt>ぶん</rt></ruby>の＿＿とだいたいおなじいみのものを、1・2・3・4のなかからえらんでください。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_C, 21):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Reading - one section, multiple passages
    out.append('''<div class="section">
<div class="section-title">2 <ruby>読解<rt>どっかい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> — 文章を<ruby>読<rt>よ</rt></ruby>んで<ruby>問題<rt>もんだい</rt></ruby>に<ruby>答<rt>こた</rt></ruby>えなさい（10問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>話<rt>はなし</rt></ruby>とあっているものを1・2・3・4の<ruby>中<rt>なか</rt></ruby>から1つ<ruby>選<rt>えら</rt></ruby>んでください。</p>
''')
    q_num = 26
    for passage, questions in READING_DATA:
        for idx, (q, opts, expl) in enumerate(questions):
            show_passage = passage if idx == 0 else None
            out.append(gen_question_html(q_num, q, opts, expl, passage=show_passage))
            q_num += 1
    out.append('</div>')

    # Kanji A
    out.append('''<div class="section">
<div class="section-title">3 <ruby>漢字<rt>かんじ</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> A — ひらがなの<ruby>漢字<rt>かんじ</rt></ruby>をえらんでください（5問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>次<rt>つぎ</rt></ruby>のひらがなの<ruby>漢字<rt>かんじ</rt></ruby>を1・2・3・4のなかから1つえらんでください。</p>
''')
    for i, (q, opts, expl) in enumerate(KANJI_A, 36):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Kanji B (6 options)
    out.append('''<div class="section">
<div class="section-title">3 <ruby>漢字<rt>かんじ</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> B — <ruby>漢字<rt>かんじ</rt></ruby>の読みかたをえらんでください（5問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>次<rt>つぎ</rt></ruby>の<ruby>漢字<rt>かんじ</rt></ruby>の読みかたを1・2・3・4・5・6のなかから1つえらんでください。</p>
''')
    for i, (q, opts, expl) in enumerate(KANJI_B, 41):
        out.append(gen_question_html(i, q, opts, expl, num_opts=6))
    out.append('</div>')

    # Sentence order (6 options)
    out.append('''<div class="section">
<div class="section-title">4 <ruby>短文作成<rt>たんぶんさくせい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> — ただしい<ruby>文<rt>ぶん</rt></ruby>を<ruby>作<rt>つく</rt></ruby>ってください（5問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px"><ruby>例<rt>れい</rt></ruby>のように3つの<ruby>言葉<rt>ことば</rt></ruby>をならべて、ただしい<ruby>文<rt>ぶん</rt></ruby>を<ruby>作<rt>つく</rt></ruby>ってください。1・2・3・4・5・6のなかからいちばんいいものを1つえらんでください。</p>
''')
    for i, (q, opts, expl) in enumerate(SENTENCE_ORDER, 46):
        out.append(gen_question_html(i, q, opts, expl, num_opts=6))
    out.append('</div>')

    out.append('''
<button class="btn-submit" id="submitBtn" onclick="submitTest()">採点する</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>

<script>
const TOTAL=50,TIME_LIMIT=3600;
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
const sections={grammar:0,grammarT:25,reading:0,readingT:10,kanji:0,kanjiT:10,sentence:0,sentenceT:5};
for(let i=1;i<=TOTAL;i++){
const sel=document.querySelector(`input[name="q${i}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${i}"]`);
let isCorrect=false;
if(sel&&sel.value==='1'){isCorrect=true;correct++;}
opts.forEach(o=>{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
});
if(i<=25){if(isCorrect)sections.grammar++;}
else if(i<=35){if(isCorrect)sections.reading++;}
else if(i<=45){if(isCorrect)sections.kanji++;}
else{if(isCorrect)sections.sentence++;}
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
<div class="result-item"><div class="label">文法・語彙</div><div class="value">${sections.grammar}/${sections.grammarT}</div></div>
<div class="result-item"><div class="label">読解</div><div class="value">${sections.reading}/${sections.readingT}</div></div>
<div class="result-item"><div class="label">漢字</div><div class="value">${sections.kanji}/${sections.kanjiT}</div></div>
<div class="result-item"><div class="label">短文作成</div><div class="value">${sections.sentence}/${sections.sentenceT}</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${Math.floor(timeUsed/60)}分${timeUsed%60}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({behavior:'smooth'});
}
startTimer();
</script>
</body>
</html>
''')

    html = '\n'.join(out)
    html = html.replace('&lt;br&gt;', '<br>')
    out_path = '/Users/hayashi./datax/Business/school/J.TEST/202603student/jtest-fg-202603.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Generated:', out_path)

if __name__ == '__main__':
    main()
