import re

def fix_div_ol_li_indentation(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    in_div_ol = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # div要素の開始を検出
        if stripped.startswith('<div class='):
            fixed_lines.append(line)
            i += 1
            # div要素内を処理
            while i < len(lines) and '</div>' not in lines[i]:
                inner_line = lines[i]
                inner_stripped = inner_line.strip()
                
                # ol要素の開始を検出
                if inner_stripped == '<ol>':
                    in_div_ol = True
                    fixed_lines.append('            <ol>')
                    i += 1
                    # ol要素内のli要素を処理
                    while i < len(lines) and '</ol>' not in lines[i]:
                        li_line = lines[i]
                        li_stripped = li_line.strip()
                        
                        # li要素の開始
                        if li_stripped.startswith('<li>'):
                            # div要素内のol要素内のli要素は16スペース
                            fixed_lines.append('                ' + li_stripped)
                        else:
                            fixed_lines.append(li_line)
                        i += 1
                    
                    # ol要素の終了
                    if i < len(lines) and '</ol>' in lines[i]:
                        in_div_ol = False
                        fixed_lines.append('            </ol>')
                        i += 1
                else:
                    fixed_lines.append(inner_line)
                    i += 1
            
            # div要素の終了
            if i < len(lines) and '</div>' in lines[i]:
                fixed_lines.append('        </div>')
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed div ol li indentation in {html_file}')

for i in range(2, 5):
    html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
    fix_div_ol_li_indentation(html_file)
