#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""J.TEST A-C 0315ゴイさん用 HTMLテスト生成スクリプト"""

# 解答: 1-indexed (1,2,3,4)
ANSWERS = {
    1:1, 2:4, 3:1, 4:2, 5:3, 6:3, 7:3, 8:2, 9:3, 10:4,
    11:3, 12:1, 13:2, 14:1, 15:2, 16:1, 17:3, 18:1, 19:4, 20:3,
    21:3, 22:3, 23:4, 24:1, 25:1, 26:2, 27:4, 28:3, 29:3, 30:1,
    31:2, 32:3, 33:3, 34:4, 35:4, 36:1, 37:2, 38:3, 39:2, 40:4,
    41:1, 42:4, 43:1, 44:4, 45:4, 46:2, 47:2, 48:4, 49:3, 50:2, 51:1,
}

def opt_val(q_num, opt_idx):
    """option index 1-4 -> value '1' if correct else '0'"""
    return '1' if ANSWERS.get(q_num) == opt_idx else '0'

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def escape_passage(s):
    """Passage用：rubyタグを保持したままエスケープ"""
    s = s.replace('<ruby>', '\uE001').replace('</ruby>', '\uE002').replace('<rt>', '\uE003').replace('</rt>', '\uE004')
    s = escape(s)
    s = s.replace('\uE001', '<ruby>').replace('\uE002', '</ruby>').replace('\uE003', '<rt>').replace('\uE004', '</rt>')
    return s

# 問題データ: (問題文, [選択肢1,2,3,4], 解説)
QUESTIONS_A = [
    ('やると言った（　）<ruby>途中<rt>とちゅう</rt></ruby>でやめることはできない。', ['からには', 'ついでに', 'ばかりか', 'わりに'], '「〜からには」＝「〜と決めた以上は」という意味で、責任や義務を表す。'),
    ('雨が降るとわかっていたら、<ruby>傘<rt>かさ</rt></ruby>を（　）んだった。', ['持って来たい', '持って来ている', '持って来なかった', '持って来る'], '「〜るんだった」は過去の後悔を表す表現。「持って来るんだった」＝「持って来ればよかった」。'),
    ('<ruby>藤田<rt>ふじた</rt></ruby>様（　）おかれましては、大変ご<ruby>活躍<rt>かつやく</rt></ruby>のことと存じます。', ['に', 'を', 'が', 'と'], '「〜におかれましては」は手紙やスピーチで使う最上級の敬語表現。'),
    ('元気だと<ruby>嘘<rt>うそ</rt></ruby>を（　）母に<ruby>心配<rt>しんぱい</rt></ruby>をかけたくなかった。', ['つくまい', 'ついてでも', 'ついたきり', 'つくくらいなら'], '「〜てでも」＝「たとえ〜という手段をとってでも」という意味。'),
    ('<ruby>課長<rt>かちょう</rt></ruby>に<ruby>褒<rt>ほ</rt></ruby>められて、<ruby>佐伯<rt>さえき</rt></ruby>さんは（　）げだ。', ['うれしく', 'うれしい', 'うれし', 'うれしくて'], '「〜げだ」は形容詞の語幹につける。「うれしい」→語幹「うれし」→「うれしげだ」。'),
    ('昨日（　）うってかわって今日の<ruby>部長<rt>ぶちょう</rt></ruby>は<ruby>機嫌<rt>きげん</rt></ruby>がいい。', ['も', 'では', 'とは', 'には'], '「昨日とはうってかわって」は慣用的な表現。「〜とはまったく変わって」の意味。'),
    ('<ruby>皆<rt>みな</rt></ruby>さん！<ruby>未来<rt>みらい</rt></ruby>の<ruby>子供達<rt>こどもたち</rt></ruby>のために、<ruby>安心<rt>あんしん</rt></ruby>して<ruby>暮<rt>く</rt></ruby>らせる町を一緒に（　）じゃありませんか！', ['作らない', '作って', '作ろう', '作る'], '「〜ようじゃありませんか」＝「一緒に〜しましょう」という呼びかけの表現。'),
    ('<ruby>事業計画<rt>じぎょうけいかく</rt></ruby>の<ruby>変更<rt>へんこう</rt></ruby>は、<ruby>市場<rt>しじょう</rt></ruby>の<ruby>変化<rt>へんか</rt></ruby>を受けての（　）だという。', ['ところ', 'こと', 'わけ', 'うち'], '「〜を受けてのことだ」＝「〜に対応した結果のことだ」という意味。'),
    ('<ruby>部長<rt>ぶちょう</rt></ruby>は<ruby>報告書<rt>ほうこくしょ</rt></ruby>に目を（　）なり、すぐに直すよう<ruby>指示<rt>しじ</rt></ruby>を出した。', ['通す', '通そう', '通した', '通して'], '「〜たなり」＝「〜するとすぐに（次の動作に移った）」という意味。'),
    ('彼は<ruby>上司<rt>じょうし</rt></ruby>がいないの（　）、仕事をしないでサボっていた。', ['にひきかえ', 'をもって', 'とあれば', 'をいいことに'], '「〜をいいことに」＝「〜という有利な状況を利用して（よくないことをする）」という意味。'),
    ('<ruby>育児<rt>いくじ</rt></ruby>（　）、その他の<ruby>家事<rt>かじ</rt></ruby>が<ruby>疎<rt>おろそ</rt></ruby>かになってしまった。', ['の極みで', 'に即して', 'にかまけて', 'といえども'], '「〜にかまけて」＝「〜に気を取られすぎて、他のことをおろそかにして」という意味。'),
    ('いくら（　）ところで、<ruby>破棄<rt>はき</rt></ruby>された<ruby>契約<rt>けいやく</rt></ruby>は元には戻らない。', ['謝った', '謝って', '謝る', '謝れば'], '「いくら〜たところで」＝「どれだけ〜しても（結果は変わらない）」という意味。'),
    ('<ruby>怪我<rt>けが</rt></ruby>をしているのに無理をしたら、治る（　）も治らない。', ['だけ', 'もの', 'こと', 'ところ'], '「治るものも治らない」＝「本来なら治るはずのものまで治らなくなる」という慣用表現。'),
    ('理由（　）いかんを問わず、チケットの<ruby>払い戻し<rt>はらいもどし</rt></ruby>は<ruby>致<rt>いた</rt></ruby>しません。', ['の', 'で', 'に', 'を'], '「〜のいかんを問わず」は「〜がどのようなものであっても関係なく」という慣用表現。'),
    ('車の窓から空き缶を道路に捨てるなんて、<ruby>非常識<rt>ひじょうしき</rt></ruby>（　）。', ['でも無理はない', 'にもほどがある', 'なものとする', 'だとか何とかだ'], '「〜にもほどがある」＝「〜にも限度がある・いくらなんでもひどすぎる」という意味。'),
    ('A：「明日の<ruby>会議<rt>かいぎ</rt></ruby>でビデオを見せるそうですね」<br>B：「（　）、5分ぐらいの短いものですよ」', ['ビデオといっても', 'ビデオというより', 'ビデオかのように', 'ビデオだからといって'], '「〜といっても」＝「〜と言っているが、実際はそれほどではない」という意味。'),
    ('A：「もう少し<ruby>金額<rt>きんがく</rt></ruby>を下げてもらうことはできませんか」<br>B：「（　）できると思います。数やお届け日のご<ruby>希望<rt>きぼう</rt></ruby>を教えてください」', ['条件をめぐって', '条件どころか', '条件次第では', '条件というと'], '「〜次第では」＝「〜の内容によっては（可能性がある）」という意味。'),
    ('<ruby>鈴木<rt>すずき</rt></ruby>：「あれ、<ruby>中井<rt>なかい</rt></ruby>さんは？」<br><ruby>山崎<rt>やまさき</rt></ruby>：「<ruby>作業<rt>さぎょう</rt></ruby><ruby>終了<rt>しゅうりょう</rt></ruby>のベルが（　）出て行きましたよ」', ['鳴ったかと思うと', '鳴るにあたって', '鳴った上は', '鳴りもしないで'], '「〜かと思うと」＝「〜したと思ったらすぐに（次のことが起きた）」という意味。'),
    ('A：「今から帰っても、お子さんはもう寝ている時間ですね」<br>B：「うん。でも、娘の寝顔も（　）」', ['かわいくなければそれまでだ', 'かわいくないものを', 'かわいいきらいがある', 'かわいいといったらないんだ'], '「〜といったらない（んだ）」＝「どれほど〜か言葉では表せないほどだ」という意味。'),
    ('A：「<ruby>専門家<rt>せんもんか</rt></ruby>が問題に<ruby>対応<rt>たいおう</rt></ruby>しているんですよね」<br>B：「ええ。しかし、彼らの（　）、<ruby>解決<rt>かいけつ</rt></ruby>は<ruby>困難<rt>こんなん</rt></ruby>のようです」', ['知識ならまだしも', '知識をものともせず', '知識をもってしても', '知識をおいて'], '「〜をもってしても」＝「〜を使っても・〜の力を借りても（それでもなお）」という意味。'),
]

