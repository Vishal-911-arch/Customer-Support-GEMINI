from pathlib import Path
import json
import tempfile
import cv2
from PIL import Image
from google import genai
from dotenv import load_dotenv
import os

from config import (
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR,
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

        load_dotenv()

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.cache = VisionCache()

        self.max_images_per_page = 2

        self.min_area = 100000

    # -----------------------------------------------------

    @staticmethod
    def compress_image(image_path):

        img = Image.open(image_path)

        img.thumbnail((1024, 1024))

        temp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        img.save(temp.name)

        return temp.name

    # -----------------------------------------------------

    def analyze_crop(self, crop):

        temp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        cv2.imwrite(temp.name, crop)

        image_path = self.compress_image(temp.name)

        uploaded_file = self.client.files.upload(
            file=image_path
        )

        prompt = """
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
"""

        response = self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=[
                prompt,
                uploaded_file
            ]

        )

        return response.text

    # -----------------------------------------------------

    def analyze_page(self, document, page):

        # ============================================
        # CACHE CHECK
        # ============================================

        if self.cache.exists(document, page):

            print(f"Cache -> Page {page}")

            cached = self.cache.load(document, page)

            if isinstance(cached, dict) and "images" in cached:
                return cached["images"]

            if isinstance(cached, list):
                return cached

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

            print(f"Gemini -> Page {page}")

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