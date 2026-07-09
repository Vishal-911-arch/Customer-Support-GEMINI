import time
from rag.figure_vision import FigureVision
from ollama import Client

from config import (
    OLLAMA_HOST,
    LLM_MODEL
)
from rag.graph_retriever import GraphRetriever
from rag.context_linker import ContextLinker
from rag.retriever import Retriever
from rag.prompt import PromptBuilder
from rag.vision_retriever import VisionRetriever
from rag.vision_gate import VisionGate
from rag.figure_retriever import FigureRetriever


class RAGPipeline:
    """
    Complete Multimodal RAG Pipeline

    Priority:

    1. Figure Retriever
    2. Vector Retrieval
    3. Vision Gate
    4. Vision Retriever
    5. Prompt Builder
    6. LLM
    """

    def __init__(self):

        self.graph = GraphRetriever()

        self.context_linker = ContextLinker()

        self.figure_vision = FigureVision()

        self.client = Client(host=OLLAMA_HOST)

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.vision = VisionRetriever()

        self.vision_gate = VisionGate()

        self.figure = FigureRetriever()

    # =======================================================
    # MAIN PIPELINE
    # =======================================================

    def ask(self, question: str):

        SMALL_TALK = [

            "hi",
            "hello",
            "hey",
            "good morning",
            "good evening",
            "how are you",
            "who are you",
            "thanks",
            "thank you",
            "bye"

        ]
        q = question.lower().strip()

        if any(x == q for x in SMALL_TALK):

            response = self.client.chat(

                model=LLM_MODEL,

                messages=[

                    {
                        "role":"system",
                        "content":"You are a friendly AI assistant."
                    },

                    {
                        "role":"user",
                        "content":question
                    }

                ]

            )

            return {

                "answer":response["message"]["content"],

                "sources":[],

                "vision":[]

            }
        total_start = time.time()

        retrieval_time = 0
        vision_time = 0
        prompt_time = 0
        llm_time = 0

        vision_context = []
        sources = []
        graph_context = ""
        print("\nRetrieving relevant documents...\n")


        # ==========================================
        # GRAPH RETRIEVAL
        # ==========================================

        graph = self.graph.retrieve(question)

        if graph:

            print("✓ Graph Retrieved")

            metadata = graph["metadatas"][0][0]
            graph_text = graph["documents"][0][0]

            prompt = f"""
        You are an aerospace engineering assistant.

        Use ONLY the graph information below.

        {graph_text}

        Question:
        {question}
        """

            response = self.client.chat(

                model=LLM_MODEL,

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ]

            )

            return {

                "answer": response["message"]["content"],

                "sources":[

                    {

                        "filename": metadata["document"] + ".pdf",

                        "page": metadata["page"],

                        "type":"graph"

                    }

                ],

                "graph":{

                    "title": metadata.get("title",""),

                    "summary": graph_text,

                    "page": metadata["page"]

                }

    }

        # =======================================================
        # STEP 1
        # FIGURE RETRIEVER
        # =======================================================

        figure = self.figure.retrieve(question)
        linked_text = ""

        if figure:

            linked_text = self.context_linker.link(

                figure["document"],
                figure["page"]

            )

            print("\n" + "=" * 80)
            print("LINKED CONTEXT")
            print("=" * 80)
            print(linked_text)
            print("=" * 80)

            print("\nLinked Context\n")
            print(linked_text[:1000])

        # =========================================================
