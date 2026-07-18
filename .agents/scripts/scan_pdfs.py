import fitz
import os

pdfs = [
    "attached_assets/Presentation_1784373084351.pdf",
    "attached_assets/SDD_1784373084352.pdf",
    "attached_assets/SRS_1784373084353.pdf",
    "attached_assets/User_Manual_1784373084354.pdf",
]

# Names to look for
keywords = ["Bharat", "Prajwal", "Rakesh", "bharat", "prajwal", "rakesh",
            "NIT Calicut", "NITC", "nitc", "Author", "author"]

for pdf_path in pdfs:
    print(f"\n{'='*60}")
    print(f"FILE: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Pages: {doc.page_count}")
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        for kw in keywords:
            if kw in text:
                # Find context around the keyword
                idx = text.find(kw)
                while idx != -1:
                    snippet = text[max(0, idx-30):idx+50].replace('\n', ' ')
                    print(f"  Page {page_num+1} [{kw}]: ...{snippet}...")
                    idx = text.find(kw, idx+1)
    doc.close()
