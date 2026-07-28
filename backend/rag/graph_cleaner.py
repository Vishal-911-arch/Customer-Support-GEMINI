import cv2
import numpy as np
import os


class GraphCleaner:

    def __init__(self):

        os.makedirs(
            "outputs",
            exist_ok=True
        )

    # -------------------------------------------------

    def clean(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(
                f"Cannot open {image_path}"
            )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # ==========================================
        # Adaptive Threshold
        # ==========================================

        binary = cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY_INV,

            21,

            5
        )

        cv2.imwrite(
            "outputs/binary.png",
            binary
        )

        H, W = binary.shape

        # ==========================================
        # Thin horizontal grid
        # ==========================================

        hk = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (30, 1)

        )

        horizontal = cv2.morphologyEx(

            binary,

            cv2.MORPH_OPEN,

            hk

        )

        cv2.imwrite(
            "outputs/horizontal.png",
            horizontal
        )

        # ==========================================
        # Thin vertical grid
        # ==========================================

        vk = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (1, 30)

        )

        vertical = cv2.morphologyEx(

            binary,

            cv2.MORPH_OPEN,

            vk

        )

        cv2.imwrite(
            "outputs/vertical.png",
            vertical
        )

        # ==========================================
        # Only remove very thin grid
        # ==========================================

        grid = cv2.add(
            horizontal,
            vertical
        )

        grid = cv2.erode(
            grid,
            np.ones((2, 2), np.uint8),
            iterations=1
        )

        cv2.imwrite(
            "outputs/grid.png",
            grid
        )

        curves = cv2.subtract(
            binary,
            grid
        )

        # ==========================================
        # Remove tiny OCR blobs only
        # ==========================================

        num_labels, labels, stats, _ = \
            cv2.connectedComponentsWithStats(
                curves
            )

        result = np.zeros_like(
            curves
        )

        for i in range(1, num_labels):

            area = stats[
                i,
                cv2.CC_STAT_AREA
            ]

            w = stats[
                i,
                cv2.CC_STAT_WIDTH
            ]

            h = stats[
                i,
                cv2.CC_STAT_HEIGHT
            ]

            aspect = max(w, h) / (
                min(w, h) + 1
            )

            # noise
            if area < 20:
                continue

            # tiny characters
            if area < 100 and aspect < 2:
                continue

            result[
                labels == i
            ] = 255

        # reconnect dashed curves

        kernel = cv2.getStructuringElement(

            cv2.MORPH_ELLIPSE,

            (3, 3)

        )

        result = cv2.morphologyEx(

            result,

            cv2.MORPH_CLOSE,

            kernel,

            iterations=1
        )

        cv2.imwrite(
            "outputs/clean.png",
            result
        )

        return result

    # -------------------------------------------------

    def save(self, image, path):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        cv2.imwrite(
            path,
            image
        )