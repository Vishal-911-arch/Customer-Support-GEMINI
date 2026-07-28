from ollama import Client

client = Client()


class VisionCurveCounter:

    def count(

            self,

            image_path

    ):

        response = client.chat(

            model="llama3.2:3b",

            messages=[

                {

                    "role":"user",

                    "content":f"""

Count ONLY plotted curves.

Ignore:

- axes
- text
- grid
- legends

Return only integer.
""",

                    "images":[

                        image_path

                    ]

                }

            ]

        )

        return response["message"]["content"]