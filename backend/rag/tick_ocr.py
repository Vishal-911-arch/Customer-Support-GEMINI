import cv2
import easyocr
import re


class TickOCR:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    # --------------------------------------------------

    def parse_number(self, text):

        text = str(text)

        text = text.strip()

        text = text.replace("O", "0")
        text = text.replace("o", "0")

        text = text.replace("I", "1")
        text = text.replace("l", "1")
        text = text.replace("|", "1")

        text = text.replace(",", "")

        match = re.search(
            r"-?\d*\.?\d+",
            text
        )

        if match:

            try:
                return float(
                    match.group()
                )

            except:
                return None

        return None

    # --------------------------------------------------

    def extract(
            self,
            image,
            ticks,
            axis="x"
    ):

        labels = []

        if image is None:
            return labels

        h, w = image.shape[:2]

        for item in ticks:

            ################################################
            # support both:
            #
            # [120,150,180]
            #
            # and
            #
            # [{"pixel":120}, ...]
            ################################################

            if isinstance(item, dict):

                p = int(
                    item.get(
                        "pixel",
                        0
                    )
                )

            else:

                p = int(item)

            ################################################
            # ROI
            ################################################

            if axis == "x":

                x1 = max(
                    0,
                    p - 35
                )

                x2 = min(
                    w,
                    p + 35
                )

                y1 = max(
                    0,
                    h - 90
                )

                y2 = h

            else:

                x1 = 0

                x2 = min(
                    90,
                    w
                )

                y1 = max(
                    0,
                    p - 25
                )

                y2 = min(
                    h,
                    p + 25
                )

            roi = image[
                  y1:y2,
                  x1:x2
                  ]

            if roi.size == 0:
                continue

            ################################################
            # preprocessing
            ################################################

            gray = cv2.cvtColor(
                roi,
                cv2.COLOR_BGR2GRAY
            )

            _, binary = cv2.threshold(

                gray,

                180,

                255,

                cv2.THRESH_BINARY

            )

            ################################################
            # OCR
            ################################################

            results = self.reader.readtext(

                binary,

                detail=0,

                paragraph=False

            )

            value = None

            for txt in results:

                value = self.parse_number(
                    txt
                )

                if value is not None:
                    break

            ################################################
            # save
            ################################################

            if value is not None:

                labels.append({

                    "pixel": int(p),

                    "value": float(value)

                })

        ####################################################
        # sort labels
        ####################################################

        labels = sorted(

            labels,

            key=lambda x:
            x["pixel"]

        )

        return labels