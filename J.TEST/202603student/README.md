# J.TEST 2026年3月度 生徒用教材

## フォルダ構成

```
202603student/
├── README.md                    # このファイル
├── jtest-ac-202603.html         # A-C テスト（ゴイさん用）※生成物
├── jtest-fg-202603.html         # F-G テスト（サードさん用）※生成物
│
├── 202603ゴイさん/              # ゴイさん用（A-C）
│   ├── 0315ゴイさんjtest a-c.pdf           # 元PDF
│   ├── 0315ゴイさんjtest_AC_解答.md        # 問題・解答・解説（ふりがな付き）
│   └── generate_jtest_ac_html.py           # HTML生成スクリプト
│
└── 202603サードさん/            # サードさん用（F-G）
    ├── 20260308サードさん jtest f-g.pdf    # 元PDF
    ├── 20260308サードさん_jtest_fg_問題・解答・解説.md  # 問題・解答・解説（ふりがな付き）
    └── generate_jtest_fg_html.py           # HTML生成スクリプト
```

## 必要なファイル

| 種別 | ファイル | 説明 |
|------|----------|------|
| ソース | *.pdf | 試験問題の元データ |
| ソース | *_解答.md | 問題・解答・解説（ふりがな付き、HTMLの参照元） |
| 生成 | generate_*.py | HTMLを生成するPythonスクリプト |
| 出力 | jtest-*.html | 生成されたHTMLテスト（デプロイ用）

## 使い方

### HTMLの再生成

```bash
# A-C（ゴイさん用）
cd 202603ゴイさん && python3 generate_jtest_ac_html.py

# F-G（サードさん用）
cd 202603サードさん && python3 generate_jtest_fg_html.py
```

生成されたHTMLは `202603student/` 直下に出力されます。

## デプロイ先

- `jlpt-kakunin-test-deploy/jtest-ac-202603.html`
- `jlpt-kakunin-test-deploy/jtest-fg-202603.html`

生成後、必要に応じて上記へコピーしてください。
