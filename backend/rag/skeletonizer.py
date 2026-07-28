import cv2
import numpy as np
import os

from skimage.morphology import skeletonize


class Skeletonizer:

    def __init__(self):

        os.makedirs(
            "outputs",
            exist_ok=True
        )

    # --------------------------------------------------
    # Core skeletonization
    # --------------------------------------------------

    def run(self, image):

        if len(image.shape) == 3:

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

        else:

            gray = image.copy()

        _, binary = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY_INV
        )

        cv2.imwrite(
            "outputs/skeleton_binary.png",
            binary
        )

        # ---------------------------------------
        # Remove tiny noise
        # ---------------------------------------

        num_labels, labels, stats, _ = \
            cv2.connectedComponentsWithStats(
                binary,
                connectivity=8
            )

        clean = np.zeros_like(binary)

        for i in range(1, num_labels):

            area = stats[
                i,
                cv2.CC_STAT_AREA
            ]

            if area < 20:
                continue

            clean[
                labels == i
            ] = 255

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (3, 3)
        )

        clean = cv2.morphologyEx(
            clean,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=1
        )

        cv2.imwrite(
            "outputs/skeleton_clean.png",
            clean
        )

        skeleton = skeletonize(
            clean > 0
        )

        skeleton = (
            skeleton.astype(np.uint8)
            * 255
        )

        cv2.imwrite(
            "outputs/skeleton.png",
            skeleton
        )

        return skeleton

    # --------------------------------------------------
    # Path wrapper
    # --------------------------------------------------

    def process(self, image_path):

        image = cv2.imread(
            image_path
        )

        if image is None:

            raise Exception(
                f"Cannot load {image_path}"
            )

        return self.run(image)