import re


class GraphParser:

    def __init__(self):
        pass

    # -----------------------------------------------------

    def parse(self, ocr, digitized):

        title = self.clean_text(

            ocr.get(
                "title",
                ""
            )

        )

        x_axis = self.clean_text(

            ocr.get(
                "x_axis",
                ""
            )

        )

        y_axis = self.clean_text(

            ocr.get(
                "y_axis",
                ""
            )

        )

        legend = self.clean_list(

            ocr.get(
                "legend",
                []
            )

        )

        annotations = self.clean_list(

            ocr.get(
                "annotations",
                []
            )

        )

        engineering_terms = list(

            set(

                ocr.get(

                    "engineering_terms",

                    []

                )

            )

        )

        ticks = ocr.get(
            "ticks",
            {}
        )

        graph_type = self.detect_graph_type(

            title,
            x_axis,
            y_axis,
            digitized

        )

        domain = self.detect_domain(

            title,
            x_axis,
            y_axis,
            legend,
            annotations,
            engineering_terms

        )

        summary_text = " ".join([

            title,
            x_axis,
            y_axis,
            " ".join(legend),
            " ".join(annotations)

        ])

        return {

            "title":

                title,

            "graph_type":

                graph_type,

            "engineering_domain":

                domain,

            "x_axis":

                x_axis,

            "y_axis":

                y_axis,

            "curve_names":

                legend,

            "annotations":

                annotations,

            "engineering_terms":

                engineering_terms,

            "ticks":

                ticks,

            "curve_count":

                digitized.get(
                    "curve_count",
                    0
                ),

            "curves":

                digitized.get(
                    "curves",
                    []
                ),

            "semantic_text":

                summary_text
        }

    # -----------------------------------------------------

    def clean_text(self, text):

        text = text.replace(
            "I",
            "1"
        )

        text = text.replace(
            "i",
            "1"
        )

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    # -----------------------------------------------------

    def clean_list(self, items):

        cleaned = []

        for item in items:

            item = self.clean_text(
                item
            )

            if len(item):

                cleaned.append(
                    item
                )

        return list(

            dict.fromkeys(

                cleaned

            )

        )

    # -----------------------------------------------------

    def detect_graph_type(

            self,

            title,

            x_axis,

            y_axis,

            digitized

    ):

        text = (

            title + " "

            + x_axis + " "

            + y_axis

        ).upper()

        if "TIME" in text:

            return "Time Series"

        if "ALTITUDE" in text:

            return "Performance Curve"

        if "PRESSURE" in text:

            return "Engineering Performance Plot"

        if digitized.get(

                "curve_count",

                0

        ) > 1:

            return "Multi-Curve Plot"

        if digitized.get(

                "curve_count",

                0

        ) == 1:

            return "Single Curve Plot"

        return "Unknown"

    # -----------------------------------------------------

    def detect_domain(

            self,

            title,

            x_axis,

            y_axis,

            legend,

            annotations,

            engineering_terms

    ):

        text = (

            title + " "

            + x_axis + " "

            + y_axis + " "

            + " ".join(legend) + " "

            + " ".join(annotations) + " "

            + " ".join(engineering_terms)

        ).upper()

        aerospace_keywords = [

            "AERODYNAMIC",
            "LIFT",
            "DRAG",
            "STALL",
            "BANK",
            "ANGLE",
            "LOAD",
            "FACTOR",
            "TURN",
            "AIRCRAFT",
            "ALTITUDE",
            "THRUST",
            "MACH",
            "CL",
            "CD",
            "CM",
            "NACA",
            "REYNOLDS",
            "AIRSPEED",
            "FLAP",
            "PITCH",
            "ROLL",
            "YAW"

        ]

        propulsion_keywords = [

            "ENGINE",
            "TURBINE",
            "COMPRESSOR",
            "RPM",
            "TEMPERATURE",
            "PRESSURE RATIO"

        ]

        structures_keywords = [

            "STRESS",
            "STRAIN",
            "FATIGUE",
            "DEFLECTION"

        ]

        for k in aerospace_keywords:

            if k in text:

                return "Aerodynamics"

        for k in propulsion_keywords:

            if k in text:

                return "Propulsion"

        for k in structures_keywords:

            if k in text:

                return "Structures"

        return "General Engineering"