QUESTIONS_B = [
    ('<ruby>晩<rt>ばん</rt></ruby>ご飯を作った時に（　）<ruby>材料<rt>ざいりょう</rt></ruby>で、次の日の<ruby>朝<rt>あさ</rt></ruby>ご飯を作った。', ['吐いた', '組んだ', '余った', '枯れた'], '「余る」＝使い切れずに残る。「余った材料」＝使わずに残った食材。'),
    ('毎年、<ruby>花見<rt>はなみ</rt></ruby>や<ruby>運動会<rt>うんどうかい</rt></ruby>など会社の（　）に参加している。', ['事件', '<ruby>秘密<rt>ひみつ</rt></ruby>', '<ruby>行事<rt>ぎょうじ</rt></ruby>', '<ruby>思い出<rt>おもいで</rt></ruby>'], '「行事」＝決まった時期に行われるイベント・催し物のこと。'),
    ('<ruby>陸上<rt>りくじょう</rt></ruby><ruby>選手<rt>せんしゅ</rt></ruby>の彼は、毎日（　）を走っている。', ['トレーニング', 'ヘリコプター', 'カロリー', 'グラウンド'], '「グラウンド」＝運動場・競技場。「グラウンドを走る」は自然な表現。'),
    ('私は（　）ので、よく<ruby>失敗<rt>しっぱい</rt></ruby>をする。', ['そそっかしい', 'あっけない', 'まぶしい', '等しい'], '「そそっかしい」＝落ち着きがなく、うっかりミスをしやすい性格。'),
    ('<ruby>片付<rt>かたづ</rt></ruby>けが済み、<ruby>部屋<rt>へや</rt></ruby>が（　）した。', ['すっきり', 'ぴったり', 'ばったり', 'にっこり'], '「すっきりする」＝散らかりがなくなってきれいに整った様子。'),
    ('一年前事故にあって、<ruby>命<rt>いのち</rt></ruby>も（　）なるほどの大けがをした。', ['<ruby>甚<rt>はなは</rt></ruby>だしく', '<ruby>危<rt>あや</rt></ruby>うく', '<ruby>険<rt>けわ</rt></ruby>しく', 'きつく'], '「命も危うくなるほど」＝命が危険になりそうなほどの大けが。'),
    ('私は<ruby>宣伝<rt>せんでん</rt></ruby>方法のアイディアを出すことで売り上げに（　）している。', ['<ruby>尊重<rt>そんちょう</rt></ruby>', '<ruby>循環<rt>じゅんかん</rt></ruby>', '<ruby>発揮<rt>はっき</rt></ruby>', '<ruby>貢献<rt>こうけん</rt></ruby>'], '「貢献する」＝役に立つ・力を与える。「売り上げに貢献する」は自然なビジネス表現。'),
    ('新しいシステムを<ruby>導入<rt>どうにゅう</rt></ruby>することが良いとは、（　）言えない。', ['ひいては', 'まして', '<ruby>一概<rt>いちがい</rt></ruby>に', 'ことごとく'], '「一概に言えない」＝一律に・すべての場合に当てはまるとは言えない。'),
    ('ご（　）いただきましたとおり、この<ruby>企画<rt>きかく</rt></ruby>には問題点がありました。', ['<ruby>勧誘<rt>かんゆう</rt></ruby>', '<ruby>決断<rt>けつだん</rt></ruby>', '<ruby>指摘<rt>してき</rt></ruby>', '<ruby>寄贈<rt>きぞう</rt></ruby>'], '「ご指摘いただきましたとおり」＝「おっしゃった通り・教えていただいた通り」。'),
    ('（　）が<ruby>滞<rt>とどこお</rt></ruby>り、<ruby>品揃<rt>しなぞろ</rt></ruby>えに<ruby>影響<rt>えいきょう</rt></ruby>が出ている。', ['<ruby>物流<rt>ぶつりゅう</rt></ruby>', '<ruby>品質<rt>ひんしつ</rt></ruby>', '<ruby>論議<rt>ろんぎ</rt></ruby>', '<ruby>豊作<rt>ほうさく</rt></ruby>'], '「物流が滞る」＝商品の輸送・流通がスムーズに進まないこと。'),
]

