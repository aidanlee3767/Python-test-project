import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)


def basic_chat_example():
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Explain Python decorators"
    )
    print(response.text)


if __name__ == "__main__":
    basic_chat_example()
