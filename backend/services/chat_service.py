from rag.pipeline import RAGPipeline

pipeline = RAGPipeline()


class ChatService:

    @staticmethod
    def ask(question: str):
        return pipeline.ask(question)