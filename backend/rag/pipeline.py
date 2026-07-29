import os
import time

from dotenv import load_dotenv
from google import genai
from config import GEMINI_MODEL
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

    Pipeline priority:

    1. Graph Retrieval
    2. Figure Retrieval
    3. Normal Vector Retrieval
    4. Vision Gate
    5. Vision Retrieval
    6. Prompt Builder
    7. Gemini LLM
    """

    def __init__(self):

        # -------------------------------------------------
        # Load Gemini API key
        # -------------------------------------------------

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured in the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # -------------------------------------------------
        # RAG Components
        # -------------------------------------------------

        self.graph = GraphRetriever()

        self.context_linker = ContextLinker()

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.vision = VisionRetriever()

        self.vision_gate = VisionGate()

        self.figure = FigureRetriever()

    # =====================================================
    # MAIN PIPELINE
    # =====================================================

    def ask(self, question: str):

        total_start = time.time()

        # -------------------------------------------------
        # SMALL TALK
        # -------------------------------------------------

        SMALL_TALK = [

            "hi",
            "hello",
            "hey",
            "how are you",
            "who are you",
            "thanks",
            "thank you",
            "bye",
            "help"

        ]

        q = question.lower().strip()

        print("=" * 60)
        print("RAG REQUEST")
        print("=" * 60)
        print("QUESTION :", question)

        # -------------------------------------------------
        # Small Talk Detection
        # -------------------------------------------------

        if any(
            phrase == q
            for phrase in SMALL_TALK
        ):

            print("\n✓ SMALL TALK DETECTED\n")

            prompt = f"""
You are a friendly AI assistant.

Answer the user normally.

Rules:
- Do not use the knowledge base.
- Do not mention documents.
- Do not mention figures.
- Do not mention graphs.
- Do not mention PDFs.
- Do not mention manuals.

User:
{question}
"""

            start = time.time()

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )

            llm_time = time.time() - start

            print(
                f"Gemini Time : {llm_time:.2f} sec"
            )

            return {

                "answer":
                    response.text.strip(),

                "sources":
                    [],

                "vision":
                    [],

                "graph":
                    None,

                "chat_title":
                    question

            }

        # -------------------------------------------------
        # Performance Timers
        # -------------------------------------------------

        retrieval_time = 0.0

        vision_time = 0.0

        prompt_time = 0.0

        llm_time = 0.0

        # -------------------------------------------------
        # Runtime Data
        # -------------------------------------------------

        vision_context = []

        sources = []

        graph_context = ""

        linked_text = ""

        # =================================================
        # STEP 1
        # GRAPH RETRIEVAL
        # =================================================

        print(
            "\nRetrieving graph information...\n"
        )

        graph_start = time.time()

        graph = self.graph.retrieve(
            question
        )

        graph_time = (
            time.time() -
            graph_start
        )

        print(
            f"Graph Retrieval : {graph_time:.2f} sec"
        )

        if graph:

            print(
                "\n✓ GRAPH RETRIEVED\n"
            )

            metadata = (
                graph["metadatas"][0][0]
            )

            graph_text = (
                graph["documents"][0][0]
            )

            prompt = f"""
You are an aerospace engineering assistant.

Use ONLY the graph information provided below.

Do not invent numerical values.

GRAPH INFORMATION:

{graph_text}

USER QUESTION:

{question}

