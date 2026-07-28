import cv2
import numpy as np


class CurveTracer:

    def __init__(self):
        pass

    # ----------------------------------------------------

    def trace(self, image_path):

        image = cv2.imread(image_path)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            200,
            255,
            cv2.THRESH_BINARY_INV
        )

        H, W = binary.shape

        # ------------------------------------
        # Remove horizontal grid
        # ------------------------------------

        hk = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (40,1)
        )

        horizontal = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            hk
        )

        # ------------------------------------
        # Remove vertical grid
        # ------------------------------------

        vk = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (1,40)
        )

        vertical = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            vk
        )

        grid = cv2.add(
            horizontal,
            vertical
        )

        curves_img = cv2.subtract(
            binary,
            grid
        )

        contours, _ = cv2.findContours(

            curves_img,

            cv2.RETR_LIST,

            cv2.CHAIN_APPROX_NONE

        )

        curves = []

        debug = cv2.cvtColor(
            curves_img,
            cv2.COLOR_GRAY2BGR
        )

        idx = 1

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area < 400:
                continue

            x,y,w,h = cv2.boundingRect(cnt)

            aspect = max(w,h) / (
                min(w,h)+1
            )

            # reject text blobs

            if aspect < 2:
                continue

            if w < 30:
                continue

            pts = cnt.reshape(-1,2)

            pts = pts[
                np.argsort(
                    pts[:,0]
                )
            ]

            sampled = []

            last_x = -999

            for p in pts:

                if abs(
                    p[0]-last_x
                ) < 2:

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

                np.random.randint(100,255),

                np.random.randint(100,255),

                np.random.randint(100,255)

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