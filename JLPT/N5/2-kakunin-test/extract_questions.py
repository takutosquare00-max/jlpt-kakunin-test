#!/usr/bin/env python3
"""Extract question stems from N5 test HTML files for duplicate checking."""
import re
import glob

def extract_stems(filepath):
    stems = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Q1-Q10 question texts (strip HTML, get text content)
    for i in range(1, 11):
        pat = rf'<div class="q-text">.*?<span class="q-num">{i}</span>(.*?)</div>'
        m = re.search(pat, content, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            text = re.sub(r'\s+', ' ', text)
            stems.append((i, text))
    # Reading passage for Q10
    rp = re.search(r'<div class="reading-passage">\s*(.*?)\s*</div>', content, re.DOTALL)
    if rp:
        passage = re.sub(r'\s+', ' ', rp.group(1).strip())
        stems.append((10, f"[PASSAGE] {passage}"))
    return stems

def main():
    files = sorted(glob.glob('n5-10min-test-v*.html'))
    all_stems = {}
    for f in files:
        v = re.search(r'v(\d+)', f).group(1)
        stems = extract_stems(f)
        all_stems[f] = stems
        print(f"\n=== {f} ===")
        for q, text in stems:
            if not text.startswith("[PASSAGE]"):
                print(f"  Q{q}: {text[:80]}...")
            else:
                print(f"  Q10 passage: {text[11:80]}...")
    return all_stems

if __name__ == '__main__':
    main()
