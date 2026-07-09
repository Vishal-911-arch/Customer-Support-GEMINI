from rag.page_renderer import PDFPageRenderer

renderer = PDFPageRenderer(
    dpi=300
)

pages = renderer.render_pdf(
    "documents/manuals/Glider_Flying_Handbook.pdf"
)

print()

print("="*60)

print("Rendered Pages")

print("="*60)

print()

print(f"Total Pages : {len(pages)}")

print()

for page in pages[:5]:

    print(page)