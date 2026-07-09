from rag.caption_finder import CaptionFinder

finder = CaptionFinder()

page = finder.find_page(

    "Basic_Aerodynamics",

    "1.10"

)

print("\nReturned page:", page)