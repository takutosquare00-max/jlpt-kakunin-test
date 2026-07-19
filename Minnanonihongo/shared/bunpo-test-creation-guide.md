# 文法学習HTMLテスト作成ガイド（unit別）

各レッスン（unit）の文法を3時間×2回の授業で学習するためのHTMLテスト一式を作成する手順。
L21で確立した方法をベースに、他unitへ展開する際の流れをまとめる。

---

## 1. 全体の流れ

```
1) プランニング       … 文法項目の分類・授業構成・問題数の設計
       ↓
2) フォルダ作成       … unit配下に `bunpo/` を新規作成
       ↓
3) 個別文法テスト作成 … 各文法ごとに1ファイル（テスト＋解説）
       ↓
4) まとめテスト作成   … 1回目／2回目の最後に出す統合テスト
       ↓
5) クイック復習作成   … 2回目の最初に出す前回復習テスト
       ↓
6) 仕上げ修正        … 表記揺れ・スタイル統一・全体検証
```

---

## 2. プランニング（最初に必ず行う）

unit内の文法項目を確認し、以下を決める。

| 項目 | 例 |
|------|----|
| 文法数 | L21は7項目 |
| 重要度の高い文法 → 1回目（前半） | 主要3〜4項目 |
| 軽めの文法 → 2回目（後半） | 残り3〜4項目 |
| 各文法の問題数 | 重要度に応じて 6〜12問 |
| 制限時間 | 14問以下＝10分、15問以上＝15分 |

**ファイル構成（L21の例）**

| 回 | ファイル種類 | 内容 |
|----|-------------|------|
| 1回目 | 文法①〜③各テスト + まとめ1 | 主要3文法 + 1回目の総合 |
| 2回目 | クイック復習1 + 文法④〜⑦各テスト + まとめ2 | 前回復習 + 残り4文法 + 2回目の総合 |

**まとめテストの設計方針**
- セクション分けはせず、文法をミックスして配置
- ページ読み込み時に問題順を自動シャッフル
- 1回目まとめは①②③、2回目まとめは④以降のみ（クイック復習で復習済みのため）

---

## 3. フォルダ・ファイル命名

```
Minnanonihongo/unit<X>/bunpo/
  ├ bunpo01-<文法名>.html
  ├ bunpo02-<文法名>.html
  ├ ...
  ├ bunpo-matome1.html
  ├ bunpo-matome2.html
  └ bunpo-quickreview1.html
```

- 文法名は英字スラッグ（例：`to-omoimasu`, `de-arimasu`, `naito`）
- 通し番号は `01〜07` のようにゼロ埋め

---

## 4. 問題作成のルール

### 4-1. 語彙制約（重要）
- **最優先**：そのunitで導入された語彙
- **使用可**：それまでに学習済みの語彙（L1〜現unitの1つ前まで）
- **使用不可**：次のunit以降に出てくる語彙

判断に迷ったら、L1〜25 は `Minnanonihongo/shared/lessons/Minna_No_Nihongo_1_lessons/lessonNN.md`、L26〜50 は `Minnanonihongo/shared/lessons/Minna_No_Nihongo_2_lessons/lessonNN.md` の語彙表を確認。

### 4-2. 問題の作り方
- 4択（ラジオボタン）
- 各問題に1つだけ正解（`value="1"`）、他は `value="0"`
- 1つの選択肢に複数の言い方を入れない（例：「行われます／開かれます」は片方に絞る）
- 選択肢末尾に意味ラベル（質問／確認／否定 等）を付けない
- 質問文・解説に `<u>` 下線は使わない

### 4-3. 会話形式の問題
A：/B：形式の問題は `dialogue` divに分離する。

```html
<div class="q-text"><span class="q-num">N</span>（　　　）に入る正しいものはどれですか。</div>
<div class="dialogue">
<p><span class="sp">A：</span>...</p>
<p><span class="sp">B：</span>...<span class="blank-paren">（　　　）</span>...</p>
</div>
<div class="options">...</div>
```

参照：`unit31-35/unit31-35-grammar-test-part1.html` の Q2 と同じスタイル。

