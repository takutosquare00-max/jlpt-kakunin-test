import re

def fix_ol_indentation(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # ol要素の開始を検出
        if stripped == '<ol>':
            # 前の行を確認して、div要素内かどうかを判断
            context = '\n'.join(fixed_lines[-5:])
            if '<div class=' in context:
                # div要素内のol要素は12スペース
                fixed_lines.append('            <ol>')
            else:
                # 通常のol要素は8スペース
                fixed_lines.append('        <ol>')
            i += 1
            
            # ol要素内のli要素を処理
            while i < len(lines) and '</ol>' not in lines[i]:
                li_line = lines[i]
                li_stripped = li_line.strip()
                
                # li要素の開始
                if li_stripped.startswith('<li>'):
                    # 前の行を確認して、div要素内かどうかを判断
                    context = '\n'.join(fixed_lines[-5:])
                    if '<div class=' in context:
                        # div要素内のol要素内のli要素は16スペース
                        fixed_lines.append('                ' + li_stripped)
                    else:
                        # 通常のol要素内のli要素は12スペース
                        fixed_lines.append('            ' + li_stripped)
                else:
                    fixed_lines.append(li_line)
                i += 1
            
            # ol要素の終了
            if i < len(lines) and '</ol>' in lines[i]:
                context = '\n'.join(fixed_lines[-5:])
                if '<div class=' in context:
                    fixed_lines.append('            </ol>')
                else:
                    fixed_lines.append('        </ol>')
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed ol indentation in {html_file}')

for i in range(2, 5):
    html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
    fix_ol_indentation(html_file)
