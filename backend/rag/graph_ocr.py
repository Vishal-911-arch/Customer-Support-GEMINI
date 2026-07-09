import easyocr
import cv2


class GraphOCR:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    # ----------------------------------------------------

    def read(self, image_path):

        results = self.reader.readtext(
            image_path,
            detail=0
        )

        return [x.strip() for x in results]

    # ----------------------------------------------------

    def extract(self, regions):

        title_text = self.read(
            regions["title"]
        )

        x_text = self.read(
            regions["x_axis"]
        )

        y_text = self.read(
            regions["y_axis"]
        )

        legend_text = self.read(
            regions["legend"]
        )

        plot_items = self.reader.readtext(
            regions["plot"],
            detail=1
        )

        plot = cv2.imread(
            regions["plot"]
        )

        h, w = plot.shape[:2]

        ocr_items = []

        raw = []

        for box, text, conf in plot_items:

            raw.append(text)

            xs = [p[0] for p in box]
            ys = [p[1] for p in box]

            ocr_items.append({

                "text": text,

                "cx": sum(xs) / 4,

                "cy": sum(ys) / 4

            })

        title = " ".join(title_text)

        x_axis = " ".join(x_text)

        y_axis = " ".join(y_text)

        legend = self.clean_legend(
            legend_text
        )

        ticks = self.find_ticks(
            ocr_items,
            w,
            h
        )

        return {

            "title": title,

            "x_axis": x_axis,

            "y_axis": y_axis,

            "legend": legend,

            "ticks": ticks,

            "raw_text": raw

        }

    # ----------------------------------------------------

    def clean_legend(self, legend):

        cleaned = []

        for item in legend:

            t = item.upper()

            t = t.replace("O", "0")

            t = t.replace("I", "1")

            t = t.replace("L", "1")

            cleaned.append(t)

        return list(dict.fromkeys(cleaned))

    # ----------------------------------------------------

    def parse_tick(self, text):

        import re

        text = text.upper()

        text = text.replace("O", "0")

        text = text.replace("I", "1")

        text = text.replace("L", "1")

        text = text.replace(",", "")

        text = text.replace("~", "")

        text = text.strip()

        if re.fullmatch(r"\d{3}", text):

            return float("." + text)

        if re.fullmatch(r"\.\d+", text):

            return float(text)

        if re.fullmatch(r"\d+\.\d+", text):

            return float(text)

        if re.fullmatch(r"\d+", text):

            return float(text)

        return None

    # ----------------------------------------------------

    def find_ticks(
        self,
        items,
        width,
        height
    ):

        x = []

        y = []

        for item in items:

            value = self.parse_tick(
                item["text"]
            )

            if value is None:
                continue

            cx = item["cx"]

            cy = item["cy"]

            if cy > height * 0.88:

                if value <= 20:

                    x.append(value)

            elif cx < width * 0.12:

                if value <= 0.05:

                    y.append(value)

        return {

            "x": sorted(set(x)),

            "y": sorted(set(y))

        }