### 4-4. 解説
- ふりがな（ruby）は**つけない**（質問文・選択肢にはOK）
- フォーマット：`✅ 正解：N — 短い説明`
- 採点ボタンを押すまでは非表示（`.explanation.show` クラスで表示）

---

## 5. HTMLテンプレート（共通仕様）

既存ファイルのHTML/CSS/JSをコピーして問題内容のみ差し替えるのが最も速い。
推奨：`unit21/bunpo/bunpo01-to-omoimasu.html` をテンプレ元に使う。

### 5-1. 共通機能（既に組み込み済み）
- 上部にタイマー（一時停止 ⏸/▶ ボタン付き）
- プログレスバー・残り問題数表示
- 採点ボタンで一括採点 → 解説の自動表示
- 選択肢の自動シャッフル（読み込み時）
- 漢字ルビ・モバイル対応

### 5-2. テーマカラー
| ファイル種別 | カラー | 例 |
|------------|-------|----|
| 通常文法テスト | 青系 `#2b6cb0` | bunpo01〜07 |
| まとめテスト | 紫系 `#6b46c1` | bunpo-matome1/2 |
| クイック復習 | オレンジ系 `#dd6b20` | bunpo-quickreview1 |

### 5-3. まとめテスト固有の機能
問題順を自動シャッフルする JS を script 内に追加：

```js
function shuffleQuestions(){
  const sec=document.getElementById('qSection');
  ...問題divをFisher-Yatesシャッフル → 再append → q-numを連番に振り直し
}
try{shuffleQuestions();shuffleAllOptions()}catch(e){}
```

問題群を包む div には `id="qSection"` を付ける。

---

## 6. 仕上げ修正（最後に必ずやる）

作成後の品質チェック・一括修正に使える sed コマンド：

```bash
cd /path/to/unit<X>/bunpo

# 解説のふりがな削除（漢字は保持）
for f in *.html; do
  sed -i '' '/class="explanation"/s|<ruby>\([^<]*\)<rt>[^<]*</rt></ruby>|\1|g' "$f"
done

# <u>タグ削除
for f in *.html; do sed -i '' 's|<u>||g; s|</u>||g' "$f"; done

# タイマーを10分に統一（14問以下の場合）
for f in *.html; do
  sed -i '' 's|<div class="timer" id="timer">[0-9]*:[0-9][0-9]</div>|<div class="timer" id="timer">10:00</div>|' "$f"
  sed -i '' 's|TIME_LIMIT=[0-9]*|TIME_LIMIT=600|' "$f"
done
```

### 最終検証
```bash
# 全てゼロが期待
grep -c "<u>" *.html                                           # uタグ残存
grep -c 'class="explanation"[^<]*<ruby>' *.html                # 解説にruby残存
grep -c '（[^）]*）</span></label>' *.html                      # 選択肢末尾ラベル残存

# 各ファイルが正しい時間設定か
for f in *.html; do echo -n "$f: "; grep -o 'TIME_LIMIT=[0-9]*' "$f" | head -1; done
```

---

## 7. よくある修正パターン

| 症状 | 修正 |
|------|------|
| HTMLタイプミス（`<span class="q-num">N">...`） | 閉じタグ `</span>` への修正 |
| `<span class="blank-paren">（　　　）</span>` の閉じカッコ抜け | 全角閉じカッコ補完 |
| 「何でも食べませんか」のような不自然な日本語 | 文脈を変えて自然な提案表現に差し替え |
| まとめテストでセクション分けが残っている | 全 `.question` を1つの `.section` に統合 |

---

## 8. 参考ファイル

- 既存実装の見本：`unit21-25/unit21/bunpo/`
- 会話形式の参照：`unit31-35/unit31-35-grammar-test-part1.html` Q2
- レッスン語彙表：`shared/lessons/lesson<NN>.md`
- 既存のクイズHTML仕様：`shared/quiz-html-creation-guide.md`

---

## 9. 進め方の推奨

1. **まずプランニングをユーザーに提示** → 文法分け・問題数・時間配分の承認を取る
2. **1ファイル目を試作** → スタイル・難易度をユーザーに確認してもらう
3. **承認後、残りを一気に作成**
4. **最後にユーザーがブラウザで全ファイルを確認** → フィードバックを受けて一括修正

各段階で「承認を取ってから次へ」が手戻りを防ぐ。
