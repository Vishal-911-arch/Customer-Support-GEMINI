import cv2
import numpy as np
from skimage.morphology import skeletonize


class CurveSegmenter:

    def __init__(self):

        # minimum size of valid curve
        self.min_component_area = 500

    # =====================================================
    # Remove grid lines
    # =====================================================

    def remove_grid(self, binary):

        H, W = binary.shape

        hk = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (max(30, W // 20), 1)
        )

        horizontal = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            hk
        )

        vk = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (1, max(30, H // 20))
        )

        vertical = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            vk
        )

        grid = cv2.add(
            horizontal,
            vertical
        )

        cv2.imwrite(
            "outputs/grid_removed.png",
            grid
        )

        curves = cv2.subtract(
            binary,
            grid
        )

        return curves

    # =====================================================
    # Connect broken dashed curves
    # =====================================================

    def connect_fragments(self, image):

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (3, 3)
        )

        image = cv2.morphologyEx(
            image,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=1
        )

        return image

    # =====================================================
    # Skeletonization
    # =====================================================

    def skeletonize_curve(self, image):

        skel = skeletonize(
            image > 0
        )

        skel = (
            skel.astype(np.uint8)
            * 255
        )

        cv2.imwrite(
            "outputs/skeleton.png",
            skel
        )

        return skel

    # =====================================================
    # Main Segmentation
    # =====================================================

    def segment(self, image_path):

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:

            raise Exception(
                f"Cannot open {image_path}"
            )

        print("=" * 60)
        print("CURVE SEGMENTER")
        print("=" * 60)

        # -------------------------------------------------
        # Threshold
        # -------------------------------------------------

        _, binary = cv2.threshold(

            image,

            180,

            255,

            cv2.THRESH_BINARY_INV

        )

        cv2.imwrite(
            "outputs/binary_curve.png",
            binary
        )

        # -------------------------------------------------
        # Remove grid
        # -------------------------------------------------

        curves_img = self.remove_grid(
            binary
        )

        cv2.imwrite(
            "outputs/no_grid.png",
            curves_img
        )

        # -------------------------------------------------
        # Connect broken pieces
        # -------------------------------------------------

        curves_img = self.connect_fragments(
            curves_img
        )

        cv2.imwrite(
            "outputs/connected.png",
            curves_img
        )

        # -------------------------------------------------
        # Skeletonization
        # -------------------------------------------------

        curves_img = self.skeletonize_curve(
            curves_img
        )

        # -------------------------------------------------
        # Connected Components
        # -------------------------------------------------

        num_labels, labels, stats, _ = \
            cv2.connectedComponentsWithStats(
                curves_img,
                connectivity=8
            )

        curves = []

        debug = cv2.cvtColor(
            curves_img,
            cv2.COLOR_GRAY2BGR
        )

        curve_id = 1

        for label in range(
                1,
                num_labels
        ):

            area = stats[
                label,
                cv2.CC_STAT_AREA
            ]

            if area < self.min_component_area:
                continue

            component = np.uint8(
                labels == label
            ) * 255

            x, y, w, h = \
                cv2.boundingRect(
                    component
                )

            aspect = max(
                w,
                h
            ) / (
                min(w, h) + 1
            )

            # -----------------------------------
            # Reject text blobs
            # -----------------------------------

            if aspect < 2:
                continue

            fill_ratio = (
                area /
                (w * h + 1)
            )

            # aircraft icons / text blocks
            if fill_ratio > 0.60:
                continue

            ys, xs = np.where(
                component > 0
            )

            if len(xs) < 40:
                continue

            pts = np.column_stack(
                (
                    xs,
                    ys
                )
            )

            pts = pts[
                np.argsort(
                    pts[:, 0]
                )
            ]

            sampled = []

            last_x = -999

            for p in pts:

                px = int(p[0])
                py = int(p[1])

                if abs(
                        px - last_x
                ) < 2:
                    continue

                sampled.append(
                    (
                        px,
                        py
                    )
                )

                last_x = px

            if len(sampled) < 20:
                continue

            curves.append({

                "id":
                    curve_id,

                "points":
                    sampled,

                "bbox":
                    [
                        int(x),
                        int(y),
                        int(w),
                        int(h)
                    ],

                "area":
                    int(area)

            })

            color = (

                np.random.randint(
                    50,
                    255
                ),

                np.random.randint(
                    50,
                    255
                ),

                np.random.randint(
                    50,
                    255
                )

            )

            debug[
                component > 0
            ] = color

            cv2.rectangle(

                debug,

                (x, y),

                (
                    x + w,
                    y + h
                ),

                color,

                2

            )

            curve_id += 1

        cv2.imwrite(

            "outputs/curve_segment_debug.png",

            debug

        )

        print(
            f"Detected Curves : "
            f"{len(curves)}"
        )

        return curves