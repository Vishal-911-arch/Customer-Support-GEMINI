from ollama import Client
from tqdm import tqdm
import time

from config import (
    OLLAMA_HOST,
    EMBEDDING_MODEL,
    BATCH_SIZE
)


class EmbeddingGenerator:

    def __init__(
        self,
        model=EMBEDDING_MODEL,
        host=OLLAMA_HOST,
        batch_size=BATCH_SIZE
    ):

        self.client = Client(host=host)
        self.model = model
        self.batch_size = batch_size

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

            response = self.client.embed(
                model=self.model,
                input=texts
            )

            embeddings.extend(
                response["embeddings"]
            )

        print(
            f"\nFinished in {time.time()-start:.2f} seconds"
        )

        return embeddings

    def embed_query(self, query):

        response = self.client.embed(
            model=self.model,
            input=query
        )

        return response["embeddings"][0]