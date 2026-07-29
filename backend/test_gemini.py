from gemini_client import client

models_to_try = [
    "GEMINI_MODEL"
]

for model in models_to_try:
    print(f"\nTesting {model}")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Say hello in one sentence."
        )

        print("SUCCESS")
        print(response.text)
        break

    except Exception as e:
        print("FAILED")
        print(e)