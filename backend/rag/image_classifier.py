from pathlib import Path
import json
import cv2
import numpy as np

from config import (
    RENDERED_PAGES_DIR,
    ARTIFACTS_DIR
)

IMAGE_CLASSIFIER_OUTPUT = ARTIFACTS_DIR / "image_classifier"
IMAGE_CLASSIFIER_OUTPUT.mkdir(parents=True, exist_ok=True)


class ImageClassifier:

    def __init__(self):

        self.min_area = 10000

    # ---------------------------------------------------------

    def classify_region(self, roi):

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 50, 150)

        edge_ratio = np.count_nonzero(edges) / edges.size

        h, w = gray.shape

        aspect = w / h

        # Table
        if edge_ratio > 0.18 and aspect > 1.2:
            return "table"

        # Graph
        if edge_ratio > 0.10:
            return "graph"

        # Diagram
        if edge_ratio > 0.04:
            return "diagram"

        return "photo"

    # ---------------------------------------------------------

    def process_page(self, image_path):

        image_path = Path(image_path)

        image = cv2.imread(str(image_path))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(
            gray,
            240,
            255,
            cv2.THRESH_BINARY_INV
        )[1]

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        output = []

        debug = image.copy()

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            area = w * h

            if area < self.min_area:
                continue

            roi = image[y:y+h, x:x+w]

            region_type = self.classify_region(roi)

            output.append({

                "bbox": [x, y, w, h],

                "type": region_type

            })

            cv2.rectangle(
                debug,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                3
            )

            cv2.putText(
                debug,
                region_type,
                (x,y-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2
            )

        return output, debug

    # ---------------------------------------------------------

    def process_document(self, document_name):

        pages = sorted(

            (RENDERED_PAGES_DIR / document_name).glob("*.png")

        )

        output_folder = IMAGE_CLASSIFIER_OUTPUT / document_name

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        print("="*60)
        print("IMAGE CLASSIFICATION")
        print("="*60)

        for page in pages:

            regions, debug = self.process_page(page)

            json_path = output_folder / f"{page.stem}.json"

            with open(json_path, "w") as f:

                json.dump(

                    regions,

                    f,

                    indent=4

                )

            debug_path = output_folder / f"{page.stem}.png"

            cv2.imwrite(

                str(debug_path),

                debug

            )

            print(f"✓ {page.name}   Regions : {len(regions)}")

        print("\nDone.")