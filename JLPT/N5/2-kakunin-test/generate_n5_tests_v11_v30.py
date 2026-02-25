#!/usr/bin/env python3
"""Generate N5 JLPT confirmation test HTML files v11 through v30."""

import os
import random

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Kanji reading: (sentence with <strong>kanji</strong>, correct reading, wrong options)
KANJI_QUESTIONS = [
    ("あめが　<strong>雨</strong>です。", "あめ", ["あま", "う", "あまい", "うめ"]),
    ("<strong>今</strong>　なんじですか。", "いま", ["こん", "きん", "いまい", "こんにち"]),
    ("<strong>金</strong>ようびに　かいものに　いきます。", "きん", ["かね", "こん", "ぎん", "きんよう"]),
    ("がっこうに　<strong>入</strong>ります。", "はい", ["いり", "にゅう", "い", "いる"]),
    ("<strong>学</strong>しゅうに　にほんごを　ならいます。", "がく", ["まな", "がっ", "まなぶ", "がくしゅう"]),
    ("この　たてものは　<strong>高</strong>いです。", "たか", ["こう", "たかい", "こうい", "たけ"]),
    ("<strong>書</strong>く　れんしゅうを　します。", "か", ["しょ", "かく", "しょく", "かき"]),
    ("<strong>先</strong>に　いってください。", "さき", ["せん", "まえ", "さっき", "せんせい"]),
    ("<strong>名</strong>まえを　かいてください。", "な", ["めい", "なま", "みょう", "なまえ"]),
    ("<strong>川</strong>で　およぎます。", "かわ", ["せん", "がわ", "かわい", "せんせい"]),
    ("<strong>聞</strong>いてください。", "き", ["ぶん", "もん", "きく", "きいて"]),
    ("<strong>食</strong>べものは　どこに　ありますか。", "しょく", ["た", "く", "しょっ", "たべ"]),
    ("<strong>車</strong>で　いきます。", "くるま", ["しゃ", "くる", "くるまい", "しゃしん"]),
    ("<strong>毎</strong>日　べんきょうします。", "まい", ["まいにち", "まいあさ", "まいつき", "まいとし"]),
    ("<strong>火</strong>ようびに　テストが　あります。", "か", ["ひ", "び", "かよう", "ひよう"]),
    ("<strong>右</strong>に　まがってください。", "みぎ", ["う", "ゆう", "みき", "うえ"]),
    ("<strong>読</strong>む　れんしゅうを　します。", "よ", ["どく", "とく", "よむ", "どっ"]),
    ("<strong>電</strong>きで　がっこうに　いきます。", "でん", ["でんき", "でんしゃ", "でんわ", "でんち"]),
    ("<strong>校</strong>しつは　3かいです。", "こう", ["がっ", "こうしつ", "がっこう", "こうえん"]),
    ("にほん<strong>語</strong>を　べんきょうしています。", "ご", ["かた", "ことば", "ごい", "が"]),
    ("<strong>土</strong>ようびは　やすみです。", "ど", ["つち", "と", "どよう", "つちよう"]),
    ("<strong>木</strong>が　おおきいです。", "き", ["もく", "ぼく", "きの", "もくよう"]),
    ("<strong>姉</strong>は　かいしゃで　はたらきます。", "あね", ["し", "あに", "ねえ", "いもうと"]),
    ("<strong>兄</strong>は　だいがくせいです。", "あに", ["きょう", "にい", "あね", "きょうだい"]),
    ("<strong>秋</strong>は　すずしいです。", "あき", ["しゅう", "あきい", "しゅうき", "あきら"]),
    ("<strong>冬</strong>は　さむいです。", "ふゆ", ["とう", "ふゆい", "とうき", "ふゆう"]),
    ("<strong>春</strong>に　はなが　さきます。", "はる", ["しゅん", "はるい", "しゅんき", "はるう"]),
    ("<strong>手</strong>を　あらいます。", "て", ["しゅ", "てあらい", "しゅう", "てがみ"]),
    ("<strong>目</strong>が　いたいです。", "め", ["もく", "めい", "もっ", "めがね"]),
    ("<strong>耳</strong>で　ききます。", "みみ", ["じ", "み", "みみい", "じみ"]),
    ("<strong>口</strong>を　あけてください。", "くち", ["こう", "く", "こうち", "くちびる"]),
    ("<strong>足</strong>が　いたいです。", "あし", ["そく", "あ", "そっ", "あしい"]),
    ("<strong>頭</strong>が　いたいです。", "あたま", ["ず", "あた", "とう", "あたまい"]),
    ("<strong>体</strong>を　うごかします。", "からだ", ["たい", "から", "たいい", "からだい"]),
    ("<strong>声</strong>が　きこえます。", "こえ", ["せい", "こ", "せえ", "こえい"]),
    ("<strong>色</strong>は　あおが　すきです。", "いろ", ["しき", "いろい", "しょく", "いろいろ"]),
    ("<strong>音</strong>が　きこえます。", "おと", ["おん", "ね", "おとい", "おんがく"]),
    ("<strong>写真</strong>を　とりました。", "しゃしん", ["しゃしん", "しゃっしん", "しゃし", "しゃしんい"]),
    ("<strong>切手</strong>を　かいました。", "きって", ["きって", "せって", "きっ手", "きて"]),
    ("<strong>手紙</strong>を　かきました。", "てがみ", ["しゅがみ", "てかみ", "てがみい", "しゅし"]),
    ("<strong>新聞</strong>を　よみます。", "しんぶん", ["しんぶん", "しんぷん", "しんぶ", "しんぶんい"]),
]

