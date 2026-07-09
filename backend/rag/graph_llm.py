from ollama import Client

from config import (
    OLLAMA_HOST,
    LLM_MODEL
)


class GraphLLM:

    def __init__(self):

        self.client = Client(
            host=OLLAMA_HOST
        )

    # ---------------------------------------------------------

    def explain(self, graph):

        prompt = f"""
You are an aerospace engineering expert.

You have already received structured information extracted from an engineering graph.

Do NOT invent numerical values.

Use ONLY the information below.

================================================

GRAPH TITLE

{graph["title"]}

GRAPH TYPE

{graph["graph_type"]}

ENGINEERING DOMAIN

{graph["engineering_domain"]}

X AXIS

{graph["x_axis"]}

Y AXIS

{graph["y_axis"]}

CURVES

{graph["curve_names"]}

NUMBER OF CURVES

{graph["curve_count"]}

AXIS TICKS

X:
{graph["ticks"]["x"]}

Y:
{graph["ticks"]["y"]}

================================================

Write the answer in exactly this format.

Graph Summary

Trend

Engineering Interpretation

Important Observations

Possible Aircraft Meaning

Do not mention OCR.

Do not mention image processing.

Speak as if you are explaining the engineering graph to an aerospace engineer.
"""

        response = self.client.generate(

            model=LLM_MODEL,

            prompt=prompt,

            options={

                "temperature": 0,

                "num_predict": 400

            }

        )

        return response["response"]