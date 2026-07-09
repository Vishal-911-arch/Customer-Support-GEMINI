from ollama import Client
import base64

client = Client(host="http://localhost:11434")

IMAGE_PATH = r"artifacts\image_classifier\Glider_Flying_Handbook\crops\page_2_img_1.png"


with open(IMAGE_PATH, "rb") as f:
    image = base64.b64encode(f.read()).decode()


response = client.generate(

    model="llava:7b",

    prompt="""
Describe this aviation image.

Mention:
- aircraft parts
- labels
- diagrams
- important maintenance information
- graphs if any
""",

    images=[image]

)

print("\n")
print("=" * 70)
print(response["response"])
print("=" * 70)