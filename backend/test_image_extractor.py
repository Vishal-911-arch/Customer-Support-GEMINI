from rag.image_extractor import ImageExtractor

pdf = "documents/manuals/Glider_Flying_Handbook.pdf"   # Replace with your PDF

extractor = ImageExtractor()

images = extractor.extract_images(pdf)

print(f"\nImages Found : {len(images)}\n")

for img in images:
    print(img)