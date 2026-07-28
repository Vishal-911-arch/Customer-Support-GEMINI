import json
import os
import cv2
from pathlib import Path
from rag.junction_detector import JunctionDetector
from rag.curve_extractor import CurveExtractor
from rag.curve_reconnector import CurveReconnector

from rag.graph_cleaner import GraphCleaner
from rag.graph_ocr import GraphOCR
from rag.graph_digitizer import GraphDigitizer
from rag.graph_parser import GraphParser
from rag.graph_llm import GraphLLM
from rag.graph_indexer import GraphIndexer

from rag.skeletonizer import Skeletonizer
from rag.curve_validator import CurveValidator
from rag.curve_segmenter import CurveSegmenter

# NEW
from rag.axis_detector import AxisDetector
from rag.tick_detector import TickDetector
from rag.tick_ocr import TickOCR
from rag.coordinate_mapper import CoordinateMapper


class GraphPipeline:

    def __init__(self):


        self.cleaner = GraphCleaner()
        self.ocr = GraphOCR()

        self.tracer = CurveSegmenter()
        self.skeletonizer = Skeletonizer()
        self.validator = CurveValidator()
        self.junction_detector = JunctionDetector()

        self.curve_extractor = CurveExtractor()

        self.curve_reconnector = CurveReconnector()
        self.digitizer = GraphDigitizer()
        self.parser = GraphParser()
        self.llm = GraphLLM()

        # -----------------------------------
        # NEW MODULES
        # -----------------------------------

        self.axis_detector = AxisDetector()
        self.tick_detector = TickDetector()
        self.tick_ocr = TickOCR()

    # -----------------------------------------------------

    def analyze(
        self,
        image_path,
        document=None,
        page=1
):

        print("=" * 70)
        print("GRAPH PIPELINE")
        print("=" * 70)

        print(f"IMAGE : {image_path}")

        # =====================================================
        # LOAD FULL IMAGE
        # =====================================================

        plot = cv2.imread(image_path)

        if plot is None:

            raise Exception(
                f"Cannot open {image_path}"
            )

        print(
            f"IMAGE SIZE : {plot.shape}"
        )

        # =====================================================
        # CLEAN
        # =====================================================

        clean_img = self.cleaner.clean(
            image_path
        )

        clean_path = (
            "artifacts/graph_crop/"
            "plot_clean.png"
        )

        os.makedirs(
            os.path.dirname(clean_path),
            exist_ok=True
        )

        self.cleaner.save(
            clean_img,
            clean_path
        )

        print("✓ Graph Cleaned")

        # =====================================================
        # OCR
        # =====================================================

        print("\nRunning OCR...")

        ocr_data = self.ocr.extract(
            image_path
        )

        print("✓ OCR Complete")

        print(
            json.dumps(
                ocr_data,
                indent=4
            )
        )

        # =====================================================
        # AXIS DETECTION
        # =====================================================

        axes = self.axis_detector.detect(
            clean_img
        )

        print("✓ Axes Detected")

        print(
            json.dumps(
                axes,
                indent=4
            )
        )

        debug = self.axis_detector.draw_axes(

            plot.copy(),

            axes
        )

        cv2.imwrite(

            "outputs/axes_debug.png",

            debug
        )

        # =====================================================
        # TICK DETECTION
        # =====================================================

        ticks = self.tick_detector.detect(

            clean_img,

            original=plot,

            axes=axes
        )

        print("✓ Tick Detection")

        print(
            json.dumps(
                ticks,
                indent=4
            )
        )

        # =====================================================
        # TICK OCR
        # =====================================================

        x_labels = self.tick_ocr.extract(

            plot,
            ticks["x_ticks"],
            axis="x"

        )

        y_labels = self.tick_ocr.extract(

            plot,
            ticks["y_ticks"],
            axis="y"

        )

        generated_labels = {

            "x_labels": x_labels,

            "y_labels": y_labels

        }

        print("✓ Tick OCR")

        print(
            json.dumps(
                generated_labels,
                indent=4
            )
        )

        # =====================================================
        # SKELETON
        # =====================================================

        skeleton = self.skeletonizer.run(
            plot
        )

        cv2.imwrite(
            "outputs/skeleton.png",
            skeleton
        )

        print("✓ Skeleton Created")

        # =====================================================
        # JUNCTION DETECTION
        # =====================================================

        junctions = (

            self.junction_detector.detect(
                skeleton
            )
        )

        print(
            f"✓ Junctions : {len(junctions)}"
        )

        # =====================================================
        # CURVE EXTRACTION
        # =====================================================

        curves = (

            self.curve_extractor.extract(

                skeleton,

                junctions
            )
        )

        curves = (

            self.curve_reconnector.merge(
                curves
            )
        )

        print(
            f"✓ Curves Found : {len(curves)}"
        )

        # =====================================================
        # DIGITIZATION
        # =====================================================

        digitized = (

            self.digitizer.digitize(
                curves
            )
        )

        print(
            "✓ Digitization Complete"
        )

        # =====================================================
        # COORDINATE MAPPING
        # =====================================================

        if (

            len(
                generated_labels["x_labels"]
            ) >= 2

            and

            len(
                generated_labels["y_labels"]
            ) >= 2
        ):

            mapper = CoordinateMapper(
                generated_labels
            )

            for curve in digitized["curves"]:

                graph_points = (

                    mapper.convert_points(
                        curve["points"]
                    )
                )

                curve[
                    "graph_points"
                ] = graph_points

            print(
                "✓ Coordinate Mapping Complete"
            )

        else:

            print(
                "⚠ Insufficient ticks for mapping"
            )

        # =====================================================
        # ATTACH TICKS
        # =====================================================

        ocr_data["ticks"] = {

            "x":
                generated_labels[
                    "x_labels"
                ],

            "y":
                generated_labels[
                    "y_labels"
                ]
        }

        # =====================================================
        # PARSE
        # =====================================================

        parsed = self.parser.parse(

            ocr_data,

            digitized
        )

        print(
            "✓ Graph Parsed"
        )

        # =====================================================
        # LLM
        # =====================================================

        # =====================================================
        # INDEX
        # =====================================================

        if document is None:

            document = Path(
                image_path
            ).stem

        

        print(
            "✓ Graph Indexed"
        )

        print("=" * 70)
        print("FINAL OUTPUT")
        print("=" * 70)

        print(
            json.dumps(
                parsed,
                indent=4
            )
        )

        return parsed