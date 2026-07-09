from pathlib import Path
import json

from config import VISION_OUTPUT_DIR


class VisionCache:

    def __init__(self):

        self.root = Path(VISION_OUTPUT_DIR)

    # -----------------------------------------

    def cache_file(self, document, page):

        folder = self.root / document

        folder.mkdir(

            parents=True,

            exist_ok=True

        )

        return folder / f"page_{page}.json"

    # -----------------------------------------

    def exists(self, document, page):

        return self.cache_file(

            document,

            page

        ).exists()

    # -----------------------------------------

    def load(self, document, page):

        with open(

            self.cache_file(

                document,

                page

            ),

            encoding="utf-8"

        ) as f:

            return json.load(f)

    # -----------------------------------------

    def save(

        self,

        document,

        page,

        data

    ):

        with open(

            self.cache_file(

                document,

                page

            ),

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )