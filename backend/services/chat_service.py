from rag.pipeline import RAGPipeline
from ollama import Client
import time
from PIL import Image
import os
from rag.graph_pipeline import GraphPipeline
from rag.image_classifier import ImageClassifier

graph_pipeline = GraphPipeline()
classifier = ImageClassifier()
pipeline = RAGPipeline()

client = Client()
graph_cache = {}

class ChatService:
    
    # ==================================================
    # PDF RAG
    # ==================================================

    @staticmethod
    def ask(question: str):

        result = pipeline.ask(question)

        title = ChatService.generate_title(

            question,

            result["answer"]

        )

        result["title"] = title

        return result

    # ==================================================
    # IMAGE CHAT
    # ==================================================

    

    @staticmethod
    def ask_image(question, image_path):

        start = time.time()

        print("QUESTION :", question)
        print("IMAGE :", image_path)

        # ======================================
        # Resize Large Images
        # ======================================

        load_start = time.time()

        img = Image.open(image_path)

        print(f"Image Load : {time.time()-load_start:.2f}s")

        w, h = img.size

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

        print(f"Classification : {time.time()-classify_start:.2f}s")

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
                question

            )

            title = ChatService.generate_title(

                question,
                answer

            )

            print(f"Graph Time : {time.time()-start:.2f}s")

            return {

                "answer": answer,

                "title": title,

                "sources": [],

                "graph": graph_data,

                "vision": []

            }
        # ======================================
        # VISION MODE
        # ======================================

        print("\n✓ VISION MODE\n")

        vision_start = time.time()

        print("Starting Qwen...")

        response = client.chat(

            model="qwen2.5vl:3b",

            keep_alive="30m",

            messages=[

                {

                    "role": "user",

                    "content": question,

                    "images": [

                        image_path

                    ]

                }

            ]

        )

        vision_end = time.time()

        print(f"Qwen Inference : {vision_end - vision_start:.2f}s")

        answer = response["message"]["content"]

        title_start = time.time()

        title = ChatService.generate_title(

            question,

            answer

        )

        title_end = time.time()

        print(f"Title Generation : {title_end - title_start:.2f}s")

        print(f"TOTAL IMAGE REQUEST : {time.time()-start:.2f}s")

        return {

            "answer": answer,

            "title": title,

            "sources": [],

            "graph": None,

            "vision": []

        }
    #===================================
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

        response = client.chat(

            model="llama3.2:3b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0
            }

        )

        return response["message"]["content"].strip()