# Writing (hiragana to kanji): (sentence, correct kanji, wrong options - 3 items)
WRITING_QUESTIONS = [
    ("まいにち　<strong>きって</strong>を　かいます。", "切手", ["切丁", "切札", "切券"]),
    ("<strong>てがみ</strong>を　だしました。", "手紙", ["手書", "手簡", "手文"]),
    ("<strong>しんぶん</strong>を　よみます。", "新聞", ["新文", "新聞紙", "新報"]),
    ("<strong>ざっし</strong>を　かいます。", "雑誌", ["雑志", "雑書", "雑紙"]),
    ("<strong>おんがく</strong>が　すきです。", "音楽", ["音学", "音曲", "音楽"]),
    ("<strong>えいがかん</strong>に　いきました。", "映画館", ["映画院", "映画場", "映画所"]),
    ("<strong>きっさてん</strong>で　コーヒーを　のみました。", "喫茶店", ["喫茶屋", "喫茶室", "喫茶場"]),
    ("<strong>ゆうびんきょく</strong>に　いきます。", "郵便局", ["郵便所", "郵便屋", "郵便店"]),
    ("<strong>こうばん</strong>は　どこですか。", "交番", ["交番所", "交番屋", "交番局"]),
    ("<strong>たいしかん</strong>は　あの　たてものです。", "大使館", ["大使所", "大使院", "大使局"]),
    ("<strong>ひこうき</strong>で　にほんに　いきます。", "飛行機", ["飛行器", "飛行船", "飛行車"]),
    ("<strong>じてんしゃ</strong>で　がっこうに　いきます。", "自転車", ["自転機", "自転乗", "自転輪"]),
    ("<strong>でんしゃ</strong>が　おくれました。", "電車", ["電機", "電乗", "電輪"]),
    ("<strong>ちかてつ</strong>で　いきます。", "地下鉄", ["地下道", "地下線", "地下路"]),
    ("<strong>きっぷ</strong>を　かいました。", "切符", ["切札", "切券", "切票"]),
    ("<strong>ちず</strong>を　みてください。", "地図", ["地画", "地表", "地版"]),
    ("<strong>まど</strong>を　あけてください。", "窓", ["窓口", "窓戸", "窓辺"]),
    ("<strong>かいだん</strong>を　のぼります。", "階段", ["階梯", "階路", "階段"]),
    ("<strong>げんかん</strong>で　くつを　ぬぎます。", "玄関", ["玄門", "玄口", "玄扉"]),
    ("<strong>だいどころ</strong>で　りょうりを　します。", "台所", ["台室", "台場", "台間"]),
    ("<strong>れいぞうこ</strong>に　やさいが　あります。", "冷蔵庫", ["冷蔵箱", "冷蔵室", "冷蔵器"]),
    ("<strong>せんたく</strong>を　します。", "洗濯", ["洗濯機", "洗濯物", "洗濯場"]),
    ("<strong>そうじ</strong>を　しました。", "掃除", ["掃地", "掃清", "掃拭"]),
    ("<strong>れんしゅう</strong>を　します。", "練習", ["練修", "練学", "練習"]),
    ("<strong>しつもん</strong>が　あります。", "質問", ["質疑", "質答", "質問"]),
]

# Vocab/context Q4 (particle): (sentence, correct, wrong)
VOCAB4_QUESTIONS = [
    ("きのう　としょかん（　）　ほんを　かりました。", "で", ["を", "に", "へ"]),
    ("にちようびに　こうえん（　）　さんぽしました。", "で", ["を", "に", "へ"]),
    ("きょう　スーパー（　）　やさいを　かいました。", "で", ["を", "に", "へ"]),
    ("きのう　デパート（　）　かいものを　しました。", "で", ["を", "に", "へ"]),
    ("きょう　びょういん（　）　いきました。", "に", ["を", "で", "へ"]),
    ("きのう　がっこう（　）　テニスを　しました。", "で", ["を", "に", "へ"]),
    ("きのう　きっさてん（　）　コーヒーを　のみました。", "で", ["を", "に", "へ"]),
    ("きのう　レストラン（　）　ひるごはんを　たべました。", "で", ["を", "に", "へ"]),
    ("きょう　うみ（　）　およぎました。", "で", ["を", "に", "へ"]),
    ("まいにち　えき（　）　でんしゃに　のります。", "で", ["を", "に", "へ"]),
    ("きのう　ゆうびんきょく（　）　てがみを　だしました。", "で", ["を", "に", "へ"]),
    ("あした　えいがかん（　）　えいがを　みます。", "で", ["を", "に", "へ"]),
    ("きのう　こうえん（　）　ともだちと　あいました。", "で", ["を", "に", "へ"]),
    ("まいにち　がっこう（　）　にほんごを　ならいます。", "で", ["を", "に", "へ"]),
    ("きのう　みせ（　）　くつを　かいました。", "で", ["を", "に", "へ"]),
    ("らいしゅう　びょういん（　）　いきます。", "に", ["を", "で", "へ"]),
    ("まいあさ　えき（　）　でんしゃを　まちます。", "で", ["を", "に", "へ"]),
    ("きのう　プール（　）　およぎました。", "で", ["を", "に", "へ"]),
    ("まいにち　いえ（　）　べんきょうします。", "で", ["を", "に", "へ"]),
    ("きのう　ホテル（　）　とまりました。", "に", ["を", "で", "へ"]),
]

