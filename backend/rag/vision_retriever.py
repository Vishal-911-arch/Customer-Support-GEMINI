from pathlib import Path
import json
import base64

import cv2
from ollama import Client

from config import (
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR,
    OLLAMA_HOST,
    VISION_MODEL,
)

from rag.vision_cache import VisionCache


class VisionRetriever:
    """
    Analyze only retrieved pages.

    Features:
    - Vision Cache
    - Avoid duplicate page analysis
    - Analyze only large detected regions
    - Analyze at most N images/page
    """

    def __init__(self):

        self.client = Client(host=OLLAMA_HOST)

        self.cache = VisionCache()

        self.max_images_per_page = 2

        self.min_area = 100000

    # -----------------------------------------------------

    def encode_image(self, image):

        ok, buffer = cv2.imencode(".png", image)

        if not ok:
            return None

        return base64.b64encode(buffer).decode("utf-8")

    # -----------------------------------------------------

    def analyze_crop(self, crop):

        encoded = self.encode_image(crop)

        if encoded is None:
            return None

        response = self.client.generate(

            model=VISION_MODEL,

            prompt="""
You are an aircraft technical manual assistant.

Describe ONLY what is visible.

Possible image types:

- Aircraft
- Aircraft component
- Cockpit
- Instrument
- Engineering drawing
- Technical illustration
- Labelled diagram
- Maintenance figure
- Flowchart
- Graph
- Table

Rules:

1. Never guess.
2. Read visible labels.
3. Mention arrows.
4. Mention important parts.
5. Keep description under 120 words.
""",

            images=[encoded]

        )

        return response["response"]

    # -----------------------------------------------------

    def analyze_page(self, document, page):

        # ============================================
        # CACHE CHECK
        # ======================================A======

        if self.cache.exists(document, page):

            print(f"Cache -> Page {page}")

            cached = self.cache.load(document, page)

                # New cache format
            if isinstance(cached, dict) and "images" in cached:
                    return cached["images"]

                # Old cache format (list)
            if isinstance(cached, list):
                    return cached

                # Unknown format
            return []

        # ============================================
        # NORMAL PROCESSING
        # ============================================

        classifier_json = (

            IMAGE_CLASSIFIER_OUTPUT_DIR
            / document
            / f"page_{page}.json"

        )

        rendered_page = (

            RENDERED_PAGES_DIR
            / document
            / f"page_{page}.png"

        )

        if not classifier_json.exists():
            return []

        if not rendered_page.exists():
            return []

        image = cv2.imread(str(rendered_page))

        if image is None:
            return []

        with open(classifier_json, "r") as f:

            detections = json.load(f)

        descriptions = []

        count = 0

        for detection in detections:

            if count >= self.max_images_per_page:
                break

            x, y, w, h = detection["bbox"]

            if w * h < self.min_area:
                continue

            crop = image[y:y+h, x:x+w]

            if crop.size == 0:
                continue

            print(f"LLaVA -> Page {page}")

            description = self.analyze_crop(crop)

            descriptions.append({

                "type": detection["type"],

                "description": description

            })

            count += 1

        # ============================================
        # SAVE CACHE
        # ============================================

        cache_data = {

            "document": document,

            "page": page,

            "images": descriptions

        }

        self.cache.save(

            document,

            page,

            cache_data

        )

        return descriptions

    # -----------------------------------------------------

    def analyze_results(self, retrieval_results):

        vision_context = []

        visited = set()

        if not retrieval_results["metadatas"]:

            return vision_context

        for meta in retrieval_results["metadatas"][0]:

            document = meta.get("document")

            page = meta.get("page")

            if document is None:

                continue

            try:

                page = int(page)

            except:

                continue

            key = (document, page)

            if key in visited:
                continue

            visited.add(key)

            images = self.analyze_page(

                document,

                page

            )

            if images:

                vision_context.append({

                    "document": document,

                    "page": page,

                    "images": images

                })

        return vision_context