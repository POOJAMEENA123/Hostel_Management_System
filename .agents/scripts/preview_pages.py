import fitz, os
os.makedirs(".agents/outputs", exist_ok=True)

files = {
    "Documentation/Presentation.pdf": "presentation_p1.png",
    "Documentation/SDD.pdf": "sdd_p1.png",
    "Documentation/SRS.pdf": "srs_p1.png",
    "Documentation/User Manual.pdf": "usermanual_p1.png",
}
for path, out in files.items():
    doc = fitz.open(path)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    pix.save(f".agents/outputs/{out}")
    doc.close()
    print(f"Saved {out}")