Answer clearly using only the provided graph information.
"""

            llm_start = time.time()

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )

            llm_time = (
                time.time() -
                llm_start
            )

            print(
                f"Graph Gemini Time : {llm_time:.2f} sec"
            )

            total_time = (
                time.time() -
                total_start
            )

            print(
                f"Total Graph Request : "
                f"{total_time:.2f} sec"
            )

            return {

                "answer":
                    response.text.strip(),

                "sources": [

                    {

                        "filename":
                            metadata.get(
                                "document",
                                "Unknown"
                            ) + ".pdf",

                        "page":
                            metadata.get(
                                "page",
                                "Unknown"
                            ),

                        "type":
                            "graph"

                    }

                ],

                "vision":
                    [],

                "graph": {

                    "title":
                        metadata.get(
                            "title",
                            ""
                        ),

                    "summary":
                        graph_text,

                    "page":
                        metadata.get(
                            "page",
                            "Unknown"
                        )

                },

                "chat_title":
                    question

            }

        # =================================================
        # STEP 2
        # FIGURE RETRIEVAL
        # =================================================

        print(
            "\nChecking Figure Retriever...\n"
        )

        figure_start = time.time()

        figure = self.figure.retrieve(
            question
        )

        figure_time = (
            time.time() -
            figure_start
        )

        print(
            f"Figure Retrieval : "
            f"{figure_time:.2f} sec"
        )

        # -------------------------------------------------
        # Figure Found
        # -------------------------------------------------

        if figure:

            print(
                f"\n✓ FIGURE FOUND"
            )

            print(
                f"Figure : "
                f"{figure.get('figure', 'Unknown')}"
            )

            print(
                f"Document : "
                f"{figure.get('document', 'Unknown')}"
            )

            print(
                f"Page : "
                f"{figure.get('page', 'Unknown')}"
            )

            # ---------------------------------------------
            # Link Figure to Surrounding Context
            # ---------------------------------------------

            link_start = time.time()

            linked_text = (
                self.context_linker.link(

                    figure["document"],

                    figure["page"]

                )
            )

            link_time = (
                time.time() -
                link_start
            )

            print(
                f"Context Linking : "
                f"{link_time:.2f} sec"
            )

            # ---------------------------------------------
            # Vision Context
            # ---------------------------------------------

            figure_description = (
                figure.get(
                    "description",
                    ""
                )
            )

            vision_context = [

                {

                    "document":
                        figure["document"],

                    "page":
                        figure["page"],

                    "images": [

                        {

                            "type":
                                "figure",

                            "description":
                                figure_description

                        }

                    ]

                }

            ]

            # ---------------------------------------------
            # Construct Retrieved Results
            # ---------------------------------------------

            retrieved_results = {

                "documents": [

                    [

                        f"""
Figure Number:
{figure.get("figure", "")}

Figure Title:
{figure.get("title", "")}

Figure Description:

