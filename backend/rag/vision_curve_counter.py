from google import genai
from dotenv import load_dotenv
import os


class VisionCurveCounter:

    def __init__(self):

        load_dotenv()

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    # ---------------------------------------------------------

    def count(self, image_path):

        uploaded = self.client.files.upload(
            file=image_path
        )

        prompt = """
You are analyzing an engineering graph.

Count ONLY the plotted curves.

Ignore:

- X axis
- Y axis
- Tick marks
- Grid lines
- Labels
- Legends
- Text
- Arrows

Return ONLY a single integer.

Example:
1
2
3

Do not explain.
"""

        response = self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=[
                prompt,
                uploaded
            ]

        )

        return response.text.strip()