QUESTIONS_C = [
    ('その<ruby>会議<rt>かいぎ</rt></ruby>には<strong>出ないわけにはいかない</strong>。', ['出ないつもりだ', '出なければならない', '出たことがない', '出ないほうがいい'], '「〜ないわけにはいかない」＝「必ず〜しなければならない」。二重否定で強い義務を表す。'),
    ('最近、ちょっとしたことで<strong><ruby>腹<rt>はら</rt></ruby>が立って</strong>しまう。', ['疲れて', '泣いて', '怒って', '喜んで'], '「腹が立つ」は「怒る・腹を立てる」という意味の慣用句。'),
    ('新しい靴を<ruby>履<rt>は</rt></ruby>いてみたら、少し<strong><ruby>緩<rt>ゆる</rt></ruby>かった</strong>。', ['柔らかかった', '固かった', '大きかった', '小さかった'], '「緩い（ゆるい）」は靴・服などが体に対してゆったりしすぎている状態。靴が緩い＝サイズが大きい。'),
    ('<ruby>商品<rt>しょうひん</rt></ruby>についての詳しい説明は<strong><ruby>省<rt>はぶ</rt></ruby>きます</strong>。', ['後でします', '書きました', '聞きたいです', 'しません'], '「省く（はぶく）」＝省略する・省いて行わない。「説明を省く」＝説明をしない。'),
    ('今年入社した<ruby>社員<rt>しゃいん</rt></ruby>は<strong><ruby>素直<rt>すなお</rt></ruby></strong>だが、自分から<ruby>積極的<rt>せっきょくてき</rt></ruby>に仕事をしない。', ['丁寧で礼儀正しい', '頭が良くて知識が多い', '何でも一生懸命にする', '他の人の意見をよく聞く'], '「素直」＝ひねくれず、人の言うことをそのまま受け入れる性格。'),
    ('<ruby>機械<rt>きかい</rt></ruby>の<ruby>故障<rt>こしょう</rt></ruby>は<strong>まれに起こる</strong>。', ['めったに起こらない', '起こったことがない', '起こるかもしれない', 'よく起こる'], '「まれに」＝ほとんどない・非常に少ない頻度で。「まれに起こる」＝ごくたまに起こる。'),
    ('その件を<ruby>課長<rt>かちょう</rt></ruby>は<strong><ruby>誤解<rt>ごかい</rt></ruby>している</strong>。', ['よく理解している', '間違った理解をしている', '解説できない', 'まだ把握していない'], '「誤解」＝「誤った解釈・理解」のこと。'),
    ('彼女の<ruby>発想<rt>はっそう</rt></ruby>は<strong>ユニーク</strong>だ。', ['ありふれている', '<ruby>柔軟<rt>じゅうなん</rt></ruby>だ', '独特だ', '<ruby>魅力的<rt>みりょくてき</rt></ruby>だ'], '「ユニーク」＝他にはない・唯一の・独自の。「独特」と同義。'),
    ('私が通っていた高校は<strong><ruby>規則<rt>きそく</rt></ruby>ずくめ</strong>だった。', ['規則を守らない生徒が多かった', '規則が非常に多かった', '規則正しい生徒が多かった', '規則に厳しくなかった'], '「〜ずくめ」＝「〜だらけ・〜ばかり・〜が非常に多い」という意味の接尾語。'),
    ('<ruby>請求書<rt>せいきゅうしょ</rt></ruby>の山を見て、<strong>途方にくれた</strong>。', ['同情した', '怒りが湧いた', '興奮した', '困り果てた'], '「途方にくれる」＝どうすればいいかわからなくて、すっかり困り果てる。'),
]

