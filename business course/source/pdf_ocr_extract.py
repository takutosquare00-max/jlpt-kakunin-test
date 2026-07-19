#!/usr/bin/env python3
"""
PDFページ100以降をPyMuPDFで画像に変換し、EasyOCRで日本語テキストを抽出するスクリプト

使い方:
  python pdf_ocr_extract.py              # 全ページ(100-214)
  python pdf_ocr_extract.py --end 110    # 100-110のみ（テスト用）
"""

import fitz  # PyMuPDF
import easyocr
import os
import sys
import tempfile
from pathlib import Path


def pdf_to_images(pdf_path: str, start_page: int = 100, end_page: int = None, dpi: int = 250) -> list:
    """
    PDFの指定ページ範囲を画像に変換する
    start_page, end_page: 1-based page numbers
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    if end_page is None:
        end_page = total_pages
    
    images = []
    for page_num in range(start_page - 1, min(end_page, total_pages)):  # 0-based index
        page = doc[page_num]
        # 解像度を上げてOCR精度を向上
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_data = pix.tobytes("png")
        images.append((page_num + 1, img_data))  # 1-based page number for output
    
    doc.close()
    return images


def ocr_images(images: list, reader=None) -> list:
    """EasyOCRで画像からテキストを抽出"""
    if reader is None:
        print("EasyOCRの初期化中（日本語+英語）...", flush=True)
        reader = easyocr.Reader(['ja', 'en'], gpu=False, verbose=False)
    
    results = []
    total = len(images)
    
    for i, (page_num, img_data) in enumerate(images):
        print(f"  OCR処理中: ページ {page_num} ({i+1}/{total})...", flush=True)
        
        # 一時ファイルに保存してEasyOCRに渡す
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(img_data)
            tmp_path = tmp.name
        
        try:
            ocr_result = reader.readtext(tmp_path, detail=1)
            # テキストをY座標でソート（上から下へ）
            ocr_result.sort(key=lambda x: (x[0][0][1], x[0][0][0]))
            text_blocks = [item[1] for item in ocr_result]
            page_text = "\n".join(text_blocks)
            results.append((page_num, page_text))
        finally:
            os.unlink(tmp_path)
    
    return results


def clean_ocr_text(text: str) -> str:
    """OCR結果からノイズを除去"""
    import re
    # PDFリーダー等のアーティファクトを除去
    noise_patterns = [
        r'Learning reading speed',
        r'Location \d+f?\d+',
        r'\d+%',
        r'\(中経出版\)\s*\([A-Z]*EDITION\)',
        r'JAPANESEEDITION',
        r'APANESEEDITION',
    ]
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or len(line) <= 1:  # 単一文字の行は文脈で結合される可能性
            continue
        # ノイズパターンに一致する行をスキップ
        skip = False
        for pat in noise_patterns:
            if re.search(pat, line, re.IGNORECASE):
                skip = True
                break
        if not skip:
            cleaned.append(line)
    return '\n'.join(cleaned)


def organize_to_markdown(results: list, title: str = "日本語のルール") -> str:
    """抽出したテキストをMarkdown形式に整理"""
    md_lines = [
        f"# {title}",
        "",
        "> **出典：** 日本語のルール.pdf よりOCR文字起こし（ページ100以降）",
        "> **作成方法：** PyMuPDF + EasyOCR",
        "> **注意：** スキャンPDFのため、OCRの精度に限りがあります。誤認識がある場合は元のPDFをご確認ください。",
        "",
        "---",
        ""
    ]
    
    for page_num, text in results:
        text = clean_ocr_text(text)
        if text.strip():
            md_lines.append(f"## ページ {page_num}")
            md_lines.append("")
            # テキストを整形（連続する空行を1つに）
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            for para in paragraphs:
                md_lines.append(para)
                md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    return "\n".join(md_lines)


def main():
    # コマンドライン引数: --start 115 --end 214 でページ範囲指定
    start_page = 100
    end_page = None
    if '--start' in sys.argv:
        idx = sys.argv.index('--start')
        if idx + 1 < len(sys.argv):
            start_page = int(sys.argv[idx + 1])
    if '--end' in sys.argv:
        idx = sys.argv.index('--end')
        if idx + 1 < len(sys.argv):
            end_page = int(sys.argv[idx + 1])
    
    pdf_path = Path(__file__).parent / "日本語のルール.pdf"
    
    if not pdf_path.exists():
        print(f"エラー: PDFファイルが見つかりません: {pdf_path}")
        return
    
    print("=" * 60, flush=True)
    print("PDF OCR 抽出スクリプト", flush=True)
    print("=" * 60, flush=True)
    print(f"PDF: {pdf_path}", flush=True)
    range_str = f"{start_page}-{end_page}" if end_page else f"{start_page}-214"
    print(f"対象: ページ {range_str}", flush=True)
    print(flush=True)
    
    # Step 1: PDFを画像に変換
    print("[1/3] PDFを画像に変換中...", flush=True)
    images = pdf_to_images(str(pdf_path), start_page=start_page, end_page=end_page, dpi=250)
    print(f"  → {len(images)} ページを変換しました")
    print()
    
    # Step 2: EasyOCRでテキスト抽出
    print("[2/3] EasyOCRでテキスト抽出中...")
    results = ocr_images(images)
    print()
    
    # Step 3: Markdownに整理
    print("[3/3] Markdown形式に整理中...")
    markdown_content = organize_to_markdown(results)
    
    # 出力ファイルに保存
    output_path = pdf_path.parent / "日本語のルール_OCR_ページ100以降.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"完了: {output_path}")
    print(f"総文字数: 約 {len(markdown_content)} 文字")


if __name__ == "__main__":
    main()
