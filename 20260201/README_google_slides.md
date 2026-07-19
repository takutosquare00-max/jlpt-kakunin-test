# Google Slidesへの変換方法

このディレクトリには、マークダウンファイルをGoogle Slidesに変換するためのスクリプトが含まれています。

## 方法1: Google Slides APIを使用（推奨）

### 必要な準備

1. **Google Cloud Consoleでプロジェクトを作成**
   - https://console.cloud.google.com/ にアクセス
   - 新しいプロジェクトを作成

2. **Google Slides APIを有効化**
   - APIとサービス > ライブラリ
   - "Google Slides API"を検索して有効化

3. **認証情報を作成**
   - APIとサービス > 認証情報
   - 「認証情報を作成」>「OAuth クライアント ID」
   - アプリケーションの種類: 「デスクトップアプリ」
   - 認証情報をダウンロードして `credentials.json` として保存

4. **必要なパッケージをインストール**
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

### 実行方法

```bash
cd /Users/hayashi./datax/Business/school/20260131
python create_google_slides.py
```

初回実行時はブラウザが開き、Googleアカウントでの認証が求められます。

## 方法2: HTMLに変換してコピー&ペースト（簡単）

マークダウンをHTMLに変換して、Google Slidesに直接貼り付ける方法です。

```bash
python convert_to_html.py
```

生成されたHTMLファイルをブラウザで開き、内容をコピーしてGoogle Slidesに貼り付けます。

## 方法3: PDFに変換してインポート

マークダウンをPDFに変換して、Google Slidesにインポートする方法です。

```bash
# Marpを使用する場合
npx @marp-team/marp-cli n5-test-20questions.md --pdf
```

生成されたPDFをGoogle Slidesにアップロードします。
