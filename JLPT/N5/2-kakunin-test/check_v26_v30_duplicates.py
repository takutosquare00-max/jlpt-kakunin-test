#!/usr/bin/env python3
"""v26-v30間で完全に同じ問題がないかチェック"""
import re
from pathlib import Path

def extract_q_text(html_path):
    """HTMLから問題文（q-text）を抽出"""
    text = Path(html_path).read_text(encoding='utf-8')
    # 問題番号ごとに抽出（Q1-Q10）
    results = {}
    for q in range(1, 11):
        # <span class="q-num">N</span> の直後のテキストを取得
        pat = rf'<span class="q-num">{q}</span>(.*?)</div>'
        m = re.search(pat, text, re.DOTALL)
        if m:
            content = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            content = re.sub(r'\s+', ' ', content)
            results[q] = content
    # 読解の本文（Q10用）
    if 10 in results:
        passage = re.search(r'<div class="reading-passage">(.*?)</div>', text, re.DOTALL)
        if passage:
            p = re.sub(r'<[^>]+>', '', passage.group(1)).strip()
            p = re.sub(r'\s+', ' ', p)
            results['passage10'] = p
    return results

def main():
    base = Path(__file__).parent
    versions = [f'n5-10min-test-v{i}.html' for i in range(26, 31)]
    data = {}
    for v in versions:
        p = base / v
        if p.exists():
            data[v] = extract_q_text(p)

    # 各問題タイプで重複チェック
    for q in range(1, 11):
        seen = {}
        dupes = []
        for v, d in data.items():
            key = q if q != 10 else 'passage10'
            if key in d:
                val = d[key]
                if val in seen:
                    dupes.append((v, seen[val], val[:60]))
                else:
                    seen[val] = v
        if dupes:
            print(f"Q{q} 重複:")
            for a, b, s in dupes:
                print(f"  {a} と {b}: {s}...")
        else:
            print(f"Q{q}: 重複なし")

if __name__ == '__main__':
    main()
