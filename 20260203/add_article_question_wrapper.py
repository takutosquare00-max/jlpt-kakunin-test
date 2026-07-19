import re

def add_wrapper(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # articleの後にquestionが続くパターンを検出してラッパーで囲む
    # パターン: </div>\n        <div class="question">
    pattern = r'(</div>\s*)\n(\s*)<div class="question">'
    
    def replace_func(match):
        closing_div = match.group(1)
        indent = match.group(2)
        # 前のarticleの開始タグを探す
        return f'{closing_div}\n{indent}</div>\n{indent}<div class="article-question-wrapper">\n{indent}    <div class="article">'
    
    # まず、articleの開始タグの前にラッパーを追加
    # articleの直後にquestionがある場合を検出
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # articleの開始タグを検出
        if '<div class="article">' in line:
            # 次の数行を確認してquestionがあるかチェック
            article_start_idx = i
            article_lines = [line]
            i += 1
            
            # articleの終了タグまで読み込む
            while i < len(lines) and '</div>' not in lines[i]:
                article_lines.append(lines[i])
                i += 1
            
            # articleの終了タグ
            if i < len(lines):
                article_lines.append(lines[i])
                i += 1
            
            # 次の行が空行か、questionの開始かチェック
            if i < len(lines):
                # 空行をスキップ
                while i < len(lines) and lines[i].strip() == '':
                    article_lines.append(lines[i])
                    i += 1
                
                # questionの開始をチェック
                if i < len(lines) and '<div class="question">' in lines[i]:
                    # ラッパーで囲む
                    indent = '        '
                    new_lines.append(f'{indent}<div class="article-question-wrapper">')
                    # articleの開始タグのインデントを調整
                    article_lines[0] = f'{indent}    <div class="article">'
                    new_lines.extend(article_lines)
                    
                    # questionの行を読み込む
                    question_start_idx = i
                    question_lines = []
                    question_lines.append(f'{indent}    <div class="question">')
                    i += 1
                    
                    # questionの終了タグまで読み込む
                    while i < len(lines) and '</div>' not in lines[i]:
                        # インデントを調整
                        if lines[i].strip():
                            indent_level = len(lines[i]) - len(lines[i].lstrip())
                            if indent_level >= 8:
                                question_lines.append('    ' + lines[i].lstrip())
                            else:
                                question_lines.append(lines[i])
                        else:
                            question_lines.append(lines[i])
                        i += 1
                    
                    # questionの終了タグ
                    if i < len(lines):
                        question_lines.append(f'{indent}    </div>')
                        i += 1
                    
                    new_lines.extend(question_lines)
                    new_lines.append(f'{indent}</div>')
                else:
                    # questionがない場合はそのまま
                    new_lines.extend(article_lines)
            else:
                new_lines.extend(article_lines)
        else:
            new_lines.append(line)
            i += 1
    
    content = '\n'.join(new_lines)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Updated {html_file}')

for i in range(1, 5):
    html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
    add_wrapper(html_file)
