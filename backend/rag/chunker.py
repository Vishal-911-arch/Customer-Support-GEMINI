from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentChunker:
    """
    Splits LangChain Documents into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_documents(self, documents):
        """
        Split documents into chunks.
        """

        return self.text_splitter.split_documents(documents)

    # Backward compatibility
    def split_documents(self, documents):
        return self.chunk_documents(documents)