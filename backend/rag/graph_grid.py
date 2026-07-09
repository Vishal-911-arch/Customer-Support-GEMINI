import cv2
import numpy as np


class GraphGrid:

    def __init__(self):
        pass

    # --------------------------------------------------

    def remove_grid(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Image not found")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # Binary

        binary = cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY_INV,

            25,

            10

        )

        # ----------------------------
        # Horizontal grid
        # ----------------------------

        horizontal_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (60,1)

        )

        horizontal = cv2.morphologyEx(

            binary,

            cv2.MORPH_OPEN,

            horizontal_kernel,

            iterations=1

        )

        # ----------------------------
        # Vertical grid
        # ----------------------------

        vertical_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (1,60)

        )

        vertical = cv2.morphologyEx(

            binary,

            cv2.MORPH_OPEN,

            vertical_kernel,

            iterations=1

        )

        # ----------------------------
        # Complete grid
        # ----------------------------

        grid = cv2.bitwise_or(

            horizontal,

            vertical

        )

        # ----------------------------
        # Remove grid
        # ----------------------------

        curve = cv2.subtract(

            binary,

            grid

        )

        # ----------------------------
        # Clean tiny dots
        # ----------------------------

        kernel = np.ones((2,2),np.uint8)

        curve = cv2.morphologyEx(

            curve,

            cv2.MORPH_OPEN,

            kernel

        )

        return {

            "binary":binary,

            "horizontal":horizontal,

            "vertical":vertical,

            "grid":grid,

            "curve":curve

        }

    # --------------------------------------------------

    def save(self, img, path):

        cv2.imwrite(path,img)