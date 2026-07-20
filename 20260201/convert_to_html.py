#!/usr/bin/env python3
"""
マークダウンファイルをHTMLに変換するスクリプト
Google Slidesにコピー&ペーストしやすい形式で出力
"""

import re
import os


def parse_markdown_slides(markdown_file):
    """マークダウンファイルを解析してスライドのリストを返す"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Marp形式のスライドを分割（---で区切られている）
    slides = []
    slide_sections = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    
    for section in slide_sections:
        section = section.strip()
        if not section:
            continue
        
        # フロントマター（YAML）を除去
        if section.startswith('marp:'):
            lines = section.split('\n')
            skip = True
            filtered_lines = []
            for line in lines:
                if skip and line.strip() == '---':
                    skip = False
                    continue
                if not skip:
                    filtered_lines.append(line)
            section = '\n'.join(filtered_lines)
        
        if section:
            slides.append(section)
    
    return slides


def markdown_to_html(markdown_text):
    """マークダウンテキストをHTMLに変換"""
    html_lines = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append('<br>')
            continue
        
        # 見出し
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
        # 太字
        elif line.startswith('**') and line.endswith('**'):
            text = line[2:-2].strip()
            html_lines.append(f'<p><strong>{text}</strong></p>')
        # リスト項目
        elif line.startswith('- '):
            text = line[2:].strip()
            html_lines.append(f'<li>{text}</li>')
        # 番号付きリスト
        elif re.match(r'^\d+\.', line):
            html_lines.append(f'<li>{line.strip()}</li>')
        else:
            # 通常のテキスト（太字や斜体を処理）
            text = line
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
            html_lines.append(f'<p>{text}</p>')
    
    return '\n'.join(html_lines)


def create_html_presentation(slides, output_file):
    """スライドからHTMLプレゼンテーションを作成"""
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JLPT N5 練習テスト（20問）</title>
    <style>
        body {
            font-family: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .slide {
            background-color: white;
            padding: 40px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            page-break-after: always;
        }
        h1 {
            color: #1a73e8;
            border-bottom: 3px solid #1a73e8;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #34a853;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h3 {
            color: #ea4335;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        p {
            line-height: 1.6;
            margin: 10px 0;
        }
        li {
            margin: 8px 0;
            line-height: 1.6;
        }
        strong {
            color: #1a73e8;
        }
        @media print {
            .slide {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
"""
    
    for i, slide_content in enumerate(slides):
        html_content += f'    <div class="slide">\n'
        html_content += markdown_to_html(slide_content)
        html_content += '\n    </div>\n'
    
    html_content += """</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'HTMLファイルが作成されました: {output_file}')


def main():
    """メイン関数"""
    markdown_file = '/Users/hayashi./DataxWorkspace/Developer/school/20260131/n5-test-20questions.md'
    output_file = '/Users/hayashi./DataxWorkspace/Developer/school/20260131/n5-test-20questions.html'
    
    print('マークダウンファイルを解析中...')
    slides = parse_markdown_slides(markdown_file)
    print(f'{len(slides)}個のスライドが見つかりました')
    
    print('HTMLファイルを作成中...')
    create_html_presentation(slides, output_file)
    
    print('\n完了しました！')
    print(f'HTMLファイルをブラウザで開いて、内容をコピーしてGoogle Slidesに貼り付けてください。')
    print(f'ファイル: {output_file}')


if __name__ == '__main__':
    main()
