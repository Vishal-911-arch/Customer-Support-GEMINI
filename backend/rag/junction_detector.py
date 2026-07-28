import cv2
import numpy as np


class JunctionDetector:

    def detect(self, skeleton):

        H, W = skeleton.shape

        junctions = []

        debug = cv2.cvtColor(
            skeleton,
            cv2.COLOR_GRAY2BGR
        )

        for y in range(1, H - 1):

            for x in range(1, W - 1):

                if skeleton[y, x] == 0:
                    continue

                roi = skeleton[
                    y - 1:y + 2,
                    x - 1:x + 2
                ]

                neighbors = np.count_nonzero(
                    roi
                ) - 1

                if neighbors >= 3:

                    junctions.append(
                        (x, y)
                    )

                    cv2.circle(
                        debug,
                        (x, y),
                        2,
                        (0, 0, 255),
                        -1
                    )

        cv2.imwrite(
            "outputs/junctions.png",
            debug
        )

        return junctions