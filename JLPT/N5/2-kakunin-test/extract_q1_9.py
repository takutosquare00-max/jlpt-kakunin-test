#!/usr/bin/env python3
"""Extract questions 1-9 from N5 tests for validation."""
import re
import os

def extract_questions(html_path):
    questions = []
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all question blocks for q1-q9
    for q in range(1, 10):
        pattern = rf'<span class="q-num">{q}</span>(.*?)</div>\s*<div class="options">(.*?)</div>\s*<div class="explanation">(.*?)</div>'
        m = re.search(pattern, content, re.DOTALL)
        if m:
            q_text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            opts = re.findall(r'value="(\d)"[^>]*>.*?<label[^>]*>(\d+)\.\s*(.*?)</label>', m.group(2))
            expl = re.sub(r'<[^>]+>', '', m.group(3)).strip()
            questions.append({
                'num': q, 'text': q_text, 'options': opts, 'explanation': expl
            })
    return questions

base = os.path.dirname(os.path.abspath(__file__))
for v in range(11, 31):
    path = os.path.join(base, f'n5-10min-test-v{v}.html')
    if not os.path.exists(path):
        continue
    qs = extract_questions(path)
    print(f"\n=== v{v} ===")
    for q in qs:
        correct = [o for o in q['options'] if o[0]=='1']
        print(f"Q{q['num']}: {q['text'][:50]}...")
        for i, (val, num, txt) in enumerate(q['options']):
            mark = "✓" if val=='1' else " "
            print(f"  {mark} {num}. {txt}")
        if len(correct) != 1:
            print(f"  ⚠ 正解が{len(correct)}個!")