# Vocab/context Q5 (adjective/vocab): (sentence, correct, wrong)
VOCAB5_QUESTIONS = [
    ("この　かばんは　（　）から、もちやすいです。", "かるい", ["おもい", "たかい", "おおきい"]),
    ("この　へやは　（　）から、ストーブを　つけてください。", "さむい", ["あつい", "あたたかい", "すずしい"]),
    ("この　へやは　（　）から、たくさん　ひとが　すわれます。", "ひろい", ["せまい", "ちいさい", "ふるい"]),
    ("この　くつは　（　）から、かいに　いきました。", "やすい", ["たかい", "おおきい", "あたらしい"]),
    ("きのうは　たくさん　あるいたので、（　）。", "つかれた", ["たのしかった", "おいしかった", "うれしかった"]),
    ("この　ほんは　（　）から、よく　よみます。", "おもしろい", ["つまらない", "むずかしい", "ながい"]),
    ("この　ほんは　（　）から、こどもも　よめます。", "やさしい", ["むずかしい", "おおきい", "たかい"]),
    ("この　みせの　りんごは　（　）から、たくさん　かいます。", "やすい", ["たかい", "おおきい", "おいしい"]),
    ("この　りょうりは　（　）です。", "おいしい", ["まずい", "つまらない", "わるい"]),
    ("この　まちは　（　）です。", "しずか", ["にぎやか", "きれい", "べんり"]),
    ("この　えいがは　（　）です。", "つまらない", ["おもしろい", "たのしい", "おいしい"]),
    ("この　へやは　（　）です。", "きれい", ["きたない", "ふるい", "ちいさい"]),
    ("この　まちは　（　）です。", "にぎやか", ["しずか", "ひま", "きれい"]),
    ("この　くつは　（　）から、あるきやすいです。", "あたらしい", ["ふるい", "ちいさい", "おおきい"]),
    ("この　ほんは　（　）から、じかんが　かかります。", "ながい", ["みじかい", "おおきい", "ちいさい"]),
    ("この　みせは　（　）から、べんりです。", "ちかい", ["とおい", "おおきい", "ちいさい"]),
    ("この　かみは　（　）です。", "うすい", ["あつい", "おもい", "ながい"]),
    ("この　みちは　（　）です。", "せまい", ["ひろい", "ながい", "みじかい"]),
    ("この　たてものは　（　）です。", "たかい", ["ひくい", "おおきい", "ちいさい"]),
    ("この　かばんは　（　）です。", "じょうぶ", ["よわい", "かるい", "おもい"]),
]

# Paraphrase Q6: (original sentence, correct paraphrase, wrong)
PARAPHRASE_QUESTIONS = [
    ("わたしの　いえは　がっこうから　<strong>ちかい</strong>です。", "とおくない", ["とおい", "ちいさい", "おおきい"]),
    ("わたしは　<strong>まいにち</strong>　はやく　おきます。", "いつも", ["ときどき", "よく", "あまり"]),
    ("この　みせの　りんごは　<strong>やすい</strong>です。", "たかくない", ["たかい", "おおきい", "おいしい"]),
    ("この　りょうりは　<strong>おいしい</strong>です。", "うまい", ["まずい", "あまい", "からい"]),
    ("この　まちは　<strong>しずか</strong>です。", "うるさくない", ["にぎやか", "ひろい", "きれい"]),
    ("この　えいがは　<strong>おもしろい</strong>です。", "たのしい", ["つまらない", "ながい", "むずかしい"]),
    ("この　へやは　<strong>きれい</strong>です。", "きたなくない", ["きたない", "ふるい", "ちいさい"]),
    ("この　まちは　<strong>にぎやか</strong>です。", "しずかじゃない", ["しずか", "ひま", "きれい"]),
    ("この　ほんは　<strong>むずかしい</strong>です。", "かんたんじゃない", ["やさしい", "おもしろい", "ながい"]),
    ("この　くつは　<strong>かるい</strong>です。", "おもくない", ["おもい", "たかい", "おおきい"]),
    ("この　かばんは　<strong>おもい</strong>です。", "かるくない", ["かるい", "ちいさい", "おおきい"]),
    ("わたしは　<strong>いそがしい</strong>です。", "ひまじゃない", ["ひま", "たのしい", "つかれました"]),
    ("この　りょうりは　<strong>からい</strong>です。", "あまくない", ["あまい", "おいしい", "まずい"]),
    ("この　ほんは　<strong>ながい</strong>です。", "みじかくない", ["みじかい", "おおきい", "ちいさい"]),
    ("この　みちは　<strong>ひろい</strong>です。", "せまくない", ["せまい", "ながい", "みじかい"]),
    ("この　たてものは　<strong>ひくい</strong>です。", "たかくない", ["たかい", "おおきい", "ちいさい"]),
    ("この　みせは　<strong>とおい</strong>です。", "ちかくない", ["ちかい", "おおきい", "ちいさい"]),
    ("この　かみは　<strong>あつい</strong>です。", "うすくない", ["うすい", "おもい", "ながい"]),
    ("わたしは　<strong>げんき</strong>です。", "びょうきじゃない", ["びょうき", "つかれました", "ねむい"]),
    ("この　くつは　<strong>あたらしい</strong>です。", "ふるくない", ["ふるい", "ちいさい", "おおきい"]),
]

