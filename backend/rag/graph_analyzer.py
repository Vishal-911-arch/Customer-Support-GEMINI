import base64

from ollama import Client

from config import (
    OLLAMA_HOST,
    VISION_MODEL
)
import json
import cv2

from config import (
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR,
    GRAPH_ANALYSIS_DIR,
    GRAPH_JSON_DIR
)

from rag.ocr import OCRProcessor


class GraphAnalyzer:

    def __init__(self):

        self.padding = 40

        self.ocr = OCRProcessor()

        self.client = Client(host=OLLAMA_HOST)
    # ------------------------------------------------------------

    def crop_graph(self, document, page):

        image_path = (
            RENDERED_PAGES_DIR
            / document
            / f"page_{page}.png"
        )

        json_path = (
            IMAGE_CLASSIFIER_OUTPUT_DIR
            / document
            / f"page_{page}.json"
        )

        if not image_path.exists():
            return None

        if not json_path.exists():
            return None

        image = cv2.imread(str(image_path))

        with open(json_path, "r") as f:
            detections = json.load(f)

        for det in detections:

            if det["type"] != "graph":
                continue

            x, y, w, h = det["bbox"]

            xmin = max(x - self.padding, 0)
            ymin = max(y - self.padding, 0)

            xmax = min(x + w + self.padding, image.shape[1])
            ymax = min(y + h + self.padding, image.shape[0])

            crop = image[ymin:ymax, xmin:xmax]

            output = (
                GRAPH_ANALYSIS_DIR
                / f"{document}_page_{page}.png"
            )

            cv2.imwrite(str(output), crop)

            print(f"\nSaved Graph Crop : {output}")

            return crop

        return None

    # ------------------------------------------------------------

    def analyze(self, document, page):

        print("\n" + "=" * 60)
        print("GRAPH ANALYZER")
        print("=" * 60)

        crop = self.crop_graph(document, page)

        if crop is None:

            print("No graph detected.")

            return None

        print("\nRunning OCR...")

        print("\nRunning OCR...")

        text = self.ocr.process_crop(crop)

        print("\nRunning Vision...")

        vision = self.understand_graph(crop)

        graph = {

    "document": document,

    "page": page,

    "ocr_text": text,

    "vision_summary": vision

}

        output = (

            GRAPH_JSON_DIR
            / f"{document}_page_{page}.json"

        )

        with open(output, "w", encoding="utf-8") as f:

            json.dump(

                graph,

                f,

                indent=4,

                ensure_ascii=False

            )

        print(f"\nSaved Graph JSON : {output}")

        return graph
    
    # ------------------------------------------------------------

    def encode(self, image):

        ok, buffer = cv2.imencode(".png", image)

        if not ok:
            return None

        return base64.b64encode(buffer).decode()

    # ------------------------------------------------------------

    def understand_graph(self, crop):

        encoded = self.encode(crop)

        response = self.client.generate(

            model=VISION_MODEL,

            prompt="""
    You are an aerospace engineering expert.

    Analyze ONLY this engineering graph.

    Return EXACTLY in this format.

    Graph Title:
    <graph title>

    X Axis:
    <label>

    Y Axis:
    <label>

    Legend:
    - ...

    Graph Type:
    (Line / Bar / Scatter)

    Trend:
    Describe what happens in the graph.

    Engineering Interpretation:
    Explain the engineering meaning.

    Do NOT invent values.

    Read visible labels carefully.
    """,

            images=[encoded]

        )

        return response["response"]