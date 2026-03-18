#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""マークダウンから解説を抽出し、HTMLの解説を更新する"""

import re

MD_PATH = '/Users/hayashi./datax/Business/school/J.TEST/202603student/202603ゴイさん/0315ゴイさんjtest_AC_解答.md'
HTML_PATH = '/Users/hayashi./datax/Business/school/J.TEST/202603student/jtest-ac-202603.html'

def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def parse_md():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = re.split(r'\n---\n', content)
    explanations = {}
    for block in blocks:
        m = re.search(r'\*\*\((\d+)\)\*\*', block)
        if not m:
            continue
        qnum = int(m.group(1))
        if qnum > 51:
            break
        expl_m = re.search(r'> ◆ 解説：(.+?)(?=\n\n|\n> |\Z)', block, re.DOTALL)
        if expl_m:
            expl = expl_m.group(1).strip()
            expl = re.sub(r'\n+', ' ', expl)
            expl = expl.replace('　', ' ')
            explanations[qnum] = expl
    return explanations

def update_html(explanations):
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 各 <div class="explanation"> を探して置換（出現順が問題番号1,2,3...に対応）
    pattern = r'(<div class="explanation">✅ 正解：\d+\. [^—]+— )(.*?)(</div>)'
    q_counter = [0]  # mutable for closure
    
    def replacer(match):
        prefix, old_expl, suffix = match.groups()
        q_counter[0] += 1
        qnum = q_counter[0]
        if qnum in explanations:
            new_expl = escape_html(explanations[qnum])
            return prefix + new_expl + suffix
        return match.group(0)
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Updated {HTML_PATH}')

def main():
    explanations = parse_md()
    print(f'Extracted {len(explanations)} explanations from markdown')
    update_html(explanations)

if __name__ == '__main__':
    main()
