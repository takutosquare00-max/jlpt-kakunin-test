#!/usr/bin/env python3
"""Extract q-text and reading-passage from N4 test HTML files for duplicate checking."""

import re
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Extract text from HTML, preserving structure for q-text."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
    
    def handle_data(self, data):
        self.text_parts.append(data)
    
    def get_text(self):
        return "".join(self.text_parts).strip()

def extract_text(html_content):
    """Extract text from HTML string, stripping tags."""
    parser = TextExtractor()
    parser.feed(html_content)
    return parser.get_text()

def clean_q_text(text):
    """Remove leading question number (e.g. '1', '2') and normalize whitespace."""
    # Remove leading number and optional space/punctuation
    text = re.sub(r'^\s*\d+\s*', '', text)
    return text.strip()

def extract_questions_from_file(filepath):
    """Extract all question texts from an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    
    # Find all question blocks
    question_blocks = re.findall(
        r'<div class="question">(.*?)</div>\s*(?:<div class="options">|</div>)',
        content,
        re.DOTALL
    )
    
    # Alternative: find q-text and reading-passage directly
    q_text_pattern = r'<div class="q-text">(.*?)</div>'
    reading_pattern = r'<div class="reading-passage">(.*?)</div>'
    
    # Get all q-text blocks in order
    q_texts = re.findall(q_text_pattern, content, re.DOTALL)
    
    # Get reading passages (usually 1 per file, for Q10)
    reading_passages = re.findall(reading_pattern, content, re.DOTALL)
    
    for i, q_html in enumerate(q_texts):
        q_num = i + 1
        raw_text = extract_text(q_html)
        # Remove leading number from the extracted text
        q_content = clean_q_text(raw_text)
        
        if q_num == 10 and reading_passages:
            passage = extract_text(reading_passages[0]).strip()
            # For Q10: include both passage and question
            full_content = f"{passage} | {q_content}"
        else:
            full_content = q_content
        
        questions.append((q_num, full_content))
    
    return questions

def main():
    base = Path(__file__).parent
    all_questions = []
    
    # Check for n4-10min-test.html (without version)
    base_files = list(base.glob("n4-10min-test.html"))
    version_files = sorted(base.glob("n4-10min-test-v*.html"), 
                          key=lambda p: int(re.search(r'v(\d+)', p.name).group(1)) if re.search(r'v(\d+)', p.name) else 0)
    
    files_to_process = base_files + version_files
    
    for filepath in files_to_process:
        try:
            questions = extract_questions_from_file(filepath)
            all_questions.append((filepath.name, questions))
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    # Output: one question per line, format "Q#: [question text]"
    # Include file source for duplicate checking across files
    output_lines = []
    for filename, questions in all_questions:
        output_lines.append(f"\n=== {filename} ===")
        for q_num, q_text in questions:
            output_lines.append(f"Q{q_num}: {q_text}")
    
    output_path = base / "n4_extracted_questions.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    
    print(f"Extracted to {output_path}")
    print(f"Total: {len(files_to_process)} files, {sum(len(q) for _, q in all_questions)} questions")
    
    # Also print to stdout for immediate view
    print("\n" + "\n".join(output_lines))

if __name__ == "__main__":
    main()
