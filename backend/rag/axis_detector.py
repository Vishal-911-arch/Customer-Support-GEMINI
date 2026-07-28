import cv2
import numpy as np


class AxisDetector:

    ############################################################

    def to_python_int(self, data):

        if data is None:
            return None

        return [int(v) for v in data]

    ############################################################

    def smooth(self, arr, k=9):

        kernel = np.ones(k) / k

        return np.convolve(
            arr,
            kernel,
            mode="same"
        )

    ############################################################

    def detect(self, image):

        h, w = image.shape

        binary = image < 180

        ########################################################
        # Remove title and bottom caption
        ########################################################

        binary[:int(h * 0.08), :] = False
        binary[int(h * 0.92):, :] = False

        ########################################################
        # Y AXIS
        ########################################################

        vproj = np.sum(
            binary,
            axis=0
        )

        vproj = self.smooth(vproj)

        # ignore page border
        vproj[:int(w * 0.02)] = 0

        # search only left half
        left_limit = int(w * 0.35)

        search = vproj[:left_limit]

        threshold = search.max() * 0.65

        peaks = np.where(
            search >= threshold
        )[0]

        if len(peaks):

            groups = np.split(
                peaks,
                np.where(
                    np.diff(peaks) > 5
                )[0] + 1
            )

            y_axis_x = int(
                np.mean(groups[0])
            )

        else:

            y_axis_x = int(
                np.argmax(search)
            )

        ########################################################
        # X AXIS
        ########################################################

        hproj = np.sum(
            binary,
            axis=1
        )

        hproj = self.smooth(hproj)

        start = int(h * 0.55)
        end = int(h * 0.90)

        roi = hproj[start:end]

        threshold = roi.max() * 0.75

        candidates = np.where(
            roi >= threshold
        )[0]

        if len(candidates):

            x_axis_y = int(
                candidates[-1]
                + start
            )

        else:

            x_axis_y = int(
                np.argmax(roi)
                + start
            )

        ########################################################
        # Small correction
        ########################################################

        y_axis_x += int(w * 0.005)
        x_axis_y -= int(h * 0.005)

        ########################################################
        # Origin
        ########################################################

        origin = (
            int(y_axis_x),
            int(x_axis_y)
        )

        ########################################################
        # Plot limits
        ########################################################

        top, right = self.detect_plot_limits(
            image,
            origin
        )

        ########################################################
        # Final axes
        ########################################################

        x_axis = (

            origin[0],
            origin[1],

            int(right),
            origin[1]
        )

        y_axis = (

            origin[0],
            int(top),

            origin[0],
            origin[1]
        )

        return {

            "x_axis":
                self.to_python_int(
                    x_axis
                ),

            "y_axis":
                self.to_python_int(
                    y_axis
                ),

            "origin":
                self.to_python_int(
                    origin
                )
        }

    ############################################################


    ############################################################
# Detect graph limits
############################################################
    def detect_plot_limits(
            self,
            image,
            origin
    ):

        ox, oy = origin

        binary = image < 180

        ########################################################
        # RIGHT BORDER
        ########################################################

        vproj = np.sum(
            binary,
            axis=0
        )

        vproj = self.smooth(vproj)

        search = vproj[ox:]

        threshold = search.max() * 0.25

        right = image.shape[1] - 1

        below = np.where(
            search < threshold
        )[0]

        if len(below):

            right = ox + below[0]

        ########################################################
        # TOP BORDER
        ########################################################

        hproj = np.sum(
            binary,
            axis=1
        )

        hproj = self.smooth(hproj)

        threshold = hproj.max() * 0.25

        top = 0

        for i in range(
                oy,
                0,
                -1
        ):

            if hproj[i] < threshold:

                top = i + 5
                break

        return int(top), int(right)






    def draw_axes(
            self,
            original,
            result
    ):

        img = original.copy()

        x_axis = result["x_axis"]
        y_axis = result["y_axis"]
        origin = result["origin"]

        cv2.line(

            img,

            (
                x_axis[0],
                x_axis[1]
            ),

            (
                x_axis[2],
                x_axis[3]
            ),

            (0, 255, 0),

            3
        )

        cv2.line(

            img,

            (
                y_axis[0],
                y_axis[1]
            ),

            (
                y_axis[2],
                y_axis[3]
            ),

            (255, 0, 0),

            3
        )

        cv2.circle(

            img,

            tuple(origin),

            8,

            (0, 0, 255),

            -1
        )

        return img



    