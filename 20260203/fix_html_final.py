import re

def fix_html_structure(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # div要素の開始タグ（class="article", "question", "answer", "practice-point"）
        if stripped.startswith('<div class='):
            fixed_lines.append('        ' + stripped)
            i += 1
            # div要素内の内容を処理
            while i < len(lines) and '</div>' not in lines[i]:
                inner_line = lines[i]
                inner_stripped = inner_line.strip()
                
                # strongタグ
                if inner_stripped.startswith('<strong>'):
                    fixed_lines.append('            ' + inner_stripped)
                # brタグ
                elif inner_stripped == '<br>' or inner_stripped.startswith('<br>'):
                    fixed_lines.append('            ' + inner_stripped)
                # ol/ulタグ
                elif inner_stripped.startswith('<ol>') or inner_stripped.startswith('<ul>'):
                    fixed_lines.append('            ' + inner_stripped)
                elif inner_stripped.startswith('</ol>') or inner_stripped.startswith('</ul>'):
                    fixed_lines.append('            ' + inner_stripped)
                # liタグ
                elif inner_stripped.startswith('<li>'):
                    # li要素内の内容を処理
                    li_content = inner_stripped
                    # 複数行にわたるli要素の場合
                    if '</li>' not in li_content:
                        temp_lines = [inner_stripped]
                        j = i + 1
                        while j < len(lines) and '</li>' not in lines[j]:
                            temp_lines.append(lines[j].strip())
                            j += 1
                        if j < len(lines):
                            temp_lines.append(lines[j].strip())
                        li_content = ' '.join(temp_lines)
                        i = j
                    
                    # li要素内の選択肢（a) b) c) d)）を適切にフォーマット
                    if '<br>' in li_content:
                        parts = li_content.split('<br>')
                        fixed_lines.append('                <li>' + parts[0].replace('<li>', '').strip())
                        for part in parts[1:]:
                            if part.strip():
                                fixed_lines.append('                    ' + part.strip())
                        fixed_lines.append('                </li>')
                    else:
                        fixed_lines.append('                ' + li_content)
                # テキスト行（div要素内の通常のテキスト）
                elif inner_stripped and not inner_stripped.startswith('<'):
                    # article div内のテキスト
                    if '<div class="article">' in '\n'.join(fixed_lines[-5:]):
                        fixed_lines.append('            ' + inner_stripped)
                    else:
                        fixed_lines.append('            ' + inner_stripped)
                else:
                    fixed_lines.append(inner_line)
                i += 1
            
            # div要素の終了タグ
            if i < len(lines) and '</div>' in lines[i]:
                fixed_lines.append('        </div>')
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    # 後処理：li要素内の選択肢のインデントを修正
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # li要素内の選択肢（a) b) c) d)）を検出
        if stripped.startswith('a)') or stripped.startswith('b)') or stripped.startswith('c)') or stripped.startswith('d)'):
            # 前の行がli要素の開始か確認
            if i > 0 and '<li>' in lines[i-1]:
                fixed_lines.append('                    ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed structure in {html_file}')

for i in range(2, 5):
    html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
    fix_html_structure(html_file)
