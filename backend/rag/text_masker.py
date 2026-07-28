import cv2
import numpy as np


class TextMasker:

    def mask(

            self,

            image_path,

            ocr_boxes

    ):

        image = cv2.imread(image_path)

        mask = np.zeros(

            image.shape[:2],

            dtype=np.uint8

        )

        for box in ocr_boxes:

            x1,y1,x2,y2 = box

            cv2.rectangle(

                mask,

                (x1,y1),

                (x2,y2),

                255,

                -1

            )

        result = cv2.inpaint(

            image,

            mask,

            5,

            cv2.INPAINT_TELEA

        )

        return result