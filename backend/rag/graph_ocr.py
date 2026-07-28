import easyocr
import cv2
import re


class GraphOCR:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

        self.engineering_keywords = [

            "LOAD",
            "STALL",
            "BANK",
            "ANGLE",
            "LIFT",
            "DRAG",
            "MACH",
            "PRESSURE",
            "THRUST",
            "ALTITUDE",
            "VELOCITY",
            "FACTOR",
            "AIRSPEED",
            "CL",
            "CD",
            "CM",
            "REYNOLDS",
            "NACA",
            "RPM"
        ]

    # =====================================================
    # Main OCR
    # =====================================================

    def extract(
            self,
            image_path
    ):

        image = cv2.imread(
            image_path
        )

        if image is None:

            raise Exception(
                f"Cannot load {image_path}"
            )

        h, w = image.shape[:2]

        results = self.reader.readtext(

            image,

            detail=1,

            paragraph=False
        )

        title = []
        x_axis = []
        y_axis = []
        legend = []
        annotations = []

        raw_items = []

        for box, text, conf in results:

            if conf < 0.20:
                continue

            text = text.strip()

            if len(text) == 0:
                continue

            xs = [p[0] for p in box]
            ys = [p[1] for p in box]

            cx = sum(xs) / 4
            cy = sum(ys) / 4

            xmin = int(min(xs))
            ymin = int(min(ys))
            xmax = int(max(xs))
            ymax = int(max(ys))

            item = {

                "text": text,

                "confidence": float(conf),

                "bbox": [

                    xmin,
                    ymin,
                    xmax,
                    ymax
                ],

                "cx": cx,
                "cy": cy
            }

            raw_items.append(item)

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            if cy < h * 0.15:

                title.append(text)

            # ------------------------------------------------
            # X AXIS
            # ------------------------------------------------

            elif cy > h * 0.88:

                x_axis.append(text)

            # ------------------------------------------------
            # Y AXIS
            # ------------------------------------------------

            elif cx < w * 0.12:

                y_axis.append(text)

            # ------------------------------------------------
            # LEGEND
            # ------------------------------------------------

            elif (

                    cx > w * 0.70

                    and

                    cy < h * 0.70
            ):

                legend.append(text)

            # ------------------------------------------------
            # ANNOTATIONS
            # ------------------------------------------------

            else:

                annotations.append(text)

        # =====================================================
        # Engineering Terms
        # =====================================================

        engineering_terms = []

        all_text = " ".join(

            x["text"]

            for x in raw_items

        )

        text_upper = all_text.upper()

        for k in self.engineering_keywords:

            if k in text_upper:

                engineering_terms.append(k)

        engineering_terms = list(

            dict.fromkeys(

                engineering_terms
            )
        )

        # =====================================================
        # OCR Ticks
        # =====================================================

        ticks = self.extract_numeric_ticks(

            raw_items,

            w,

            h
        )

        return {

            "title":

                " ".join(title),

            "x_axis":

                " ".join(x_axis),

            "y_axis":

                " ".join(y_axis),

            "legend":

                self.clean_legend(
                    legend
                ),

            "annotations":

                list(

                    dict.fromkeys(
                        annotations
                    )
                ),

            "engineering_terms":

                engineering_terms,

            "ticks":

                ticks,

            "ocr_items":

                raw_items,

            "raw_text":

                [

                    x["text"]

                    for x in raw_items

                ]
        }

    # =====================================================
    # Number Parser
    # =====================================================

    def parse_number(
            self,
            text
    ):

        text = text.upper()

        text = text.replace(
            "O",
            "0"
        )

        text = text.replace(
            "I",
            "1"
        )

        text = text.replace(
            "L",
            "1"
        )

        text = text.replace(
            ",",
            ""
        )

        text = text.strip()

        m = re.search(

            r"-?\d+\.?\d*",

            text
        )

        if not m:
            return None

        try:

            return float(
                m.group()
            )

        except:
            return None

    # =====================================================
    # Tick Extraction
    # =====================================================

    def extract_numeric_ticks(

            self,
            items,
            width,
            height

    ):

        x_ticks = []
        y_ticks = []

        for item in items:

            value = self.parse_number(

                item["text"]

            )

            if value is None:
                continue

            cx = item["cx"]
            cy = item["cy"]

            if cy > height * 0.84:

                x_ticks.append({

                    "value": value,

                    "pixel": float(cx)

                })

            elif cx < width * 0.15:

                y_ticks.append({

                    "value": value,

                    "pixel": float(cy)

                })

        x_ticks = sorted(

            x_ticks,

            key=lambda x: x["pixel"]
        )

        y_ticks = sorted(

            y_ticks,

            key=lambda x: x["pixel"]
        )

        return {

            "x": x_ticks,

            "y": y_ticks
        }

    # =====================================================
    # Legend Cleaner
    # =====================================================

    def clean_legend(
            self,
            legend
    ):

        cleaned = []

        for item in legend:

            t = item.upper()

            t = t.replace(
                "O",
                "0"
            )

            t = t.replace(
                "I",
                "1"
            )

            t = t.replace(
                "L",
                "1"
            )

            t = re.sub(

                r"\s+",

                " ",

                t
            )

            cleaned.append(
                t
            )

        return list(

            dict.fromkeys(
                cleaned
            )
        )