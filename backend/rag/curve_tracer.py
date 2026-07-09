import cv2
import numpy as np


class CurveTracer:

    def __init__(self):
        pass

    # ----------------------------------------------------

    def trace(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(f"Cannot open {image_path}")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY
        )

        binary = cv2.bitwise_not(binary)

        kernel = np.ones((3, 3), np.uint8)

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

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE
        )

        debug = cv2.cvtColor(
            binary,
            cv2.COLOR_GRAY2BGR
        )

        curves = []

        idx = 1

        H, W = binary.shape

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area < 100:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            # Ignore axes
            if w > W * 0.90:
                continue

            if h > H * 0.90:
                continue

            # Ignore legend boxes
            if w > 120 and h < 40:
                continue

            pts = cnt.reshape(-1, 2)

            # sort left -> right
            pts = pts[np.argsort(pts[:, 0])]

            # remove duplicate x values
            sampled = []

            last_x = -999

            for p in pts:

                if abs(p[0] - last_x) < 2:
                    continue

                sampled.append(
                    (
                        int(p[0]),
                        int(p[1])
                    )
                )

                last_x = p[0]

            curves.append({

                "id": idx,

                "points": sampled

            })

            color = (

                np.random.randint(50, 255),

                np.random.randint(50, 255),

                np.random.randint(50, 255)

            )

            cv2.drawContours(

                debug,

                [cnt],

                -1,

                color,

                2

            )

            idx += 1

        cv2.imwrite(
            "curve_trace_debug.png",
            debug
        )

        return curves