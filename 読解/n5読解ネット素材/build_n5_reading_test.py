#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N5読解まとめ.md の長文読解問題から n5-reading-test.html を生成する。
テンプレートは N4 読解テスト（jlpt-kakunin-test-deploy/n4-reading-test.html）と同構成:
- view-hub（数字アイコンでテスト選択）/ view-work（work-headヘッダー＋タイマー＋一時停止）
- 本文(左)・設問(右)の material-group、狭い画面は上下分割で本文 sticky
- テーマ色は N5 の紫 (#667eea → #764ba2)
文中の {漢字|よみ} は <ruby> に変換される。
"""
import re, html

RUBY = re.compile(r"\{([^|{}]+)\|([^|{}]+)\}")

def r(text):
    return RUBY.sub(r"<ruby>\1<rt>\2</rt></ruby>", text)

# ──────────────────────────────────────────────
# ブロック定義: passage は HTML 断片のリスト（<p>等は自動付与しない）
# questions: (stem, [options×4], correct(1-4), note)
# ──────────────────────────────────────────────

def P(*paras):
    return "".join(f"<p>{r(p)}</p>" for p in paras)

def BOX(head, body):
    return f'<div class="passage-box"><div class="box-head">{r(head)}</div>{r(body)}</div>'

def DLG(*lines):
    out = []
    for speaker, text in lines:
        if speaker:
            out.append(f'<p><span class="speaker">{r(speaker)}</span>{r(text)}</p>')
        else:
            out.append(f"<p>{r(text)}</p>")
    return "".join(out)

BLOCKS = [
# 0 ── 公式2009 もんだい5
dict(title="No.01 公式2009 ヤンさんのうち",
 passage=P(
  "ヤンさんのうちは{町|まち}の{中|なか}のべんりなところにあります。",
  "となりにパンやがあります。{前|まえ}ははなやで、はなやのとなりはさかなやです。{近|ちか}くにくすりやとにくやもあります。ゆうびんきょくとびょういんもあります。",
  "{今日|きょう}のゆうがた、ヤンさんの{友|とも}だちがあそびに{来|き}ます。ヤンさんはとりにくのりょうりとさかなのりょうりを{作|つく}ります。れいぞうこの{中|なか}にとりにくとさかながありませんから、ヤンさんはこれから{買|か}いものにでかけます。それから、ゆうびんきょくへ{行|い}って、きってを{買|か}います。"),
 questions=[
  ("つぎの{中|なか}で、ヤンさんのうちからいちばん{近|ちか}い{店|みせ}はどれですか。",
   ["にくや","パンや","くすりや","さかなや"],2,
   "「となりにパンやがあります」とある。うちのとなりが、いちばん{近|ちか}い。"),
  ("ヤンさんは{今日|きょう}どこへ{行|い}きますか。",
   ["にくや、さかなや、ゆうびんきょく","パンや、くすりや、ゆうびんきょく","びょういん、はなや、さかなや","びょういん、にくや、パンや"],1,
   "とりにくとさかなを{買|か}いに{行|い}き（にくや・さかなや）、ゆうびんきょくへ{行|い}って、きってを{買|か}う。"),
 ]),
# 1 ── 公式2012 もんだい5
dict(title="No.02 公式2012 みんなのかさ",
 passage=P(
  "きのうの{夜|よる}はおそくまでしごとをしました。とてもつかれました。しごとのあと、{電車|でんしゃ}で{帰|かえ}りました。",
  "{家|いえ}の{近|ちか}くの{駅|えき}で{電車|でんしゃ}をおりました。{外|そと}は{雨|あめ}でしたが、わたしはかさがありませんでした。とても<u>①こまりました</u>。",
  "{駅|えき}の{人|ひと}がわたしを{見|み}て、「あのはこの{中|なか}のかさを{使|つか}ってください。」と{言|い}いました。はこの{中|なか}にはかさが３{本|ぼん}ありました。",
  "わたしは「えっ、いいんですか。」と{聞|き}きました。",
  "{駅|えき}の{人|ひと}は「あれは『みんなのかさ』です。お{金|かね}はいりません。あした、あのはこにかえしてください。」と{言|い}いました。",
  "わたしは「わかりました。ありがとうございます。」と{言|い}って、かさをかりて{帰|かえ}りました。"),
 questions=[
  ("どうして<u>①こまりました</u>か。",
   ["おそい{時間|じかん}に{駅|えき}に{着|つ}いたから","しごとがたくさんあったから","とてもつかれたから","かさがなかったから"],4,
   "「{外|そと}は{雨|あめ}でしたが、わたしはかさがありませんでした。とてもこまりました」とある。"),
  ("「わたし」は、あしたどうしますか。",
   ["かさをはこの{中|なか}に{入|い}れます。","かさを{駅|えき}の{人|ひと}にわたします。","お{金|かね}をはこの{中|なか}に{入|い}れます。","お{金|かね}を{駅|えき}の{人|ひと}にわたします。"],1,
   "{駅|えき}の{人|ひと}が「あした、あのはこにかえしてください」と{言|い}った。かりたかさをはこにかえす。"),
 ]),
# 2 ── 公式2018 もんだい5
dict(title="No.03 公式2018 まちがえました",
 passage=P("これはチンさんが{書|か}いたさくぶんです。") +
  BOX("まちがえました　チン・シュン",
   "わたしはきのうの{日曜日|にちようび}、{友|とも}だちとサッカーをしました。{朝|あさ}からゆうがたまでしましたから、とてもつかれました。ゆうべはばんご{飯|はん}を{食|た}べたあとで、すぐにねました。ですから、{今日|きょう}のかんじテストのべんきょうができませんでした。<br>けさは<u>①５{時|じ}</u>に{起|お}きました。シャワーをあびて、{朝|あさ}ご{飯|はん}を{食|た}べました。それから、すぐかんじのテキストの４１ページから６０ページまでべんきょうしました。それから{学校|がっこう}へ{行|い}きました。とてもいそがしい{朝|あさ}でした。<br>しかし、きょうしつでかんじをべんきょうしている{人|ひと}はいませんでした。<u>②まちがえました</u>。テストは{今日|きょう}ではなくて、あしたでした。"),
 questions=[
  ("どうして<u>①５{時|じ}</u>に{起|お}きましたか。",
   ["{朝|あさ}からゆうがたまでサッカーをしたかったから","かんじテストのべんきょうがしたかったから","シャワーをあびて、{朝|あさ}ご{飯|はん}を{食|た}べたかったから","{学校|がっこう}へ{行|い}って、べんきょうがしたかったから"],2,
   "{前|まえ}の{日|ひ}に「かんじテストのべんきょうができませんでした」から、{朝|あさ}{早|はや}く{起|お}きてべんきょうした。"),
  ("チンさんは{何|なに}を<u>②まちがえました</u>か。",
   ["かんじのテキスト","かんじのテキストのページ","かんじのテストがある{日|ひ}","かんじのテストをするきょうしつ"],3,
   "「テストは{今日|きょう}ではなくて、あしたでした」→ テストがある{日|ひ}をまちがえた。"),
 ]),
# 3 ── 演習3 としょかん
dict(title="No.04 としょかんで",
 passage=DLG(
  ("{学生|がくせい}","「すみません。この{本|ほん}をかりたいです。」"),
  ("としょかんの{人|ひと}","「この{学校|がっこう}の{学生|がくせい}ですか。」"),
  ("{学生|がくせい}","「はい。」"),
  ("としょかんの{人|ひと}","「では、はじめにこのかみに{名前|なまえ}とじゅうしょと{電話|でんわ}ばんごうを{書|か}いてください。」"),
  ("{学生|がくせい}","「はい。」"),
  ("としょかんの{人|ひと}","「{書|か}きましたか。」"),
  ("{学生|がくせい}","「はい。」"),
  ("としょかんの{人|ひと}","「これはじしょですね。としょかんの{中|なか}でつかってください。」"),
  ("{学生|がくせい}","「はい、わかりました。では、この７さつをかしてください。」"),
  ("としょかんの{人|ひと}","「ああ、{学生|がくせい}は４さつまでです。」"),
  ("{学生|がくせい}","「そうですか。では、この３さつはかりません。」"),
  ("としょかんの{人|ひと}","「わかりました。では、こちらの{本|ほん}は２しゅうかん、ざっしは１しゅうかんでかえしてください。きょうは１５{日|にち}ですから、［　　　］」"),
  ("{学生|がくせい}","「はい、わかりました。」")),
 questions=[
  ("［　　　］には{何|なに}を{入|い}れますか。",
   ["{本|ほん}は２９{日|にち}、ざっしは２２{日|にち}です。","{本|ほん}は２２{日|にち}、ざっしは２９{日|にち}です。","{本|ほん}もざっしも２９{日|にち}です。","{本|ほん}もざっしも２２{日|にち}です。"],1,
   "{本|ほん}は２しゅうかん（１５{日|にち}＋１４{日|にち}＝２９{日|にち}）、ざっしは１しゅうかん（１５{日|にち}＋７{日|にち}＝２２{日|にち}）。"),
  ("この{学生|がくせい}は{何|なん}さつかりましたか。",
   ["３さつ","４さつ","５さつ","６さつ"],2,
   "７さつのうち３さつをやめたので、７−３＝４さつ。"),
  ("この{学生|がくせい}はとしょかんで{何|なに}をしましたか。",
   ["{本|ほん}に{名前|なまえ}を{書|か}きました。","かみに{本|ほん}の{名前|なまえ}を{書|か}きました。","じしょをかりました。","{本|ほん}とざっしをかりました。"],4,
   "かりた４さつの{中|なか}に{本|ほん}とざっしがある（「{本|ほん}は２しゅうかん、ざっしは１しゅうかんで…」）。じしょはとしょかんの{中|なか}でつかう。"),
  ("このとしょかんで{学生|がくせい}ができることは{何|なん}ですか。",
   ["ざっしを２しゅうかんかりること","{本|ほん}を５さつかりること","{本|ほん}やざっしを４さつまでかりること","{本|ほん}とじしょを１しゅうかんかりること"],3,
   "「{学生|がくせい}は４さつまでです」とある。"),
 ]),
# 4 ── 演習4 田中さんの旅行
dict(title="No.05 田中さんの旅行",
 passage=P(
  "{田中|たなか}さんは{絵|え}を{見|み}るのが{好|す}きです。{一人|ひとり}でゆっくりと{好|す}きな{絵|え}を{見|み}るために、{今年|ことし}は５{月|がつ}の{休|やす}みに{外国|がいこく}へ{行|い}くことにしました。でも、{一人|ひとり}で{飛行機|ひこうき}に{乗|の}るのははじめてで、{少|すこ}し{心配|しんぱい}でした。{旅行|りょこう}した{国|くに}では、{日本|にほん}と{時間|じかん}が{違|ちが}うので、はじめは{少|すこ}しねむくなりました。また{食|た}べ{物|もの}もからかったので、{水|みず}をたくさん{飲|の}みすぎて、お{腹|なか}が{痛|いた}くなってしまいました。でも、{見|み}たかった{絵|え}をゆっくり{見|み}ることができたので、そんなことはすぐ{忘|わす}れてしまいました。{田中|たなか}さんは、{旅行中|りょこうちゅう}に{友達|ともだち}になった{人|ひと}に、{今|いま}でも{手紙|てがみ}を{書|か}いています。"),
 questions=[
  ("{田中|たなか}さんはどんなことが{好|す}きですか。",
   ["{友達|ともだち}と{美術館|びじゅつかん}に{行|い}くこと","{一人|ひとり}でゆっくり{絵|え}を{見|み}ること","５{月|がつ}の{休|やす}みに{旅行|りょこう}に{行|い}くこと","{外国|がいこく}に{行|い}って{友達|ともだち}に{手紙|てがみ}を{書|か}くこと"],2,
   "「{一人|ひとり}でゆっくりと{好|す}きな{絵|え}を{見|み}るために…{外国|がいこく}へ{行|い}くことにしました」とある。"),
  ("{田中|たなか}さんは{旅行|りょこう}に{行|い}く{前|まえ}にどんなことが{心配|しんぱい}でしたか。",
   ["はじめて{一人|ひとり}で{飛行機|ひこうき}に{乗|の}ること","{食|た}べ{物|もの}がからくて{水|みず}を{飲|の}みすぎること","{旅行|りょこう}した{国|くに}でねむくなってしまうこと","{水|みず}を{飲|の}みすぎてお{腹|なか}が{痛|いた}くなること"],1,
   "「{一人|ひとり}で{飛行機|ひこうき}に{乗|の}るのははじめてで、{少|すこ}し{心配|しんぱい}でした」とある。"),
 ]),
# 5 ── 演習2 おきなわ旅行
dict(title="No.06 おきなわ旅行",
 passage=P(
  "{先月|せんげつ}わたしは{学校|がっこう}の{友達|ともだち}といっしょに、おきなわへ{旅行|りょこう}に{行|い}きました。わたしたちは、{旅行|りょこう}の{前|まえ}に、おきなわから{来|き}た{日本人|にほんじん}の{友達|ともだち}にいろいろ（ ア ）。{友達|ともだち}は、「おきなわはとうきょうよりずっと{南|みなみ}だから、とても{暑|あつ}いよ。（ イ ）、{夏|なつ}の{服|ふく}をたくさん{持|も}っていったほうがいい」と{言|い}いました。そのころとうきょうはまだ４{月|がつ}だったので、きおんが１４どぐらいでした。（ ウ ）、わたしはおしいれのおくから、{夏|なつ}の{洋服|ようふく}を{出|だ}して、かばんにいっぱい{入|い}れて{出|で}かけることにしました。２はく３{日|か}の{旅行|りょこう}ですが、{一日中|いちにちじゅう}、おきなわの{町|まち}をけんぶつしたり、{海|うみ}で{泳|およ}いだりするので、ようふくはたくさんあったほうがいいと{思|おも}ったのです。"),
 questions=[
  ("（ ア ）には{何|なに}を{入|い}れますか。",
   ["{話|はな}しました","{答|こた}えました","{呼|よ}びました","{聞|き}きました"],4,
   "{旅行|りょこう}の{前|まえ}に、おきなわをよく{知|し}っている{友達|ともだち}にいろいろ「{聞|き}きました」（しつもんした）。"),
  ("（ イ ）には{何|なに}を{入|い}れますか。",
   ["だから","それから","すると","だけど"],1,
   "「とても{暑|あつ}い。だから、{夏|なつ}の{服|ふく}を{持|も}っていったほうがいい」— {理由|りゆう}→けっかの「だから」。"),
  ("（ ウ ）には{何|なに}を{入|い}れますか。",
   ["そうすると","ところが","それで","それに"],3,
   "とうきょうはまだ{寒|さむ}かったが、おきなわは{暑|あつ}いと{聞|き}いた。「それで」{夏|なつ}の{洋服|ようふく}をかばんに{入|い}れた。"),
 ]),
# 6 ── 演習5 駅でかさ
dict(title="No.07 駅でかさをさがす",
 passage=DLG(
  ("すずき","「あのう、すみません。きのう{電車|でんしゃ}にかさをわすれました。」"),
  ("{駅|えき}の{人|ひと}","「どこに{行|い}く{電車|でんしゃ}ですか。」"),
  ("すずき","「さくら{駅|えき}に{行|い}く{電車|でんしゃ}です。９{時|じ}１５{分|ふん}につばき{駅|えき}でのって、あやめ{駅|えき}でおりました。」"),
  ("{駅|えき}の{人|ひと}","「そうですか。どんなかさですか。」"),
  ("すずき","「{長|なが}くて{大|おお}きいかさです。いろはくろです。」"),
  ("{駅|えき}の{人|ひと}","「{長|なが}くてくろいかさですね。」"),
  ("すずき","「はい。」"),
  ("{駅|えき}の{人|ひと}","「ちょっとまってください……これはみじかいですね……あ、ありました。えー、２{本|ほん}あります。かさには{名前|なまえ}が{書|か}いてありますか。」"),
  ("すずき","「はい、すずきと{書|か}いてあります。」"),
  ("{駅|えき}の{人|ひと}","「すずき……。ああ、こちらですね。」"),
  ("すずき","「そうです。［　　　］！ありがとうございました。」")),
 questions=[
  ("［　　　］には{何|なに}を{入|い}れますか。",
   ["けっこうです","こちらこそ","いいですね","よかった"],4,
   "なくしたかさが{見|み}つかったので「よかった」とよろこんでいる。"),
  ("{今日|きょう}すずきさんはどうして{駅|えき}の{人|ひと}と{話|はな}しましたか。",
   ["かさに{名前|なまえ}を{書|か}いたから","かさをわすれたから","{電車|でんしゃ}にのりたかったから","さくら{駅|えき}に{行|い}きたかったから"],2,
   "「きのう{電車|でんしゃ}にかさをわすれました」と{駅|えき}の{人|ひと}に{話|はな}している。"),
  ("すずきさんのかさはつぎのどれですか。",
   ["みじかいかさで、{名前|なまえ}が{書|か}いてあります。","くろいかさで、{名前|なまえ}が{書|か}いてあります。","{長|なが}いかさで、{名前|なまえ}は{書|か}いてありません。","{大|おお}きいかさで、{名前|なまえ}は{書|か}いてありません。"],2,
   "「{長|なが}くてくろいかさ」で、「すずき」と{名前|なまえ}が{書|か}いてある。"),
 ]),
# 7 ── 演習6 テープレコーダー
dict(title="No.08 テープレコーダーのつかいかた",
 passage=DLG(
  ("Ａ","「このおんがくはとてもいいですよ。いっしょに{聞|き}きましょう。テープレコーダーはありますか。」"),
  ("Ｂ","「ええ。{後|うし}ろにありますよ。」"),
  ("Ａ","「これは（ ア ）つかいますか。おしえてください。」"),
  ("Ｂ","「はじめに、そのボタンをおしてください。」"),
  ("Ａ","「（ イ ）。」"),
  ("Ｂ","「いいえ、あおいボタンです。」"),
  ("Ａ","「ああ、わかりました。（ ウ ）{白|しろ}いボタンですか。」"),
  ("Ｂ","「いいえ、その{前|まえ}に、ここにテープを{入|い}れてください。」"),
  ("Ａ","「はい、{入|い}れました。これでいいですか。」")),
 questions=[
  ("（ ア ）には{何|なに}を{入|い}れますか。",
   ["なぜ","どう","どんなに","なにが"],2,
   "つかいかたをたずねるときは「どうつかいますか」。"),
  ("（ イ ）には{何|なに}を{入|い}れますか。",
   ["これですね","どれですか","あおいボタンですね","ええ、そうです"],1,
   "「そのボタンを」と{言|い}われて「これですね」とかくにんした。つぎのＢの「いいえ、あおいボタンです」につながる。"),
  ("（ ウ ）には{何|なに}を{入|い}れますか。",
   ["それは","つぎから","つぎに","それでは"],3,
   "じゅんばんをたずねている。「つぎに{白|しろ}いボタンですか」。"),
  ("ただしいものはどれですか。",
   ["{白|しろ}いボタンをおしてから、テープを{入|い}れます。","{白|しろ}いボタンをおしてから、あおいボタンをおします。","テープを{入|い}れてから、あおいボタンをおします。","あおいボタンをおしてから、テープを{入|い}れます。"],4,
   "はじめにあおいボタンをおす →（{白|しろ}いボタンの{前|まえ}に）テープを{入|い}れる、のじゅんばん。"),
 ]),
# 8 ── 演習8 中山
dict(title="No.09 中山へ行く",
 passage=P(
  "{明日|あした}{車|くるま}で{中山|なかやま}へ{行|い}く。うちから{山|やま}までふつうは３{時間|じかん}ぐらいかかる。でも、{明日|あした}は{土曜日|どようび}で、{道|みち}がこむから、{少|すこ}し{早|はや}く{家|いえ}を{出|で}たほうがいいだろう。１１{時|じ}までには{山|やま}に{着|つ}きたい。{着|つ}いたら、すぐ{昼|ひる}ごはんを{食|た}べるつもりだ。",
  "{中山|なかやま}には{美|うつく}しい{湖|みずうみ}があって、たくさんの{人|ひと}が{遊|あそ}びに{来|く}る。{天気|てんき}がよければ、{泳|およ}いだり、{魚|さかな}をつったりすることができる。ふねにも{乗|の}れる。わたしは、{魚|さかな}がつりたい。でも、{天気|てんき}があまりよくなかったら、つりはやめて、{山|やま}でめずらしい{花|はな}や{鳥|とり}を{見|み}ようと{思|おも}う。",
  "{湖|みずうみ}のそばににんぎょうの{美術館|びじゅつかん}がある。{日本|にほん}のだけでなく、{世界中|せかいじゅう}のにんぎょうがかざってあるらしい。{時間|じかん}があったら、{見|み}てみたい。{帰|かえ}りにいなかの{家|いえ}によって、{両親|りょうしん}と{一緒|いっしょ}に{晩|ばん}ご{飯|はん}を{食|た}べるつもりだ。{母|はは}の{料理|りょうり}はひさしぶりなので、とてもたのしみだ。"),
 questions=[
  ("{明日|あした}この{人|ひと}はどうして{早|はや}く{出|で}かけますか。",
   ["{土曜日|どようび}で{車|くるま}が{多|おお}いから","{美|うつく}しい{湖|みずうみ}があるから","めずらしい{花|はな}や{鳥|とり}がいるから","あまり{天気|てんき}がよくないから"],1,
   "「{明日|あした}は{土曜日|どようび}で、{道|みち}がこむから、{少|すこ}し{早|はや}く{家|いえ}を{出|で}たほうがいい」とある。"),
  ("この{人|ひと}は{明日|あした}{天気|てんき}がよかったら、{何|なに}をしますか。",
   ["{花|はな}や{鳥|とり}を{見|み}ます","{湖|みずうみ}で{泳|およ}ぎます","ふねに{乗|の}ります","{魚|さかな}をつります"],4,
   "「わたしは、{魚|さかな}がつりたい」とある。{天気|てんき}がわるかったら{花|はな}や{鳥|とり}を{見|み}る。"),
  ("この{人|ひと}は{美術館|びじゅつかん}に{行|い}きますか。",
   ["{行|い}かないつもりです","{行|い}くかもしれません","{行|い}きません","{行|い}きたくないです"],2,
   "「{時間|じかん}があったら、{見|み}てみたい」→ {行|い}くかもしれない。"),
 ]),
# 9 ── 演習7 東山こうえん
dict(title="No.10 東山こうえんへ",
 passage=DLG(
  ("すずき","「もしもし、ヤンさんですか。すずきです。あした、いっしょに{東山|ひがしやま}こうえんへ{行|い}きませんか。わたしはよくさんぽをしますが、ひろくてきれいですよ。」"),
  ("ヤン","「いいですね。でも、{東山|ひがしやま}こうえんへどう{行|い}きますか。わたしはわかりません。」"),
  ("すずき","「じゃ、あした{東山駅|ひがしやまえき}で{会|あ}いましょう。」"),
  ("ヤン","「{何時|なんじ}にしますか。」"),
  ("すずき","「１０{時|じ}はどうですか。」"),
  ("ヤン","「（ ア ）。９{時半|じはん}はどうですか。」"),
  ("すずき","「いいですよ。{駅|えき}の{前|まえ}にきっさてんがあるから、その{前|まえ}で（ イ ）。」"),
  ("ヤン","「わかりました。ひるごはんをもって{行|い}きますか。」"),
  ("すずき","「こうえんのちかくにいいレストランがあるから、そこでいっしょに{食|た}べませんか。{駅|えき}の{前|まえ}のきっさてんは{高|たか}いですが、こうえんのちかくのレストランは{安|やす}くておいしいですよ。」"),
  ("ヤン","「それはいいですね。じゃ、そうしましょう。」")),
 questions=[
  ("ヤンさんとすずきさんははじめて{東山|ひがしやま}こうえんへ{行|い}きますか。",
   ["ヤンさんもすずきさんもはじめてです。","ヤンさんもすずきさんも{前|まえ}に{行|い}きました。","ヤンさんははじめてですが、すずきさんは{前|まえ}に{行|い}きました。","すずきさんははじめてですが、ヤンさんは{前|まえ}に{行|い}きました。"],3,
   "ヤンさんは{行|い}き{方|かた}が「わかりません」。すずきさんは「よくさんぽをします」→ {前|まえ}に{行|い}ったことがある。"),
  ("（ ア ）には{何|なに}を{入|い}れますか。",
   ["１０{時|じ}に{行|い}きましょう。","１０{時|じ}はちょっと……","１０{時|じ}がいいですね。","１０{時|じ}はおそいです。"],2,
   "そのあと「９{時半|じはん}はどうですか」とべつの{時間|じかん}をていあんしている → １０{時|じ}はつごうがわるい。"),
  ("（ イ ）には{何|なに}を{入|い}れますか。",
   ["まっています","まつでしょう","まちました","まちません"],1,
   "{待|ま}ち{合|あ}わせの{約束|やくそく}。「その{前|まえ}でまっています」。"),
  ("ひるごはんはどこで{食|た}べますか。",
   ["{駅|えき}の{前|まえ}のきっさてんで{食|た}べます。","こうえんの{中|なか}のきっさてんで{食|た}べます。","{駅|えき}のちかくのレストランで{食|た}べます。","こうえんのちかくのレストランで{食|た}べます。"],4,
   "「こうえんのちかくにいいレストランがあるから、そこでいっしょに{食|た}べませんか」→「そうしましょう」。"),
 ]),
# 10 ── 演習5 王さんの日記
dict(title="No.11 王さんの日記",
 passage=BOX("{王|おう}さんの{日記|にっき}",
  "{昨日|きのう}なおこさんと{銀座|ぎんざ}のデパートに{行|い}った。なおこさんと１０{時|じ}に{駅|えき}の{西口|にしぐち}で{会|あ}う{約束|やくそく}をしていたが、１０{時半|じはん}になっても、なおこさんは{来|こ}なかった。{東口|ひがしぐち}とまちがえたかもしれないと{思|おも}って、{東口|ひがしぐち}のほうへ{行|い}ってみたが、やはりなおこさんはいなかった。おかしいと{思|おも}ってなおこさんの{家|いえ}に{電話|でんわ}をしたら、なおこさんはまだ{家|いえ}にいて、１２{時|じ}の{約束|やくそく}だと{思|おも}っていたと{言|い}った。なおこさんがすぐ{出|で}てきてくれたので、１１{時|じ}には{会|あ}うことができた。"),
 questions=[
  ("{王|おう}さんはどうしてなおこさんと１０{時|じ}に{会|あ}うことができなかったのですか。",
   ["{王|おう}さんが{西口|にしぐち}と{東口|ひがしぐち}をまちがえていたからです。","{王|おう}さんが１０{時|じ}と１１{時|じ}をまちがえていたからです。","なおこさんが{西口|にしぐち}と{東口|ひがしぐち}をまちがえていたからです。","なおこさんが１０{時|じ}と１２{時|じ}をまちがえていたからです。"],4,
   "なおこさんは「１２{時|じ}の{約束|やくそく}だと{思|おも}っていた」→ {時間|じかん}をまちがえていた。"),
 ]),
# 11 ── 演習6 週末のせいかつ
dict(title="No.12 わたしの週末",
 passage=P(
  "{土曜日|どようび}と{日曜日|にちようび}は{忙|いそが}しくないです。わたしは１０{時|じ}ごろ{起|お}きます。そして、{朝|あさ}ごはんを{食|た}べます。それから、{区|く}のたいいくかんでうんどうをします。ゆうがた{近|ちか}くのスーパーへ{行|い}きます。{肉|にく}や{野菜|やさい}や{牛乳|ぎゅうにゅう}などを{買|か}います。ときどき{友達|ともだち}といっしょに{国|くに}の{料理|りょうり}を{作|つく}ります。そして、いっしょに{宿題|しゅくだい}をします。",
  "{一週間|いっしゅうかん}はとてもはやいです。{毎日|まいにち}{同|おな}じせいかつです。しかし、このせいかつはたのしいです。"),
 questions=[
  ("この{人|ひと}のせいかつとあわないものはどれですか。",
   ["しゅうまつはひまではありません。","{朝|あさ}ごはんを{食|た}べたあと、うんどうをします。","ちかくのスーパーでやさいやミルクなどを{買|か}います。","{友達|ともだち}といっしょに{料理|りょうり}を{作|つく}ったり、{宿題|しゅくだい}をしたりします。"],1,
   "「{土曜日|どようび}と{日曜日|にちようび}は{忙|いそが}しくないです」→ しゅうまつはひま。「ひまではありません」は{合|あ}わない。"),
 ]),
# 12 ── 演習4 ちかてつとバス
dict(title="No.13 ちかてつとバス",
 passage=P(
  "わたしの{家|いえ}から{会社|かいしゃ}までちかてつでもバスでも{行|い}ける。バスはやすいが、{乗|の}るところまで{遠|とお}いし、{長|なが}い{時間|じかん}{待|ま}たなければならない。ちかてつはバスにくらべると{高|たか}いが、{駅|えき}は{近|ちか}い。さいきんは{運動|うんどう}のために{天気|てんき}のいい{日|ひ}だけは{遠|とお}くまで{歩|ある}いてバスに{乗|の}ることにしている。"),
 questions=[
  ("ただしいものはどれですか。",
   ["この{人|ひと}はいつもバスに{乗|の}る","この{人|ひと}はいつもちかてつに{乗|の}る","この{人|ひと}は{雨|あめ}の{日|ひ}はバスに{乗|の}る","この{人|ひと}は{雨|あめ}の{日|ひ}はちかてつに{乗|の}る"],4,
   "{天気|てんき}のいい{日|ひ}「だけ」{歩|ある}いてバスに{乗|の}る → {雨|あめ}の{日|ひ}はちかてつ。"),
 ]),
# 13 ── 演習10 誕生パーティーの手紙
dict(title="No.14 誕生パーティーの手紙",
 passage=BOX("しずかさんへの{手紙|てがみ}",
  "しずかさん、お{元気|げんき}ですか。（ ア ）。この{前|まえ}の{同窓会|どうそうかい}で{会|あ}ってから（ イ ）{会|あ}っていませんね。<br>（ ウ ）６{月|がつ}１８{日|にち}{金曜日|きんようび}は、わたしの{誕生日|たんじょうび}なんです。みんなに{会|あ}いたいので、{誕生|たんじょう}パーティーをひらくことにしました。わたしの{家|いえ}はアパートだし、せまいので、{近|ちか}くのお{店|みせ}をよやくしました。しょうたいした{人|ひと}は、なおみさんやひろみさんなど、しずかさんが{知|し}っている{人|ひと}ばかりです。かいひを２{千|せん}５{百円|ひゃくえん}いただきますから、プレゼントなどのご{心配|しんぱい}はいりません。{場所|ばしょ}は{地図|ちず}を{入|い}れておいたので、{来|き}てください。<br>つごうがわるいばあいは、おてすうですが、{前|まえ}の{日|ひ}までにわたしのところにお{電話|でんわ}をお{願|ねが}いします。それでは、ぜひ{来|き}てください。{待|ま}っています。<br>{明子|あきこ}より"),
 questions=[
  ("（ ア ）には{何|なに}を{入|い}れますか。",
   ["しつれいします","ごめんください","ごぶさたしています","ようこそ"],3,
   "{久|ひさ}しぶりに{手紙|てがみ}を{書|か}くときのあいさつは「ごぶさたしています」。"),
  ("（ イ ）には{何|なに}を{入|い}れますか。",
   ["あまり","ほとんど","よくは","たくさん"],2,
   "{同窓会|どうそうかい}で{会|あ}ってから「ほとんど」{会|あ}っていない。"),
  ("（ ウ ）には{何|なに}を{入|い}れますか。",
   ["ところが","ところで","じつは","これは"],3,
   "{本題|ほんだい}に{入|はい}るときの「じつは」。"),
 ]),
# 14 ── 演習11 たんじょうびの電話
dict(title="No.15 たんじょうびの電話",
 passage=DLG(
  ("ヤン","「もしもし、{大山|おおやま}さんですか。ヤンです。」"),
  ("{大山|おおやま}","「アメリカにいるヤンさん？　おげんきですか。」"),
  ("ヤン","「はい。げんきです。{大山|おおやま}さん、おたんじょうび、おめでとうございます。」"),
  ("{大山|おおやま}","「ああ、ヤンさん、わたしのたんじょうびをまだおぼえていましたか。ありがとうございます。」"),
  ("ヤン","「もちろんです。でもことしはいっしょにたんじょうびのパーティーができませんでしたね。もうパーティーをしましたか。」"),
  ("{大山|おおやま}","「ええ。きのうかいしゃのともだちとケーキを{食|た}べたり、ダンスをしたりしてたのしかったですよ。あしたはかぞくとレストランへ{行|い}きます。」"),
  ("ヤン","「（ ア ）」"),
  ("{大山|おおやま}","「{来月|らいげつ}しごとでアメリカへ{行|い}きますからヤンさんにもいちどあいたいですね。」"),
  ("ヤン","「ほんとうですか。（ イ ）そのときは{電話|でんわ}をください。」")),
 questions=[
  ("（ ア ）には{何|なに}を{入|い}れますか。",
   ["そうでした","そうですか","そうしましょう","そうします"],2,
   "{相手|あいて}の{話|はなし}を{聞|き}いてうけるあいづちの「そうですか」。"),
  ("（ イ ）には{何|なに}を{入|い}れますか。",
   ["じゃあ","たぶん","どうも","あれから"],1,
   "「じゃあ、そのときは{電話|でんわ}をください」。"),
  ("ヤンさんはどうして{大山|おおやま}さんに{電話|でんわ}をしましたか。",
   ["{大山|おおやま}さんにあいたいから{電話|でんわ}しました","{大山|おおやま}さんがアメリカに{行|い}くから{電話|でんわ}しました","{大山|おおやま}さんがパーティーをするから{電話|でんわ}しました","{大山|おおやま}さんのたんじょうびだから{電話|でんわ}しました"],4,
   "はじめに「おたんじょうび、おめでとうございます」と{言|い}っている。"),
  ("ただしいものはどれですか。",
   ["{大山|おおやま}さんはあしたかいしゃのともだちとパーティーをします。","{大山|おおやま}さんはきのうかいしゃのともだちとパーティーをしました。","{大山|おおやま}さんはあしたたんじょうびだからともだちとレストランへ{行|い}きます。","{大山|おおやま}さんはきのうたんじょうびだったからかぞくとパーティーをしました。"],2,
   "「きのうかいしゃのともだちとケーキを{食|た}べたり、ダンスをしたりして…」とある。あしたはかぞくとレストラン。"),
 ]),
# 15 ── 演習14 本のよみかた（穴埋め）
dict(title="No.16 本のよみかた（穴埋め）",
 passage=P(
  "「うちでこの{本|ほん}をよんでください。すこしむずかしいですが、とても（ １ ）ですから、がんばってください。{知|し}らない（ ２ ）がはいっていますが、はじめはじしょをひかないでぜんぶ（ ３ ）ください。つぎにじしょをひきながらもう（ ４ ）よんでください。いいですか。２かいよむんですよ。」"),
 questions=[
  ("（ １ ）にはなにをいれますか。",
   ["おもしろい","つまらない","やさしい","むずかしい"],1,
   "「むずかしいですが、とてもおもしろい」—「〜が」の{前|まえ}と{後|うし}ろは、はんたいのこと。"),
  ("（ ２ ）にはなにをいれますか。",
   ["{本|ほん}","ことば","じしょ","{人|ひと}"],2,
   "{知|し}らない「ことば」がはいっている → じしょをひく、につながる。"),
  ("（ ３ ）にはなにをいれますか。",
   ["はなして","よんで","ひいて","はいって"],2,
   "じしょをひかないで、ぜんぶ「よんで」ください。"),
  ("（ ４ ）にはなにをいれますか。",
   ["いっさつ","ひとり","いっぽん","いちど"],4,
   "「２かいよむんですよ」→ もう「いちど」よむ。"),
 ]),
# 16 ── 演習14 えいがの日（穴埋め）
dict(title="No.17 えいがの日（穴埋め）",
 passage=P(
  "きのうはともだちと（ １ ）でえいがに{行|い}きました。えいがは２じかんぐらいでおわりました。ひるごはんのじかんに（ ２ ）のでしょくどうにはいってごはんをたべました。（ ３ ）デパートでかいものをしました。すこしつかれたけれど、（ ４ ）いちにちでした。"),
 questions=[
  ("（ １ ）にはなにをいれますか。",
   ["ふたり","ににん","ににち","にかい"],1,
   "{人数|にんずう}は「ふたり」。"),
  ("（ ２ ）にはなにをいれますか。",
   ["いた","した","なった","たべた"],3,
   "「ひるごはんのじかんになったので」。"),
  ("（ ３ ）にはなにをいれますか。",
   ["それでは","そのまえ","そのうち","それから"],4,
   "じゅんばんをあらわす「それから」。"),
  ("（ ４ ）にはなにをいれますか。",
   ["わるい","たのしい","きたない","むずかしい"],2,
   "「つかれたけれど、たのしいいちにちでした」。"),
 ]),
# 17 ── 公式2018 もんだい6（情報検索）
dict(title="No.18 公式2018 高木大学への行き方",
 passage=BOX("{高木大学|たかぎだいがく}に{来|き}たい{人|ひと}へ",
  "① かかる{時間|じかん}：４６{分|ぷん}　かかるお{金|かね}：３００{円|えん}<br>　{寺西駅|てらにしえき}バスてい１ばん →（バス４５{分|ふん}）→ バスてい「{高木大学前|たかぎだいがくまえ}」→（{歩|ある}く１{分|ぷん}）→ {高木大学|たかぎだいがく}<br>"
  "② かかる{時間|じかん}：３０{分|ぷん}　かかるお{金|かね}：５５０{円|えん}<br>　{花田駅|はなだえき} →（{電車|でんしゃ}２５{分|ふん}）→ {水村駅|みずむらえき} →（{歩|ある}く５{分|ふん}）→ {高木大学|たかぎだいがく}<br>"
  "③ かかる{時間|じかん}：４０{分|ぷん}　かかるお{金|かね}：４５０{円|えん}<br>　{花田駅|はなだえき} →（ちかてつ３０{分|ぷん}）→ {木山駅|きやまえき} →（{歩|ある}く１０{分|ぷん}）→ {高木大学|たかぎだいがく}<br>"
  "④ かかる{時間|じかん}：３５{分|ぷん}　かかるお{金|かね}：４３０{円|えん}<br>　{糸川駅|いとかわえき} →（{電車|でんしゃ}２５{分|ふん}）→ {木山駅|きやまえき} →（{歩|ある}く１０{分|ぷん}）→ {高木大学|たかぎだいがく}"),
 questions=[
  ("パブロさんは{高木大学|たかぎだいがく}に{行|い}きたいです。{花田駅|はなだえき}か{糸川駅|いとかわえき}から{乗|の}ります。{駅|えき}から{大学|だいがく}までかかるお{金|かね}は５００{円|えん}までで、{時間|じかん}はみじかいほうがいいです。パブロさんはどの{行|い}き{方|かた}で{行|い}きますか。",
   ["①","②","③","④"],4,
   "{花田駅|はなだえき}・{糸川駅|いとかわえき}{発|はつ}で５００{円|えん}{以下|いか}は③（４５０{円|えん}・４０{分|ぷん}）と④（４３０{円|えん}・３５{分|ふん}）。{時間|じかん}がみじかいのは④。①は{寺西駅|てらにしえき}{発|はつ}なので{乗|の}れない。"),
 ]),
]

TESTS = [
    ("テスト1", [3, 0]),        # としょかん4 + 公式2009ヤン2 = 6問
    ("テスト2", [7, 1]),        # テープレコーダー4 + 公式2012かさ2 = 6問
    ("テスト3", [9, 2]),        # 東山こうえん4 + 公式2018まちがえました2 = 6問
    ("テスト4", [5, 6]),        # おきなわ3 + 駅でかさ3 = 6問
    ("テスト5", [8, 13]),       # 中山3 + 誕生パーティーの手紙3 = 6問
    ("テスト6", [14, 10, 11]),  # たんじょうびの電話4 + 王さんの日記1 + 週末1 = 6問
    ("テスト7", [15, 4]),       # 穴埋め・本4 + 田中さんの旅行2 = 6問
    ("テスト8", [16, 12, 17]),  # 穴埋め・えいが4 + ちかてつ1 + 公式2018高木大学1 = 6問
]

# ──────────────────────────────────────────────
# HTML 生成
# ──────────────────────────────────────────────

def build_question(qid, stem, options, correct, note):
    opts = []
    for i, o in enumerate(options, 1):
        c = "1" if i == correct else "0"
        opts.append(
            f'<div class="option" data-correct="{c}"><input type="radio" name="q{qid}" id="q{qid}_{i}" value="{i}">'
            f'<label for="q{qid}_{i}">{i}. {r(o)}</label></div>')
    ans = f'{correct}. {r(options[correct-1])}'
    return (
        f'<div class="q-slide" data-slide-index="1"><div class="slide-card slide-card-question">'
        f'<div class="question" data-qid="{qid}" data-scored="1">'
        f'<div class="q-stem-row"><span class="q-num">{qid}</span><div class="q-stem">{r(stem)}</div></div>'
        f'<div class="options">\n' + "\n".join(opts) + '\n</div>'
        f'<div class="explanation"><div class="explanation-answer"><ruby>正解<rt>せいかい</rt></ruby>：{ans}</div>'
        f'<div class="explanation-note">{r(note)}</div></div></div></div></div>')

blocks_html = []
qid = 0
for bi, b in enumerate(BLOCKS):
    qs = []
    for stem, options, correct, note in b["questions"]:
        qid += 1
        qs.append(build_question(qid, stem, options, correct, note))
    blocks_html.append(
        f'<!-- {b["title"]} -->\n'
        f'<div class="block-player" id="block-player-{bi}" data-player-title="{html.escape(b["title"])}" hidden>\n'
        f'<div class="q-slide block-passage-once"><div class="slide-card slide-card-passage">\n'
        f'<div class="passage-text">\n{b["passage"]}\n</div>\n</div></div>\n'
        + "\n".join(qs) + "\n</div>")

hub_buttons = "\n".join(
    f'<button type="button" class="icon-link" data-test="{i}">{i+1}</button>'
    for i in range(len(TESTS)))

tests_js = ",\n".join(
    f"  {{ label: '{label}', blocks: [{', '.join(map(str, blocks))}] }}"
    for label, blocks in TESTS)

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>N5 読解 練習テスト（長文・全__NTESTS__回・各約10分）</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Hiragino Kaku Gothic ProN','Hiragino Sans','Noto Sans JP',Meiryo,sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.container{max-width:800px;margin:0 auto;padding:20px}
/* テスト中は横幅を広く使い、本文(左)・問題(右)の左右分割を活かす */
body:has(#view-work:not([hidden])) .container{max-width:1180px}
/* ふりがな（漢字のみに付与） */
ruby{ruby-align:center;white-space:nowrap}
rt{font-size:.58em;font-weight:400;line-height:1.1;color:inherit}
#view-hub[hidden],#view-work[hidden]{display:none!important}
/* ── header (hub & work share the same gradient header) ── */
header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 4px 15px rgba(102,126,234,.4)}
header h1{font-size:1.45em;margin-bottom:4px}
header p{font-size:.9em;margin-top:8px;opacity:.95}
.header-info{display:flex;justify-content:center;gap:20px;align-items:center;margin-top:12px;flex-wrap:wrap}
.timer-group{display:flex;align-items:center;gap:8px}
.timer{font-size:1.8em;font-weight:bold;font-variant-numeric:tabular-nums}
.timer.warning{color:#ffd700;animation:pulse 1s infinite}
.timer.danger{color:#ff4757;animation:pulse .5s infinite}
.timer.paused{color:#cbd5e0;animation:none}
.pause-btn{background:rgba(255,255,255,.25);border:none;color:#fff;width:36px;height:36px;border-radius:50%;font-size:1em;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s;padding:0;line-height:1;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.pause-btn:hover{background:rgba(255,255,255,.4)}
.pause-btn:active{transform:scale(.95)}
.pause-btn:disabled{opacity:.4;cursor:not-allowed}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.progress-bar{width:160px;height:8px;background:rgba(255,255,255,.3);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:#fff;border-radius:4px;transition:width .3s}
.score-badge{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.9em}
.header-back{display:flex;justify-content:flex-start;margin-bottom:10px}
.btn-back{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:6px 14px;background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.5);border-radius:10px;font-size:.9em;font-weight:600;cursor:pointer;touch-action:manipulation;transition:background .2s}
.btn-back:hover{background:rgba(255,255,255,.32)}
/* ── work header (一段・中央タイトル・ゆとりあり) ── */
.work-head{padding:16px 24px;border-radius:16px;margin-bottom:20px;text-align:center}
.work-head-row{display:flex;align-items:center;gap:16px}
.work-head h1{flex:1;min-width:0;font-size:1.2em;margin:0;font-weight:700;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.work-head .btn-back{flex-shrink:0;min-height:38px;padding:7px 15px;font-size:1.1em;line-height:1}
.work-head .timer-group{flex-shrink:0}
.work-head .timer{font-size:1.5em}
.work-head .pause-btn{width:34px;height:34px}
.work-head .progress-bar{width:100%;height:6px;margin-top:14px}
.section{background:#fff;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-title{font-size:1.1em;font-weight:bold;color:#667eea;border-left:4px solid #667eea;padding-left:12px;margin-bottom:16px}
.note-box{background:#edeffd;border:1px solid #b3bef2;border-radius:10px;padding:14px 16px;margin-bottom:20px;font-size:.88em;color:#3b3663;line-height:1.65}
.example-picker{display:grid;gap:10px}
/* ── テスト選択：数字アイコン ── */
.sub-section-title{font-size:.9em;color:#666;margin-bottom:12px;padding-left:4px}
.icon-row{display:flex;flex-wrap:wrap;gap:10px}
.icon-row .icon-link{display:flex;align-items:center;justify-content:center;min-width:56px;height:56px;padding:0 16px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:none;border-radius:12px;font-family:inherit;font-weight:bold;font-size:1.1em;line-height:1;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(102,126,234,.3);transition:transform .2s,box-shadow .2s;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.icon-row .icon-link:hover{box-shadow:0 4px 12px rgba(102,126,234,.4)}
.icon-row .icon-link:active{transform:scale(.96)}
.btn-submit{display:block;width:100%;min-height:48px;padding:16px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:none;border-radius:12px;font-size:1.1em;font-weight:bold;cursor:pointer;transition:transform .2s,box-shadow .2s;margin-top:24px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.btn-submit:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(102,126,234,.4)}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
/* ── material group: 本文(左)を見ながら問題(右)を解く 2カラム ── */
.material-group{display:flex;gap:20px;align-items:flex-start;background:#fff;border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
/* 本文は左側に固定。原則スクロールなしで全文表示（画面に収まらない長文のみ内部スクロール） */
.passage-pane{flex:0 0 46%;position:sticky;top:var(--sticky-top,150px);max-height:calc(100vh - var(--sticky-top,150px) - 28px);overflow-y:auto;-webkit-overflow-scrolling:touch;z-index:5;background:#f7fafc;border:1px solid #cbd5e0;border-radius:10px;padding:14px 16px}
.questions-col{flex:1;min-width:0}
.passage-text{font-size:.92rem;line-height:1.9;color:#1a202c}
.passage-text p{margin:0 0 .7em}
.passage-text p:last-child{margin-bottom:0}
.passage-text .speaker{font-weight:700;color:#3b3663}
.passage-box{margin:10px 0;padding:12px 14px;background:#fff;border:1px dashed #667eea;border-radius:10px;line-height:1.9}
.passage-box .box-head{font-weight:700;color:#3b3663;margin-bottom:6px}
.passage-text table{width:100%;border-collapse:collapse;margin:8px 0;font-size:.85rem}
.passage-text th,.passage-text td{border:1px solid #cbd5e0;padding:5px 7px;text-align:left;vertical-align:top}
.passage-text th{background:#edeffd;color:#3b3663}
/* 縦長・狭い画面（iPad縦/スマホ）は上下に積む。本文は上部に固定して問題と同時に見える */
@media(max-width:820px){
  .material-group{flex-direction:column}
  .passage-pane{flex:none;width:100%;position:sticky;top:var(--sticky-top,150px);max-height:38vh;overflow-y:auto}
}
.question{padding:16px 0;border-top:1px solid #e2e8f0}
.questions-col .question:first-child{border-top:none;padding-top:0}
.q-stem-row{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}
.q-num{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;min-width:32px;height:32px;padding:0 10px;background:#667eea;color:#fff;border-radius:50%;font-weight:700;font-size:.9rem;line-height:1.2}
.q-stem{flex:1;min-width:0;font-size:1rem;line-height:1.95;font-weight:500}
.options{display:grid;grid-template-columns:1fr;gap:10px}
.option input{display:none}
.option label{display:block;min-height:48px;padding:11px 14px;border:2px solid #e2e8f0;border-radius:8px;cursor:pointer;transition:.15s;font-size:.95rem;line-height:1.95;word-break:break-word;touch-action:manipulation}
.option label:hover{border-color:#667eea;background:#f3f5fe}
.option input:checked+label{border-color:#667eea;background:#edeffd;color:#3b3663;font-weight:600}
.option.correct label{border-color:#48bb78!important;background:#f0fff4!important;color:#276749!important}
.option.wrong label{border-color:#fc8181!important;background:#fff5f5!important;color:#9b2c2c!important}
.option.picked-nokey label{border-color:#667eea!important;background:#edeffd!important;color:#3b3663!important}
.explanation{display:none;margin-top:8px;padding:10px;background:#fffbeb;border-radius:8px;font-size:.9em;border-left:3px solid #f6ad55;color:#744210}
.explanation.show{display:block}
.explanation-answer{font-weight:600}
.explanation-note{margin-top:8px;padding-top:8px;border-top:1px dashed #ecc94b;font-size:.92em;line-height:1.65;color:#5c4a21}
.result-panel{background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-top:24px;display:none}
.result-panel.show{display:block}
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
</style>
</head>
<body>
<div class="container">
<div id="view-hub">
<header>
<h1>N5 読解 練習テスト（長文）</h1>
</header>
<div class="section">
<div class="section-title">テストを選ぶ</div>
<div class="sub-section-title">各約10分（長文読解・各6問）</div>
<div class="icon-row">
__HUB_BUTTONS__
</div>
</div>
</div>

<div id="view-work" hidden>
<header class="work-head">
<div class="work-head-row">
<button type="button" class="btn-back" id="btnBackHub" aria-label="テスト一覧へ戻る">←</button>
<h1 id="chromeBlockTitle">N5<ruby>読解<rt>どっかい</rt></ruby>テスト</h1>
<div class="timer-group">
<div class="timer" id="workTimer">10:00</div>
<button type="button" class="pause-btn" id="pauseBtn" aria-label="一時停止">⏸</button>
</div>
</div>
<div class="progress-bar"><div class="progress-fill" id="workProgress" style="width:100%"></div></div>
</header>
<div id="test-mount"></div>
<button type="button" class="btn-submit" id="submitBtnWork"><ruby>採点<rt>さいてん</rt></ruby>する</button>
<div class="result-panel" id="resultPanel"><h2 id="resultTitle"></h2><div class="result-score" id="resultScore"></div><div class="result-detail" id="resultDetail"></div></div>
</div>

<div id="block-store" hidden>

__BLOCKS__

</div>
</div>
<script>
// 各テストに含める教材（block-player の index）。1問90秒で約10分になるようにまとめる。
const TESTS = [
__TESTS__
];
const TIME_LIMIT = 600; // 全テスト共通 10分

let currentTest = -1;
let timerInterval = null;
let timeLeft = 0;
let submitted = false;
let paused = false;

function clearQTimer() {
  if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
}

function updateTimerUi() {
  const el = document.getElementById('workTimer');
  if (!el) return;
  const t = Math.max(0, timeLeft);
  const m = Math.floor(t / 60);
  const s = t % 60;
  el.textContent = m + ':' + String(s).padStart(2, '0');
  if (paused) { el.className = 'timer paused'; }
  else if (timeLeft <= 60) el.className = 'timer danger';
  else if (timeLeft <= 300) el.className = 'timer warning';
  else el.className = 'timer';
  const prog = document.getElementById('workProgress');
  if (prog) prog.style.width = Math.max(0, (t / TIME_LIMIT) * 100) + '%';
}

function startQTimer() {
  clearQTimer();
  paused = false;
  const pb = document.getElementById('pauseBtn');
  if (pb) { pb.textContent = '⏸'; pb.disabled = false; pb.setAttribute('aria-label', '一時停止'); }
  updateTimerUi();
  timerInterval = setInterval(() => {
    if (submitted || paused) return;
    timeLeft--;
    updateTimerUi();
    if (timeLeft <= 0) { clearQTimer(); submitTest(); }
  }, 1000);
}

function togglePause() {
  if (submitted) return;
  paused = !paused;
  const pb = document.getElementById('pauseBtn');
  if (pb) {
    pb.textContent = paused ? '▶' : '⏸';
    pb.setAttribute('aria-label', paused ? '再開' : '一時停止');
  }
  updateTimerUi();
}

function openTest(ti) {
  const test = TESTS[ti];
  if (!test) return;
  submitted = false;
  currentTest = ti;
  document.getElementById('view-hub').setAttribute('hidden', '');
  document.getElementById('view-work').removeAttribute('hidden');

  const mount = document.getElementById('test-mount');
  mount.innerHTML = '';
  test.blocks.forEach(bi => {
    const srcPanel = document.getElementById('block-player-' + bi);
    if (!srcPanel) return;
    const group = document.createElement('div');
    group.className = 'material-group';

    const srcPassage = srcPanel.querySelector('.block-passage-once .slide-card-passage');
    if (srcPassage) {
      const pane = document.createElement('div');
      pane.className = 'passage-pane';
      pane.innerHTML = srcPassage.innerHTML;
      group.appendChild(pane);
    }
    const qcol = document.createElement('div');
    qcol.className = 'questions-col';
    srcPanel.querySelectorAll('.q-slide:not(.block-passage-once) .question').forEach(q => {
      const clone = q.cloneNode(true);
      clone.querySelectorAll('input[type="radio"]').forEach(inp => { inp.checked = false; });
      clone.querySelectorAll('.option').forEach(o => o.classList.remove('correct', 'wrong', 'picked-nokey'));
      clone.querySelectorAll('.explanation').forEach(ex => ex.classList.remove('show'));
      qcol.appendChild(clone);
    });
    group.appendChild(qcol);
    mount.appendChild(group);
  });

  const nQ = mount.querySelectorAll('.question').length;
  const ht = document.getElementById('chromeBlockTitle');
  if (ht) ht.textContent = 'N5読解テスト' + (ti + 1) + '（10分・' + nQ + '問）';

  const panel = document.getElementById('resultPanel');
  if (panel) panel.classList.remove('show');
  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = false;

  timeLeft = TIME_LIMIT;
  startQTimer();
  setStickyTop();
  window.scrollTo(0, 0);
}

// 固定表示する本文が、ヘッダーの下に重ならないように位置を計算する
function setStickyTop() {
  const header = document.querySelector('#view-work header');
  const h = header ? header.offsetHeight : 120;
  document.documentElement.style.setProperty('--sticky-top', (h + 8) + 'px');
}

function goHub() {
  clearQTimer();
  submitted = false;
  paused = false;
  currentTest = -1;
  timeLeft = 0;
  document.getElementById('view-work').setAttribute('hidden', '');
  document.getElementById('view-hub').removeAttribute('hidden');
  const mount = document.getElementById('test-mount');
  if (mount) mount.innerHTML = '';
  const panel = document.getElementById('resultPanel');
  if (panel) panel.classList.remove('show');
  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = false;
  window.scrollTo(0, 0);
}

function submitTest() {
  if (submitted) return;
  if (currentTest < 0) return;
  const mount = document.getElementById('test-mount');
  if (!mount) return;
  submitted = true;
  clearQTimer();
  const pb = document.getElementById('pauseBtn');
  if (pb) pb.disabled = true;

  const blockQs = mount.querySelectorAll('.question');
  let nKeyed = 0;
  let correct = 0;
  blockQs.forEach(el => {
    const scored = el.dataset.scored === '1';
    const sel = el.querySelector('input[type="radio"]:checked');
    const opts = el.querySelectorAll('.option');
    opts.forEach(o => {
      o.classList.remove('correct', 'wrong', 'picked-nokey');
      if (scored) {
        if (o.dataset.correct === '1') o.classList.add('correct');
        else if (sel && o.contains(sel)) o.classList.add('wrong');
      } else if (sel && o.contains(sel)) {
        o.classList.add('picked-nokey');
      }
    });
    el.querySelectorAll('.explanation').forEach(e => e.classList.add('show'));
    if (scored) {
      nKeyed++;
      if (sel) {
        const p = sel.closest('.option');
        if (p && p.dataset.correct === '1') correct++;
      }
    }
  });

  const panel = document.getElementById('resultPanel');
  const sc = document.getElementById('resultScore');
  const tt = document.getElementById('resultTitle');
  const pct = nKeyed > 0 ? Math.round(correct / nKeyed * 100) : 0;
  if (panel && sc && tt) {
    panel.classList.add('show');
    sc.textContent = correct + ' / ' + nKeyed + '（' + pct + '%）';
    sc.className = 'result-score ' + (pct >= 90 ? 'excellent' : pct >= 70 ? 'good' : pct >= 50 ? 'fair' : 'poor');
    tt.textContent = pct >= 90 ? 'すばらしい！' : pct >= 70 ? 'よくできました！' : pct >= 50 ? 'もうすこし！' : 'がんばりましょう！';
    const used = TIME_LIMIT - Math.max(0, timeLeft);
    document.getElementById('resultDetail').innerHTML =
      '<div class="result-item"><div class="label">せいかい</div><div class="value">' + correct + '/' + nKeyed + '</div></div>' +
      '<div class="result-item"><div class="label">じかん</div><div class="value">' + Math.floor(used / 60) + '分' + (used % 60) + '秒</div></div>';
    panel.scrollIntoView({ behavior: 'smooth' });
  }

  const sub = document.getElementById('submitBtnWork');
  if (sub) sub.disabled = true;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.icon-link[data-test]').forEach(btn => {
    btn.addEventListener('click', () => openTest(parseInt(btn.dataset.test, 10)));
  });
  document.getElementById('btnBackHub').addEventListener('click', goHub);
  document.getElementById('submitBtnWork').addEventListener('click', submitTest);
  document.getElementById('pauseBtn').addEventListener('click', togglePause);
  window.addEventListener('resize', () => { if (currentTest >= 0) setStickyTop(); });
});
</script>
</body>
</html>
"""

out = (HTML
       .replace("__NTESTS__", str(len(TESTS)))
       .replace("__HUB_BUTTONS__", hub_buttons)
       .replace("__BLOCKS__", "\n\n".join(blocks_html))
       .replace("__TESTS__", tests_js))

import os
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "n5-reading-test.html")
with open(dst, "w", encoding="utf-8") as f:
    f.write(out)
print(f"written: {dst}")
print(f"blocks: {len(BLOCKS)}, questions: {qid}, tests: {len(TESTS)}")
