import re

def fix_li_tags(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 余分な</li>タグを削除
    content = re.sub(r'</li>\s*</li>', '</li>', content)
    
    # li要素内の選択肢を<br>タグで区切る
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # li要素の開始行を検出
        if stripped.startswith('<li>') and 'a)' in stripped:
            # li要素の内容を取得
            li_content = stripped.replace('<li>', '').replace('</li>', '').strip()
            
            # 選択肢を分割
            parts = li_content.split('。')
            if len(parts) > 1:
                question = parts[0] + '。'
                choices = parts[1].strip()
                
                # 選択肢をa) b) c) d)で分割
                choice_pattern = r'(a\)|b\)|c\)|d\))'
                choices_list = re.split(choice_pattern, choices)
                
                # フォーマット
                formatted = '                <li>' + question + '<br>\n'
                j = 1
                while j < len(choices_list):
                    if choices_list[j] in ['a)', 'b)', 'c)', 'd)']:
                        formatted += '                    ' + choices_list[j] + ' ' + choices_list[j+1].strip() + '<br>\n'
                        j += 2
                    else:
                        j += 1
                formatted = formatted.rstrip('\n') + '\n                </li>'
                fixed_lines.append(formatted)
            else:
                # 既に<br>タグがある場合はそのまま
                if '<br>' in stripped:
                    fixed_lines.append('                ' + stripped)
                else:
                    # 選択肢を検出して<br>タグを追加
                    if 'a)' in stripped and 'b)' in stripped:
                        # 複数行にわたる場合
                        li_parts = []
                        current_line = stripped
                        j = i + 1
                        while j < len(lines) and '</li>' not in lines[j] and (lines[j].strip().startswith('a)') or lines[j].strip().startswith('b)') or lines[j].strip().startswith('c)') or lines[j].strip().startswith('d)')):
                            current_line += ' ' + lines[j].strip()
                            j += 1
                        
                        # 選択肢を分割
                        question_match = re.match(r'<li>(.+?)。', current_line)
                        if question_match:
                            question = question_match.group(1) + '。'
                            choices_text = current_line.replace('<li>', '').replace('</li>', '').replace(question, '').strip()
                            
                            formatted = '                <li>' + question + '<br>\n'
                            choice_pattern = r'(a\)|b\)|c\)|d\))\s*([^a-d)]+)'
                            for match in re.finditer(choice_pattern, choices_text):
                                formatted += '                    ' + match.group(1) + ' ' + match.group(2).strip() + '<br>\n'
                            formatted = formatted.rstrip('\n') + '\n                </li>'
                            fixed_lines.append(formatted)
                            i = j - 1
                        else:
                            fixed_lines.append('                ' + stripped)
                    else:
                        fixed_lines.append('                ' + stripped)
        else:
            fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # 再度余分な</li>タグを削除
    content = re.sub(r'</li>\s*</li>', '</li>', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed li tags in {html_file}')

for i in range(2, 5):
    html_file = f'JTEST-FG-reading-practice-lesson{i}.html'
    fix_li_tags(html_file)
