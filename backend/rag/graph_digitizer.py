import numpy as np


class GraphDigitizer:

    def __init__(self):
        pass

    # -------------------------------------------------------
    # Sort points from left → right
    # -------------------------------------------------------

    def sort_curve(self, points):

        points = sorted(points, key=lambda p: p[0])

        return points

    # -------------------------------------------------------
    # Remove duplicate x values
    # -------------------------------------------------------

    def remove_duplicates(self, points):

        unique = {}

        for x, y in points:

            if x not in unique:
                unique[x] = y

        cleaned = []

        for x in sorted(unique.keys()):
            cleaned.append((x, unique[x]))

        return cleaned

    # -------------------------------------------------------
    # Smooth curve
    # -------------------------------------------------------

    def smooth(self, points):

        if len(points) < 5:
            return points

        smooth = []

        for i in range(len(points)):

            left = max(0, i - 2)
            right = min(len(points), i + 3)

            xs = [p[0] for p in points[left:right]]
            ys = [p[1] for p in points[left:right]]

            smooth.append(

                (
                    int(np.mean(xs)),
                    int(np.mean(ys))
                )

            )

        return smooth

    # -------------------------------------------------------
    # Digitize
    # -------------------------------------------------------

    def digitize(self, curves):

        digitized = []

        for curve in curves:

            pts = curve["points"]

            pts = self.sort_curve(pts)

            pts = self.remove_duplicates(pts)

            pts = self.smooth(pts)

            digitized.append({

                "id": curve["id"],

                "points": pts,

                "point_count": len(pts)

            })

        return {

            "curve_count": len(digitized),

            "curves": digitized

        }