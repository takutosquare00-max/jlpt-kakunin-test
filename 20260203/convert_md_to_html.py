#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

def markdown_to_html(md_text):
    """MarkdownテキストをHTMLに変換"""
    html = md_text
    
    # 見出しの変換
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 水平線
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
    
    # 太字
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 番号付きリスト
    def replace_ordered_list(match):
        items = match.group(0).strip().split('\n')
        result = '<ol>\n'
        for item in items:
            if item.strip():
                text = re.sub(r'^\d+\.\s*', '', item)
                result += f'    <li>{text}</li>\n'
        result += '</ol>'
        return result
    
    # 番号付きリストの処理（連続する番号付き行をグループ化）
    lines = html.split('\n')
    result_lines = []
    in_list = False
    list_items = []
    
    for line in lines:
        if re.match(r'^\d+\.\s+', line):
            if not in_list:
                in_list = True
                list_items = []
            list_items.append(line)
        else:
            if in_list:
                # リストをHTMLに変換
                result_lines.append('<ol>')
                for item in list_items:
                    text = re.sub(r'^\d+\.\s+', '', item)
                    result_lines.append(f'    <li>{text}</li>')
                result_lines.append('</ol>')
                in_list = False
                list_items = []
            result_lines.append(line)
    
    if in_list:
        result_lines.append('<ol>')
        for item in list_items:
            text = re.sub(r'^\d+\.\s+', '', item)
            result_lines.append(f'    <li>{text}</li>')
        result_lines.append('</ol>')
    
    html = '\n'.join(result_lines)
    
    # 箇条書きリスト
    lines = html.split('\n')
    result_lines = []
    in_list = False
    list_items = []
    
    for line in lines:
        if re.match(r'^-\s+', line):
            if not in_list:
                in_list = True
                list_items = []
            text = re.sub(r'^-\s+', '', line)
            list_items.append(text)
        else:
            if in_list:
                result_lines.append('<ul>')
                for item in list_items:
                    result_lines.append(f'    <li>{item}</li>')
                result_lines.append('</ul>')
                in_list = False
                list_items = []
            result_lines.append(line)
    
    if in_list:
        result_lines.append('<ul>')
        for item in list_items:
            result_lines.append(f'    <li>{item}</li>')
        result_lines.append('</ul>')
    
    html = '\n'.join(result_lines)
    
    # 段落の処理（空行で区切る）
    html = re.sub(r'\n\n+', r'</p>\n<p>', html)
    html = '<p>' + html + '</p>'
    html = re.sub(r'<p></p>', '', html)
    html = re.sub(r'<p>(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ol>)', r'\1', html)
    html = re.sub(r'(</ol>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>)', r'\1', html)
    html = re.sub(r'(</ul>)</p>', r'\1', html)
    html = re.sub(r'<p>(<hr>)', r'\1', html)
    html = re.sub(r'(</hr>)</p>', r'\1', html)
    
    return html

def create_html_file(md_file, html_file):
    """Markdownファイルを読み込んでHTMLファイルを作成"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_body = markdown_to_html(md_content)
    
    # 特別な処理：練習ポイント、文章、問題、解答のクラスを追加
    html_body = re.sub(r'<strong>練習ポイント</strong>：(.+?)(?=<|$)', r'<div class="practice-point"><strong>練習ポイント</strong>：\1</div>', html_body, flags=re.DOTALL)
    html_body = re.sub(r'<strong>文章\d*</strong>', r'<div class="article"><strong>文章</strong>', html_body)
    html_body = re.sub(r'<strong>問題</strong>', r'</div><div class="question"><strong>問題</strong>', html_body)
    html_body = re.sub(r'<strong>解答例</strong>', r'</div><div class="answer"><strong>解答例</strong>', html_body)
    
    html_template = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_file.replace('.md', '')}</title>
    <style>
        body {{
            font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Meiryo", "MS PGothic", sans-serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
            margin-bottom: 20px;
        }}
        h3 {{
            color: #555;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        h4 {{
            color: #666;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        strong {{
            color: #e74c3c;
            font-weight: bold;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        .practice-point {{
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 15px 0;
        }}
        .article {{
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .question {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        .answer {{
            background-color: #d4edda;
            padding: 15px;
            border-left: 4px solid #28a745;
            margin: 15px 0;
        }}
        p {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
{html_body}
    </div>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f'Converted {md_file} to {html_file}')

if __name__ == '__main__':
    for i in range(2, 5):
        md_file = f'JTEST-FG-reading-practice-lesson{i}.md'
        html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
        create_html_file(md_file, html_file)
