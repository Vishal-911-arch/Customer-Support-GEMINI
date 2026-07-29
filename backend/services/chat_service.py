import os
import time
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from PIL import Image
from config import GEMINI_MODEL
from rag.pipeline import RAGPipeline
from rag.graph_pipeline import GraphPipeline
from rag.image_classifier import ImageClassifier

load_dotenv()

graph_pipeline = GraphPipeline()
classifier = ImageClassifier()
pipeline = RAGPipeline()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

graph_cache = {}


class ChatService:

    ACKNOWLEDGMENTS = {
        "ok", "okay", "sure", "yes", "yeah", "yep", "yup",
        "thanks", "thank you", "thx", "got it",
        "cool", "nice", "great", "understood", "done", "perfect",
        "alright", "fine", "awesome", "sounds good"
    }

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def is_acknowledgment(text: str) -> bool:
        q = text.strip().lower().rstrip("!.?,")
        return q in ChatService.ACKNOWLEDGMENTS

    @staticmethod
    def ack_response():
        return {
            "answer": "Sure — ask me the next question whenever you're ready.",
            "sources": [],
            "vision": [],
            "graph": None,
            "chat_title": "chat"
        }

    @staticmethod
    def rewrite_follow_up(question: str, history: Optional[List[dict]] = None) -> str:
        history = history or []

        if not history:
            return question

        recent = history[-6:]

        convo_lines = []
        for msg in recent:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            convo_lines.append(f"{role}: {content}")

        prompt = f"""
Rewrite the user's last message into a standalone question.

Rules:
- If the message is only an acknowledgment like "okay", "thanks", "sure", or "got it", return exactly the same text.
- If it is a follow-up, rewrite it using the conversation context.
- Do not answer the question.
- Return only the rewritten text.

Conversation:
{chr(10).join(convo_lines)}

Last message:
{question}
"""

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            rewritten = response.text.strip()
            return rewritten or question
        except Exception:
            return question

    # ==================================================
    # PDF RAG
    # ==================================================

    @staticmethod
    def ask(question: str, history: Optional[List[dict]] = None):
        history = history or []

        if ChatService.is_acknowledgment(question):
            return ChatService.ack_response()

        standalone_question = ChatService.rewrite_follow_up(question, history)

        if ChatService.is_acknowledgment(standalone_question):
            return ChatService.ack_response()
             
        result = pipeline.ask(standalone_question)

        title = ChatService.generate_title(
            standalone_question,
            result["answer"]
        )

        result["title"] = title
        return result

    # ==================================================
    # IMAGE CHAT
    # ==================================================

    @staticmethod
    def ask_image(question, image_path, history: Optional[List[dict]] = None):
        history = history or []

        if ChatService.is_acknowledgment(question):
            return ChatService.ack_response()

        standalone_question = ChatService.rewrite_follow_up(question, history)

        if ChatService.is_acknowledgment(standalone_question):
            return ChatService.ack_response()

        start = time.time()

        print("QUESTION :", standalone_question)
        print("IMAGE :", image_path)

        # ======================================
        # Resize Large Images
        # ======================================

        load_start = time.time()

        with Image.open(image_path) as img:
            w, h = img.size
            print(f"Image Load : {time.time() - load_start:.2f}s")
            print(f"Original Size : {w} x {h}")

            if max(w, h) > 1500:
                img.thumbnail((1200, 1200))

                resized_path = os.path.join(
                    os.path.dirname(image_path),
                    "temp_resized.png"
                )

                img.save(resized_path)
                image_path = resized_path

                print("Using resized image.")
            else:
                print("Using original image.")

        # ======================================
        # Classify Image
        # ======================================

        classify_start = time.time()

        image_type = classifier.classify_image(image_path)

        print("IMAGE TYPE :", image_type)
        print(f"Classification : {time.time() - classify_start:.2f}s")

        # ======================================
        # GRAPH MODE
        # ======================================

        if image_type == "graph":

            print("\n✓ GRAPH MODE\n")

            if image_path in graph_cache:
                print("✓ Using cached graph")
                graph_data = graph_cache[image_path]
            else:
                print("✓ Running graph pipeline")
                graph_data = graph_pipeline.analyze(image_path)
                graph_cache[image_path] = graph_data

            answer = graph_pipeline.llm.answer_question(
                graph_data,
                standalone_question
            )

            title = ChatService.generate_title(
                standalone_question,
                answer
            )

            print(f"Graph Time : {time.time() - start:.2f}s")

            return {
                "answer": answer,
                "title": title,
                "sources": [],
                "graph": graph_data,
                "vision": []
            }

        # ======================================
        # GEMINI VISION MODE
        # ======================================

        print("\n✓ GEMINI VISION MODE\n")

        vision_start = time.time()

        uploaded = client.files.upload(
            file=image_path
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                uploaded,
                standalone_question
            ]
        )

        vision_end = time.time()

        print(f"Gemini Vision : {vision_end - vision_start:.2f}s")

        answer = response.text

        title_start = time.time()

        title = ChatService.generate_title(
            standalone_question,
            answer
        )

        title_end = time.time()

        print(f"Title Generation : {title_end - title_start:.2f}s")
        print(f"TOTAL IMAGE REQUEST : {time.time() - start:.2f}s")

        return {
            "answer": answer,
            "title": title,
            "sources": [],
            "graph": None,
            "vision": []
        }

    # ==================================================
    # GENERATE CHAT TITLE
    # ==================================================

    @staticmethod
    def generate_title(question, answer):
        prompt = f"""
You generate short chat titles.

Rules:
- Maximum 4 words.
- No punctuation.
- No quotes.
- Return ONLY the title.

Question:
{question}

Answer:
{answer}
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text.strip()