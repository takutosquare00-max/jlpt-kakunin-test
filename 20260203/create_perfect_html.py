#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def markdown_to_perfect_html(md_text):
    """Markdownを完璧なHTML構造に変換"""
    lines = md_text.split('\n')
    html_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 空行
        if not line:
            html_lines.append('')
            i += 1
            continue
        
        # 見出し
        if line.startswith('#### '):
            html_lines.append(f'        <h4>{line[5:]}</h4>')
        elif line.startswith('### '):
            html_lines.append(f'        <h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'        <h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'        <h1>{line[2:]}</h1>')
        
        # 水平線
        elif line == '---':
            html_lines.append('        <hr>')
        
        # 練習ポイント
        elif '練習ポイント' in line and line.startswith('**'):
            text = re.sub(r'\*\*練習ポイント\*\*：', '', line)
            html_lines.append('        <div class="practice-point">')
            html_lines.append(f'            <strong>練習ポイント</strong>：{text}')
            html_lines.append('        </div>')
        
        # 文章の開始
        elif line.startswith('**文章'):
            # 文章番号を取得
            article_num = ''
            if '文章' in line:
                match = re.search(r'文章(\d+|A)?', line)
                if match:
                    article_num = match.group(1) or ''
            
            html_lines.append('        <div class="article">')
            html_lines.append(f'            <strong>文章{article_num}</strong><br>')
            
            # 次の行から文章内容を読み込む
            i += 1
            article_lines = []
            while i < len(lines) and not lines[i].strip().startswith('**問題'):
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    article_lines.append(lines[i].strip())
                i += 1
            i -= 1  # 戻る
            
            # 文章内容を追加
            if article_lines:
                html_lines.append('            ' + ' '.join(article_lines))
            html_lines.append('        </div>')
        
        # 問題の開始
        elif line.startswith('**問題'):
            html_lines.append('        <div class="question">')
            question_text = line.replace('**', '')
            html_lines.append(f'            <strong>{question_text}</strong>')
            html_lines.append('            <ol>')
            
            # 次の行から問題を読み込む
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line or next_line.startswith('---') or next_line.startswith('#'):
                    break
                if re.match(r'^\d+\.\s+', next_line):
                    text = re.sub(r'^\d+\.\s+', '', next_line)
                    html_lines.append(f'                <li>{text}</li>')
                elif next_line.startswith('a)') or next_line.startswith('b)') or next_line.startswith('c)') or next_line.startswith('d)'):
                    # 選択肢
                    html_lines.append(f'                <li>{next_line}</li>')
                i += 1
            i -= 1
            
            html_lines.append('            </ol>')
            html_lines.append('        </div>')
        
        # 解答例
        elif line.startswith('**') and ('解答' in line or ('練習' in line and '（' in line)):
            html_lines.append('        <div class="answer">')
            answer_text = line.replace('**', '')
            html_lines.append(f'            <strong>{answer_text}</strong>')
            
            # 次の行から解答を読み込む
            i += 1
            answer_items = []
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line or (next_line.startswith('---') and answer_items) or (next_line.startswith('##') and answer_items):
                    break
                if re.match(r'^\d+\.\s+', next_line):
                    text = re.sub(r'^\d+\.\s+', '', next_line)
                    answer_items.append(text)
                i += 1
            i -= 1
            
            if answer_items:
                html_lines.append('            <ol>')
                for item in answer_items:
                    html_lines.append(f'                <li>{item}</li>')
                html_lines.append('            </ol>')
            html_lines.append('        </div>')
        
        # 番号付きリスト
        elif re.match(r'^\d+\.\s+', line):
            html_lines.append('        <ol>')
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
                text = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                html_lines.append(f'            <li>{text}</li>')
                i += 1
            i -= 1
            html_lines.append('        </ol>')
        
        # 箇条書きリスト
        elif line.startswith('- '):
            html_lines.append('        <ul>')
            while i < len(lines) and lines[i].strip().startswith('- '):
                text = lines[i].strip()[2:]
                html_lines.append(f'            <li>{text}</li>')
                i += 1
            i -= 1
            html_lines.append('        </ul>')
        
        # 通常の段落
        else:
            html_lines.append(f'        <p>{line}</p>')
        
        i += 1
    
    return '\n'.join(html_lines)

def create_perfect_html(md_file, html_file):
    """完璧なHTMLファイルを作成"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_body = markdown_to_perfect_html(md_content)
    
    title = md_file.replace('.md', '').replace('JTEST-FG-reading-practice-', 'J.TEST F級・G級 リーディング速度向上練習教材 ')
    
    html_template = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
    
    print(f'Created perfect HTML: {html_file}')

if __name__ == '__main__':
    for i in range(2, 5):
        md_file = f'JTEST-FG-reading-practice-lesson{i}.md'
        html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
        create_perfect_html(md_file, html_file)
