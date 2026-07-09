import cv2
import numpy as np


class GraphCleaner:

    def __init__(self):
        pass

    # ----------------------------------------------------
    # Remove text, arrows and thin grid
    # ----------------------------------------------------

    def clean(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(f"Cannot load {image_path}")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY_INV
        )

        kernel = np.ones((2,2), np.uint8)

        binary = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            kernel
        )

        binary = cv2.dilate(
            binary,
            kernel,
            iterations=1
        )

        return binary

    # ----------------------------------------------------

    def save(self, image, path):

        cv2.imwrite(path, image)