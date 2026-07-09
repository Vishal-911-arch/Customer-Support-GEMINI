import json

from langchain_core.documents import Document

from config import (
    FIGURE_INDEX_DIR,
    GRAPH_JSON_DIR
)


class ContextLinker:

    def __init__(self):

        self.figures = self.load_folder(FIGURE_INDEX_DIR)

        self.graphs = self.load_folder(GRAPH_JSON_DIR)

    # ----------------------------------------------------

    def load_folder(self, folder):

        items = []

        if not folder.exists():
            return items

        for file in folder.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:

                obj = json.load(f)

                if isinstance(obj, list):
                    items.extend(obj)
                else:
                    items.append(obj)

        return items

    # ----------------------------------------------------

    def nearest(self, page, collection):

        if len(collection) == 0:
            return None

        return min(
            collection,
            key=lambda x: abs(x["page"] - page)
        )

    # ----------------------------------------------------

    def link(self, chunks):

        linked = []

        print("\nLinking multimodal context...\n")

        for chunk in chunks:

            page = chunk.metadata.get("page", 0)

            document = chunk.metadata.get("source", "")

            figures = [

                x for x in self.figures

                if x["document"] in document

            ]

            graphs = [

                x for x in self.graphs

                if x["document"] in document

            ]

            figure = None

            for item in figures:
                if item["page"] == page:
                    figure = item
                    break

            graph = None

            for item in graphs:
                if item["page"] == page:
                    graph = item
                    break
            multimodal_text = chunk.page_content

# ---------------- Figure ----------------

            if figure:

                multimodal_text += "\n\n========== FIGURE ==========\n"

                multimodal_text += f"Title: {figure.get('title','')}\n\n"

                multimodal_text += figure.get("description","")

            # ---------------- Graph ----------------

            if graph:

                multimodal_text += "\n\n========== GRAPH ==========\n"

                multimodal_text += graph.get("ocr","")

                multimodal_text += "\n\n"

                multimodal_text += graph.get("vision","")

            # ---------------- Create Document ----------------

            linked.append(

                Document(

                    page_content=multimodal_text,

                    metadata=chunk.metadata

                )

            )

        print(f"Linked {len(linked)} chunks")

        return linked