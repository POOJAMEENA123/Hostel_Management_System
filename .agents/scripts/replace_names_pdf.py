import fitz
import os

REPLACEMENTS = [
    ("Ghoradkar Prajwal Pandurang", "Pooja Meena"),
    ("Rakesh Chowdary Yarlagadda",  "Pooja Meena"),
    ("T. Bharat Bhushan Reddy",     "Pooja Meena"),
    # roll numbers — just erase
    ("B160497CS", ""),
    ("B160710CS", ""),
    ("B160198CS", ""),
]

FILES = {
    "attached_assets/Presentation_1784373084351.pdf": "Documentation/Presentation.pdf",
    "attached_assets/SDD_1784373084352.pdf":          "Documentation/SDD.pdf",
    "attached_assets/SRS_1784373084353.pdf":          "Documentation/SRS.pdf",
    "attached_assets/User_Manual_1784373084354.pdf":  "Documentation/User Manual.pdf",
}

os.makedirs("Documentation", exist_ok=True)

for src, dst in FILES.items():
    print(f"\nProcessing: {src}")
    doc = fitz.open(src)

    for page_num in range(doc.page_count):
        page = doc[page_num]

        # Step 1: collect all hits with their rects BEFORE redacting
        hits = []
        for old_text, new_text in REPLACEMENTS:
            for rect in page.search_for(old_text):
                hits.append((rect, new_text, old_text))
                print(f"  Page {page_num+1}: '{old_text}' → '{new_text}' @ {rect}")

        if not hits:
            continue

        # Step 2: redact all hits (white box)
        for rect, new_text, old_text in hits:
            page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

        # Step 3: insert replacement text at the saved positions
        for rect, new_text, old_text in hits:
            if not new_text:
                continue
            fontsize = rect.height * 0.72   # scale to fit original line height
            page.insert_text(
                (rect.x0, rect.y1 - 2),
                new_text,
                fontsize=fontsize,
                color=(0, 0, 0),
            )

    doc.save(dst)
    doc.close()
    print(f"  → Saved: {dst}")

print("\nAll done!")
