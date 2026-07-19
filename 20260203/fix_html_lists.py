#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_html_lists(html_file):
    """HTMLファイルのリスト構造を修正"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # <li>タグの前に<ol>タグがない場合を修正
    # <strong>問題</strong>の後に<ol>がない場合
    content = re.sub(
        r'(<strong>問題</strong>)\s*(<li>)',
        r'\1\n            <ol>\n                \2',
        content
    )
    
    # </ol>の前に</div>がある場合を修正
    content = re.sub(
        r'(</ol>)\s*(</div>)',
        r'\1\n        \2',
        content
    )
    
    # 解答例のリストも修正
    content = re.sub(
        r'(<strong>文章\d+</strong><br>)\s*(<li>)',
        r'\1\n            <ol>\n                \2',
        content
    )
    
    # 解答例のリストも修正（文章番号なしの場合）
    content = re.sub(
        r'(<div class="answer">)\s*(<strong>[^<]+</strong>)\s*(<li>)',
        r'\1\n            \2\n            <ol>\n                \3',
        content
    )
    
    # 選択問題の構造を修正（lesson3）
    # a) b) c) d) の選択肢を正しく処理
    content = re.sub(
        r'</ol>\s*([a-d]\)\s*[^\n]+)',
        r'</ol>\n                <p>\1</p>',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed lists in {html_file}')

if __name__ == '__main__':
    for i in range(2, 5):
        html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
        fix_html_lists(html_file)
