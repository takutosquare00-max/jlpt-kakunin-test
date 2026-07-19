---
name: bunpo
description: みんなの日本語の文法テスト・クイズHTMLを作成する。「unit◯◯のbunpoを作って」「unit◯◯のクイズを作成」「文法テスト作成」と言われたら使う。既存ガイドに従い、実装はサブエージェントに委譲する。
---

# bunpo / クイズHTML作成

引数: unit番号（例: `36`）と種類（bunpo / quiz。未指定なら確認する）。

## 手順

1. **ガイドを読む**（必須・作業前に）:
   - 文法テスト: `Minnanonihongo/shared/bunpo-test-creation-guide.md`
   - クイズ: `Minnanonihongo/shared/quiz-html-creation-guide.md`
   - 問題文作成が絡む場合: `Minnanonihongo/shared/test-questions-guide.md`
2. **ソース確認**: 対象unitの教材md（`Minnanonihongo/unit◯◯-◯◯/unit◯◯/` 配下）と、既存の完成例（直近のunit）を1つ見て体裁を合わせる
3. **プラン提示**: ファイル構成（何パート・何問）をユーザーに確認してから着手
4. **実装**: ガイドとプランが確定したら、`implementer` サブエージェントに委譲する（ガイドのパス・対象unit・完成例のパスをプロンプトに含める）
5. **検証**: 問題数・選択肢数・正解設定・ふりがなをガイドの規則と突き合わせて確認
6. **デプロイ**: ユーザーが望めば `/deploy` スキルの手順で公開する
