import re


class VisionGate:
    """
    Determines whether a user query actually
    requires visual reasoning.

    If False:
        Skip Vision completely.

    If True:
        Run Figure Retriever / Vision Retriever.
    """

    def __init__(self):

        self.figure_pattern = re.compile(
            r"figure\s+\d+[-.]\d+",
            re.IGNORECASE
        )

        self.visual_keywords = {

            "figure",
            "fig",
            "image",
            "photo",
            "picture",
            "diagram",
            "illustration",
            "graph",
            "chart",
            "plot",
            "table",
            "flowchart",
            "drawing",
            "layout",
            "shown",
            "show",
            "looks",
            "displayed",
            "visible",
            "see"

        }

    # -------------------------------------

    def requires_vision(self, question):

        q = question.lower()

        if self.figure_pattern.search(q):
            return True

        for word in self.visual_keywords:

            if word in q:
                return True

        return False