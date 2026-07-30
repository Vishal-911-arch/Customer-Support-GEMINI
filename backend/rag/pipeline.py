import os
import time

from dotenv import load_dotenv
from google import genai

from config import GEMINI_MODEL
from rag.retriever import Retriever
from rag.prompt import PromptBuilder


class RAGPipeline:
    """
    Text-only RAG Pipeline for free deployment.

    Pipeline priority:

    1. Normal Vector Retrieval
    2. Prompt Builder
    3. Gemini LLM
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

        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()

    # =====================================================
    # MAIN PIPELINE
    # =====================================================

    def ask(self, question: str):
        total_start = time.time()

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

        if any(phrase == q for phrase in SMALL_TALK):
            print("\n✓ SMALL TALK DETECTED\n")

            return {
            "answer": (
                "Hello! I’m AI Customer Support.\n"
                "I can help you with:\n"
                "• answering questions from uploaded PDFs\n"
                "• analyzing uploaded images\n"
                "• explaining document content clearly\n"
                "• finding useful information from the knowledge base\n"
                "Upload a file or ask me a question to begin."
            ),
            "sources": [],
            "vision": [],
            "graph": None,
            "chat_title": "Welcome"
        }
        # -------------------------------------------------
        # Performance Timers
        # -------------------------------------------------

        retrieval_time = 0.0
        prompt_time = 0.0
        llm_time = 0.0

        # -------------------------------------------------
        # Runtime Data
        # -------------------------------------------------

        vision_context = []
        sources = []
        linked_text = ""
        graph_context = ""

        # =================================================
        # STEP 1
        # NORMAL VECTOR RETRIEVAL
        # =================================================

        print("\nRetrieving relevant documents...\n")

        retrieval_start = time.time()

        results = self.retriever.retrieve(
            question,
            top_k=5
        )

        retrieval_time = time.time() - retrieval_start

        print(f"Retrieval : {retrieval_time:.2f} sec")

        # =================================================
        # STEP 2
        # COLLECT SOURCES
        # =================================================

        seen = set()
        metadatas = results.get("metadatas", [])

        if metadatas:
            for meta in metadatas[0]:
                filename = meta.get("filename", "Unknown")
                page = meta.get("page", "Unknown")

                source_key = (filename, page)

                if source_key in seen:
                    continue

                seen.add(source_key)

                sources.append(
                    {
                        "filename": filename,
                        "page": page,
                        "type": meta.get("type", "pdf")
                    }
                )

        # =================================================
        # STEP 3
        # BUILD FINAL PROMPT
        # =================================================

        print("\nBuilding Prompt...\n")

        prompt_start = time.time()

        prompt = self.prompt_builder.build_prompt(
            question,
            results,
            vision_context,
            linked_text,
            graph_context=graph_context
        )

        prompt_time = time.time() - prompt_start

        print(f"Prompt Builder : {prompt_time:.2f} sec")

        # =================================================
        # STEP 4
        # GEMINI GENERATION
        # =================================================

        print("\nGenerating Answer...\n")

        llm_start = time.time()

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        llm_time = time.time() - llm_start

        answer = response.text.strip()

        # =================================================
        # PERFORMANCE
        # =================================================

        total_time = time.time() - total_start

        print("\n" + "=" * 60)
        print("MULTIMODAL RAG PERFORMANCE")
        print("=" * 60)

        print(f"Retrieval       : {retrieval_time:.2f} sec")
        print(f"Vision          : {0.00:.2f} sec")
        print(f"Prompt Builder  : {prompt_time:.2f} sec")
        print(f"LLM             : {llm_time:.2f} sec")

        print("-" * 60)
        print(f"TOTAL           : {total_time:.2f} sec")
        print("=" * 60)

        # =================================================
        # RETURN
        # =================================================

        return {
            "answer": answer,
            "sources": sources,
            "vision": vision_context,
            "graph": None,
            "chat_title": question
        }