# Grammar Q7: (sentence, correct, wrong) - を/が/に/で
GRAMMAR7_QUESTIONS = [
    ("わたしは　にほんご（　）　べんきょうしています。", "を", ["が", "に", "で"]),
    ("わたしは　まいにち　バス（　）　がっこうに　いきます。", "で", ["を", "に", "が"]),
    ("わたしは　まいにち　でんしゃ（　）　がっこうに　いきます。", "で", ["を", "に", "が"]),
    ("わたしは　まいにち　おちゃ（　）　のみます。", "を", ["が", "に", "で"]),
    ("わたしは　コーヒー（　）　すきです。", "が", ["を", "に", "で"]),
    ("わたしは　えいご（　）　へたです。", "が", ["を", "に", "で"]),
    ("わたしは　りんご（　）　すきです。", "が", ["を", "に", "で"]),
    ("わたしは　ごはん（　）　まえに　てを　あらいます。", "を", ["が", "に", "で"]),
    ("あめが　ふった（　）　かいものに　いきませんでした。", "から", ["で", "に", "を"]),
    ("らいしゅう　とうきょう（　）　いきます。", "に", ["を", "で", "が"]),
    ("らいげつ　おおさか（　）　しごとに　いきます。", "に", ["を", "で", "が"]),
    ("らいしゅう　だれ（　）　いっしょに　りょこうに　いきますか。", "と", ["を", "で", "が"]),
    ("きのう　はは（　）　でんわを　かけました。", "に", ["を", "で", "が"]),
    ("きのう　としょかん（　）　ほんを　かりに　いきました。", "に", ["を", "で", "が"]),
    ("しゅくだいを　（　）　まえに　テレビを　みます。", "する", ["して", "した", "します"]),
    ("よる　10じ（　）　ねます。", "に", ["で", "を", "が"]),
    ("まいばん　11じ（　）　ねます。", "に", ["で", "を", "が"]),
    ("まいあさ　7じ（　）　おきます。", "に", ["で", "を", "が"]),
    ("きょうの　よる　（　）を　して、あした　せんせいに　だします。", "しゅくだい", ["べんきょう", "れんしゅう", "しつもん"]),
]

# Grammar Q8: (sentence, correct, wrong) - に/で/を/と
GRAMMAR8_QUESTIONS = [
    ("あした　9じ（　）　えきで　あいましょう。", "に", ["で", "を", "が"]),
    ("まいあさ　7じ（　）　おきます。", "に", ["で", "を", "が"]),
    ("よる　10じ（　）　ねます。", "に", ["で", "を", "が"]),
    ("まいばん　11じ（　）　ねます。", "に", ["で", "を", "が"]),
    ("らいしゅう　だれ（　）　いっしょに　りょこうに　いきますか。", "と", ["を", "で", "に"]),
    ("きのう　ともだち（　）　あいました。", "に", ["を", "で", "が"]),
    ("きのう　はは（　）　でんわを　かけました。", "に", ["を", "で", "が"]),
    ("らいしゅう　とうきょう（　）　いきます。", "に", ["を", "で", "が"]),
    ("らいげつ　おおさか（　）　しごとに　いきます。", "に", ["を", "で", "が"]),
    ("しゅくだいを　（　）　まえに　テレビを　みます。", "する", ["して", "した", "します"]),
    ("あした　テストが　ある（　）、きょうは　べんきょうします。", "から", ["で", "に", "を"]),
    ("きのう　としょかん（　）　ほんを　かりに　いきました。", "に", ["を", "で", "が"]),
    ("あめが　ふった（　）　かいものに　いきませんでした。", "から", ["で", "に", "を"]),
    ("わたしは　ごはん（　）　まえに　てを　あらいます。", "を", ["が", "に", "で"]),
    ("わたしは　コーヒー（　）　すきです。", "が", ["を", "に", "で"]),
    ("わたしは　えいご（　）　へたです。", "が", ["を", "に", "で"]),
    ("わたしは　りんご（　）　すきです。", "が", ["を", "に", "で"]),
    ("わたしは　まいにち　バス（　）　がっこうに　いきます。", "で", ["を", "に", "が"]),
    ("わたしは　まいにち　でんしゃ（　）　がっこうに　いきます。", "で", ["を", "に", "が"]),
    ("わたしは　にほんご（　）　べんきょうしています。", "を", ["が", "に", "で"]),
]

