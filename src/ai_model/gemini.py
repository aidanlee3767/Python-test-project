"""Google Gemini AI Model Integration

Provides basic functionality to interact with Google's Gemini AI model
for text generation and chat operations.
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)


def basic_chat_example():
    """
    Basic example of using Gemini for content generation.

    Demonstrates how to use the Gemini client to generate content
    about Python decorators.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Explain Python decorators"
    )
    print(response.text)


if __name__ == "__main__":
    basic_chat_example()
