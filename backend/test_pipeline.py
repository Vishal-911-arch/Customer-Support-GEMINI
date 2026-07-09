from rag.pipeline import RAGPipeline

pipeline = RAGPipeline()

question = input("\nQuestion : ")

result = pipeline.ask(question)

print("\n")

print("=" * 80)

print("ANSWER")

print("=" * 80)

print(result["answer"])

print("\n")

print("=" * 80)

print("SOURCES")

print("=" * 80)

for source in result["sources"]:

    print(source)

print("\n")

print("=" * 80)

print("VISION")

print("=" * 80)

print(result["vision"])