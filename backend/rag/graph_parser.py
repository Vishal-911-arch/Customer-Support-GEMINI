import re


class GraphParser:

    def __init__(self):
        pass

    # --------------------------------------------------

    def parse(self, ocr, digitized):

        title = self.clean_title(
            ocr.get("title", "")
        )

        x_axis = self.clean_axis(
            ocr.get("x_axis", "")
        )

        y_axis = self.clean_axis(
            ocr.get("y_axis", "")
        )

        legend = self.clean_legend(
            ocr.get("legend", [])
        )

        ticks = ocr.get(
            "ticks",
            {}
        )

        graph_type = self.detect_graph_type(
            digitized
        )

        domain = self.detect_domain(
            title,
            x_axis,
            y_axis,
            legend
        )

        return {

            "title": title,

            "graph_type": graph_type,

            "engineering_domain": domain,

            "x_axis": x_axis,

            "y_axis": y_axis,

            "curve_names": legend,

            "ticks": ticks,

            "curve_count": digitized["curve_count"],

            "curves": digitized["curves"]

        }

    # --------------------------------------------------

    def clean_title(self, title):

        title = title.replace(
            "SURFACE",
            "Surface"
        )

        title = re.sub(
            r"\s+",
            " ",
            title
        )

        return title.strip()

    # --------------------------------------------------

    def clean_axis(self, axis):

        axis = axis.replace("i", "1")

        axis = axis.replace("I", "1")

        return axis.strip()

    # --------------------------------------------------

    def clean_legend(self, legend):

        cleaned = []

        for item in legend:

            item = item.upper()

            item = item.replace("OOO", "000")

            item = item.replace("OO", "00")

            item = item.replace("O", "0")

            item = item.replace("I", "1")

            item = item.replace("L", "1")

            item = re.sub(
                r"\s+",
                " ",
                item
            )

            cleaned.append(item)

        return list(dict.fromkeys(cleaned))

    # --------------------------------------------------

    def detect_graph_type(self, digitized):

        if digitized["curve_count"] > 1:

            return "Multi-line Graph"

        elif digitized["curve_count"] == 1:

            return "Line Graph"

        return "Unknown"

    # --------------------------------------------------

    def detect_domain(

        self,

        title,

        x_axis,

        y_axis,

        legend

    ):

        text = (

            title + " "

            + x_axis + " "

            + y_axis + " "

            + " ".join(legend)

        ).upper()

        keywords = [

            "NACA",

            "LIFT",

            "DRAG",

            "CD",

            "CL",

            "REYNOLDS",

            "RN",

            "MACH"

        ]

        for word in keywords:

            if word in text:

                return "Aerodynamics"

        return "General Engineering"