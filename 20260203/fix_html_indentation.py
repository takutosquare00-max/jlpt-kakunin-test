#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_html_indentation(html_file):
    """HTMLファイルのインデントとリスト構造を修正"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # リスト項目のインデントを統一
    content = re.sub(
        r'            <ol>\n                <li>',
        r'            <ol>\n                <li>',
        content
    )
    
    # インデントが不統一なリスト項目を修正
    content = re.sub(
        r'\n    <li>',
        r'\n                <li>',
        content
    )
    
    # </ol>のインデントを修正
    content = re.sub(
        r'\n</ol>',
        r'\n            </ol>',
        content
    )
    
    # 練習ポイントの構造を修正
    content = re.sub(
        r'<div class="answer">\s*<strong>練習ポイント：',
        r'<div class="practice-point">\n            <strong>練習ポイント</strong>：',
        content
    )
    
    # 解答例の構造を修正
    content = re.sub(
        r'<div class="article">\s*<strong>文章\d+</strong><br>\s*<ol>',
        r'<div class="answer">\n            <strong>文章</strong>\n            <ol>',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed indentation in {html_file}')

if __name__ == '__main__':
    for i in range(2, 5):
        html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
        fix_html_indentation(html_file)
