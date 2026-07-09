from pathlib import Path
import json

import cv2
import pytesseract

from config import (
    TESSERACT_PATH,
    OCR_OUTPUT_DIR
)


class OCRProcessor:
    """
    OCR Processor for rendered PDF pages.

    Input:
        artifacts/rendered_pages/<document>/*.png

    Output:
        artifacts/ocr_output/<document>/*.json
    """

    def __init__(self):

        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    # ----------------------------------------------------

    def preprocess(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise FileNotFoundError(image_path)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return gray

    # ----------------------------------------------------

    def process_image(self, image_path):

        image = self.preprocess(image_path)

        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT,
            config="--oem 3 --psm 6"
        )

        words = []

        full_text = []

        total = len(data["text"])

        for i in range(total):

            text = data["text"][i].strip()

            if text == "":
                continue

            try:
                confidence = float(data["conf"][i])
            except:
                confidence = -1

            if confidence < 0:
                continue

            words.append({

                "text": text,

                "confidence": confidence,

                "bbox": {

                    "left": data["left"][i],

                    "top": data["top"][i],

                    "width": data["width"][i],

                    "height": data["height"][i]

                }

            })

            full_text.append(text)

        return {

            "document": image_path.parent.name,

            "page": image_path.stem,

            "image_path": str(image_path),

            "text": " ".join(full_text),

            "words": words

        }

    # ----------------------------------------------------
        # ----------------------------------------------------

    def process_crop(self, image):

        """
        OCR directly on an OpenCV image (crop).

        Returns plain extracted text.
        """

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        data = pytesseract.image_to_data(
            gray,
            output_type=pytesseract.Output.DICT,
            config="--oem 3 --psm 6"
        )

        words = []

        total = len(data["text"])

        for i in range(total):

            text = data["text"][i].strip()

            if text == "":
                continue

            words.append(text)

        return " ".join(words)

    def process_directory(self, image_directory):

        
        image_directory = Path(image_directory)

        document_name = image_directory.name

        output_directory = (
            OCR_OUTPUT_DIR /
            document_name
        )
        print("Image Directory :", image_directory)
        print("Output Directory:", output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        images = sorted(
            image_directory.glob("*.png")
        )

        print(f"\nFound {len(images)} PNG images\n")

        for img in images[:5]:
            print(img)
        print("\n" + "=" * 60)
        print(f"OCR : {document_name}")
        print("=" * 60)

        results = []

        for image in images:

            result = self.process_image(image)

            json_file = (
                output_directory /
                f"{image.stem}.json"
            )

            with open(
                json_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    result,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print(f"✓ {image.name}")

            results.append(result)

        print("\nOCR Completed")
        print(f"Pages Processed : {len(results)}")

        return results