{figure_description}
"""

                    ]

                ],

                "metadatas": [

                    [

                        {

                            "filename":
                                figure["document"]
                                + ".pdf",

                            "document":
                                figure["document"],

                            "page":
                                figure["page"],

                            "type":
                                "figure"

                        }

                    ]

                ]

            }

            # ---------------------------------------------
            # Build Prompt
            # ---------------------------------------------

            prompt_start = time.time()

            prompt = (
                self.prompt_builder.build_prompt(

                    question,

                    retrieved_results,

                    vision_context,

                    linked_text,

                    graph_context=""

                )
            )

            prompt_time = (
                time.time() -
                prompt_start
            )

            print(
                f"Prompt Builder : "
                f"{prompt_time:.2f} sec"
            )

            # ---------------------------------------------
            # Gemini Answer
            # ---------------------------------------------

            print(
                "\nGenerating Figure Answer...\n"
            )

            llm_start = time.time()

            response = (
                self.client.models.generate_content(

                    model=GEMINI_MODEL,

                    contents=prompt

                )
            )

            llm_time = (
                time.time() -
                llm_start
            )

            answer = (
                response.text.strip()
            )

            total_time = (
                time.time() -
                total_start
            )

            print(
                "\n" + "=" * 60
            )

            print(
                "FIGURE RAG PERFORMANCE"
            )

            print(
                "=" * 60
            )

            print(
                f"Figure Retrieval : "
                f"{figure_time:.2f} sec"
            )

            print(
                f"Context Linking  : "
                f"{link_time:.2f} sec"
            )

            print(
                f"Prompt Builder    : "
                f"{prompt_time:.2f} sec"
            )

            print(
                f"Gemini            : "
                f"{llm_time:.2f} sec"
            )

            print(
                "-" * 60
            )

            print(
                f"TOTAL             : "
                f"{total_time:.2f} sec"
            )

            print(
                "=" * 60
            )

            return {

                "answer":
                    answer,

                "sources": [

                    {

                        "filename":
                            figure["document"]
                            + ".pdf",

                        "page":
                            figure["page"],

                        "type":
                            "figure"

                    }

                ],

                "vision":
                    vision_context,

                "graph":
                    None,

                "chat_title":
                    question

            }

        # =================================================
        # STEP 3
        # NORMAL VECTOR RETRIEVAL
        # =================================================

        print(
            "\nRetrieving relevant documents...\n"
        )

        retrieval_start = time.time()

        results = (
            self.retriever.retrieve(

                question,

                top_k=5

            )
        )

        retrieval_time = (
            time.time() -
            retrieval_start
        )

        print(
            f"Retrieval : "
            f"{retrieval_time:.2f} sec"
        )

        # =================================================
        # STEP 4
        # VISION GATE
        # =================================================

        print(
            "\nChecking Vision Gate...\n"
        )

        if (
            self.vision_gate.requires_vision(
                question
            )
        ):

            print(
                "✓ Vision Required\n"
            )

            vision_start = time.time()

            vision_context = (
                self.vision.analyze_results(

                    results

                )
            )

            vision_time = (
                time.time() -
                vision_start
            )

            print(
                f"Vision : "
                f"{vision_time:.2f} sec"
            )

        else:

            print(
                "✓ Vision Skipped"
            )

        # =================================================
        # STEP 5
        # COLLECT SOURCES
        # =================================================

        seen = set()

        metadatas = (
            results.get(
                "metadatas",
                []
            )
        )

        if metadatas:

            for meta in metadatas[0]:

                filename = (
                    meta.get(
                        "filename",
                        "Unknown"
                    )
                )

                page = (
                    meta.get(
                        "page",
                        "Unknown"
                    )
                )

                source_key = (

                    filename,

                    page

                )

                if source_key in seen:
                    continue

                seen.add(
                    source_key
                )

                sources.append(

                    {

                        "filename":
                            filename,

                        "page":
                            page,

                        "type":
                            meta.get(
                                "type",
                                "pdf"
                            )

                    }

                )

        # =================================================
        # STEP 6
        # BUILD FINAL PROMPT
        # =================================================

        print(
            "\nBuilding Prompt...\n"
        )

        prompt_start = time.time()

        prompt = (
            self.prompt_builder.build_prompt(

                question,

                results,

                vision_context,

                linked_text,

                graph_context=""

            )
        )

        prompt_time = (
            time.time() -
            prompt_start
        )

        print(
            f"Prompt Builder : "
            f"{prompt_time:.2f} sec"
        )

        # =================================================
        # STEP 7
        # GEMINI GENERATION
        # =================================================

        print(
            "\nGenerating Answer...\n"
        )

        llm_start = time.time()

        response = (
            self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )
        )

        llm_time = (
            time.time() -
            llm_start
        )

        answer = (
            response.text.strip()
        )

        # =================================================
        # PERFORMANCE
        # =================================================

        total_time = (
            time.time() -
            total_start
        )

        print(
            "\n" + "=" * 60
        )

        print(
            "MULTIMODAL RAG PERFORMANCE"
        )

        print(
            "=" * 60
        )

        print(
            f"Retrieval       : "
            f"{retrieval_time:.2f} sec"
        )

        print(
            f"Vision          : "
            f"{vision_time:.2f} sec"
        )

        print(
            f"Prompt Builder  : "
            f"{prompt_time:.2f} sec"
        )

        print(
            f"LLM             : "
            f"{llm_time:.2f} sec"
        )

        print(
            "-" * 60
        )

        print(
            f"TOTAL           : "
            f"{total_time:.2f} sec"
        )

        print(
            "=" * 60
        )

        # =================================================
        # RETURN
        # =================================================

        return {

            "answer":
                answer,

            "sources":
                sources,

            "vision":
                vision_context,

            "graph":
                None,

            "chat_title":
                question

        }