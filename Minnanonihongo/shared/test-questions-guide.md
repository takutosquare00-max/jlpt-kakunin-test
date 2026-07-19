# みんなの日本語　テスト問題作成ガイド

各ユニットの `unit{XX}-test-questions.md` を同一フォーマットで作成するための手順書。
**フォーマットは固定、内容はユニットごとに変わる。**

---

## 1. ファイル規則

| 項目 | 規則 |
|---|---|
| ファイル名 | `unit{XX}-test-questions.md` |
| タイトル行 | `# 第{XX}課 テスト問題（4択選択肢）` |
| 保存場所 | そのユニットのフォルダ内 |

---

## 2. MDファイルの骨格（固定）

```
# 第XX課 テスト問題（4択選択肢）

---

## 【文法・文型問題】

### 問題1：{学習項目名}
...

---

## 【語彙・漢字問題】

### 問題N：読み方を選んでください
### 問題N+1：意味を選んでください
### 問題N+2：漢字を選んでください

---

## 【解答】

| 問題 | 答え | 問題 | 答え | 問題 | 答え |
| --- | --- | --- | --- | --- | --- |
| 1   |     | 21  |     | 41  |     |
...
```

- 大セクションは `##`、問題グループは `###`
- 問題番号は課全体で1から連番（セクションをまたいでも続く）
- 答えは末尾の解答表にのみ書く

---

## 3. 問題のフォーマット（固定）

```markdown
### 問題{N}：{学習項目名}

{グループ共通の指示文}

**{番号}. {問題文}**

a. {選択肢}　　b. {選択肢}　　c. {選択肢}　　d. {選択肢}

**{番号+1}. {問題文}**

a. {選択肢}　　b. {選択肢}　　c. {選択肢}　　d. {選択肢}
```

**書式ルール：**
- 問題文は `**番号. 〜**` で太字
- 選択肢は `a.` `b.` `c.` `d.` を**同一行**に、全角スペース2つ `　　` で区切る
- 問題間は1行空ける、グループ間は `---` で区切る

---

## 4. 問題タイプ（内容に応じて選ぶ）

ユニットで扱う学習内容に応じて、以下のタイプを組み合わせる。

| タイプ | 指示文 | 使う場面 |
|---|---|---|
| **形変換** | `活用形として正しいものはどれですか。` | 新しい活用形を学ぶとき |
| **空欄補充** | `（　）に入る正しいものはどれですか。` | 文型・助詞・接続を確認するとき |
| **正文選択** | `正しい文はどれですか。` | 文型の正用・誤用を区別させるとき |
| **誤文選択** | `正しくない文はどれですか。` | 同上（逆から問うとき） |
| **意味・用法** | `意味として正しいものはどれですか。` | 文型・語彙・表現の意味を確認するとき |
| **読み方** | `読み方として正しいものはどれですか。` | 漢字語彙の読みを確認するとき |
| **漢字** | `漢字として正しいものはどれですか。` | ひらがな→漢字の変換を確認するとき |
| **その他** | （内容に合わせて設定） | ことわざ・標識・慣用表現など |

---

## 5. 問題数について

問題数は固定しない。**そのユニットの文法ポイント・語彙・漢字を網羅的に学習できる数**を作成する。解答表の列数は問題数に合わせて増やす。

---

## 6. 作成手順

### Step 1　ユニットの内容を把握する
そのユニットの `.md` ファイルを読み、以下を確認する。
- 学習する文型・文法ポイントは何か
- 新出語彙・漢字は何か（語彙リストを全数確認する）
- 特殊な内容（ことわざ・標識・慣用表現など）はあるか

### Step 2　セクション構成を決める
文法ポイント1つにつき1セクション（`### 問題N`）を割り当てる。
語彙は「読み方・意味・漢字」で別セクションにする。

