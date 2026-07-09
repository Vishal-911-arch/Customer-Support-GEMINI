import cv2
from pathlib import Path


class GraphCropper:

    def __init__(self):

        self.output_dir = Path("artifacts/graph_crop")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # -----------------------------------------------------

    def crop(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(f"Cannot open {image_path}")

        h, w = image.shape[:2]

        # -----------------------------
        # Adjustable margins
        # -----------------------------

        top_margin = int(h * 0.12)

        bottom_margin = int(h * 0.88)

        left_margin = int(w * 0.15)

        right_margin = int(w * 0.78)

        # -----------------------------
        # Crop regions
        # -----------------------------

        title = image[
            0:top_margin,
            :
        ]

        y_axis = image[
            top_margin:bottom_margin,
            0:left_margin
        ]

        x_axis = image[
            bottom_margin:h,
            left_margin:right_margin
        ]

        legend = image[
            top_margin:bottom_margin,
            right_margin:w
        ]

        plot = image[
            top_margin:bottom_margin,
            left_margin:right_margin
        ]

        # -----------------------------
        # Save
        # -----------------------------

        regions = {

            "title": title,

            "y_axis": y_axis,

            "x_axis": x_axis,

            "legend": legend,

            "plot": plot

        }

        paths = {}

        for name, img in regions.items():

            path = self.output_dir / f"{name}.png"

            cv2.imwrite(str(path), img)

            paths[name] = str(path)

        return paths