# Sentence construction Q9: (sentence with ★, correct answer, wrong)
SENTENCE_QUESTIONS = [
    ("わたしは　＿＿　＿＿　★　＿＿　いきます。", "バスで", ["まいにち", "8じに", "がっこうに"]),
    ("わたしは　＿＿　＿＿　★　＿＿　かきました。", "ペンで", ["きのう", "てがみを", "ともだちに"]),
    ("わたしは　＿＿　＿＿　★　＿＿　たべます。", "あさごはんを", ["まいにち", "7じに", "いえで"]),
    ("わたしは　＿＿　＿＿　★　＿＿　かえります。", "でんしゃで", ["まいにち", "5じに", "いえに"]),
    ("わたしは　＿＿　＿＿　★　＿＿　のみます。", "おちゃを", ["まいにち", "あさ", "いえで"]),
    ("わたしは　＿＿　＿＿　★　＿＿　よみます。", "ほんを", ["まいにち", "よる", "へやで"]),
    ("きのう　＿＿　＿＿　★　＿＿　よみました。", "ほんを", ["としょかんで", "2さつ", "よむ"]),
    ("にちようび　＿＿　＿＿　★　＿＿　いきます。", "バスで", ["こうえんに", "ともだちと", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　かきます。", "ペンで", ["まいにち", "にっきを", "かく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　いきます。", "じてんしゃで", ["まいにち", "がっこうに", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　のみます。", "みずを", ["まいにち", "たくさん", "のむ"]),
    ("わたしは　＿＿　＿＿　★　＿＿　たべます。", "ひるごはんを", ["まいにち", "12じに", "がっこうで"]),
    ("わたしは　＿＿　＿＿　★　＿＿　いきます。", "あるいて", ["まいにち", "えきに", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　よみます。", "しんぶんを", ["まいにち", "あさ", "よむ"]),
    ("わたしは　＿＿　＿＿　★　＿＿　いきます。", "ちかてつで", ["まいにち", "かいしゃに", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　たべます。", "ばんごはんを", ["まいにち", "7じに", "いえで"]),
    ("わたしは　＿＿　＿＿　★　＿＿　いきました。", "タクシーで", ["きのう", "えきに", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　のみます。", "コーヒーを", ["まいにち", "あさ", "きっさてんで"]),
    ("わたしは　＿＿　＿＿　★　＿＿　いきます。", "バスで", ["あした", "びょういんに", "いく"]),
    ("わたしは　＿＿　＿＿　★　＿＿　かきます。", "てがみを", ["まいにち", "ともだちに", "かく"]),
]

# Reading Q10: (passage, question, correct, wrong)
READING_QUESTIONS = [
    ("すずきさんは まいにち 6じに おきます。あさごはんを たべて、7じに いえを でます。じてんしゃで がっこうに いきます。がっこうは 4じに おわります。", "すずきさんは がっこうに なんの のりもので いきますか。", "じてんしゃ", ["バス", "でんしゃ", "あるいて"]),
    ("やまださんは まいにち 8じに おきます。あさごはんを たべて、8じはんに いえを でます。あるいて えきまで いって、でんしゃで かいしゃに いきます。", "やまださんは えきから かいしゃまで なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
    ("たなかさんは まいにち 7じに おきます。あさごはんを たべて、8じはんに いえを でます。バスで えきまで いって、でんしゃで かいしゃに いきます。かいしゃは 5じに おわります。", "たなかさんは えきから かいしゃまで なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
    ("やまもとさんは にちようびに かぞくで うみに いきます。いえから えきまで あるいて いって、でんしゃで うみまで いきます。", "やまもとさんのかぞくは えきから うみまで なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
    ("いとうさんは まいにち 7じはんに おきます。あさごはんを たべて、8じに いえを でます。バスで かいしゃに いきます。かいしゃは 6じに おわります。", "いとうさんは かいしゃに なんの のりもので いきますか。", "バス", ["でんしゃ", "じてんしゃ", "あるいて"]),
    ("かとうさんは まいにち 7じに おきます。あさごはんを たべて、7じはんに いえを でます。あるいて えきまで いって、でんしゃで がっこうに いきます。", "かとうさんは がっこうに なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
    ("さとうさんは まいにち 8じに おきます。あさごはんを たべて、8じはんに いえを でます。バスで えきまで いって、でんしゃで かいしゃに いきます。", "さとうさんは えきから かいしゃまで なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
    ("はやしさんは まいにち 6じに おきます。がっこうは 3じに おわります。がっこうの あとで プールで およぎます。", "はやしさんは がっこうの あとで よく どこで およぎますか。", "プール", ["うみ", "かわ", "いえ"]),
    ("なかむらさんは まいにち 7じに おきます。がっこうは 4じに おわります。がっこうの あとで プールで およぎます。", "なかむらさんは がっこうの あとで よく どこで およぎますか。", "プール", ["うみ", "かわ", "いえ"]),
    ("たなかさんは じゅぎょうの あとで よく としょかんに いきます。そこで ほんを よんだり、しゅくだいを したり します。", "たなかさんは じゅぎょうの あとで よく どこに いきますか。", "としょかん", ["プール", "こうえん", "えき"]),
    ("すずきさんは ふつう バスで がっこうに いきます。でも きょうは バスが おくれて、でんしゃで いきました。", "すずきさんは ふつう なんの のりもので がっこうに いきますか。", "バス", ["でんしゃ", "じてんしゃ", "あるいて"]),
    ("やまださんは きのう バスで かいしゃに いきました。いつもは でんしゃで いきます。", "やまださんは きのう なんの のりもので かいしゃに いきましたか。", "バス", ["でんしゃ", "じてんしゃ", "あるいて"]),
    ("さとうさんは まいにち 7じに おきます。あさごはんを たべて、7じはんに いえを でます。ちかてつで かいしゃに いきます。", "さとうさんは かいしゃに なんの のりもので いきますか。", "ちかてつ", ["バス", "でんしゃ", "じてんしゃ"]),
    ("かとうさんは まいにち じてんしゃで がっこうに いきます。がっこうは ちかいです。", "かとうさんは がっこうに なんの のりもので いきますか。", "じてんしゃ", ["バス", "でんしゃ", "あるいて"]),
    ("いとうさんは まいにち タクシーで かいしゃに いきます。かいしゃは とおいです。", "いとうさんは かいしゃに なんの のりもので いきますか。", "タクシー", ["バス", "でんしゃ", "じてんしゃ"]),
    ("はやしさんは まいにち あるいて がっこうに いきます。がっこうは とても ちかいです。", "はやしさんは がっこうに なんの のりもので いきますか。", "あるいて", ["バス", "でんしゃ", "じてんしゃ"]),
    ("なかむらさんは まいにち ひこうきで しごとに いきます。なかなか とおい まちで はたらきます。", "なかむらさんは しごとに なんの のりもので いきますか。", "ひこうき", ["でんしゃ", "バス", "タクシー"]),
    ("たなかさんは まいにち 7じに おきます。あさごはんを たべて、8じに いえを でます。ちかてつで かいしゃに いきます。", "たなかさんは かいしゃに なんの のりもので いきますか。", "ちかてつ", ["バス", "でんしゃ", "じてんしゃ"]),
    ("すずきさんは まいにち 8じに おきます。あさごはんを たべて、8じはんに いえを でます。でんしゃで がっこうに いきます。がっこうは 4じに おわります。", "すずきさんは がっこうに なんの のりもので いきますか。", "でんしゃ", ["バス", "じてんしゃ", "あるいて"]),
]

def make_options(correct, wrong_list, correct_val="1"):
    """Create 4 options with correct having value=1."""
    options = [(correct, correct_val)]
    for w in wrong_list[:3]:
        opt = w if isinstance(w, str) else w[0] if isinstance(w, (list, tuple)) else str(w)
        options.append((opt, "0"))
    random.shuffle(options)
    return options

def render_options(options, qnum, prefix):
    lines = []
    labels = "abcd"
    for i, (text, val) in enumerate(options):
        lid = f"q{qnum}{labels[i]}"
        num = i + 1
        lines.append(f'<div class="option"><input type="radio" name="q{qnum}" id="{lid}" value="{val}"><label for="{lid}">{num}. {text}</label></div>')
    return "\n".join(lines)

def generate_html(version):
    vnum = 10 + version  # v11 = 11, v30 = 30
    idx = version - 1  # 0..19

    # Select questions - use different indices for each test
    k1, k2 = (idx * 2) % len(KANJI_QUESTIONS), (idx * 2 + 1) % len(KANJI_QUESTIONS)
    w = idx % len(WRITING_QUESTIONS)
    v4 = idx % len(VOCAB4_QUESTIONS)
    v5 = idx % len(VOCAB5_QUESTIONS)
    p = idx % len(PARAPHRASE_QUESTIONS)
    g7 = idx % len(GRAMMAR7_QUESTIONS)
    g8 = (idx + 10) % len(GRAMMAR8_QUESTIONS)
    s = idx % len(SENTENCE_QUESTIONS)
    r = idx % len(READING_QUESTIONS)

    # Ensure variety - offset some by version
    k1 = (idx * 3) % len(KANJI_QUESTIONS)
    k2 = (idx * 3 + 1) % len(KANJI_QUESTIONS)
    w = (idx + 5) % len(WRITING_QUESTIONS)
    v4 = (idx + 7) % len(VOCAB4_QUESTIONS)
    v5 = (idx + 11) % len(VOCAB5_QUESTIONS)
    p = (idx + 13) % len(PARAPHRASE_QUESTIONS)
    g7 = (idx + 17) % len(GRAMMAR7_QUESTIONS)
    g8 = (idx + 19) % len(GRAMMAR8_QUESTIONS)
    s = (idx + 23) % len(SENTENCE_QUESTIONS)
    r = idx % len(READING_QUESTIONS)

    kq1 = KANJI_QUESTIONS[k1]
    kq2 = KANJI_QUESTIONS[k2]
    wq = WRITING_QUESTIONS[w]
    v4q = VOCAB4_QUESTIONS[v4]
    v5q = VOCAB5_QUESTIONS[v5]
    pq = PARAPHRASE_QUESTIONS[p]
    g7q = GRAMMAR7_QUESTIONS[g7]
    g8q = GRAMMAR8_QUESTIONS[g8]
    sq = SENTENCE_QUESTIONS[s]
    rq = READING_QUESTIONS[r]

    w_wrong = [x for x in wq[2] if x != wq[1]][:3] if len(wq) > 2 else ["誤1", "誤2", "誤3"]
    v5_wrong = [x for x in v5q[2] if x != v5q[1]][:3] if len(v5q) > 2 else []
    p_wrong = [str(x) for x in pq[2] if x != pq[1]][:3] if len(pq) > 2 else []

    # Build Q1 (kanji)
    k1_opts = make_options(kq1[1], kq1[2])
    q1_html = f'''<div class="question">
<div class="q-text"><span class="q-num">1</span>{kq1[0]}</div>
<div class="options">
{render_options(k1_opts, 1, "q1")}
</div>
<div class="explanation">✅ 正解：{kq1[1]} — 正しい読みです。</div>
</div>'''

    # Q2
    k2_opts = make_options(kq2[1], kq2[2])
    q2_html = f'''<div class="question">
<div class="q-text"><span class="q-num">2</span>{kq2[0]}</div>
<div class="options">
{render_options(k2_opts, 2, "q2")}
</div>
<div class="explanation">✅ 正解：{kq2[1]} — 正しい読みです。</div>
</div>'''

    # Q3
    w_opts = make_options(wq[1], w_wrong)
    q3_html = f'''<div class="question">
<div class="q-text"><span class="q-num">3</span>{wq[0]}</div>
<div class="options">
{render_options(w_opts, 3, "q3")}
</div>
<div class="explanation">✅ 正解：{wq[1]} — 「{wq[0].split("strong>")[1].split("<")[0]}」は「{wq[1]}」と書きます。</div>
</div>'''

    # Q4
    v4_opts = make_options(v4q[1], v4q[2])
    q4_html = f'''<div class="question">
<div class="q-text"><span class="q-num">4</span>{v4q[0]}</div>
<div class="options">
{render_options(v4_opts, 4, "q4")}
</div>
<div class="explanation">✅ 正解：{v4q[1]} — 文脈に合う助詞です。</div>
</div>'''

    # Q5
    v5_opts = make_options(v5q[1], v5_wrong)
    q5_html = f'''<div class="question">
<div class="q-text"><span class="q-num">5</span>{v5q[0]}</div>
<div class="options">
{render_options(v5_opts, 5, "q5")}
</div>
<div class="explanation">✅ 正解：{v5q[1]} — 文脈に合う語です。</div>
</div>'''

    # Q6
    p_opts = make_options(pq[1], p_wrong)
    # Paraphrase needs full sentence options
    p_correct_sent = pq[1] if len(pq[1]) > 10 else f"この　ほんは　{pq[1]}です。"
    p_wrong_sents = [f"この　ほんは　{x}です。" if len(str(x)) < 15 else str(x) for x in p_wrong]
    if "いえ" in pq[0] or "まち" in pq[0]:
        p_correct_sent = f"わたしの　いえは　がっこうから　{pq[1]}です。" if "ちかい" in pq[0] else pq[1]
    p_opts_data = [(p_correct_sent, "1")] + [(x, "0") for x in p_wrong_sents[:3]]
    random.shuffle(p_opts_data)
    p_opts_html = "\n".join([f'<div class="option"><input type="radio" name="q6" id="q6{chr(97+i)}" value="{v}"><label for="q6{chr(97+i)}">{i+1}. {t}</label></div>' for i, (t, v) in enumerate(p_opts_data)])
    q6_html = f'''<div class="question">
<div class="q-text"><span class="q-num">6</span>{pq[0]}</div>
<div class="options">
{p_opts_html}
</div>
<div class="explanation">✅ 正解：{pq[1]} — 言い換え表現です。</div>
</div>'''

    # Simplify Q6 - use simple options
    p_simple_opts = make_options(pq[1], p_wrong)
    q6_html = f'''<div class="question">
<div class="q-text"><span class="q-num">6</span>{pq[0]}</div>
<div class="options">
{render_options(p_simple_opts, 6, "q6")}
</div>
<div class="explanation">✅ 正解：{pq[1]} — 言い換え表現です。</div>
</div>'''

    # Q7
    g7_opts = make_options(g7q[1], g7q[2])
    q7_html = f'''<div class="question">
<div class="q-text"><span class="q-num">7</span>{g7q[0]}</div>
<div class="options">
{render_options(g7_opts, 7, "q7")}
</div>
<div class="explanation">✅ 正解：{g7q[1]} — 文法に合う助詞です。</div>
</div>'''

    # Q8
    g8_opts = make_options(g8q[1], g8q[2])
    q8_html = f'''<div class="question">
<div class="q-text"><span class="q-num">8</span>{g8q[0]}</div>
<div class="options">
{render_options(g8_opts, 8, "q8")}
</div>
<div class="explanation">✅ 正解：{g8q[1]} — 文法に合う表現です。</div>
</div>'''

    # Q9
    s_opts = make_options(sq[1], sq[2])
    q9_html = f'''<div class="question">
<div class="q-text"><span class="q-num">9</span>{sq[0]}</div>
<div class="options">
{render_options(s_opts, 9, "q9")}
</div>
<div class="explanation">✅ 正解：{sq[1]} — ★の位置に入る表現です。</div>
</div>'''

    # Q10
    r_opts = make_options(rq[2], rq[3])
    q10_html = f'''<div class="question">
<div class="reading-passage">
{rq[0]}
</div>
<div class="q-text"><span class="q-num">10</span>{rq[1]}</div>
<div class="options">
{render_options(r_opts, 10, "q10")}
</div>
<div class="explanation">✅ 正解：{rq[2]} — 本文の内容から正しい答えです。</div>
</div>'''

    template = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>JLPT N5 確認テスト{vnum}（10分・10問）</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}}
body{{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}}
.container{{max-width:800px;margin:0 auto;padding:20px}}
header{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(102,126,234,0.4)}}
header h1{{font-size:1.5em;margin-bottom:4px}}
.header-info{{display:flex;justify-content:center;gap:24px;align-items:center;margin-top:8px;flex-wrap:wrap}}
.timer{{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}}
.timer.warning{{color:#ffd700;animation:pulse 1s infinite}}
.timer.danger{{color:#ff4757;animation:pulse .5s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.6}}}}
.progress-bar{{width:200px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}}
.progress-fill{{height:100%;background:#fff;border-radius:4px;transition:width .3s}}
.score-badge{{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}}
.section{{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.section-title{{font-size:1.1em;font-weight:bold;color:#667eea;border-left:4px solid #667eea;padding-left:12px;margin-bottom:16px}}
.question{{padding:16px 0;border-bottom:1px solid #e2e8f0}}
.question:last-child{{border-bottom:none}}
.q-num{{display:inline-block;background:#667eea;color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:.85em;font-weight:bold;margin-right:8px}}
.q-text{{font-size:1.05em;margin-bottom:12px;font-weight:500}}
.options{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
@media(max-width:600px){{.options{{grid-template-columns:1fr}}}}
.option{{position:relative}}
.option input{{display:none}}
.option label{{display:flex;align-items:center;min-height:44px;padding:10px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:all .2s;font-size:.95em;touch-action:manipulation;-webkit-user-select:none;user-select:none}}
.option label:hover{{border-color:#667eea;background:#f7f8ff}}
.option input:checked+label{{border-color:#667eea;background:#eef0ff;color:#667eea;font-weight:600}}
.option.correct label{{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}}
.option.wrong label{{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}}
.reading-passage{{background:#f7fafc;border-left:3px solid #667eea;padding:16px;margin:12px 0;border-radius:0 8px 8px 0;font-size:.95em;line-height:1.9}}
.btn-submit{{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}}
.btn-submit:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(102,126,234,.4)}}
.btn-submit:disabled{{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}}
.result-panel{{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}}
.result-panel h2{{font-size:1.8em;margin-bottom:8px}}
.result-score{{font-size:3em;font-weight:bold;margin:16px 0}}
.result-score.excellent{{color:#48bb78}}
.result-score.good{{color:#667eea}}
.result-score.fair{{color:#ed8936}}
.result-score.poor{{color:#fc8181}}
.result-detail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}}
.result-item{{background:#f7fafc;padding:12px;border-radius:8px}}
.result-item .label{{font-size:.8em;color:#718096}}
.result-item .value{{font-size:1.2em;font-weight:bold}}
.explanation{{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55}}
.explanation.show{{display:block}}
</style>
</head>
<body>
<div class="container">
<header>
<h1>JLPT N5 確認テスト{vnum}（10分・10問）</h1>
<div class="header-info">
<div class="timer" id="timer">10:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">全10問</div>
</div>
</header>

<div class="section">
<div class="section-title">もんだい1 — 漢字の読み（2問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">＿＿のことばは ひらがなで どう かきますか。1・2・3・4から いちばん いいものを ひとつ えらんでください。</p>
{q1_html}
{q2_html}
</div>

<div class="section">
<div class="section-title">もんだい2 — 表記（1問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">＿＿のことばは どう かきますか。1・2・3・4から いちばん いいものを ひとつ えらんでください。</p>
{q3_html}
</div>

<div class="section">
<div class="section-title">もんだい3 — 語彙・文脈規定（2問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">（　）に なにを いれますか。1・2・3・4から いちばん いいものを ひとつ えらんでください。</p>
{q4_html}
{q5_html}
</div>

<div class="section">
<div class="section-title">もんだい4 — 言い換え類義（1問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">＿＿のぶんと　だいたい おなじ いみの ぶんは どれですか。</p>
{q6_html}
</div>

<div class="section">
<div class="section-title">もんだい5 — 文法（3問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">（　）に なにを いれますか。1・2・3・4から いちばん いいものを ひとつ えらんでください。</p>
{q7_html}
{q8_html}
</div>

<div class="section">
<div class="section-title">もんだい6 — 文の組み立て（1問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">★に入るものは どれですか。</p>
{q9_html}
</div>

<div class="section">
<div class="section-title">もんだい7 — 読解（1問）</div>
{q10_html}
</div>

<button class="btn-submit" id="submitBtn" onclick="submitTest()">採点する</button>
<div class="result-panel" id="resultPanel">
<h2 id="resultTitle"></h2>
<div class="result-score" id="resultScore"></div>
<div class="result-detail" id="resultDetail"></div>
<button class="btn-submit" onclick="location.reload()" style="margin-top:20px">もう一度</button>
</div>
</div>

<script>
const TOTAL=10,TIME_LIMIT=600;
let timeLeft=TIME_LIMIT,timerInterval,submitted=false;
function startTimer(){{
timerInterval=setInterval(()=>{{
timeLeft--;
const m=Math.floor(timeLeft/60),s=timeLeft%60;
const el=document.getElementById('timer');
el.textContent=`${{m}}:${{s.toString().padStart(2,'0')}}`;
document.getElementById('progress').style.width=`${{(timeLeft/TIME_LIMIT)*100}}%`;
if(timeLeft<=60)el.className='timer danger';
else if(timeLeft<=180)el.className='timer warning';
if(timeLeft<=0){{clearInterval(timerInterval);submitTest();}}
}},1000);
}}
function submitTest(){{
if(submitted)return;submitted=true;
clearInterval(timerInterval);
let correct=0;
const sections={{kanji:0,kanjiT:2,vocab:0,vocabT:2,paraphrase:0,paraphraseT:1,grammar:0,grammarT:3,sentence:0,sentenceT:1,reading:0,readingT:1}};
for(let i=1;i<=TOTAL;i++){{
const sel=document.querySelector(`input[name="q${{i}}"]:checked`);
const opts=document.querySelectorAll(`input[name="q${{i}}"]`);
let isCorrect=false;
if(sel&&sel.value==='1'){{isCorrect=true;correct++;}}
opts.forEach(o=>{{
const p=o.parentElement;
if(o.value==='1')p.classList.add('correct');
else if(o.checked&&o.value!=='1')p.classList.add('wrong');
}});
if(i<=2){{if(isCorrect)sections.kanji++;}}
else if(i===3){{if(isCorrect)sections.vocab++;}}
else if(i===5){{if(isCorrect)sections.vocab++;}}
else if(i===4||(i>=7&&i<=8)){{if(isCorrect)sections.grammar++;}}
else if(i===6){{if(isCorrect)sections.paraphrase++;}}
else if(i===9){{if(isCorrect)sections.sentence++;}}
else if(i===10){{if(isCorrect)sections.reading++;}}
}}
document.querySelectorAll('.explanation').forEach(e=>e.classList.add('show'));
const pct=Math.round((correct/TOTAL)*100);
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
<div class="result-item"><div class="label">漢字の読み</div><div class="value">${{sections.kanji}}/${{sections.kanjiT}}</div></div>
<div class="result-item"><div class="label">語彙・表記</div><div class="value">${{sections.vocab}}/${{sections.vocabT}}</div></div>
<div class="result-item"><div class="label">言い換え</div><div class="value">${{sections.paraphrase}}/${{sections.paraphraseT}}</div></div>
<div class="result-item"><div class="label">文法</div><div class="value">${{sections.grammar}}/${{sections.grammarT}}</div></div>
<div class="result-item"><div class="label">文の組み立て</div><div class="value">${{sections.sentence}}/${{sections.sentenceT}}</div></div>
<div class="result-item"><div class="label">読解</div><div class="value">${{sections.reading}}/${{sections.readingT}}</div></div>
<div class="result-item"><div class="label">所要時間</div><div class="value">${{Math.floor(timeUsed/60)}}分${{timeUsed%60}}秒</div></div>
`;
document.getElementById('submitBtn').disabled=true;
panel.scrollIntoView({{behavior:'smooth'}});
}}
startTimer();
</script>
</body>
</html>'''

    return template.format(
        vnum=vnum,
        q1_html=q1_html,
        q2_html=q2_html,
        q3_html=q3_html,
        q4_html=q4_html,
        q5_html=q5_html,
        q6_html=q6_html,
        q7_html=q7_html,
        q8_html=q8_html,
        q9_html=q9_html,
        q10_html=q10_html,
    )

def main():
    random.seed(42)
    for v in range(1, 21):  # v11 to v30
        html = generate_html(v)
        out_path = os.path.join(OUTPUT_DIR, f"n5-10min-test-v{10+v}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created {out_path}")

if __name__ == "__main__":
    main()