### Step 3　問題を書く
各セクションで問題タイプを選び、問題文と選択肢を書く。
誤答（ダミー）は**混乱しやすい理由があるもの**を選ぶ。
- 形変換の誤答 → よくある活用ミス
- 意味の誤答 → 似た意味・反対の意味
- 読み方の誤答 → 音が似ている・同じ漢字を含む

### Step 4　解答表を作る
全問の答えを末尾の表に書く。問題文の近くには答えを書かない。

---

## 7. 作成済みユニット一覧

| 課 | 主な学習内容 | ファイル |
|---|---|---|
| 第1課 | N₁はN₂です、N₁はN₂じゃありません、Sか（疑問文）、Nも、N₁のN₂（所属）、〜さん | [unit1-test-questions.md](../unit1-2/unit1/unit1-test-questions.md) |
| 第2課 | これ・それ・あれ・どれ、この/その/あの/どの＋N、そうです・そうじゃありません、S₁かS₂か、N₁のN₂（代替）、そうですか | [unit2-test-questions.md](../unit1-2/unit2/unit2-test-questions.md) |
| 第3課 | ここ・そこ・あそこ・どこ、こちら・そちら・あちら・どちら、〜はどこ/どちらですか、〜の〜（原産地・所属）、いくらですか、〜をください | [unit3-test-questions.md](../unit3-5/unit3/unit3-test-questions.md) |
| 第4課 | 時刻（今何時ですか・〜時〜分・〜時半）、曜日、〜から〜まで、〜に（時間）、動詞のます形・ません・ました・ませんでした | [unit4-test-questions.md](../unit3-5/unit4/unit4-test-questions.md) |
| 第5課 | 〜へ（行き先）、〜で（交通手段）、〜と（同伴）、〜に（時）、どこへも〜ません、疑問詞の使い分け、過去形 | [unit5-test-questions.md](../unit3-5/unit5/unit5-test-questions.md) |
| 第6課 | 〜を（目的語）、〜で（行為の場所）、〜へ（移動の方向）、〜ませんか（誘い）、〜ましょう（提案）、何も〜ません、それから | [unit6-test-questions.md](../unit6-10/unit6/unit6-test-questions.md) |
| 第7課 | 手段・方法の「で」、〜語で、あげます・もらいます（助詞と使い分け）、もう〜ました・まだです | [unit7-test-questions.md](../unit6-10/unit7/unit7-test-questions.md) |
| 第8課 | な形容詞・い形容詞の肯定・否定文、連体修飾（〜な＋名詞・〜い＋名詞）、程度副詞、どう・どんな、逆接「〜ですが」 | [unit8-test-questions.md](../unit6-10/unit8/unit8-test-questions.md) |
| 第9課 | 〜が好きです・嫌いです、〜が上手です・下手です、〜がわかります、〜があります（所有）、〜から（理由）、どうして〜か | [unit9-test-questions.md](../unit6-10/unit9/unit9-test-questions.md) |
| 第10課 | あります・います（存在の使い分け）、〜に（存在の場所）、だれも・なにも＋否定、位置表現（上/下/中/前/後ろ/隣/近く/間） | [unit10-test-questions.md](../unit6-10/unit10/unit10-test-questions.md) |
| 第11課 | ひとつ〜とお（和語数詞）、助数詞（〜人/台/枚/回）、期間表現（〜日/週間/ヶ月/年）、いくつ・どのくらい、〜ぐらい、〜だけ、频度に | [unit11-test-questions.md](../unit11-15/unit11/unit11-test-questions.md) |
| 第12課 | 名詞・な形容詞の過去形、い形容詞の過去形、〜より比較、どちらが〜、〜のほうが、〜の中でいちばん | [unit12-test-questions.md](../unit11-15/unit12/unit12-test-questions.md) |
| 第13課 | Nがほしい、Vたい、Vます形に＋V（目的移動）、NにV/NをV、どこか・なにか | [unit13-test-questions.md](../unit11-15/unit13/unit13-test-questions.md) |
| 第14課 | 動詞グループ（Ⅰ・Ⅱ・Ⅲ）、て形の作り方、Vてください、Vています（進行）、ましょうか | [unit14-test-questions.md](../unit11-15/unit14/unit14-test-questions.md) |
| 第15課 | Vてもいいです、Vてはいけません、Vています（継続状態・習慣）、知りません | [unit15-test-questions.md](../unit11-15/unit15/unit15-test-questions.md) |
| 第16課 | て形連続動作（〜て〜て）、い形〜くて接続、N/な形で接続、Vてから、N₁はN₂が＋形容詞、どうやって・どのN | [unit16-test-questions.md](../unit16-20/unit16/unit16-test-questions.md) |
| 第17課 | ない形の作り方、Vないでください、Vなければなりません、Vなくてもいいです、N（時間）までに | [unit17-test-questions.md](../unit16-20/unit17/unit17-test-questions.md) |
| 第18課 | 辞書形の作り方、Vことができます、趣味はVことです、Vまえに、なかなか・ぜひ | [unit18-test-questions.md](../unit16-20/unit18/unit18-test-questions.md) |
| 第19課 | た形の作り方、Vたことがあります、Vたりたりします、〜くなります/になります（変化） | [unit19-test-questions.md](../unit16-20/unit19/unit19-test-questions.md) |
| 第20課 | 普通体（動詞・い形・な形/名詞）、普通体疑問文、けど（逆接） | [unit20-test-questions.md](../unit16-20/unit20/unit20-test-questions.md) |
| 第21課 | 普通体＋と思います、普通体＋と言います（直接・間接引用）、〜でしょう（確認）、N(place)でNがあります | [unit21-test-questions.md](../unit21-25/unit21/unit21-test-questions.md) |
| 第22課 | 節による名詞修飾、修飾節内のが、V辞書形＋時間/約束/用事 | [unit22-test-questions.md](../unit21-25/unit22/unit22-test-questions.md) |
| 第23課 | V辞書形/V ない形 とき（When）、辞書形とき vs た形とき（未完了/完了）、V辞書形＋と（必然的結果）、N(place)をV（通過） | [unit23-test-questions.md](../unit21-25/unit23/unit23-test-questions.md) |
| 第24課 | くれます、Vてあげます/もらいます/くれます、疑問詞がV | [unit24-test-questions.md](../unit21-25/unit24/unit24-test-questions.md) |
| 第25課 | 〜たら（条件：If）、〜たら（時間：When/After）、〜ても/でも（逆接：Even if）、もし/いくら | [unit25-test-questions.md](../unit21-25/unit25/unit25-test-questions.md) |
| 第26課 | 〜んです（理由・事情の説明／んですか・んです・んですが）、Vていただけませんか、疑問詞＋Vたらいいですか、N（目的語）は | [unit26-test-questions.md](../unit26-30/unit26/unit26-test-questions.md) |
| 第27課 | 可能動詞（作り方・を→が）、見えます/聞こえます、できます（完成）、は（対比）、も、しか | [unit27-test-questions.md](../unit26-30/unit27/unit27-test-questions.md) |
| 第28課 | V₁ますながらV₂、Vています（習慣）、普通形＋し（理由列挙）、それに、それで | [unit28-test-questions.md](../unit26-30/unit28/unit28-test-questions.md) |
| 第29課 | Vています（結果の状態・自動詞）、Vてしまいました/しまいます（完了・後悔）、ありました、どこかで/どこかに | [unit29-test-questions.md](../unit26-30/unit29/unit29-test-questions.md) |
| 第30課 | Vてあります（意図的行為の結果・他動詞）、Vておきます（準備・後始末）、まだ＋V（肯定）、それは〜 | [unit30-test-questions.md](../unit26-30/unit30/unit30-test-questions.md) |
| 第31課 | 意向形（〜よう）、〜（よ）うと思っています、まだ〜ていません、〜つもりです、〜予定です | [unit31-test-questions.md](../unit31-35/unit31/unit31-test-questions.md) |
| 第32課 | 〜たほうがいいです、〜ないほうがいいです、〜でしょう（推量）、〜かもしれません | [unit32-test-questions.md](../unit31-35/unit32/unit32-test-questions.md) |
| 第33課 | 命令形・禁止形 | [unit33-test-questions.md](../unit31-35/unit33/unit33-test-questions.md) |
| 第34課 | 〜とおりに、〜たあとで、〜ないで | [unit34-test-questions.md](../unit31-35/unit34/unit34-test-questions.md) |
| 第35課 | 〜ば、〜なら、ことわざ | [unit35-test-questions.md](../unit31-35/unit35/unit35-test-questions.md) |
| 第36課 | 〜ように、〜ようになります、〜ようにします | [unit36-test-questions.md](../unit36-40/unit36/unit36-test-questions.md) |
| 第37課 | 受身形、迷惑の受け身、から／でつくります | [unit37-test-questions.md](../unit36-40/unit37/unit37-test-questions.md) |
| 第38課 | の の名詞化（〜のは・〜のが・〜のを忘れました・〜のは〜です） | [unit38-test-questions.md](../unit36-40/unit38/unit38-test-questions.md) |
| 第39課 | 〜て（で）原因・理由、名詞で、途中で | [unit39-test-questions.md](../unit36-40/unit39/unit39-test-questions.md) |
| 第40課 | 〜か（間接疑問）、〜かどうか、〜てみます、い形容詞→〜さ | [unit40-test-questions.md](../unit36-40/unit40/unit40-test-questions.md) |
| 第41課 | いただきます・くださいます・やります、てくださいませんか、名詞に（目的） | [unit41-test-questions.md](../unit41-45/unit41/unit41-test-questions.md) |
| 第42課 | 〜ために（目的）、〜のに（用途）、ために vs ように、数量は vs も、〜によって | [unit42-test-questions.md](../unit41-45/unit42/unit42-test-questions.md) |
| 第43課 | 〜そうです（様態）、〜てきます、〜てくれませんか | [unit43-test-questions.md](../unit41-45/unit43/unit43-test-questions.md) |
| 第44課 | 〜すぎます、〜やすい/にくい、〜を〜く/にします、名詞にします | [unit44-test-questions.md](../unit41-45/unit44/unit44-test-questions.md) |
| 第45課 | 〜場合は、〜のに（逆接・不満） | [unit45-test-questions.md](../unit41-45/unit45/unit45-test-questions.md) |
| 第46課 | 〜ところです（辞書形・ている・た）、〜ばかりです、〜はずです | [unit46-test-questions.md](../unit46-50/unit46/unit46-test-questions.md) |
| 第47課 | 〜そうです（伝聞）、〜ようです、声／音／におい／味がします | [unit47-test-questions.md](../unit46-50/unit47/unit47-test-questions.md) |
| 第48課 | 使役形の作り方、使役文の助詞（をとに）、〜させていただけませんか | [unit48-test-questions.md](../unit46-50/unit48/unit48-test-questions.md) |
| 第49課 | 尊敬語（受身形タイプ・お〜になります・特別尊敬語）、お/ご〜ください、〜まして/ますので | [unit49-test-questions.md](../unit46-50/unit49/unit49-test-questions.md) |
| 第50課 | 謙譲語I（お/ご〜します）、謙譲語II（特別謙譲語：まいります・おります・もうします・いたします・いただきます・ぞんじます） | [unit50-test-questions.md](../unit46-50/unit50/unit50-test-questions.md) |

新しいユニットを作成したらこの表に追記する。

---

## 8. 作成後チェックリスト

- [ ] ファイル名・タイトルが規則どおりか
- [ ] 問題番号が課全体で連番になっているか
- [ ] 選択肢が同一行にあるか
- [ ] 答えが解答表以外に書かれていないか
- [ ] 解答表の番号と問題番号が一致しているか
- [ ] 新出語彙・漢字が語彙・漢字問題で網羅されているか
- [ ] ユニット一覧（セクション7）を更新したか
