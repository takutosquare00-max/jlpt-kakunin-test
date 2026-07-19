# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ構成

日本語教室の教材制作・管理。教材ソース（md）から学習用HTML（クイズ・文法テスト）を生成し、GitHub Pagesで公開するワークフローが中心。

| ディレクトリ | 内容 |
|---|---|
| `Minnanonihongo/` | みんなの日本語 単元別教材・クイズ（unit1〜50） |
| `JLPT/` | JLPT確認テスト（N1〜N5）・過去問 |
| `J.TEST/` | J.TEST対策教材 |
| `読解/` `聴解/` | 読解・聴解テキスト |
| `*-deploy/` | GitHub Pages公開用リポジトリ（それぞれ独立git） |

## 作業前に必ず参照するガイド

定型作業には確立されたワークフロー文書がある。**該当作業ではまずこれを読むこと**:

- 文法テスト作成: `Minnanonihongo/shared/bunpo-test-creation-guide.md`
- クイズHTML作成: `Minnanonihongo/shared/quiz-html-creation-guide.md`
- テスト問題作成: `Minnanonihongo/shared/test-questions-guide.md`
- PDF・画像の文字起こし: `Minnanonihongo/shared/transcription_guide.md`
- JLPT確認テスト作成ルール: `JLPT/description/rules for check test creation.md`

## デプロイ（GitHub Pages）

デプロイ用ディレクトリは独立gitリポジトリ。**push はユーザーが明示的に依頼したときのみ**。ソース→デプロイ用ディレクトリへコピー → commit & push の順。

| デプロイ先 | Pages ベース URL |
|---|---|
| `minnanonihongo-quiz-deploy/` | https://takutosquare00-max.github.io/minnanonihongo-quiz/ |
| `minnanonihongo-bunpo-deploy/` | https://takutosquare00-max.github.io/minnanonihongo-bunpo/ |
| `kanji-deploy/` | https://takutosquare00-max.github.io/kanji-practice/ |
| `jtest-fg-deploy/` | https://takutosquare00-max.github.io/jtest-reading-practice/ |
| `moji-gakushu/` | https://takutosquare00-max.github.io/moji-gakushu/ |
| `romaji-typing-practice/` | https://takutosquare00-max.github.io/romaji-typing-practice/ |
| JLPT等ルート直下 | https://takutosquare00-max.github.io/jlpt-kakunin-test/ |

HTMLをpushしたら「完了です」で返答を始め、同時に `open -a Safari "公開URL"` で公開ページを開く（file:// は開かない）。詳細ルール: `.cursor/rules/github-html-deploy-complete.mdc`

- `jlpt-kakunin-test-deploy.nested-git-backup/` はバックアップなので触らない
- 日本語ファイル名・スペース入りパスが多い。パスは常にクォートする
- Pythonスクリプト実行はルートの `venv/` を使う
