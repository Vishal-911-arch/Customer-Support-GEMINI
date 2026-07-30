from google import genai
from google.genai import errors
from dotenv import load_dotenv
from tqdm import tqdm
import os
import time
import re


class EmbeddingGenerator:

    def __init__(self, batch_size=32, min_delay_seconds=0.75, max_retries=5):

        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        print("GEMINI_API_KEY present:", bool(key))
        print("GEMINI_API_KEY prefix:", repr(key[:8] if key else None))
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.batch_size = batch_size
        self.model = "gemini-embedding-001"
        self.min_delay_seconds = min_delay_seconds
        self.max_retries = max_retries

    # ---------------------------------------------------------

    def _sleep_on_rate_limit(self, error_message: str, fallback_seconds: int = 40):
        """
        Gemini may return a retry delay in the error text.
        Example:
        'Please retry in 38.717842252s.'
        """
        match = re.search(r"retry in ([0-9.]+)s", error_message, re.IGNORECASE)
        if match:
            wait_seconds = float(match.group(1))
        else:
            wait_seconds = float(fallback_seconds)

        wait_seconds = max(wait_seconds, 1.0)
        print(f"Rate limit hit. Waiting {wait_seconds:.1f} seconds...")
        time.sleep(wait_seconds)

    # ---------------------------------------------------------

    def _embed_texts(self, texts):
        """
        Retry-safe embedding request for one batch.
        """
        attempt = 0

        while True:
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=texts
                )

                return [
                    item.values
                    for item in response.embeddings
                ]

            except errors.ClientError as e:
                message = str(e)

                if "RESOURCE_EXHAUSTED" in message or "429" in message:
                    attempt += 1

                    if attempt > self.max_retries:
                        raise

                    print(f"Embedding rate limit on attempt {attempt}/{self.max_retries}")
                    self._sleep_on_rate_limit(message)
                    continue

                raise

    # ---------------------------------------------------------

    def embed_documents(self, documents):

        embeddings = []
        total = len(documents)

        print(f"\nGenerating embeddings for {total} chunks...\n")

        start = time.time()

        for i in tqdm(
            range(0, total, self.batch_size),
            desc="Embedding"
        ):

            batch = documents[i:i + self.batch_size]

            texts = [
                doc.page_content
                for doc in batch
            ]

            batch_start = time.time()

            batch_embeddings = self._embed_texts(texts)

            embeddings.extend(batch_embeddings)

            elapsed = time.time() - batch_start
            if elapsed < self.min_delay_seconds:
                time.sleep(self.min_delay_seconds - elapsed)

        print(f"\nFinished in {time.time() - start:.2f} seconds")

        return embeddings

    # ---------------------------------------------------------

    def embed_query(self, query):

        attempt = 0

        while True:
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=query
                )

                return response.embeddings[0].values

            except errors.ClientError as e:
                message = str(e)

                if "RESOURCE_EXHAUSTED" in message or "429" in message:
                    attempt += 1

                    if attempt > self.max_retries:
                        raise

                    print(f"Query embedding rate limit on attempt {attempt}/{self.max_retries}")
                    self._sleep_on_rate_limit(message)
                    continue

                raise