# FIGURE RETRIEVAL
# =========================================================



        if figure:

            print(f"\nFigure {figure['figure']} found!")
            print(f"Page : {figure['page']}")

            # --------------------------------------------
            # FULL PAGE VISION
            # --------------------------------------------

            vision_description = figure["description"]

            vision_context = [

    {

        "document": figure["document"],

        "page": figure["page"],

        "images": [

            {

                "type": "figure",

                "description": figure["description"]

            }

        ]

    }

]

            retrieved_results = {

    "documents": [[

        f"""
Figure Number : {figure['figure']}

Figure Title : {figure['title']}

Figure Description :

{figure['description']}
"""

    ]],

    "metadatas": [[

        {

            "filename": figure["document"] + ".pdf",

            "document": figure["document"],

            "page": figure["page"],

            "type": "figure"

        }

    ]]

}

            prompt = self.prompt_builder.build_prompt(

                question,

                retrieved_results,

                vision_context,

                linked_text,

                graph_context=""
            )

            response = self.client.chat(

                model=LLM_MODEL,

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                options={

                    "temperature": 0,

                    "num_predict": 350,

                    "num_ctx": 4096

                }

            )

            return {

                "answer": response["message"]["content"],

                "sources": [

                    {

                        "filename": figure["document"] + ".pdf",

                        "page": figure["page"],

                        "type": "figure"

                    }

                ],

                "vision": vision_context

            }

            if images:

                vision_context.append(
                    {
                        "document": figure["document"],
                        "page": figure["page"],
                        "images": images
                    }
                )

            results = {

                "documents": [
                    [
                        figure["text"]
                    ]
                ],

                "metadatas": [
                    [
                        {

                            "filename":
                            figure["document"] + ".pdf",

                            "page":
                            figure["page"],

                            "document":
                            figure["document"],

                            "type":
                            "ocr"

                        }
                    ]
                ]

            }

            sources.append(
                {
                    "filename":
                    figure["document"] + ".pdf",

                    "page":
                    figure["page"],

                    "type":
                    "ocr"
                }
            )

        # =======================================================
        # STEP 2
        # NORMAL RETRIEVAL
        # =======================================================

        else:

            t = time.time()

            results = self.retriever.retrieve(

                question,

                top_k=5

            )

            retrieval_time = time.time() - t

            print("\nChecking Vision Gate...\n")

            if self.vision_gate.requires_vision(question):

                print("✓ Vision Required\n")

                t = time.time()

                vision_context = self.vision.analyze_results(
                    results
                )

                vision_time = time.time() - t

            else:

                print("✓ Vision Skipped")

            # -----------------------------------------------
            # Sources
            # -----------------------------------------------

            seen = set()

            if results["metadatas"]:

                for meta in results["metadatas"][0]:

                    filename = meta.get(
                        "filename",
                        "Unknown"
                    )

                    page = meta.get(
                        "page",
                        "Unknown"
                    )

                    src = (filename, page)

                    if src in seen:
                        continue

                    seen.add(src)

                    sources.append(
                        {
                            "filename": filename,
                            "page": page,
                            "type": meta.get(
                                "type",
                                "pdf"
                            )
                        }
                    )

        # =======================================================
        # STEP 3
        # BUILD PROMPT
        # =======================================================

        print("\nBuilding Prompt...\n")

        t = time.time()

        prompt = self.prompt_builder.build_prompt(

            question,

            results,

            vision_context,

            linked_text,

            graph_context=""

        )

        prompt_time = time.time() - t
        # =======================================================
        # STEP 4
        # ASK LLM
        # =======================================================

        print("\nGenerating Answer...\n")

        t = time.time()

        response = self.client.chat(

            model=LLM_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={

                "temperature": 0,

                "num_predict": 300,

                "num_ctx": 4096

            }

        )

        llm_time = time.time() - t

        answer = response["message"]["content"]

        # =======================================================
        # PERFORMANCE
        # =======================================================

        total_time = time.time() - total_start

        print("\n" + "=" * 60)
        print("MULTIMODAL RAG PERFORMANCE")
        print("=" * 60)

        print(f"Retrieval       : {retrieval_time:.2f} sec")
        print(f"Vision          : {vision_time:.2f} sec")
        print(f"Prompt Builder  : {prompt_time:.2f} sec")
        print(f"LLM             : {llm_time:.2f} sec")

        print("-" * 60)

        print(f"TOTAL           : {total_time:.2f} sec")

        print("=" * 60)

        # =======================================================
        # RETURN
        # =======================================================

        return {

            "answer": answer,

            "sources": sources,

            "vision": vision_context

        }