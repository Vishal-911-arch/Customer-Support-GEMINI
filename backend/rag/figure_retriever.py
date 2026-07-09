from pathlib import Path
import json
import re

from config import FIGURE_INDEX_DIR

class FigureRetriever:

    def __init__(self):

        self.index_dir = FIGURE_INDEX_DIR

    # -------------------------------------------------------------
    def load_all_indexes(self):

        figures = []

        for file in self.index_dir.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:

                figures.extend(json.load(f))

        return figures
    def retrieve(self, question):

        match = re.search(

            r"^Figure\s+(\d+\.\d+)\.\s+(.+)$",

            question,

            re.IGNORECASE

        )

        if not match:

            return None

        figure = match.group(1)

        print(f"\nSearching Figure Index for Figure {figure}...")

        figures = self.load_all_indexes()

        for item in figures:

            if item["figure"] == figure:

                print(f"\n✓ Figure {figure} found")

                print("Document :", item["document"])

                print("Page     :", item["page"])

                return item

        return None