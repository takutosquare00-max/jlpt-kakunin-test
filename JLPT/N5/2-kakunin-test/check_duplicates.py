#!/usr/bin/env python3
"""Check for duplicate question stems between v26-v30 and v1-v25."""
import re
import glob

def extract_stems(filepath):
    stems = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for i in range(1, 11):
        pat = rf'<div class="q-text">.*?<span class="q-num">{i}</span>(.*?)</div>'
        m = re.search(pat, content, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            text = re.sub(r'\s+', ' ', text)
            # Normalize: remove ( ) blanks for comparison
            norm = re.sub(r'[（\(][　\s]*[）\)]', '（　）', text)
            stems.append((i, text, norm))
    return stems

def main():
    # Get v1-v25 stems
    old_stems = {}
    for f in sorted(glob.glob('n5-10min-test-v*.html')):
        m = re.search(r'v(\d+)', f)
        if m and 1 <= int(m.group(1)) <= 25:
            stems = extract_stems(f)
            for q, text, norm in stems:
                key = (q, norm)
                if key not in old_stems:
                    old_stems[key] = []
                old_stems[key].append((f, text))

    # Get v26-v30 stems and check
    duplicates = []
    for f in sorted(glob.glob('n5-10min-test-v2[6-9].html')) + sorted(glob.glob('n5-10min-test-v30.html')):
        stems = extract_stems(f)
        for q, text, norm in stems:
            key = (q, norm)
            if key in old_stems:
                for old_file, old_text in old_stems[key]:
                    duplicates.append({
                        'new_file': f,
                        'old_file': old_file,
                        'q': q,
                        'stem': text[:60] + '...' if len(text) > 60 else text,
                    })

    # Also check stem similarity (partial match)
    new_stems = {}
    for f in sorted(glob.glob('n5-10min-test-v2[6-9].html')) + sorted(glob.glob('n5-10min-test-v30.html')):
        stems = extract_stems(f)
        new_stems[f] = stems

    print("=== Duplicate Check Report ===\n")
    print(f"Exact duplicate question stems: {len(duplicates)}")
    if duplicates:
        for d in duplicates:
            print(f"  - {d['new_file']} Q{d['q']} duplicates {d['old_file']}")
            print(f"    Stem: {d['stem']}")
    else:
        print("  No exact duplicates found.")

    # List all v26-v30 stems for manual review
    print("\n=== v26-v30 Question Stems (for reference) ===")
    for f in sorted(glob.glob('n5-10min-test-v2[6-9].html')) + sorted(glob.glob('n5-10min-test-v30.html')):
        stems = extract_stems(f)
        print(f"\n{f}:")
        for q, text, _ in stems:
            short = text[:70] + '...' if len(text) > 70 else text
            print(f"  Q{q}: {short}")

if __name__ == '__main__':
    main()
