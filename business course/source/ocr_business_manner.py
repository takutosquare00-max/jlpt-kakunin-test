#!/usr/bin/env python3
"""
ビジネスマナー.pdf をOCRで文字起こしするスクリプト
"""

import fitz
import easyocr
import os
import re
import sys
import tempfile
from pathlib import Path


def pdf_to_images(pdf_path: str, start_page: int = 1, end_page: int = None, dpi: int = 150) -> list:
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    if end_page is None:
        end_page = total_pages
    images = []
    for page_num in range(start_page - 1, min(end_page, total_pages)):
        page = doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_data = pix.tobytes("png")
        images.append((page_num + 1, img_data))
    doc.close()
    return images


def ocr_images(images: list, reader=None) -> list:
    if reader is None:
        print("EasyOCRの初期化中...", flush=True)
        reader = easyocr.Reader(['ja', 'en'], gpu=False, verbose=False)
    results = []
    total = len(images)
    for i, (page_num, img_data) in enumerate(images):
        print(f"  OCR: ページ {page_num} ({i+1}/{total})...", flush=True)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(img_data)
            tmp_path = tmp.name
        try:
            ocr_result = reader.readtext(tmp_path, detail=1)
            ocr_result.sort(key=lambda x: (x[0][0][1], x[0][0][0]))
            text_blocks = [item[1] for item in ocr_result]
            page_text = "\n".join(text_blocks)
            results.append((page_num, page_text))
        finally:
            os.unlink(tmp_path)
    return results


def clean_ocr_text(text: str) -> str:
    noise_patterns = [
        r'Learning reading speed', r'Location \d+f?\d+', r'\d+%',
        r'\(中経出版\)\s*\([A-Z]*EDITION\)', r'JAPANESEEDITION',
    ]
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or len(line) <= 1:
            continue
        skip = any(re.search(p, line, re.I) for p in noise_patterns)
        if not skip:
            cleaned.append(line)
    return '\n'.join(cleaned)


def main():
    pdf_path = Path(__file__).parent / "ビジネスマナー.pdf"
    if not pdf_path.exists():
        print(f"エラー: {pdf_path} が見つかりません")
        return 1

    print("ビジネスマナー.pdf OCR処理開始...", flush=True)
    images = pdf_to_images(str(pdf_path), start_page=1, dpi=150)
    print(f"  {len(images)} ページを変換", flush=True)
    
    results = ocr_images(images)
    
    md_lines = [
        "# ビジネスマナー",
        "",
        "> **出典：** ビジネスマナー.pdf よりOCR文字起こし",
        "> **作成方法：** PyMuPDF + EasyOCR",
        "> **注意：** スキャンPDFのため、OCRの精度に限りがあります。",
        "",
        "---", ""
    ]
    
    for page_num, text in results:
        text = clean_ocr_text(text)
        if text.strip():
            md_lines.append(f"## ページ {page_num}")
            md_lines.append("")
            for para in [p.strip() for p in text.split('\n') if p.strip()]:
                md_lines.append(para)
                md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    output_path = pdf_path.parent / "ビジネスマナー_文字起こし.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
    
    print(f"完了: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
