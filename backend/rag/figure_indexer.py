import json
import re
from pathlib import Path
from rag.caption_finder import CaptionFinder
from rag.figure_vision import FigureVision
from rag.figure_detector import FigureDetector
from rag.figure_vision import FigureVision

from config import (
    FIGURE_INDEX_DIR,
)
class FigureIndexer:

    """
    Builds a searchable index of all figures
    found in every document.

    Output:

    figure_index.json
    """

    def __init__(self):
        self.caption_finder = CaptionFinder()

        self.detector = FigureDetector()

        self.vision = FigureVision()

        FIGURE_INDEX_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    
        
    def build_index(self, document_name):

            figures = self.extract_figures(document_name)

            index = []

            print(f"\nFound {len(figures)} figures")

            for figure in figures:

                if figure["figure"] != "1.10":
                    continue

                print("-" * 60)

                print(
                    f"Analyzing Figure {figure['figure']} "
                    f"(Page {figure['figure_page']})"
                )

                true_page = self.caption_finder.find_page(

                    figure["document"],

                    figure["figure"]

                )

                if true_page is None:

                    true_page = figure["page"]

                print("True Page :", true_page)

                description = self.vision.analyze(

                    figure["document"],

                    true_page

                )

                index.append({

                    "figure": figure["figure"],

                    "title": figure["title"],

                    "document": figure["document"],

                    "page": true_page,

                    "description": description

                })

            return index
        



    def save_index(self, document_name, index):

            output = FIGURE_INDEX_DIR / f"{document_name}.json"

            with open(output, "w", encoding="utf-8") as f:

                json.dump(

                    index,

                    f,

                    indent=4,

                    ensure_ascii=False

                )

            print(f"\nSaved Figure Index : {output}")
    def build_and_save(self, document_name):

                print("\n" + "=" * 60)
                print("BUILDING FIGURE INDEX")
                print("=" * 60)

                index = self.build_index(document_name)

                self.save_index(

                    document_name,

                    index

                )

                print(f"\nIndexed {len(index)} figures.")

                return index