READING_PASSAGES = [
    '''2026/03/03 11：15
<ruby>件名<rt>けんめい</rt></ruby>：3月6日に使用する<ruby>資料<rt>しりょう</rt></ruby>について

<ruby>渡辺<rt>わたなべ</rt></ruby><ruby>部長<rt>ぶちょう</rt></ruby>

お<ruby>疲<rt>つか</rt></ruby>れ様です。<ruby>黒木<rt>くろき</rt></ruby>です。

3月6日の<ruby>会議<rt>かいぎ</rt></ruby>に使用する<ruby>資料<rt>しりょう</rt></ruby>作りを<ruby>担当<rt>たんとう</rt></ruby>させてくださり、ありがとうございます。その<ruby>締め切り<rt>しめきり</rt></ruby>について伺いたく、メールいたしました。

<ruby>部長<rt>ぶちょう</rt></ruby>からは、3月4日の午前中までに作ったものを見せてほしいということでしたが、明日の午前中にお<ruby>客様<rt>きゃくさま</rt></ruby>との約束が入っています。
また、その際に<ruby>必要<rt>ひつよう</rt></ruby>な<ruby>書類<rt>しょるい</rt></ruby>を<ruby>準備<rt>じゅんび</rt></ruby>しなければならないので、<ruby>会議<rt>かいぎ</rt></ruby><ruby>資料<rt>しりょう</rt></ruby>を作り始められるのは明日の午後からとなってしまいます。

明日の午後から始めれば、5日の午前中に資料をお見せできると思います。
それで間に合うでしょうか。

<ruby>黒木<rt>くろき</rt></ruby>''',
    '''2026/03/06 10：35
<ruby>件名<rt>けんめい</rt></ruby>：新<ruby>製品<rt>せいひん</rt></ruby>「<ruby>風味<rt>ふうみ</rt></ruby>豊かな<ruby>野菜<rt>やさい</rt></ruby>スープ」<ruby>発表会<rt>はっぴょうかい</rt></ruby>のご<ruby>案内<rt>あんない</rt></ruby>

<ruby>株式会社<rt>かぶしきがいしゃ</rt></ruby>ゼンテン<ruby>商事<rt>しょうじ</rt></ruby>　<ruby>販売部<rt>はんばいぶ</rt></ruby>　<ruby>菅原<rt>すがわら</rt></ruby>様

お世話になっております。<ruby>株式会社<rt>かぶしきがいしゃ</rt></ruby><ruby>月美食品<rt>つきみしょくひん</rt></ruby><ruby>営業部<rt>えいぎょうぶ</rt></ruby>　<ruby>久保<rt>くぼ</rt></ruby>です。

さて、新<ruby>製品<rt>せいひん</rt></ruby><ruby>発表会<rt>はっぴょうかい</rt></ruby>のご<ruby>案内<rt>あんない</rt></ruby>です。<ruby>栄養<rt>えいよう</rt></ruby>バランスに優れ、つつも<ruby>野菜<rt>やさい</rt></ruby>のおいしさを感じられる「<ruby>風味<rt>ふうみ</rt></ruby>豊かな<ruby>野菜<rt>やさい</rt></ruby>スープ」を<ruby>数種類<rt>すうしゅるい</rt></ruby>の味で<ruby>発売<rt>はつばい</rt></ruby>する予定です。

つきましては、下記のとおり<ruby>発表会<rt>はっぴょうかい</rt></ruby>を行い、<ruby>試食<rt>ししょく</rt></ruby>していただき、ご<ruby>意見<rt>いけん</rt></ruby>・ご<ruby>感想<rt>かんそう</rt></ruby>をいただきたく存じます。ぜひお誘い合わせのうえ、ご出席くださいますようお願い申し上げます。なお、ご<ruby>来場<rt>らいじょう</rt></ruby>いただいた皆様には心ばかりのプレゼントをお渡しする予定です。お日にちが近づきましたら<ruby>文書<rt>ぶんしょ</rt></ruby>にてご<ruby>招待状<rt>しょうたいじょう</rt></ruby>をお送りいたします。

日時：2026年4月6日　午後1時〜3時
<ruby>会場<rt>かいじょう</rt></ruby>：東京都○○<ruby>青空町<rt>あおぞらちょう</rt></ruby>7-10-5　南センター5<ruby>階<rt>かい</rt></ruby>（<ruby>小西<rt>こにし</rt></ruby><ruby>駅<rt>えき</rt></ruby>下車徒歩3分）''',
    '''2026年3月12日
<ruby>営業部長<rt>えいぎょうぶちょう</rt></ruby>　<ruby>寺本<rt>てらもと</rt></ruby><ruby>正樹<rt>まさき</rt></ruby>　殿　　<ruby>長谷川<rt>はせがわ</rt></ruby><ruby>鈴子<rt>すずこ</rt></ruby>

新<ruby>製品<rt>せいひん</rt></ruby>RX556の<ruby>製造<rt>せいぞう</rt></ruby>の遅れについて、<ruby>長野<rt>ながの</rt></ruby><ruby>工場<rt>こうじょう</rt></ruby>に<ruby>状況<rt>じょうきょう</rt></ruby>を<ruby>確認<rt>かくにん</rt></ruby>するため、<ruby>出張<rt>しゅっちょう</rt></ruby>いたしましたので、ご<ruby>報告<rt>ほうこく</rt></ruby>いたします。

記
・<ruby>出張先<rt>しゅっちょうさき</rt></ruby>　<ruby>長野<rt>ながの</rt></ruby><ruby>工場<rt>こうじょう</rt></ruby>（<ruby>長野<rt>ながの</rt></ruby>県<ruby>長野<rt>ながの</rt></ruby>市）
・日時　　3月10日　8：00〜17：50
・<ruby>目的<rt>もくてき</rt></ruby>　　新<ruby>製品<rt>せいひん</rt></ruby>RX556の<ruby>製造<rt>せいぞう</rt></ruby>スケジュールについて打合せ
・<ruby>内容<rt>ないよう</rt></ruby>　　<ruby>長野<rt>ながの</rt></ruby><ruby>工場<rt>こうじょう</rt></ruby>訪問。<ruby>工場長<rt>こうじょうちょう</rt></ruby>から<ruby>事情<rt>じじょう</rt></ruby>の聞き取り

［聞き取りの<ruby>内容<rt>ないよう</rt></ruby>］
○RX556の<ruby>製造<rt>せいぞう</rt></ruby>の遅れについて
・RX556に使われている部品を作っている<ruby>工場<rt>こうじょう</rt></ruby>が、先月の大雨の<ruby>影響<rt>えいきょう</rt></ruby>で1週間作業を<ruby>停止<rt>ていし</rt></ruby>し、その後も<ruby>製造<rt>せいぞう</rt></ruby>が遅れている。その<ruby>結果<rt>けっか</rt></ruby>、RX556の<ruby>製造<rt>せいぞう</rt></ruby>が遅れた。他の<ruby>工場<rt>こうじょう</rt></ruby>の部品に<ruby>変更<rt>へんこう</rt></ruby>はできないとのこと。

○今後の<ruby>見通し<rt>みとおし</rt></ruby>
・RX556の<ruby>製造<rt>せいぞう</rt></ruby>は予定より10日ほど遅れているが、遅れは少しずつ取り戻している。<ruby>工場長<rt>こうじょうちょう</rt></ruby>の<ruby>予想<rt>よそう</rt></ruby>では、遅れは最終的に1週間程度になりそうだとのこと。

○<ruby>所感<rt>しょかん</rt></ruby>
・RX556の<ruby>販売<rt>はんばい</rt></ruby>スケジュールは多少<ruby>余裕<rt>よゆう</rt></ruby>があるので、1週間の遅れであれば、スケジュール<ruby>変更<rt>へんこう</rt></ruby>は必要ない。<ruby>工場長<rt>こうじょうちょう</rt></ruby>には、1週間以上の遅れは大きな問題になるので急いでほしいと伝えた。しかし、もしもの場合を考えて、<ruby>販売<rt>はんばい</rt></ruby>スケジュールの見直しも考えておくべきだと思う。

以上''',
    '''2026年4月1日
<ruby>株式会社<rt>かぶしきがいしゃ</rt></ruby>四つ葉<ruby>物産<rt>ぶっさん</rt></ruby>　御中
<ruby>株式会社<rt>かぶしきがいしゃ</rt></ruby><ruby>青山<rt>あおやま</rt></ruby>フーズ　<ruby>代表取締役<rt>だいひょうとりしまりやく</rt></ruby><ruby>社長<rt>しゃちょう</rt></ruby>　<ruby>小川<rt>おがわ</rt></ruby><ruby>雄弁<rt>ゆうべん</rt></ruby>

<ruby>価格<rt>かかく</rt></ruby><ruby>改定<rt>かいてい</rt></ruby>のお願い

<ruby>拝啓<rt>はいけい</rt></ruby>　貴社ますますご<ruby>清栄<rt>せいえい</rt></ruby>のこととお<ruby>慶<rt>よろこ</rt></ruby>び申し上げます。<ruby>平素<rt>へいそ</rt></ruby>は格別のご<ruby>高配<rt>こうはい</rt></ruby>を<ruby>賜<rt>たまわ</rt></ruby>り、厚く御礼申し上げます。
さて、この度は貴社より長年ご発注いただいております弊社のチョコパイシリーズにつきまして、<ruby>価格<rt>かかく</rt></ruby><ruby>改定<rt>かいてい</rt></ruby>をさせていただきたく思っております。
以前より<ruby>人件費<rt>じんけんひ</rt></ruby>、<ruby>燃料代<rt>ねんりょうだい</rt></ruby>などは<ruby>上昇<rt>じょうしょう</rt></ruby>しておりましたが、<ruby>原料<rt>げんりょう</rt></ruby>の<ruby>価格<rt>かかく</rt></ruby>を抑えることによって、近年の<ruby>物価高<rt>ぶっかこう</rt></ruby>で他<ruby>商品<rt>しょうひん</rt></ruby>を値上げせざるを得ない状況にあっても、弊社の<ruby>看板<rt>かんばん</rt></ruby><ruby>商品<rt>しょうひん</rt></ruby>であるチョコパイシリーズだけは、<ruby>価格<rt>かかく</rt></ruby>を維持してまいりました。
しかしながら、最近、<ruby>原料<rt>げんりょう</rt></ruby>の<ruby>乳製品<rt>にゅうせいひん</rt></ruby>の<ruby>価格<rt>かかく</rt></ruby>が<ruby>上昇<rt>じょうしょう</rt></ruby>し、それも<ruby>限界<rt>げんかい</rt></ruby>に達しております。
つきましては、誠に<ruby>心苦<rt>こころぐる</rt></ruby>しいのですが、2026年6月1日以降の<ruby>納品<rt>のうひん</rt></ruby>分から、以下の通り、<ruby>価格<rt>かかく</rt></ruby>を引き上げさせていただきたく、何卒ご理解のほど、よろしくお願い申し上げます。

記
ミルクチョコパイ6個入　1箱　380円→420円
ミニチョコパイ8個入　　1箱　260円→290円

以上

今後も変わらぬご<ruby>愛顧<rt>あいこ</rt></ruby>のほど、よろしくお願い申し上げます。

<ruby>敬具<rt>けいぐ</rt></ruby>''',
    '''私が<ruby>作家<rt>さっか</rt></ruby>になりたいと思ったのは何時頃だったか。中学2年生くらいの時にはすでにぼんやりと考えており、少なくとも高校の<ruby>卒業<rt>そつぎょう</rt></ruby>アルバムにある将来の夢の欄には小説家と書いていた。
だが10代、20代は一度も書こうとはしなかった。私は<ruby>文芸誌<rt>ぶんげいし</rt></ruby>を読むような高校生だった。そこには憧れの歴史小説家たちのエッセイ、<ruby>対談<rt>たいだん</rt></ruby>などが掲載されているのだが、どの先生も口を揃えて、
――小説の勉強をするよりも、人生経験を積むべき。
と、<ruby>仰<rt>おっしゃ</rt></ruby>っていたからである。小説の勉強が無駄という訳ではない。ただそれよりも大切なことがあるといったような内容であった。そして私はまだその時ではないと本気で思っていた。

（<ruby>文芸誌<rt>ぶんげいし</rt></ruby>…小説や詩、<ruby>随筆<rt>ずいひつ</rt></ruby>などの文学作品が中心の雑誌）
（<ruby>対談<rt>たいだん</rt></ruby>…あるテーマについて二人で話したもの）''',
    '''人手が足りないといつも<ruby>嘆<rt>なげ</rt></ruby>いている<ruby>企業<rt>きぎょう</rt></ruby>は、自分たちの仕事内容や<ruby>将来性<rt>しょうらいせい</rt></ruby>、あるいは<ruby>賃金<rt>ちんぎん</rt></ruby>や<ruby>待遇<rt>たいぐう</rt></ruby>などの待遇が「<ruby>魅力的<rt>みりょくてき</rt></ruby>ではない」と思われているのだと、早めにわが身を振り返るべきです。
仕事を選ぶ基準は、人それぞれの<ruby>価値観<rt>かちかん</rt></ruby>によって違います。
「給料だけがすべてではないし」と面白そうで給料の安い仕事を選ぶ人もいれば、つまらなそうで高い仕事を選ぶ人もいます。その判断基準は、それぞれの<ruby>価値観<rt>かちかん</rt></ruby>になってきます。
だからこそ人を集めたい<ruby>企業<rt>きぎょう</rt></ruby>は、自分たちの会社の<ruby>魅力<rt>みりょく</rt></ruby>は何なのか、仕事自体の<ruby>魅力<rt>みりょく</rt></ruby>なのか、<ruby>将来性<rt>しょうらいせい</rt></ruby>なのか、<ruby>賃金<rt>ちんぎん</rt></ruby>なのか……などと、よく考えるべきです。

（わが身を振り返る…自分の発言や行動を反省する）''',
    '''<ruby>松本<rt>まつもと</rt></ruby>市で8月11日〜9月9日に開くセイジ・オザワ<ruby>松本<rt>まつもと</rt></ruby>フェスティバル（OMF）の<ruby>実行<rt>じっこう</rt></ruby><ruby>委員会<rt>いいんかい</rt></ruby>は今月19日まで、<ruby>公演<rt>こうえん</rt></ruby>の運営を担うボランティア組織「OMFコンチェルト」の新規メンバーを募集している。<ruby>活動<rt>かつどう</rt></ruby>期間は7月20日〜9月9日。チケット確認や会場のドアの開閉、グッズ<ruby>販売<rt>はんばい</rt></ruby>、会場案内などを担う。
高校生を除く18歳以上が対象で、<ruby>活動<rt>かつどう</rt></ruby>日は申し込み後に調整する。7月26日午後1時から市まつもと市民<ruby>芸術館<rt>げいじゅつかん</rt></ruby>で開く<ruby>研修会<rt>けんしゅうかい</rt></ruby>に参加できることが<ruby>条件<rt>じょうけん</rt></ruby>。<ruby>登録<rt>とうろく</rt></ruby>フォームから申し込む。顔写真が必要。今月20日以降に<ruby>実行<rt>じっこう</rt></ruby>委事務局が<ruby>活動<rt>かつどう</rt></ruby>希望調査票をメールで送る。

（グッズ<ruby>販売<rt>はんばい</rt></ruby>…<ruby>公演<rt>こうえん</rt></ruby>に関係する商品を販売すること）''',
]

