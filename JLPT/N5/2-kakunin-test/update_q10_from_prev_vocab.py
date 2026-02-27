#!/usr/bin/env python3
"""
v2-v30のQ10を、それぞれ前のテスト(v1-v29)のQ1-Q9で出題された単語を使って作成する。
"""
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def extract_vocab_from_html(html):
    """Q1-Q9から語彙を抽出。q-textの内容と正解オプションのラベルから単語を取得"""
    vocab = set()
    # Q1-Q9のq-textを抽出
    q_texts = re.findall(r'<div class="q-text"><span class="q-num">\d</span>([^<]+)</div>', html)
    for i, text in enumerate(q_texts[:9]):  # Q1-Q9のみ
        # <strong>タグを除去してテキスト取得
        clean = re.sub(r'<[^>]+>', '', text)
        clean = clean.replace('　', ' ').strip()
        # 単語に分割（ひらがな、カタカナ、漢字の境界で）
        words = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u0020-\u007E]+', clean)
        for w in words:
            w = w.strip()
            if len(w) >= 2 and w not in ('から', 'まで', 'ので', 'のに', 'では', 'には', 'を', 'に', 'で', 'が', 'は', 'へ', 'と'):
                vocab.add(w)
    # 正解オプション(value="1")のラベルからも取得
    options = re.findall(r'<label for="q\d+[abcd]">\d+\. ([^<]+)</label>', html)
    for opt in options:
        opt = opt.strip()
        if len(opt) >= 2:
            vocab.add(opt)
    return vocab

def create_passage_from_vocab(vocab, prev_correct_answer=None):
    """
    語彙を使って読解文を作成。
    のりもので問題を基本形とする。vocabに含まれる単語をできるだけ使う。
    """
    # よく使う語彙をチェック
    has_bus = any('バス' in v or 'ばす' in v for v in vocab)
    has_dencha = any('でんしゃ' in v or '電車' in v for v in vocab)
    has_jitensha = any('じてんしゃ' in v or '自転車' in v for v in vocab)
    has_chikatetsu = any('ちかてつ' in v or '地下鉄' in v for v in vocab)
    has_aruite = any('あるいて' in v for v in vocab)
    has_asagohan = any('あさごはん' in v or '朝ご飯' in v for v in vocab)
    has_gakkou = any('がっこう' in v or '学校' in v for v in vocab)
    has_kaisha = any('かいしゃ' in v for v in vocab)
    has_eki = any('えき' in v or '駅' in v for v in vocab)
    has_tomodachi = any('ともだち' in v for v in vocab)
    has_hon = any('ほん' in v or '本' in v for v in vocab)
    has_yasashii = any('やさしい' in v for v in vocab)
    has_nihongo = any('にほんご' in v for v in vocab)
    has_benkyou = any('べんきょう' in v for v in vocab)
    has_kinou = any('きのう' in v for v in vocab)
    has_ashita = any('あした' in v for v in vocab)
    has_maiasa = any('まいあさ' in v or 'まいにち' in v for v in vocab)
    
    # 使える乗り物を決定（vocabに含まれるものから）
    norimono = None
    wrong = []
    if has_dencha:
        norimono = 'でんしゃ'
        wrong = ['バス', 'じてんしゃ', 'あるいて'] if not has_bus else ['じてんしゃ', 'ちかてつ', 'あるいて']
    elif has_chikatetsu:
        norimono = 'ちかてつ'
        wrong = ['バス', 'でんしゃ', 'じてんしゃ']
    elif has_jitensha:
        norimono = 'じてんしゃ'
        wrong = ['バス', 'でんしゃ', 'あるいて']
    elif has_bus:
        norimono = 'バス'
        wrong = ['でんしゃ', 'じてんしゃ', 'あるいて']
    elif has_aruite:
        norimono = 'あるいて'
        wrong = ['バス', 'でんしゃ', 'じてんしゃ']
    else:
        norimono = 'でんしゃ'
        wrong = ['バス', 'じてんしゃ', 'あるいて']
    
    # 場所
    place = 'がっこう' if has_gakkou else 'かいしゃ' if has_kaisha else 'がっこう'
    
    #  passage構築
    parts = []
    name = 'たなかさん'
    
    if has_maiasa or has_asagohan:
        parts.append(f"{name}は まいにち 7じに おきます。")
        if has_asagohan:
            parts.append("あさごはんを たべて、7じはんに いえを でます。")
    else:
        parts.append(f"{name}は まいにち 7じに おきます。7じはんに いえを でます。")
    
    if has_eki and norimono != 'あるいて':
        parts.append(f"えきまで あるいて 10ぷん いきます。")
    
    parts.append(f"{norimono}で {place}に いきます。")
    
    if has_hon and has_yasashii:
        parts.append("がっこうで にほんごの ほんを よみます。この ほんは やさしいです。")
    elif has_nihongo and has_benkyou:
        parts.append("がっこうで にほんごを べんきょうします。")
    
    if has_tomodachi and has_eki:
        day = "きのう" if has_kinou else "あした" if has_ashita else "まいにち"
        parts.append(f"{day} えきで ともだちと あいました。")
    
    passage = "".join(parts)
    question = f"{name}は {place}に なんの のりもので いきますか。"
    
    return passage, question, norimono, wrong

def main():
    for n in range(2, 31):
        prev_file = os.path.join(BASE, f'n5-10min-test-v{n-1}.html')
        curr_file = os.path.join(BASE, f'n5-10min-test-v{n}.html')
        if not os.path.exists(prev_file) or not os.path.exists(curr_file):
            print(f"Skip v{n}: file not found")
            continue
        with open(prev_file, 'r', encoding='utf-8') as f:
            prev_html = f.read()
        with open(curr_file, 'r', encoding='utf-8') as f:
            curr_html = f.read()
        
        vocab = extract_vocab_from_html(prev_html)
        # 現在のQ10の正解を取得
        match = re.search(r'<div class="option"><input type="radio" name="q10"[^>]*value="1"[^>]*><label for="q10[abcd]">[^<]*\d+\. ([^<]+)</label>', curr_html)
        prev_correct = match.group(1).strip() if match else None
        
        passage, question, correct, wrong = create_passage_from_vocab(vocab, prev_correct)
        
        print(f"--- v{n} (uses v{n-1} vocab) ---")
        print(f"Passage: {passage}")
        print(f"Q: {question}")
        print(f"Correct: {correct}, Wrong: {wrong}")
        print()

if __name__ == '__main__':
    main()
