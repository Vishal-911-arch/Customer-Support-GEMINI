from rag.graph_cropper import GraphCropper

IMAGE = r"artifacts/graph_analysis/Basic_Aerodynamics_page_17.png"

cropper = GraphCropper()

files = cropper.crop(IMAGE)

print(files)