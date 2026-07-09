from pathlib import Path
import json
import re

import cv2
import easyocr

from config import (
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR,
)


class FigureDetector:
    """
    Detects figure captions from rendered pages.

    Output:
        figure number
        title
        page
        bbox
    """

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

        # extend crop upward to include caption
        self.caption_padding = 300

    # -------------------------------------------------------

    def detect(self, document):

        image_dir = RENDERED_PAGES_DIR / document
        json_dir = IMAGE_CLASSIFIER_OUTPUT_DIR / document

        figures = []

        pages = sorted(image_dir.glob("page_*.png"))

        for image_path in pages:

            page = int(image_path.stem.split("_")[1])

            json_path = json_dir / f"page_{page}.json"

            if not json_path.exists():
                continue

            image = cv2.imread(str(image_path))

            with open(json_path) as f:
                detections = json.load(f)

            for det in detections:

                if det["type"] not in [
                    "diagram",
                    "graph",
                    "table",
                    "photo"
                ]:
                    continue

                x, y, w, h = det["bbox"]

                ymin = max(0, y - self.caption_padding)

                crop = image[
                    ymin:y+h,
                    x:x+w
                ]

                text = self.read_crop(crop)

                print("\n==========================")
                print(f"Page : {page}")
                print("OCR Crop:")
                print(text)

                info = self.extract_caption(text)

                if info is None:
                    continue

                info["page"] = page
                info["bbox"] = det["bbox"]
                info["document"] = document

                figures.append(info)

        return figures

    # -------------------------------------------------------

    def read_crop(self, crop):

        result = self.reader.readtext(
            crop,
            detail=0,
            paragraph=True
        )

        return "\n".join(result)

    # -------------------------------------------------------

    def extract_caption(self, text):

        m = re.search(

            r"Figure\s*(\d+\.\d+)\.?\s*(.*)",

            text,

            re.IGNORECASE

        )

        if not m:
            return None

        return {

            "figure": m.group(1),

            "title": m.group(2).strip()

        }