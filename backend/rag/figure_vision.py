

from pathlib import Path
import json
import base64

import cv2
import easyocr
from ollama import Client

from config import (
    OLLAMA_HOST,
    VISION_MODEL,
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR
)


class FigureVision:

    def __init__(self):

        self.client = Client(host=OLLAMA_HOST)

        self.padding = 80

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )
    # -----------------------------------------------------

    def encode(self, image):

        ok, buffer = cv2.imencode(".png", image)

        if not ok:
            return None

        return base64.b64encode(buffer).decode()

    # -----------------------------------------------------

    def crop_complete_figure(self, document, page):

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

        print("\nIMAGE :", image_path)
        print("JSON  :", json_path)

        print("Image exists :", image_path.exists())
        print("JSON exists  :", json_path.exists())

        if not image_path.exists():
            return None

        if not json_path.exists():
            return None

        image = cv2.imread(str(image_path))

        print("Image shape :", image.shape)

        with open(json_path, "r") as f:
            detections = json.load(f)

        print("\nDetections")

        for d in detections:
            print(d)

        if len(detections) == 0:
            return image

        xmins = []
        ymins = []
        xmaxs = []
        ymaxs = []

        for det in detections:

            x, y, w, h = det["bbox"]

            xmins.append(x)
            ymins.append(y)
            xmaxs.append(x + w)
            ymaxs.append(y + h)

        xmin = max(min(xmins) - self.padding, 0)
        ymin = max(min(ymins) - self.padding, 0)

        xmax = min(max(xmaxs) + self.padding, image.shape[1])
        ymax = min(max(ymaxs) + self.padding, image.shape[0])

        print("\nCrop Coordinates")
        print(xmin, ymin, xmax, ymax)

        crop = image[ymin:ymax, xmin:xmax]

        print("Crop shape :", crop.shape)

        saved = cv2.imwrite(
            str(Path.cwd() / "debug_crop.png"),
            crop
        )

        print("Saved :", saved)
        print("Output :", Path.cwd() / "debug_crop.png")

        return crop
    
    # -----------------------------------------------------
    def crop_caption(self, figure_crop):

        """
        Extract the bottom portion of the figure where
        figure captions are usually located.
        """

        h, w = figure_crop.shape[:2]

        # Bottom 20%
        caption_crop = figure_crop[int(h * 0.80):, :]

        cv2.imwrite(
            str(Path.cwd() / "debug_caption.png"),
            caption_crop
        )

        print("\nCaption Crop")
        print("Shape :", caption_crop.shape)
        print("Saved :", Path.cwd() / "debug_caption.png")

        return caption_crop
    def analyze(self, document, page):

        print("\nRunning Figure Vision...")

        crop = self.crop_complete_figure(
            document,
            page
        )
        

        if crop is None:
            return ""
        
        caption = self.read_caption(crop)
        # Resize large images
        h, w = crop.shape[:2]

        max_width = 1024

        if w > max_width:
            scale = max_width / w
            crop = cv2.resize(
                crop,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA
            )
        encoded = self.encode(crop)

        response = self.client.generate(

            model=VISION_MODEL,

            prompt="""
You are an aerospace engineering expert.

This image is a SINGLE engineering figure extracted from an aircraft textbook.

Your task is to READ the figure, not simply describe it.

Return EXACTLY in this format.

Figure Title:
<one short title>

Summary:
<2-4 sentences explaining what the figure teaches>

Visible Labels:
- label
- label
- label

Engineering Concepts:
- concept
- concept

Relationships:
Explain how the labelled components relate to each other.

Do NOT describe the page.

Do NOT mention image quality.

Do NOT say "I cannot read".

Do NOT invent labels.

If a label is partially visible, infer only obvious words from nearby labels.

Focus on engineering meaning rather than visual appearance.
""",

            images=[encoded]

        )

        return response["response"]