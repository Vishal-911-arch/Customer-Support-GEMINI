import numpy as np


class CoordinateMapper:

    def __init__(
            self,
            generated_labels
    ):

        self.labels = generated_labels

        self.x_pixels = []
        self.x_values = []

        self.y_pixels = []
        self.y_values = []

        #################################################
        # X
        #################################################

        for item in generated_labels["x_labels"]:

            self.x_pixels.append(
                float(item["pixel"])
            )

            self.x_values.append(
                float(item["value"])
            )

        #################################################
        # Y
        #################################################

        for item in generated_labels["y_labels"]:

            self.y_pixels.append(
                float(item["pixel"])
            )

            self.y_values.append(
                float(item["value"])
            )

        self.x_pixels = np.array(
            self.x_pixels,
            dtype=np.float32
        )

        self.x_values = np.array(
            self.x_values,
            dtype=np.float32
        )

        self.y_pixels = np.array(
            self.y_pixels,
            dtype=np.float32
        )

        self.y_values = np.array(
            self.y_values,
            dtype=np.float32
        )

    #########################################################
    # Pixel X → Graph X
    #########################################################

    def pixel_to_graph_x(
            self,
            pixel_x
    ):

        return float(

            np.interp(

                pixel_x,

                self.x_pixels,

                self.x_values
            )
        )

    #########################################################
    # Pixel Y → Graph Y
    #########################################################

    def pixel_to_graph_y(
            self,
            pixel_y
    ):

        #################################################
        # image y increases downward
        #################################################

        return float(

            np.interp(

                pixel_y,

                self.y_pixels[::-1],

                self.y_values[::-1]
            )
        )

    #########################################################
    # Convert point
    #########################################################

    def pixel_to_graph(
            self,
            x,
            y
    ):

        gx = self.pixel_to_graph_x(
            x
        )

        gy = self.pixel_to_graph_y(
            y
        )

        return {

            "x": round(gx, 5),
            "y": round(gy, 5)
        }

    #########################################################
    # Batch conversion
    #########################################################

    def convert_points(
            self,
            points
    ):

        result = []

        for p in points:

            g = self.pixel_to_graph(

                p[0],
                p[1]
            )

            result.append(g)

        return result