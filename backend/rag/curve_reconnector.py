import numpy as np


class CurveReconnector:

    ##################################################

    def endpoint(self, curve):

        pts = curve["points"]

        return pts[0], pts[-1]

    ##################################################

    def distance(
            self,
            p1,
            p2
    ):

        return np.sqrt(

            (p1[0]-p2[0])**2
            +
            (p1[1]-p2[1])**2
        )

    ##################################################

    def merge(
            self,
            curves,
            threshold=30
    ):

        changed = True

        while changed:

            changed = False

            for i in range(len(curves)):

                if changed:
                    break

                for j in range(i+1,
                               len(curves)):

                    a1, a2 = self.endpoint(
                        curves[i]
                    )

                    b1, b2 = self.endpoint(
                        curves[j]
                    )

                    d = min(

                        self.distance(a1, b1),

                        self.distance(a1, b2),

                        self.distance(a2, b1),

                        self.distance(a2, b2)
                    )

                    if d < threshold:

                        curves[i]["points"] += \
                            curves[j]["points"]

                        curves.pop(j)

                        changed = True
                        break

        for i, c in enumerate(curves):

            c["id"] = i + 1

        return curves