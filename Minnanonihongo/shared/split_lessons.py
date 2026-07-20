from pypdf import PdfReader, PdfWriter
import os

PDF_PATH = '/Users/hayashi./DataxWorkspace/Developer/school/Minnanonihongo/shared/minnanonihongo all lessons.pdf'
OUT_DIR = '/Users/hayashi./DataxWorkspace/Developer/school/Minnanonihongo/shared/lessons'

OFFSET = 20  # PDF page = book page + OFFSET

# Sections: (name, start_book_page, end_book_page_inclusive)
sections = [
    ('00_introduction_preliminary', 1, 11),   # covers + intro + preliminary + terms + abbrev
    ('01_lesson1',  12, 17),
    ('02_lesson2',  18, 23),
    ('03_lesson3',  24, 29),
    ('04_lesson4',  30, 35),
    ('05_lesson5',  36, 41),
    ('06_lesson6',  42, 47),
    ('07_lesson7',  48, 53),
    ('08_lesson8',  54, 59),
    ('09_lesson9',  60, 65),
    ('10_lesson10', 66, 71),
    ('11_lesson11', 72, 77),
    ('12_lesson12', 78, 83),
    ('13_lesson13', 84, 89),
    ('14_lesson14', 90, 95),
    ('15_lesson15', 96, 101),
    ('16_lesson16', 102, 107),
    ('17_lesson17', 108, 113),
    ('18_lesson18', 114, 119),
    ('19_lesson19', 120, 125),
    ('20_lesson20', 126, 131),
    ('21_lesson21', 132, 137),
    ('22_lesson22', 138, 143),
    ('23_lesson23', 144, 149),
    ('24_lesson24', 150, 155),
    ('25_lesson25', 156, 162),
    ('26_summary',  163, 171),
    ('27_appendices', 172, 9999),  # to end
]

reader = PdfReader(PDF_PATH)
total = len(reader.pages)
print(f'Total PDF pages: {total}')

for name, start_book, end_book in sections:
    # Convert to 0-indexed PDF page numbers
    if start_book == 1:
        # Front matter: PDF pages 0..30 (book pages 1-11 but also covers)
        # Covers are PDF pages 0-2 (before book page numbering)
        pdf_start = 0
    else:
        pdf_start = start_book + OFFSET - 1  # 0-indexed

    if end_book == 9999:
        pdf_end = total - 1
    else:
        pdf_end = end_book + OFFSET - 1  # 0-indexed

    pdf_end = min(pdf_end, total - 1)

    writer = PdfWriter()
    for i in range(pdf_start, pdf_end + 1):
        writer.add_page(reader.pages[i])

    out_path = os.path.join(OUT_DIR, f'{name}.pdf')
    with open(out_path, 'wb') as f:
        writer.write(f)

    print(f'Created {name}.pdf  (PDF pages {pdf_start+1}-{pdf_end+1}, {pdf_end-pdf_start+1} pages)')

print('Done.')
