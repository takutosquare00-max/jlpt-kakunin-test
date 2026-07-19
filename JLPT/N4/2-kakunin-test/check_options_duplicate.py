#!/usr/bin/env python3
"""Check for duplicate options (選択肢) across N4 tests v26-v30."""

import re
from pathlib import Path
from collections import defaultdict

def extract_options(html_content):
    """Extract option texts from each question. Returns list of (q_num, [opt1, opt2, opt3, opt4])."""
    # Pattern: <label for="qNa">1. テキスト</label> or 2. テキスト etc.
    label_pattern = r'<label for="q\d+[a-d]">\d+\.\s*(.*?)</label>'
    
    questions = []
    # Split by question blocks
    question_blocks = re.split(r'<div class="question">', html_content)
    
    for block in question_blocks:
        labels = re.findall(label_pattern, block)
        if labels:
            # Clean option text (strip whitespace)
            opts = [l.strip() for l in labels]
            if len(opts) == 4:
                # Get question number from the block
                q_match = re.search(r'<span class="q-num">(\d+)</span>', block)
                q_num = int(q_match.group(1)) if q_match else 0
                questions.append((q_num, opts))
    
    return questions

def normalize_options(opts):
    """Create a normalized key for option set (sorted tuple) for comparison."""
    return tuple(sorted(opts))

def main():
    base = Path(__file__).parent
    files = sorted(
        [base / f"n4-10min-test-v{v}.html" for v in range(26, 31)],
        key=lambda p: int(re.search(r'v(\d+)', p.name).group(1))
    )
    
    # Map: (q_num, normalized_options) -> [(file, opts), ...]
    option_sets = defaultdict(list)
    # Map: individual option text -> [(file, q_num, position), ...]
    individual_options = defaultdict(list)
    
    for filepath in files:
        content = filepath.read_text(encoding='utf-8')
        questions = extract_options(content)
        
        for q_num, opts in questions:
            key = (q_num, normalize_options(opts))
            option_sets[key].append((filepath.name, opts))
            
            for i, opt in enumerate(opts):
                individual_options[opt].append((filepath.name, q_num, i+1))
    
    print("=" * 60)
    print("選択肢セットの重複（同じ問題番号で同じ4つの選択肢）")
    print("=" * 60)
    set_dups = [(k, v) for k, v in option_sets.items() if len(v) > 1]
    if set_dups:
        for (q_num, _), sources in set_dups:
            print(f"\nQ{q_num} で同じ選択肢セット:")
            for fname, opts in sources:
                print(f"  {fname}: {opts}")
    else:
        print("\n重複なし")
    
    print("\n" + "=" * 60)
    print("選択肢の重複（同じ選択肢が複数問題に出現）")
    print("=" * 60)
    # Filter: same option text in 2+ different (file, q_num) combinations
    opt_dups = []
    for opt_text, sources in individual_options.items():
        unique_sources = set((f, q) for f, q, _ in sources)
        if len(unique_sources) > 1:
            opt_dups.append((opt_text, sources))
    
    if opt_dups:
        for opt_text, sources in sorted(opt_dups, key=lambda x: -len(set((s[0], s[1]) for s in x[1]))):
            locations = set((s[0], s[1]) for s in sources)
            if len(locations) > 1:
                print(f"\n「{opt_text[:40]}{'...' if len(opt_text)>40 else ''}」")
                for f, q, pos in sorted(set(sources)):
                    print(f"  {f} Q{q} 選択肢{pos}")
    else:
        print("\n重複なし")
    
    # Also check for 予定/準備/計画/予約 type - common vocab options
    print("\n" + "=" * 60)
    print("語彙問題でよく使う選択肢の出現状況")
    print("=" * 60)
    common = ["予定", "準備", "計画", "予約", "資料", "返事"]
    for word in common:
        if word in individual_options:
            locs = individual_options[word]
            files_set = set(f for f, _, _ in locs)
            if len(files_set) > 1:
                print(f"「{word}」: {len(locs)}回出現")
                for f, q, pos in sorted(set((l[0], l[1], l[2]) for l in locs)):
                    print(f"  {f} Q{q} 選択肢{pos}")

if __name__ == "__main__":
    main()
