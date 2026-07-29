from pathlib import Path
import json
import tempfile
import cv2
import easyocr
from PIL import Image
from google import genai
from dotenv import load_dotenv
import os

from config import (
    RENDERED_PAGES_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR
)


class FigureVision:

    def __init__(self):

        load_dotenv()

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.padding = 80

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

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

        if image is None:
            return None

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

        cv2.imwrite(
            str(Path.cwd() / "debug_crop.png"),
            crop
        )

        print("Output :", Path.cwd() / "debug_crop.png")

        return crop

    # -----------------------------------------------------

    def crop_caption(self, figure_crop):

        """
        Extract the bottom portion of the figure where
        figure captions are usually located.
        """

        h, w = figure_crop.shape[:2]

        caption_crop = figure_crop[int(h * 0.80):, :]

        cv2.imwrite(
            str(Path.cwd() / "debug_caption.png"),
            caption_crop
        )

        print("\nCaption Crop")
        print("Shape :", caption_crop.shape)
        print("Saved :", Path.cwd() / "debug_caption.png")

        return caption_crop
        # -----------------------------------------------------

    def analyze(self, document, page):

        print("\nRunning Figure Vision...")

        crop = self.crop_complete_figure(
            document,
            page
        )

        if crop is None:
            return ""

        # Optional OCR caption (keep if your project uses it)
        try:
            caption = self.read_caption(crop)
            print("Caption :", caption)
        except Exception:
            caption = ""

        # Resize large image
        h, w = crop.shape[:2]

        if w > 1024:

            scale = 1024 / w

            crop = cv2.resize(

                crop,

                (
                    int(w * scale),
                    int(h * scale)
                ),

                interpolation=cv2.INTER_AREA

            )

        # ---------------------------------------------
        # Save temporary image
        # ---------------------------------------------

        temp = tempfile.NamedTemporaryFile(

            suffix=".png",

            delete=False

        )

        cv2.imwrite(temp.name, crop)

        image_path = self.compress_image(temp.name)

        # ---------------------------------------------
        # Upload to Gemini
        # ---------------------------------------------

        uploaded_file = self.client.files.upload(

            file=image_path

        )

        prompt = f"""
You are an aerospace engineering expert.

This image is a SINGLE engineering figure extracted from an aircraft textbook.

Your task is to READ the figure, not simply describe it.

Caption detected (may help):

{caption}

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
"""

        response = self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=[

                prompt,

                uploaded_file

            ]

        )

        return response.text