READING_QUESTIONS = [
    (41, '<ruby>渡辺<rt>わたなべ</rt></ruby><ruby>部長<rt>ぶちょう</rt></ruby>は<ruby>黒木<rt>くろき</rt></ruby>さんに何を頼みましたか。', ['<ruby>資料<rt>しりょう</rt></ruby>を作ること', '<ruby>会議<rt>かいぎ</rt></ruby>の日を変えること', '<ruby>資料<rt>しりょう</rt></ruby>を<ruby>客<rt>きゃく</rt></ruby>に送ること', '<ruby>資料<rt>しりょう</rt></ruby>の<ruby>内容<rt>ないよう</rt></ruby>を直すこと'], 'メールの冒頭に「3月6日の会議に使用する資料作りを担当させてくださり」とある。部長が依頼したのは資料を作ること。'),
    (42, '<ruby>黒木<rt>くろき</rt></ruby>さんは3月4日の午前にどんな予定がありますか。', ['<ruby>会議<rt>かいぎ</rt></ruby>に出席する予定', '<ruby>渡辺<rt>わたなべ</rt></ruby><ruby>部長<rt>ぶちょう</rt></ruby>に<ruby>会議<rt>かいぎ</rt></ruby><ruby>資料<rt>しりょう</rt></ruby>を見せる予定', '<ruby>客<rt>きゃく</rt></ruby>に渡す<ruby>書類<rt>しょるい</rt></ruby>を<ruby>準備<rt>じゅんび</rt></ruby>する予定', '<ruby>客<rt>きゃく</rt></ruby>と会う予定'], 'メールに「明日（＝3月4日）の午前中にお客様との約束が入っています」とある。'),
    (43, '新<ruby>製品<rt>せいひん</rt></ruby>について、メールの内容と合っているのはどれですか。', ['<ruby>栄養<rt>えいよう</rt></ruby>のバランスが良い。', '<ruby>野菜<rt>やさい</rt></ruby>の味をあまり感じない。', '味の<ruby>種類<rt>しゅるい</rt></ruby>は1<ruby>種類<rt>しゅるい</rt></ruby>である。', 'ゼンテン<ruby>商事<rt>しょうじ</rt></ruby>が作った<ruby>商品<rt>しょうひん</rt></ruby>である。'], 'メールに「栄養バランスに優れ」とある→1が正しい。'),
    (44, 'メールの<ruby>内容<rt>ないよう</rt></ruby>と合っているのはどれですか。', ['<ruby>発表会<rt>はっぴょうかい</rt></ruby>に出席するかどうかをメールで返事しなければならない。', '<ruby>発表会<rt>はっぴょうかい</rt></ruby>に参加しなくても、新<ruby>製品<rt>せいひん</rt></ruby>をプレゼントとしてもらえる。', '<ruby>発表会<rt>はっぴょうかい</rt></ruby>に参加できるのは、各<ruby>会社<rt>かいしゃ</rt></ruby>1人である。', '後で<ruby>招待状<rt>しょうたいじょう</rt></ruby>が送られる。'], '「お日にちが近づきましたら文書にてご招待状をお送りいたします」とある→4が正しい。'),
    (45, '<ruby>長谷川<rt>はせがわ</rt></ruby>さんが<ruby>出張<rt>しゅっちょう</rt></ruby>で<ruby>確認<rt>かくにん</rt></ruby>できたこととは何ですか。', ['RX556の部品を<ruby>製造<rt>せいぞう</rt></ruby>している<ruby>工場<rt>こうじょう</rt></ruby>が、<ruby>現在<rt>げんざい</rt></ruby>動いていない理由', 'RX556の部品がない理由と<ruby>工場長<rt>こうじょうちょう</rt></ruby>が今まで行ってきた<ruby>対応<rt>たいおう</rt></ruby>', 'RX556の<ruby>製造<rt>せいぞう</rt></ruby>のための部品の<ruby>変更<rt>へんこう</rt></ruby>の決定と、今後の予定', 'RX556の<ruby>製造<rt>せいぞう</rt></ruby>が遅れた理由と、今後どの程度遅れるかという<ruby>予想<rt>よそう</rt></ruby>'], '聞き取りの内容に①遅れた理由、②今後の見通し（1週間程度の遅れ）がある。'),
    (46, '<ruby>長谷川<rt>はせがわ</rt></ruby>さんは、これから何をしたほうがいいと言っていますか。', ['<ruby>工場長<rt>こうじょうちょう</rt></ruby>にこれ以上遅れないように厳しく注意すること', '<ruby>工場長<rt>こうじょうちょう</rt></ruby>の<ruby>予想<rt>よそう</rt></ruby>と違った場合の<ruby>対応<rt>たいおう</rt></ruby>を考えておくこと', 'RX556の<ruby>販売<rt>はんばい</rt></ruby>スケジュールを<ruby>大幅<rt>おおはば</rt></ruby>に<ruby>変更<rt>へんこう</rt></ruby>すること', '<ruby>製造<rt>せいぞう</rt></ruby>の遅れを取り戻すための方法を考えておくこと'], '所感に「もしもの場合を考えて、販売スケジュールの見直しも考えておくべきだと思う」とある。'),
    (47, '<ruby>青山<rt>あおやま</rt></ruby>フーズでは、どうしてチョコパイシリーズの値上げをすることにしましたか。', ['<ruby>人件費<rt>じんけんひ</rt></ruby>が高くなったから', '<ruby>乳製品<rt>にゅうせいひん</rt></ruby>の<ruby>価格<rt>かかく</rt></ruby>が高くなったから', '<ruby>燃料代<rt>ねんりょうだい</rt></ruby>が高くなったから', '<ruby>物価<rt>ぶっか</rt></ruby>が高くなったから'], '今回値上げの直接の理由は「最近、原料の乳製品の価格が上昇し、それも限界に達した」から。'),
    (48, '文書の内容と合っているのはどれですか。', ['四つ葉<ruby>物産<rt>ぶっさん</rt></ruby>は<ruby>青山<rt>あおやま</rt></ruby>フーズのチョコパイを初めて注文した。', '<ruby>青山<rt>あおやま</rt></ruby>フーズのチョコパイの値上げは過去にも行われている。', '<ruby>青山<rt>あおやま</rt></ruby>フーズのチョコパイ以外の<ruby>商品<rt>しょうひん</rt></ruby>はまだ一度も値上げしていない。', '<ruby>青山<rt>あおやま</rt></ruby>フーズのチョコパイは6月1日以降の<ruby>納品<rt>のうひん</rt></ruby>分から値上げする。'], '「2026年6月1日以降の納品分から価格を引き上げさせていただきたく」とある。'),
    (49, '「その時ではない」とありますが、何をする時ではないと筆者は考えましたか。', ['将来の夢を他人に言う時', '人生経験を積む時', '小説の勉強をする時', '<ruby>文芸誌<rt>ぶんげいし</rt></ruby>を読む時'], '先生たちは「小説の勉強をするよりも、人生経験を積むべき」と言っていた。筆者は「まだその時ではない（＝小説の勉強をする時ではない）」と思った。'),
    (50, '筆者の考えに最も近いのはどれですか。', ['<ruby>慢性的<rt>まんせいてき</rt></ruby>な人手不足に悩んでいる<ruby>企業<rt>きぎょう</rt></ruby>に<ruby>魅力<rt>みりょく</rt></ruby>は感じられないので、対策を立てても人は集まらない。', '仕事を選ぶ基準は人それぞれ異なるため、人を集めるためには自社の<ruby>魅力<rt>みりょく</rt></ruby>を見直すべきである。', '給料が高ければ人は自然と集まるので、<ruby>企業<rt>きぎょう</rt></ruby>はもっと<ruby>賃金<rt>ちんぎん</rt></ruby>を<ruby>重視<rt>じゅうし</rt></ruby>したほうがいい。', '仕事内容より<ruby>将来性<rt>しょうらいせい</rt></ruby>を強調すれば<ruby>優秀<rt>ゆうしゅう</rt></ruby>な<ruby>人材<rt>じんざい</rt></ruby>が集まりやすい。'], '①仕事を選ぶ基準は人それぞれ、②人を集めたい企業は自社の魅力をよく考えるべき、の2点。'),
    (51, '<ruby>活動<rt>かつどう</rt></ruby>日について、文章の内容と合っているのはどれですか。', ['メンバーは7月20日にメールで<ruby>活動<rt>かつどう</rt></ruby>日を知らされる。', '7月26日は全メンバーが参加しなければならない。', 'フェスティバル期間中は全日程参加しなければならない。', 'フェスティバル終了後も<ruby>活動<rt>かつどう</rt></ruby>がある。'], '「今月20日以降に活動希望調査票をメールで送る」。申し込み後に活動日が調整され、メールで知らされる。'),
]

