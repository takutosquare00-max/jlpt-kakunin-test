#!/usr/bin/env python3
"""Check for duplicate questions across N4 tests v1-v30."""

import re
from pathlib import Path
from collections import defaultdict

def extract_q_text(html_content):
    """Extract question texts (normalized) from HTML."""
    # Get q-text content, strip HTML tags, normalize
    pattern = r'<div class="q-text">(.*?)</div>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    texts = []
    for m in matches:
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', m)
        clean = re.sub(r'\s+', ' ', clean).strip()
        # Remove leading question number
        clean = re.sub(r'^\d+\s*', '', clean)
        if clean:
            texts.append(clean)
    return texts

def extract_reading(html_content):
    """Extract reading passage for Q10."""
    pattern = r'<div class="reading-passage">(.*?)</div>'
    m = re.search(pattern, html_content, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', ' ', m.group(1))
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean[:100]  # First 100 chars for comparison
    return ""

def main():
    base = Path(__file__).parent
    version_files = sorted(
        [f for f in base.glob("n4-10min-test-v*.html")],
        key=lambda p: int(re.search(r'v(\d+)', p.name).group(1))
    )
    
    # Map: normalized_question -> [(file, q_num), ...]
    question_to_sources = defaultdict(list)
    
    for filepath in version_files:
        content = filepath.read_text(encoding='utf-8')
        q_texts = extract_q_text(content)
        reading = extract_reading(content)
        
        for i, q in enumerate(q_texts):
            q_num = i + 1
            if q_num == 10 and reading:
                key = f"Q10:{reading}|{q[:50]}"
            else:
                key = f"Q{q_num}:{q}"
            question_to_sources[key].append((filepath.name, q_num))
    
    # Find duplicates
    duplicates = []
    for key, sources in question_to_sources.items():
        if len(sources) > 1:
            duplicates.append((key, sources))
    
    if duplicates:
        print("=== 重複している問題 ===\n")
        for key, sources in sorted(duplicates):
            print(f"問題: {key[:80]}...")
            for f, q in sources:
                print(f"  - {f} Q{q}")
            print()
    else:
        print("重複はありませんでした。")
    
    print(f"\n確認済み: {len(version_files)} ファイル")

if __name__ == "__main__":
    main()
