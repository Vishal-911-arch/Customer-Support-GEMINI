import cv2
import numpy as np


class CurveExtractor:

    def __init__(self):

        self.visited = None

    ##################################################

    def get_neighbors(
            self,
            img,
            x,
            y
    ):

        pts = []

        H, W = img.shape

        for dy in [-1, 0, 1]:

            for dx in [-1, 0, 1]:

                if dx == 0 and dy == 0:
                    continue

                nx = x + dx
                ny = y + dy

                if (
                        0 <= nx < W
                        and
                        0 <= ny < H
                ):

                    if img[ny, nx] > 0:

                        pts.append(
                            (nx, ny)
                        )

        return pts

    ##################################################

    def find_endpoints(
            self,
            skeleton
    ):

        endpoints = []

        H, W = skeleton.shape

        for y in range(1, H - 1):

            for x in range(1, W - 1):

                if skeleton[y, x] == 0:
                    continue

                n = self.get_neighbors(
                    skeleton,
                    x,
                    y
                )

                if len(n) == 1:

                    endpoints.append(
                        (x, y)
                    )

        return endpoints

    ##################################################

    def dfs(
            self,
            skeleton,
            start
    ):

        stack = [start]

        curve = []

        while stack:

            x, y = stack.pop()

            if self.visited[y, x]:
                continue

            self.visited[y, x] = True

            curve.append(
                (x, y)
            )

            neigh = self.get_neighbors(

                skeleton,
                x,
                y
            )

            for p in neigh:

                px, py = p

                if not self.visited[
                    py,
                    px
                ]:

                    stack.append(
                        p
                    )

        return curve

    ##################################################

    def extract(
            self,
            skeleton,
            junctions=None
    ):

        H, W = skeleton.shape

        self.visited = np.zeros(
            (H, W),
            dtype=bool
        )

        endpoints = self.find_endpoints(
            skeleton
        )

        curves = []

        idx = 1

        debug = cv2.cvtColor(
            skeleton,
            cv2.COLOR_GRAY2BGR
        )

        for ep in endpoints:

            x, y = ep

            if self.visited[y, x]:
                continue

            curve = self.dfs(

                skeleton,
                ep
            )

            if len(curve) < 40:
                continue

            curves.append({

                "id": idx,
                "points": curve
            })

            color = (

                np.random.randint(50, 255),
                np.random.randint(50, 255),
                np.random.randint(50, 255)
            )

            for px, py in curve:

                debug[
                    py,
                    px
                ] = color

            idx += 1

        cv2.imwrite(

            "outputs/extracted_curves.png",

            debug
        )

        return curves