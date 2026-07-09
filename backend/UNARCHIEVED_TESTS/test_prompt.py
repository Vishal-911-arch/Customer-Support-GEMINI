from rag.retriever import Retriever
from rag.prompt import PromptBuilder

retriever = Retriever()
prompt_builder = PromptBuilder()

question = "How should hydraulic pressure be checked?"

results = retriever.retrieve(question)

prompt = prompt_builder.build_prompt(
    question,
    results
)

print(prompt)