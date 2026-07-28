import cv2
import numpy as np


class TickDetector:

    ########################################################
    # Remove nearby duplicate ticks
    ########################################################
    def remove_nearby(
            self,
            points,
            threshold=28
    ):

        if len(points) == 0:
            return []

        points = sorted(points)

        result = [points[0]]

        for p in points[1:]:

            if abs(
                    p - result[-1]
            ) > threshold:

                result.append(p)

        return result

    ########################################################
    # Main Detection
    ########################################################
    def detect(
            self,
            image,
            original=None,
            axes=None
    ):

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

        ox, oy = axes["origin"]

        ####################################################
        # X AXIS TICKS
        ####################################################

        x_roi = binary[
            max(0, oy - 18):
            min(binary.shape[0], oy + 18),

            ox:
            axes["x_axis"][2]
        ]

        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (1, 14)
        )

        x_img = cv2.morphologyEx(
            x_roi,
            cv2.MORPH_OPEN,
            vertical_kernel
        )

        contours, _ = cv2.findContours(
            x_img,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        x_ticks = []

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            ################################################
            # ignore tiny grid lines
            ################################################

            if h < 10:
                continue

            if h > 40:
                continue

            tick_x = (
                    ox
                    + x
                    + w // 2
            )

            x_ticks.append(
                int(tick_x)
            )

        ####################################################
        # Y AXIS TICKS
        ####################################################

        y_roi = binary[
            axes["y_axis"][1]:
            oy,

            max(0, ox - 18):
            min(binary.shape[1], ox + 18)
        ]

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (14, 1)
        )

        y_img = cv2.morphologyEx(
            y_roi,
            cv2.MORPH_OPEN,
            horizontal_kernel
        )

        contours, _ = cv2.findContours(
            y_img,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        y_ticks = []

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            ################################################
            # remove grid intersections
            ################################################

            if w < 10:
                continue

            if w > 45:
                continue

            tick_y = (
                    axes["y_axis"][1]
                    + y
                    + h // 2
            )

            y_ticks.append(
                int(tick_y)
            )

        ####################################################
        # remove duplicates
        ####################################################

        x_ticks = sorted(
            list(set(x_ticks))
        )

        y_ticks = sorted(
            list(set(y_ticks))
        )

        x_ticks = self.remove_nearby(
            x_ticks,
            threshold=35
        )

        y_ticks = self.remove_nearby(
            y_ticks,
            threshold=32
        )

        ####################################################
        # Remove ticks very close to origin
        ####################################################

        x_ticks = [

            x for x in x_ticks

            if abs(x - ox) > 10
        ]

        y_ticks = [

            y for y in y_ticks

            if abs(y - oy) > 10
        ]

        ####################################################
        # DEBUG IMAGE
        ####################################################

        if (
                original is not None
                and
                axes is not None
        ):

            debug = original.copy()

            for x in x_ticks:

                cv2.line(
                    debug,
                    (x, oy - 12),
                    (x, oy + 12),
                    (0, 0, 255),
                    2
                )

            for y in y_ticks:

                cv2.line(
                    debug,
                    (ox - 12, y),
                    (ox + 12, y),
                    (255, 0, 0),
                    2
                )

            cv2.imwrite(
                "outputs/ticks_debug.png",
                debug
            )

        return {

            "x_ticks":
                x_ticks,

            "y_ticks":
                y_ticks
        }