from pathlib import Path
import json
import base64

import cv2

from ollama import Client

from config import (
    IMAGE_CLASSIFIER_OUTPUT_DIR,
    RENDERED_PAGES_DIR,
    VISION_OUTPUT_DIR,
    OLLAMA_HOST,
    VISION_MODEL
)


class VisionProcessor:

    def __init__(self):

        self.client = Client(host=OLLAMA_HOST)

        # Ignore tiny detections
        self.min_area = 60000

    # ---------------------------------------------------------

    def encode_image(self, image):

        success, buffer = cv2.imencode(".png", image)

        if not success:
            raise RuntimeError("Unable to encode image.")

        return base64.b64encode(buffer).decode("utf-8")

    # ---------------------------------------------------------

    def describe_image(self, crop):

        encoded = self.encode_image(crop)

        response = self.client.generate(

            model=VISION_MODEL,

            prompt="""
You are an aviation technical assistant.

Describe this image.

If it is:

- aircraft
- aircraft component
- maintenance figure
- engineering drawing
- graph
- chart
- labelled diagram

explain it carefully.

Mention visible labels.

Do not invent anything.
""",

            images=[encoded]

        )

        return response["response"]

    # ---------------------------------------------------------

    def process_document(self, document_name):

        classifier_dir = (
            IMAGE_CLASSIFIER_OUTPUT_DIR /
            document_name
        )

        rendered_dir = (
            RENDERED_PAGES_DIR /
            document_name
        )

        output_dir = (
            VISION_OUTPUT_DIR /
            document_name
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        json_files = sorted(
            classifier_dir.glob("*.json")
        )

        print("=" * 60)
        print("VISION PROCESSING")
        print("=" * 60)

        for json_file in json_files:

            rendered_page = (
                rendered_dir /
                f"{json_file.stem}.png"
            )

            page = cv2.imread(str(rendered_page))

            if page is None:

                print(f"Cannot open {rendered_page}")

                continue

            with open(json_file, "r") as f:

                detections = json.load(f)

            page_results = []

            for idx, detection in enumerate(detections):

                x, y, w, h = detection["bbox"]

                area = w * h

                if area < self.min_area:
                    continue

                crop = page[
                    y:y+h,
                    x:x+w
                ]

                if crop.size == 0:
                    continue

                print(
                    f"{json_file.stem} -> Image {idx+1}"
                )

                description = self.describe_image(crop)

                page_results.append({

                    "type": detection["type"],

                    "bbox": detection["bbox"],

                    "description": description

                })

            output = {

                "document": document_name,

                "page": json_file.stem,

                "vision": page_results

            }

            with open(

                output_dir / json_file.name,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    output,

                    f,

                    indent=4,

                    ensure_ascii=False

                )

        print("\nVision Processing Complete.")