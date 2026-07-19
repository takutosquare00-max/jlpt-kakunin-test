#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_html_structure(html_content):
    """HTMLの構造を修正"""
    
    # <hr></p> を <hr> に修正
    html_content = re.sub(r'<hr></p>', r'<hr>', html_content)
    
    # <p>タグの中に<div>が入っている場合を修正
    html_content = re.sub(r'<p><div class="([^"]+)">', r'<div class="\1">', html_content)
    html_content = re.sub(r'</div></p>', r'</div>', html_content)
    
    # <p>タグの中に<ul>や<ol>が入っている場合を修正
    html_content = re.sub(r'<p>([^<]*?)<ul>', r'\1<ul>', html_content)
    html_content = re.sub(r'<p>([^<]*?)<ol>', r'\1<ol>', html_content)
    html_content = re.sub(r'</ul></p>', r'</ul>', html_content)
    html_content = re.sub(r'</ol></p>', r'</ol>', html_content)
    
    # <p>タグの中に<h2>などが入っている場合を修正
    html_content = re.sub(r'<p>([^<]*?)<h([1-6])>', r'\1<h\2>', html_content)
    html_content = re.sub(r'</h([1-6])></p>', r'</h\1>', html_content)
    
    # 不正な<p>タグを削除
    html_content = re.sub(r'<p>\s*</p>', r'', html_content)
    html_content = re.sub(r'<p>\s*<hr>', r'<hr>', html_content)
    
    # 文章と問題の構造を修正
    # <div class="article">の後に問題が来る場合
    html_content = re.sub(r'</div><div class="question">', r'</div>\n        <div class="question">', html_content)
    
    # 選択問題の構造を修正（lesson3）
    # 選択肢がリスト外にある場合を修正
    html_content = re.sub(r'</ol>\s*([a-d]\)\s*[^\n]+)', r'</ol>\n            <p>\1</p>', html_content)
    
    # 段落の構造を修正
    # 連続する<p>タグを整理
    html_content = re.sub(r'</p>\s*<p>', r'<br>\n            ', html_content)
    
    # 文章の構造を修正（文章番号を追加）
    html_content = re.sub(r'<div class="article"><strong>文章</strong>', r'<div class="article">\n            <strong>文章</strong>', html_content)
    
    return html_content

def process_html_file(html_file):
    """HTMLファイルを読み込んで修正"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 構造を修正
    fixed_content = fix_html_structure(content)
    
    # ファイルに書き戻し
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f'Fixed {html_file}')

if __name__ == '__main__':
    for i in range(2, 5):
        html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
        process_html_file(html_file)
