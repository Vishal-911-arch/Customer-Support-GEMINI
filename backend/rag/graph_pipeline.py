import json
from pathlib import Path
import os
from rag.graph_indexer import GraphIndexer
from rag.graph_cropper import GraphCropper
from rag.graph_cleaner import GraphCleaner
from rag.graph_ocr import GraphOCR
from rag.curve_tracer import CurveTracer
from rag.graph_digitizer import GraphDigitizer
from rag.graph_parser import GraphParser
from rag.graph_llm import GraphLLM


class GraphPipeline:

    def __init__(self):

        self.cropper = GraphCropper()

        self.cleaner = GraphCleaner()

        self.ocr = GraphOCR()

        self.tracer = CurveTracer()

        self.digitizer = GraphDigitizer()

        self.parser = GraphParser()

        self.llm = GraphLLM()

    # -----------------------------------------------------

    

    def analyze(
        self,
        image_path,
        document=None,
        page=1
    ):

        print("=" * 60)
        print("GRAPH PIPELINE")
        print("=" * 60)

        # -----------------------------
        # Crop
        # -----------------------------

        regions = self.cropper.crop(image_path)

        print("✓ Graph Cropped")

        # -----------------------------
        # Clean Plot
        # -----------------------------

        clean_img = self.cleaner.clean(
            regions["plot"]
        )

        clean_path = "artifacts/graph_crop/plot_clean.png"

        os.makedirs(
            os.path.dirname(clean_path),
            exist_ok=True
        )

        self.cleaner.save(
            clean_img,
            clean_path
        )

        print("✓ Graph Cleaned")

        # -----------------------------
        # OCR
        # -----------------------------

        ocr_data = self.ocr.extract(
            regions
        )

        print("✓ OCR Complete")

        # -----------------------------
        # Curve Tracing
        # -----------------------------

        curves = self.tracer.trace(
            clean_path
        )

        print(
            f"✓ Curves Found : {len(curves)}"
        )

        # -----------------------------
        # Digitization
        # -----------------------------

        digitized = self.digitizer.digitize(
            curves
        )

        print("✓ Digitization Complete")

        # -----------------------------
        # Parsing
        # -----------------------------

        parsed = self.parser.parse(
            ocr_data,
            digitized
        )

        print("✓ Graph Parsed")

        # -----------------------------
        # LLM Explanation
        # -----------------------------

        explanation = self.llm.explain(parsed)

        parsed["llm_summary"] = explanation
        from rag.graph_indexer import GraphIndexer

        # ----------------------------------
        # Automatic indexing
        # ----------------------------------

        if document is None:

            document = Path(image_path).stem

        GraphIndexer().index(

            parsed,

            document=document,

            page=page

        )

        print("✓ Graph Explained")

        print()

        print(json.dumps(
            parsed,
            indent=4
        ))

        return parsed