def gen_question_html(q_num, q_text, options, explanation, is_reading=False, passage=None):
    ans = ANSWERS[q_num]
    opts_html = []
    for i, opt in enumerate(options, 1):
        v = opt_val(q_num, i)
        lid = f'q{q_num}{chr(97+i-1)}'
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
<title>過去問J.TEST A-C 2026年3月度（80分・51問）</title>
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
<h1>過去問J.TEST A-C 2026年3月度（80分・51問）</h1>
<div class="header-info">
<div class="timer" id="timer">80:00</div>
<div class="progress-bar"><div class="progress-fill" id="progress" style="width:100%"></div></div>
<div class="score-badge" id="scoreBadge">全51問</div>
</div>
</header>
''')

    # Section A
    out.append('''<div class="section">
<div class="section-title">文法・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> A — （　）に最も適当な言葉を入れなさい（20問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">次の文の（　）に1・2・3・4の中から最も適当な言葉を入れなさい。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_A, 1):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Section B
    out.append('''<div class="section">
<div class="section-title">文法・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> B — （　）に最も適当な言葉を入れなさい（10問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">次の文の（　）に1・2・3・4の中から最も適当な言葉を入れなさい。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_B, 21):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Section C
    out.append('''<div class="section">
<div class="section-title">文法・<ruby>語彙<rt>ごい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> C — 意味に最も近いものを選びなさい（10問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">次の文の＿＿＿の意味に最も近いものを1・2・3・4の中から選びなさい。</p>
''')
    for i, (q, opts, expl) in enumerate(QUESTIONS_C, 31):
        out.append(gen_question_html(i, q, opts, expl))
    out.append('</div>')

    # Reading - need to group by passage
    passage_idx = [0,0,1,1,2,2,3,3,4,5,6]  # Q41-51
    for idx, (qnum, q, opts, expl) in enumerate(READING_QUESTIONS):
        pid = passage_idx[idx]
        passage = READING_PASSAGES[pid] if pid < len(READING_PASSAGES) else None
        # Show passage only for first question of each passage group
        prev_pid = passage_idx[idx-1] if idx > 0 else -1
        show_passage = (idx == 0) or (pid != prev_pid)
        p = passage if show_passage else None
        html = gen_question_html(qnum, q, opts, expl, is_reading=True, passage=p)
        if idx == 0:
            out.append('''<div class="section">
<div class="section-title"><ruby>読解<rt>どっかい</rt></ruby><ruby>問題<rt>もんだい</rt></ruby> — 文章を読んで<ruby>問題<rt>もんだい</rt></ruby>に答えなさい（11問）</div>
<p style="color:#718096;font-size:.9em;margin-bottom:12px">答えは1・2・3・4の中から最も適当なものを1つ選びなさい。</p>
''')
        out.append(html)
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
const TOTAL=51,TIME_LIMIT=4800;
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
const sections={grammarA:0,grammarAT:20,grammarB:0,grammarBT:10,vocabC:0,vocabCT:10,reading:0,readingT:11};
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
if(i<=20){if(isCorrect)sections.grammarA++;}
else if(i<=30){if(isCorrect)sections.grammarB++;}
else if(i<=40){if(isCorrect)sections.vocabC++;}
else{if(isCorrect)sections.reading++;}
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
<div class="result-item"><div class="label">文法A</div><div class="value">${sections.grammarA}/${sections.grammarAT}</div></div>
<div class="result-item"><div class="label">文法B</div><div class="value">${sections.grammarB}/${sections.grammarBT}</div></div>
<div class="result-item"><div class="label">語彙C</div><div class="value">${sections.vocabC}/${sections.vocabCT}</div></div>
<div class="result-item"><div class="label">読解</div><div class="value">${sections.reading}/${sections.readingT}</div></div>
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
    # Fix: explanation div uses HTML in q_text for <br>
    html = html.replace('&lt;br&gt;', '<br>')
    with open('/Users/hayashi./datax/Business/school/J.TEST/202603student/jtest-ac-0315-goi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Generated: jtest-ac-0315-goi.html')

if __name__ == '__main__':
    main()
