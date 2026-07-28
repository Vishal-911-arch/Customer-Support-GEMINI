import numpy as np
from scipy.signal import savgol_filter


class GraphDigitizer:

    def __init__(self):

        pass

    # -------------------------------------------------------
    # Sort left → right
    # -------------------------------------------------------

    def sort_curve(self, points):

        return sorted(
            points,
            key=lambda p: p[0]
        )

    # -------------------------------------------------------
    # Remove duplicate x values
    # -------------------------------------------------------

    def remove_duplicates(self, points):

        unique = {}

        for x, y in points:

            if x not in unique:

                unique[x] = []

            unique[x].append(y)

        cleaned = []

        for x in sorted(unique.keys()):

            y = int(
                np.mean(
                    unique[x]
                )
            )

            cleaned.append(
                (x, y)
            )

        return cleaned

    # -------------------------------------------------------
    # Remove outliers
    # -------------------------------------------------------

    def remove_outliers(self, points):

        if len(points) < 10:
            return points

        ys = np.array(
            [p[1] for p in points]
        )

        median = np.median(ys)

        std = np.std(ys)

        cleaned = []

        for x, y in points:

            if abs(y - median) < 4 * std:

                cleaned.append(
                    (x, y)
                )

        return cleaned

    # -------------------------------------------------------
    # Smooth curve
    # -------------------------------------------------------

    def smooth(self, points):

        if len(points) < 15:
            return points

        xs = np.array(
            [p[0] for p in points]
        )

        ys = np.array(
            [p[1] for p in points]
        )

        try:

            ys = savgol_filter(

                ys,

                window_length=11,

                polyorder=2

            )

        except:

            pass

        result = []

        for x, y in zip(xs, ys):

            result.append(

                (
                    int(x),
                    int(y)
                )

            )

        return result

    # -------------------------------------------------------
    # Interpolate missing x values
    # -------------------------------------------------------

    def interpolate(self, points):

        if len(points) < 5:
            return points

        pts = []

        for i in range(
                len(points) - 1
        ):

            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            pts.append(
                (x1, y1)
            )

            gap = x2 - x1

            if gap > 4:

                for j in range(
                        1,
                        gap
                ):

                    t = j / gap

                    x = x1 + j

                    y = int(

                        y1 +

                        t *

                        (y2 - y1)

                    )

                    pts.append(
                        (x, y)
                    )

        pts.append(
            points[-1]
        )

        return pts

    # -------------------------------------------------------
    # Main Digitization
    # -------------------------------------------------------

    def digitize(self, curves):

        digitized = []

        for curve in curves:

            pts = curve["points"]

            pts = self.sort_curve(
                pts
            )

            pts = self.remove_duplicates(
                pts
            )

            pts = self.remove_outliers(
                pts
            )

            pts = self.interpolate(
                pts
            )

            pts = self.smooth(
                pts
            )

            digitized.append({

                "id":

                    curve["id"],

                "points":

                    pts,

                "point_count":

                    len(pts)

            })

        return {

            "curve_count":

                len(digitized),

            "curves":

                digitized

        }