#!/usr/bin/env python3
"""
N2確認テストの完全同一問題の重複チェック
問題文（q-text）と正解選択肢を正規化して比較する
"""
import re
import os
from pathlib import Path

def extract_questions(html_path):
    """HTMLファイルから問題を抽出"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    # 問題ブロックを抽出（div.question単位）
    question_blocks = re.split(r'<div class="question">', content)
    
    for block in question_blocks[1:]:  # 最初は空
        q_num_match = re.search(r'<span class="q-num">(\d+)</span>', block)
        if not q_num_match:
            continue
        q_num = int(q_num_match.group(1))
        
        q_text_match = re.search(r'<span class="q-num">\d+</span>(.*?)</div>', block, re.DOTALL)
        q_text = q_text_match.group(1) if q_text_match else ""
        q_text_clean = re.sub(r'<[^>]+>', '', q_text).strip()
        q_text_clean = re.sub(r'\s+', ' ', q_text_clean)
        
        # Q10（読解）の場合はreading-passageの内容も含める
        passage = ""
        if q_num == 10:
            passage_match = re.search(r'<div class="reading-passage">(.*?)</div>', block, re.DOTALL)
            if passage_match:
                passage = re.sub(r'<[^>]+>', '', passage_match.group(1)).strip()[:100]
        
        # optionsは複数のoption divを含むので、explanationの手前まで取得
        options_match = re.search(r'<div class="options">(.*?)</div>\s*<div class="explanation">', block, re.DOTALL)
        options = options_match.group(1) if options_match else ""
        # 正解は value="1" を含む option 内の label の内容
        correct_ans = ""
        for opt in re.finditer(r'<div class="option">(.*?)</div>', options, re.DOTALL):
            opt_content = opt.group(1)
            if 'value="1"' in opt_content:
                lbl = re.search(r'<label[^>]*>\d+\.\s*(.*?)</label>', opt_content)
                if lbl:
                    correct_ans = lbl.group(1).strip()
                break
        
        # 署名：問題文+正解。Q10は本文の冒頭も含める
        sig_text = f"{q_text_clean}|{passage}|{correct_ans}"
        questions.append({
            'num': q_num,
            'text': q_text_clean,
            'correct': correct_ans,
            'signature': sig_text
        })
    
    return questions

def main():
    base_dir = Path(__file__).parent
    html_files = sorted([f for f in base_dir.glob('n2-10min-test-v*.html')])
    
    all_questions = {}  # signature -> (file, q_num)
    duplicates = []
    
    for html_file in html_files:
        version = html_file.stem.replace('n2-10min-test-', '')
        try:
            questions = extract_questions(html_file)
            for q in questions:
                sig = q['signature']
                if sig in all_questions:
                    orig_file, orig_q = all_questions[sig]
                    duplicates.append({
                        'dup': (str(html_file.name), q['num'], q['text'][:50], q['correct'][:20]),
                        'orig': (orig_file, orig_q)
                    })
                else:
                    all_questions[sig] = (html_file.name, q['num'])
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    print("=" * 60)
    print("N2 確認テスト 重複チェック結果")
    print("=" * 60)
    print(f"チェック対象: {len(html_files)} ファイル")
    print(f"総問題数: {len(all_questions)} ユニーク問題")
    print()
    
    if duplicates:
        print("⚠️ 重複が見つかりました:")
        for d in duplicates:
            print(f"  - {d['dup'][0]} Q{d['dup'][1]}: {d['dup'][2]}... (正解:{d['dup'][3]})")
            print(f"    重複元: {d['orig'][0]} Q{d['orig'][1]}")
        print(f"\n重複数: {len(duplicates)}")
    else:
        print("✅ 完全に同じ問題の重複はありませんでした。")
    
    return len(duplicates)

if __name__ == '__main__':
    exit(main())
