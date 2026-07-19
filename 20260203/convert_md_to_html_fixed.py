#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def markdown_to_html_fixed(md_text):
    """Markdownテキストを正しいHTML構造に変換"""
    
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    list_type = None
    list_items = []
    in_article = False
    in_question = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 空行
        if not line:
            if in_list:
                # リストを閉じる
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            if in_article:
                html_lines.append('        </div>')
                in_article = False
            if in_question:
                html_lines.append('        </div>')
                in_question = False
            i += 1
            continue
        
        # 見出し
        if line.startswith('#### '):
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append(f'        <h4>{line[5:]}</h4>')
        elif line.startswith('### '):
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append(f'        <h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append(f'        <h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append(f'        <h1>{line[2:]}</h1>')
        
        # 水平線
        elif line == '---':
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            if in_article:
                html_lines.append('        </div>')
                in_article = False
            if in_question:
                html_lines.append('        </div>')
                in_question = False
            html_lines.append('        <hr>')
        
        # リスト項目
        elif re.match(r'^\d+\.\s+', line):
            if not in_list:
                in_list = True
                list_type = 'ol'
                list_items = []
            text = re.sub(r'^\d+\.\s+', '', line)
            list_items.append(text)
        elif re.match(r'^-\s+', line):
            if not in_list:
                in_list = True
                list_type = 'ul'
                list_items = []
            text = re.sub(r'^-\s+', '', line)
            list_items.append(text)
        
        # 文章の開始
        elif line.startswith('**文章') and not in_article:
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append('        <div class="article">')
            html_lines.append(f'            <strong>{line.replace("**", "")}</strong><br>')
            in_article = True
        
        # 問題の開始
        elif line.startswith('**問題') and not in_question:
            if in_article:
                html_lines.append('        </div>')
                in_article = False
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append('        <div class="question">')
            html_lines.append(f'            <strong>{line.replace("**", "")}</strong>')
            in_question = True
        
        # 解答例の開始
        elif line.startswith('**') and ('解答' in line or '練習' in line) and not in_question:
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            if in_article:
                html_lines.append('        </div>')
                in_article = False
            html_lines.append('        <div class="answer">')
            html_lines.append(f'            <strong>{line.replace("**", "")}</strong>')
            in_question = True
        
        # 練習ポイント
        elif '練習ポイント' in line:
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            text = re.sub(r'\*\*練習ポイント\*\*：', '', line)
            html_lines.append('        <div class="practice-point">')
            html_lines.append(f'            <strong>練習ポイント</strong>：{text}')
            html_lines.append('        </div>')
        
        # 通常のテキスト（文章の中）
        elif in_article and not line.startswith('**'):
            html_lines.append(f'            {line}')
        
        # 通常のテキスト（段落）
        elif not line.startswith('**') and not line.startswith('#') and not line.startswith('-') and not re.match(r'^\d+\.', line):
            if in_list:
                for item in list_items:
                    html_lines.append(f'    <li>{item}</li>')
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_items = []
                list_type = None
            html_lines.append(f'        <p>{line}</p>')
        
        i += 1
    
    # 最後のリストを閉じる
    if in_list:
        html_lines.append(f'<{list_type}>')
        for item in list_items:
            html_lines.append(f'    <li>{item}</li>')
        html_lines.append(f'</{list_type}>')
    
    # 最後のdivを閉じる
    if in_article:
        html_lines.append('        </div>')
    if in_question:
        html_lines.append('        </div>')
    
    return '\n'.join(html_lines)

def create_html_file_fixed(md_file, html_file):
    """Markdownファイルを読み込んで正しいHTMLファイルを作成"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_body = markdown_to_html_fixed(md_content)
    
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
        create_html_file_fixed(md_file, html_file)
