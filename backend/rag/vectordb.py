import hashlib
import chromadb

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME
)


class VectorDatabase:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    # ==========================================================
    # Generate Unique ID
    # ==========================================================

    def generate_id(self, chunk):

        metadata = chunk.metadata

        source = (
            metadata.get("source")
            or metadata.get("filename")
            or metadata.get("document")
            or "unknown"
        )

        page = metadata.get("page", 0)

        modality = metadata.get("type", "text")

        unique_string = (
            f"{modality}|"
            f"{source}|"
            f"{page}|"
            f"{chunk.page_content}"
        )

        return hashlib.sha256(
            unique_string.encode("utf-8")
        ).hexdigest()

    # ==========================================================
    # Add Documents
    # ==========================================================

    def add_documents(
        self,
        chunks,
        embeddings
    ):

        ids = []
        docs = []
        metas = []
        embs = []

        existing = set(
            self.collection.get()["ids"]
        )

        skipped = 0

        for chunk, embedding in zip(chunks, embeddings):

            doc_id = self.generate_id(chunk)

            if doc_id in existing:
                print("Duplicate graph found.")
                skipped += 1
                continue

            ids.append(doc_id)
            docs.append(chunk.page_content)
            metas.append(chunk.metadata)
            embs.append(embedding)
            print("\nMetadata :", chunk.metadata)

            doc_id = self.generate_id(chunk)

            print("Generated ID :", doc_id[:25])

        if ids:
            print("\nAdding to ChromaDB...")
            self.collection.add(

                ids=ids,

                documents=docs,

                metadatas=metas,

                embeddings=embs

            )
            print("Added successfully.")

        print(f"\nAdded   : {len(ids)} chunks")
        print(f"Skipped : {skipped} chunks")

        return len(ids)

    # ==========================================================
    # Utilities
    # ==========================================================

    def count(self):

        return self.collection.count()

    def collection_info(self):

        return self.collection.get()